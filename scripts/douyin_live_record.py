#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
douyin_live_record.py — 录制抖音直播

按直播间分享链接 / 短链 / 房间 ID 录制，自动完成：
  分享链接 → 房间 ID → 带签名 FLV 拉流地址 → ffmpeg 分段录制
  → 断流自动重试（指数退避）→ 录完自动转封装 MP4（无损）

用法:
  python3 douyin_live_record.py "https://live.douyin.com/1234567890"
  python3 douyin_live_record.py "https://v.douyin.com/xxxxxxx/"
  python3 douyin_live_record.py 1234567890
  python3 douyin_live_record.py <目标> --dry-run        # 只解析拉流地址，不录
  python3 douyin_live_record.py <目标> --no-remux       # 录完不转 MP4
  python3 douyin_live_record.py <目标> --loop           # 常驻监控，开播自动录（Ctrl-C 退出）

依赖:
  - ffmpeg  (macOS: brew install ffmpeg)
  - python3 + requests  (pip install requests)

注意:
  「房间 ID → 拉流地址」依赖抖音接口和签名算法，经常改版。若 --dry-run
  取不到流，优先给脚本传 --cookie（浏览器里抖音直播间页面的 Cookie），
  仍不行则需按当前接口调整 get_stream_url 里的方法。
"""
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
BACKOFF = [5, 10, 20, 30, 60, 60, 60, 60]  # 断流重试间隔（秒），与 max_retries 配合


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def safe_name(s):
    """文件名安全化：清掉文件系统非法字符，防主播昵称带 / : 等。"""
    return re.sub(r'[\\/:*?"<>|\s]+', '_', str(s))


def _headers(room_id, cookie):
    h = {
        "User-Agent": UA,
        "Referer": f"https://live.douyin.com/{room_id}",
    }
    if cookie:
        h["Cookie"] = cookie
    return h


def resolve_share_url(url, cookie="", timeout=15):
    """跟随 v.douyin.com 短链的 302 跳转，返回最终真实地址。"""
    return requests.get(
        url, headers={"User-Agent": UA, "Cookie": cookie} if cookie else {"User-Agent": UA},
        allow_redirects=True, timeout=timeout,
    ).url


def resolve_room_id(target, cookie=""):
    """把直播间链接 / 短链 / 纯房间 ID 统一解析成房间 ID。"""
    t = target.strip()
    if t.isdigit():
        return t
    m = re.search(r"(?:live\.douyin\.com|douyin\.com/live)/(\d+)", t)
    if m:
        return m.group(1)
    if "douyin.com" in t:
        final = resolve_share_url(t, cookie=cookie)
        m = re.search(r"live\.douyin\.com/(\d+)", final)
        if m:
            return m.group(1)
        if re.search(r"douyin\.com/(?:user|root)/[A-Za-z0-9_-]{20,}", final):
            raise ValueError(
                "分享的是用户主页而非直播间，无法定位当前正在直播的房间。"
                "请分享直播间页面链接（live.douyin.com/{房间ID} 或直播间短链）。"
            )
        raise ValueError(f"短链重定向到 {final}，无法解析出房间 ID")
    raise ValueError("无法识别目标格式：请给直播间链接、分享短链或纯房间 ID")


def _get_stream_url_via_api(room_id, timeout=15, cookie=""):
    """方法 1：网页端房间进入接口（经典方案）。

    返回 (stream_url, nickname)；明确未开播返回 (None, None)。
    """
    api = "https://live.douyin.com/webcast/room/web/enter/"
    params = {
        "aid": "6383",
        "app_name": "douyin_web",
        "live_id": "1",
        "device_platform": "web",
        "enter_from": "web_live",
        "web_rid": str(room_id),
    }
    r = requests.get(api, params=params, headers=_headers(room_id, cookie), timeout=timeout)
    r.raise_for_status()
    payload = r.json()
    d = payload.get("data")
    rooms = d.get("data") if isinstance(d, dict) else d
    if not isinstance(rooms, list) or not rooms:
        raise RuntimeError("接口返回结构异常: " + str(payload)[:200])
    room = rooms[0]
    # status: 2=直播中, 4=未开播（见 DouyinLiveRecorder 等项目的解析逻辑）
    if room.get("status") != 2:
        return None, None
    flv = (room.get("stream_url") or {}).get("flv_pull_url") or {}
    if not flv:
        # status=2 但无流：常见于直播已结束但开了回放
        return None, None
    url = next((flv[q] for q in ("FULL_HD1", "HD1", "SD1", "SD2") if q in flv),
               next(iter(flv.values())))
    nickname = (room.get("owner") or {}).get("nickname") or str(room_id)
    return url, nickname


def _get_stream_url_from_page(room_id, timeout=15, cookie=""):
    """方法 2：抓直播间 HTML，从内嵌状态里正则找 flv 地址（兜底）。"""
    page = f"https://live.douyin.com/{room_id}"
    r = requests.get(page, headers=_headers(room_id, cookie), timeout=timeout)
    r.raise_for_status()
    html = r.text
    if re.search(r'"status"\s*:\s*4', html):
        return None, None  # 明确未开播
    found = re.findall(r'https?:\\?/\\?/[^"\'\s\\]+?\.flv[^"\'\s\\]*', html)
    if found:
        return found[0].replace("\\/", "/").replace("\\u0026", "&"), None
    raise RuntimeError("页面里没找到 flv 地址（可能需要登录 Cookie 或验证）")


def get_stream_url(room_id, timeout=15, cookie=""):
    """房间 ID → 带签名 FLV 拉流地址。返回 (url, nickname)。

    未开播 → (None, None)；取流彻底失败 → 抛 RuntimeError。
    抖音接口/签名经常改版，本函数是脚本最需要维护的部分。
    """
    errs = []
    try:
        url, nick = _get_stream_url_via_api(room_id, timeout, cookie)
        if url:
            return url, nick
        if nick is None:
            return None, None  # 明确未开播，不必再试页面
    except Exception as e:
        errs.append(f"接口: {e}")
    try:
        url, _ = _get_stream_url_from_page(room_id, timeout, cookie)
        if url:
            return url, str(room_id)
        return None, None
    except Exception as e:
        errs.append(f"页面: {e}")
    raise RuntimeError("取流失败 | " + " | ".join(errs))


def is_live(room_id, cookie=""):
    """主播是否在播。True/False；接口异常返回 None（未知，按在播继续重试）。"""
    try:
        url, _ = get_stream_url(room_id, timeout=10, cookie=cookie)
        return url is not None
    except Exception:
        return None


def run_ffmpeg(stream_url, session_dir, attempt, segment_minutes):
    """跑一次 ffmpeg 录制。返回 ffmpeg 退出码（0=正常结束）。"""
    base = f"{session_dir.name}_r{attempt:02d}"
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "warning",
        "-rw_timeout", "15000000",          # 15s 无数据判定断流，避免 ffmpeg 挂死
        "-reconnect", "1",                  # HTTP 层自动重连（仅 http/https 输入有效）
        "-reconnect_streamed", "1",
        "-reconnect_delay_max", "5",
        "-reconnect_max_retries", "3",      # 内层限次重试，真断流时让 ffmpeg 尽快退出交还外层看门狗
        "-i", stream_url,
        "-c", "copy",                       # 只拷贝流，不转码（无损、省 CPU）
        "-flush_packets", "1",              # 逐包落盘，崩溃最多丢 1 秒
        "-f", "segment",
        "-segment_time", str(segment_minutes * 60),
        "-reset_timestamps", "1",
        "-segment_format", "flv",           # 录制阶段用 flv，断了也能播
        str(session_dir / f"{base}_%d.flv"),
    ]
    log("ffmpeg: " + " ".join(cmd))
    # 不设整体 timeout：直播可能录几小时，靠 rw_timeout + 重连自行退出
    return subprocess.run(cmd).returncode


def remux_to_mp4(session_dir, keep_flv=False):
    """把分片 flv 逐个无损转封装成 mp4（-c copy，不重新编码）。"""
    flvs = sorted(session_dir.glob("*.flv")) if session_dir else []
    if not flvs:
        return
    log(f"转封装 {len(flvs)} 个分片 → MP4 ...")
    for f in flvs:
        out = f.with_suffix(".mp4")
        rc = subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "warning",
            "-i", str(f), "-c", "copy",
            "-movflags", "+faststart",          # moov 前置，手机/网页播放友好
            "-avoid_negative_ts", "make_zero",  # 修 flv 常见负时间戳
            str(out),
        ]).returncode
        if rc == 0:
            log(f"  ✓ {f.name} -> {out.name}")
            if not keep_flv:
                f.unlink()
        else:
            log(f"  ✗ {f.name} 转封装失败（退出码 {rc}），保留原始 flv")


def record_session(room_id, out_dir, segment_minutes, max_retries, cookie,
                   no_remux, keep_flv):
    """录制一场完整直播：取流→分段录制→断流重试→收尾转封装。

    未开播/取不到流 → 返回 False（不建目录）。
    录制中主播下播会被 is_live 提前发现并结束，而不是耗满重试次数。
    """
    stream_url, anchor = get_stream_url(room_id, cookie=cookie)
    if not stream_url:
        return False
    ts = time.strftime("%Y%m%d_%H%M%S")
    session_dir = Path(out_dir) / f"{safe_name(anchor)}_{ts}"
    session_dir.mkdir(parents=True, exist_ok=True)
    log(f"输出目录: {session_dir}")
    ended = False
    try:
        for attempt in range(1, max_retries + 1):
            if attempt > 1:
                log(f"[{attempt}/{max_retries}] 断流重试：查状态并重新取签名地址")
                if is_live(room_id, cookie) is False:
                    log("主播已下播，结束录制")
                    ended = True
                    break
                stream_url, _ = get_stream_url(room_id, cookie=cookie)
                if not stream_url:
                    wait = BACKOFF[attempt - 1]
                    log(f"重新取流失败，{wait}s 后重试")
                    time.sleep(wait)
                    continue

            rc = run_ffmpeg(stream_url, session_dir, attempt, segment_minutes)
            if rc == 0:
                log("直播正常结束")
                ended = True
                break
            log(f"录制中断（ffmpeg 退出码 {rc}）")
            if attempt < max_retries:
                wait = BACKOFF[attempt - 1]
                log(f"{wait}s 后重试...")
                time.sleep(wait)

        if not ended:
            log("达到重试上限仍未成功")
    finally:
        if no_remux:
            log("已跳过 MP4 转封装（--no-remux）")
        else:
            remux_to_mp4(session_dir, keep_flv=keep_flv)
    return True


EXAMPLES = """
示例:
  %(prog)s "https://live.douyin.com/1234567890"
  %(prog)s "https://v.douyin.com/xxxxxxx/"
  %(prog)s 1234567890 --dry-run          # 只解析拉流地址，不录制
  %(prog)s 1234567890 --cookie 'ttwid=..; __ac_signature=..'
  %(prog)s 1234567890 --no-remux --keep-flv
"""


def main():
    ap = argparse.ArgumentParser(
        description="录制抖音直播：解析链接→取流→分段录制→断流重试→转 MP4。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EXAMPLES,
    )
    ap.add_argument("target", help="直播间链接 / 分享短链 / 房间 ID")
    ap.add_argument("--out-dir", default="recordings", help="输出目录（默认 recordings/）")
    ap.add_argument("--segment-minutes", type=int, default=60, help="每多少分钟切一片（默认 60）")
    ap.add_argument("--max-retries", type=int, default=8, help="断流后最多重试次数（默认 8）")
    ap.add_argument("--no-remux", action="store_true", help="录完不自动转 MP4（默认会转）")
    ap.add_argument("--keep-flv", action="store_true", help="转 MP4 后保留原始 flv（默认删除）")
    ap.add_argument("--cookie", default="", help="抖音 Cookie（可选；受限直播间需要）")
    ap.add_argument("--dry-run", action="store_true", help="只解析出拉流地址并退出")
    ap.add_argument("--loop", action="store_true",
                    help="常驻监控：定时检查开播，开播即自动录制（Ctrl-C 退出）")
    ap.add_argument("--check-interval", type=int, default=300,
                    help="--loop 模式下每次检查的间隔秒数（默认 300）")
    args = ap.parse_args()

    if args.max_retries > len(BACKOFF):
        BACKOFF.extend([60] * (args.max_retries - len(BACKOFF)))

    if args.loop and args.dry_run:
        log("--loop 与 --dry-run 不能同时使用")
        return 2

    try:
        room_id = resolve_room_id(args.target, args.cookie)
        log(f"房间 ID: {room_id}")

        if args.dry_run:
            url, nick = get_stream_url(room_id, cookie=args.cookie)
            if not url:
                log("未开播或取不到流。若你有浏览器里直播间页面的 Cookie，用 --cookie 传入再试。")
                return 1
            log(f"主播: {nick}")
            log(f"拉流地址: {url}")
            return 0

        if args.loop:
            log(f"常驻监控模式：每 {args.check_interval}s 检查一次开播状态（Ctrl-C 退出）")
            while True:
                try:
                    started = record_session(
                        room_id, args.out_dir, args.segment_minutes,
                        args.max_retries, args.cookie, args.no_remux, args.keep_flv)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    log(f"监控循环出错（继续监控）: {e}")
                    started = False
                if started:
                    log("本场录制结束，继续监控下一场...")
                else:
                    log(f"未开播，{args.check_interval}s 后再次检查...")
                time.sleep(args.check_interval)

        started = record_session(
            room_id, args.out_dir, args.segment_minutes,
            args.max_retries, args.cookie, args.no_remux, args.keep_flv)
        if not started:
            log("当前未开播或取不到流。先用 --dry-run 排查；或加 --loop 常驻等待开播。")
            return 1
    except KeyboardInterrupt:
        log("用户中断（Ctrl-C）")
    except ValueError as e:
        log(f"参数错误: {e}")
        return 2
    except Exception as e:
        log(f"出错: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
