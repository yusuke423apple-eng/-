#!/usr/bin/env bash
# 毎朝の言葉セレクター実行スクリプト
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/daily_wisdom.log"
CONTEXT_FILE="$SCRIPT_DIR/today_context.txt"

# ログローテーション（30日分保持）
if [ -f "$LOG_FILE" ] && [ "$(wc -l < "$LOG_FILE")" -gt 900 ]; then
    tail -n 600 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

echo "────────────────────────────────────────" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') 実行開始" >> "$LOG_FILE"

# 今日のコンテキストファイルがあれば読み込む
CONTEXT_ARG=""
if [ -f "$CONTEXT_FILE" ]; then
    CONTEXT_ARG="--context $(cat "$CONTEXT_FILE")"
fi

# APIキーが設定されていれば Claude API を使う、なければ --no-api
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
    python3 "$SCRIPT_DIR/daily_wisdom.py" $CONTEXT_ARG 2>&1 | tee -a "$LOG_FILE"
else
    echo "[INFO] ANTHROPIC_API_KEY が未設定のため --no-api モードで実行" >> "$LOG_FILE"
    python3 "$SCRIPT_DIR/daily_wisdom.py" --no-api 2>&1 | tee -a "$LOG_FILE"
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') 完了" >> "$LOG_FILE"
