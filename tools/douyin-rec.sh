#!/bin/bash
# douyin-rec — 抖音直播原画录制工具
# 用法: douyin-rec <直播间URL或ID> [-q 画质] [-t 秒数] [-o 输出目录]
#
# 示例:
#   douyin-rec 42406061739                          # 持续录制，30分钟一段，下播/Ctrl+C 自动保存
#   douyin-rec 42406061739 -t 180                   # 只录3分钟
#   douyin-rec 42406061739 -q hd -o ~/Videos        # 高清，持续录制

# === 默认值 ===
QUALITY="or4"
DURATION=""
OUTDIR="$HOME/Downloads"
SEGMENT_TIME=1800       # 30分钟
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# === 全局状态 ===
ROOM_ID=""
NICKNAME=""
INTERRUPTED=false
CURRENT_TS=""
CURRENT_OUT=""

# === 解析参数 ===
while [[ $# -gt 0 ]]; do
  case $1 in
    http*://live.douyin.com/*) ROOM_ID=$(echo "$1" | sed -E 's/.*live\.douyin\.com\/([0-9]+).*/\1/') ;;
    http*) echo "❌ 不是抖音直播链接: $1"; exit 1 ;;
    -q) QUALITY="$2"; shift ;;
    -t) DURATION="$2"; shift ;;
    -o) OUTDIR="$2"; shift ;;
    --daemon) DAEMON=true ;;
    --stop) STOP_DAEMON=true ;;
    --status) STATUS_DAEMON=true ;;
    -h|--help) sed -n '2,6p' "$0"; exit 0 ;;
    ''|--) ;;
    *) ROOM_ID="$1" ;;
  esac
  shift
done

if [ -z "$ROOM_ID" ] && [ "$STOP_DAEMON" != true ] && [ "$STATUS_DAEMON" != true ]; then
  echo "❌ 缺少直播间ID或URL"
  echo "用法: douyin-rec <直播间URL或ID> [-q 画质] [-t 秒数] [--daemon] [--stop] [--status]"
  exit 1
fi

# === launchd 常驻模式 ===
LAUNCHD_LABEL="com.douyin.rec.${ROOM_ID}"
PLIST="$HOME/Library/LaunchAgents/${LAUNCHD_LABEL}.plist"
LOG_FILE="/tmp/douyin-rec-${ROOM_ID}.log"

if [ "$STOP_DAEMON" = true ]; then
  launchctl bootout gui/$(id -u) "$PLIST" 2>/dev/null && echo "✅ 已停止录制 ($ROOM_ID)" || echo "⚠️ 未找到运行中的录制任务"
  rm -f "$PLIST"
  exit 0
fi

if [ "$STATUS_DAEMON" = true ]; then
  if launchctl print gui/$(id -u)/${LAUNCHD_LABEL} &>/dev/null; then
    echo "✅ 录制中 ($ROOM_ID)"
    echo "--- 最近日志 ---"
    tail -5 "$LOG_FILE" 2>/dev/null
  else
    echo "⏸ 未在录制 ($ROOM_ID)"
  fi
  exit 0
fi

if [ "$DAEMON" = true ]; then
  mkdir -p "$HOME/Library/LaunchAgents"

  # 构建运行参数（去掉 --daemon）
  SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  DAEMON_ARGS="$ROOM_ID -q $QUALITY -o $OUTDIR"
  [ -n "$DURATION" ] && DAEMON_ARGS="$DAEMON_ARGS -t $DURATION"

  cat > "$PLIST" << PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LAUNCHD_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${SCRIPT_PATH}</string>
        <string>${ROOM_ID}</string>
        <string>-q</string>
        <string>${QUALITY}</string>
        <string>-o</string>
        <string>${OUTDIR}</string>
        ${DURATION:+<string>-t</string>}
        ${DURATION:+<string>${DURATION}</string>}
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
    <key>WorkingDirectory</key>
    <string>${OUTDIR}</string>
    <key>StandardOutPath</key>
    <string>${LOG_FILE}</string>
    <key>StandardErrorPath</key>
    <string>${LOG_FILE}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
PLIST_EOF

  launchctl bootstrap gui/$(id -u) "$PLIST" 2>/dev/null || \
    launchctl load "$PLIST" 2>/dev/null

  echo "✅ 已启动后台录制 (launchd 守护)"
  echo "   房间: $ROOM_ID | 画质: $QUALITY"
  echo "   查看状态: $0 --status"
  echo "   停止录制: $0 --stop"
  echo "   日志: tail -f $LOG_FILE"
  exit 0
fi

# === 画质映射 ===
case "$QUALITY" in
  or4|原画) QPAT="or4|_hd5[^0-9]|_hd[^0-9]" ;;
  hd|高清)  QPAT="Stage0T000hd|_hd[^0-9]" ;;
  sd|标清)  QPAT="Stage0T000sd|_sd" ;;
  ld|流畅)  QPAT="Stage0T000ld|_ld" ;;
  *) echo "❌ 未知画质: $QUALITY (可选: or4/hd/sd/ld)"; exit 1 ;;
esac

# === 抓取页面获取流地址 ===
fetch_stream() {
  local page url
  page=$(curl -sL --max-time 10 -A "$UA" "https://live.douyin.com/$ROOM_ID" 2>/dev/null)

  # 是否在播
  url=$(echo "$page" | grep -oE 'http://pull-flv[^"]+' | head -1)
  if [ -z "$url" ]; then
    url=$(echo "$page" | grep -oE 'http://pull-hls[^"]+' | head -1)
    [ -z "$url" ] && return 1
  fi

  # 根据画质选流
  STREAM_URL=$(echo "$page" | grep -oE 'http://pull-hls[^"]+' | grep -E "$QPAT" | head -1 | sed 's/\\u0026/\&/g')
  [ -z "$STREAM_URL" ] && return 1

  # 提取昵称（仅首次）
  if [ -z "$NICKNAME" ]; then
    NICKNAME=$(echo "$page" | grep -oE 'nickname[^,}]+' | grep -v undefined | head -1 | awk -F'"' '{print $3}' | tr -d '\\')
    [ -z "$NICKNAME" ] && NICKNAME="$ROOM_ID"
  fi

  return 0
}

# === 中断处理：保存当前片段 ===
on_interrupt() {
  INTERRUPTED=true
  if [ -n "$CURRENT_TS" ] && [ -f "$CURRENT_TS" ] && [ -s "$CURRENT_TS" ]; then
    printf "\n💾 正在保存当前片段..."
    ffmpeg -hide_banner -loglevel error -y -i "$CURRENT_TS" -c copy -movflags +faststart "$CURRENT_OUT" 2>/dev/null && {
      local sz=$(du -h "$CURRENT_OUT" 2>/dev/null | cut -f1)
      echo " ✅ $(basename "$CURRENT_OUT") ($sz)"
    }
    rm -f "$CURRENT_TS"
    CURRENT_TS=""
  fi
}
trap 'on_interrupt' INT TERM

# === 录制一段 ===
# 参数: $1=标签 $2=时长(秒) $3=输出文件路径
# 返回: 0=成功 1=失败(流断/中断/无内容)
record_segment() {
  local label="$1" duration="$2" out="$3"

  CURRENT_TS=$(mktemp "/tmp/douyin_$$_XXXXXX.ts")
  CURRENT_OUT="$out"

  echo "🔴 录制中: $label"

  # ffmpeg 自身出错或连接断开 → 非 0 退出
  ffmpeg -hide_banner -loglevel error -y \
    -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10 \
    -i "$STREAM_URL" -c copy -t "$duration" "$CURRENT_TS" 2>/dev/null
  local rc=$?

  # 中断信号 → trap 已保存，直接返回失败
  if [ "$INTERRUPTED" = true ]; then
    [ -n "$CURRENT_TS" ] && rm -f "$CURRENT_TS"
    CURRENT_TS=""
    return 1
  fi

  # ffmpeg 失败且没内容 → 流断了
  if [ "$rc" -ne 0 ]; then
    if [ -s "$CURRENT_TS" ]; then
      # 有部分内容，尝试保存
      echo "⚠️ 流中断，保存已录制部分..."
      ffmpeg -hide_banner -loglevel error -y -i "$CURRENT_TS" -c copy -movflags +faststart "$out" 2>/dev/null
      local sz=$(du -h "$out" 2>/dev/null | cut -f1)
      echo "✅ $(basename "$out") ($sz)"
    fi
    rm -f "$CURRENT_TS"
    CURRENT_TS=""
    return 1
  fi

  # 正常完成：TS → MP4
  if [ -s "$CURRENT_TS" ]; then
    echo "🔄 转码中..."
    ffmpeg -hide_banner -loglevel error -y -i "$CURRENT_TS" -c copy -movflags +faststart "$out" 2>/dev/null
    local sz=$(du -h "$out" 2>/dev/null | cut -f1)
    echo "✅ $(basename "$out") ($sz)"
  fi

  rm -f "$CURRENT_TS"
  CURRENT_TS=""
  return 0
}

# ==========================================
# === 主流程 ===
# ==========================================

echo "🔍 获取直播间信息..."
if ! fetch_stream; then
  echo "💤 直播间未开播或不存在"
  exit 1
fi

echo "📺 $NICKNAME ($ROOM_ID)"
echo "🎨 $QUALITY"

BASENAME="${NICKNAME}_$(date +%Y%m%d_%H%M)"

# ====================
# 单段模式（-t 指定时长）
# ====================
if [ -n "$DURATION" ]; then
  echo "💾 ${OUTDIR}/${BASENAME}.mp4"
  echo "  时长: ${DURATION}秒"

  record_segment "单段 ${DURATION}秒" "$DURATION" "${OUTDIR}/${BASENAME}.mp4" || true
  echo "🏁 完成"
  exit 0
fi

# ====================
# 持续模式：30分钟分段 + 下播自动停
# ====================
echo "💾 ${OUTDIR}/${BASENAME}_p1.mp4 ..."
echo "⏱ 每30分钟分段 | 下播自动停 | Ctrl+C 停止"
echo ""

SEG=0
RETRY_COUNT=0
RETRY_DELAYS=(1 3 5 30 60)   # 重试延迟（秒），递增

while [ "$INTERRUPTED" = false ]; do
  # 每段开始前刷新流地址 + 检测在播状态
  echo "🔄 检查直播状态..."
  if ! fetch_stream; then
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ "$RETRY_COUNT" -ge 5 ]; then
      echo "💤 连续5次检测失败，直播可能已结束"
      break
    fi
    DELAY=${RETRY_DELAYS[$((RETRY_COUNT - 1))]}
    echo "⚠️ 检测失败(第${RETRY_COUNT}/5次)，${DELAY}秒后重试..."
    sleep "$DELAY"
    continue
  fi
  RETRY_COUNT=0

  SEG=$((SEG + 1))
  SEG_FILE="${OUTDIR}/${BASENAME}_p${SEG}.mp4"

  if ! record_segment "第${SEG}段 (30分钟)" "$SEGMENT_TIME" "$SEG_FILE"; then
    if [ "$INTERRUPTED" = true ]; then
      break
    fi
    echo "⚠️ 第${SEG}段中断，10秒后重试..."
    sleep 10
    continue
  fi
done

echo "🏁 录制结束，共 ${SEG} 段"
