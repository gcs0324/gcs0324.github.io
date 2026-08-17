#!/bin/bash
# douyin-rec-batch — 批量录制多个抖音直播间（串行 + 间隔，防抖音风控）
# 用法: douyin-rec-batch <房间ID1> [<房间ID2> ...] [-q 画质] [-t 秒数] [-o 输出目录]
#
# 示例:
#   douyin-rec-batch 39582706356 755230492079 -t 60
#   douyin-rec-batch 123 456 789 -q hd -t 180 -o ~/Videos
#
# 说明: 串行执行（一次一个），每房间间隔 8 秒，避免并发触发抖音验证码
# 依赖: douyin-rec.sh (同目录)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REC="$SCRIPT_DIR/douyin-rec.sh"

QUALITY="or4"
DURATION=""
OUTDIR="$HOME/Downloads"
ROOMS=()
DELAY=8

# === 解析参数 ===
while [[ $# -gt 0 ]]; do
  case $1 in
    -q) QUALITY="$2"; shift ;;
    -t) DURATION="$2"; shift ;;
    -o) OUTDIR="$2"; shift ;;
    -d) DELAY="$2"; shift ;;
    -h|--help) sed -n '2,5p' "$0"; exit 0 ;;
    http*://live.douyin.com/*)
      RID=$(echo "$1" | sed -E 's/.*live\.douyin\.com\/([0-9]+).*/\1/')
      ROOMS+=("$RID") ;;
    http*://v.douyin.com/*)
      echo "⚠️ 短链接 $1 请先解析出房间ID再使用" ;;
    *) ROOMS+=("$1") ;;
  esac
  shift
done

if [ ${#ROOMS[@]} -eq 0 ]; then
  echo "❌ 缺少直播间ID"
  echo "用法: douyin-rec-batch <房间ID1> [<房间ID2> ...] [-q 画质] [-t 秒数]"
  exit 1
fi

if [ ! -f "$REC" ]; then
  echo "❌ 找不到 $REC"
  exit 1
fi

echo "🎬 批量录制 ${#ROOMS[@]} 个直播间 (画质: $QUALITY, 时长: ${DURATION:-持续}, 间隔: ${DELAY}s)"
echo "----------------------------------------"

SUCCESS=0
FAIL=0
for RID in "${ROOMS[@]}"; do
  echo ""
  echo "▶️  [${RID}] 开始..."
  if bash "$REC" "$RID" -q "$QUALITY" ${DURATION:+-t "$DURATION"} -o "$OUTDIR"; then
    SUCCESS=$((SUCCESS + 1))
  else
    FAIL=$((FAIL + 1))
    echo "❌ [${RID}] 失败（可能未开播/风控）"
  fi
  # 最后一个房间后不再等待
  if [ "$RID" != "${ROOMS[${#ROOMS[@]}-1]}" ]; then
    echo "⏳ 等待 ${DELAY}s 再录下一个..."
    sleep "$DELAY"
  fi
done

echo ""
echo "----------------------------------------"
echo "🏁 批量录制结束: 成功 $SUCCESS / ${#ROOMS[@]}"
echo "📂 输出目录: $OUTDIR"
