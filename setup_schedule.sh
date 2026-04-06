#!/usr/bin/env bash
# 毎朝7時に daily_wisdom.py を自動実行するスケジュールをセットアップする
# 対応方式: systemd user timer > crontab > Python スケジューラー（常駐）
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_SCRIPT="$SCRIPT_DIR/run_daily_wisdom.sh"
HOUR="${WISDOM_HOUR:-7}"   # デフォルト 7:00 AM（環境変数で変更可）
MINUTE="${WISDOM_MIN:-0}"

chmod +x "$RUN_SCRIPT"

# ─────────────────────────────────────────────
# systemd user timer（推奨）
# ─────────────────────────────────────────────
setup_systemd() {
    local unit_dir="$HOME/.config/systemd/user"
    mkdir -p "$unit_dir"

    cat > "$unit_dir/daily-wisdom.service" <<EOF
[Unit]
Description=斎藤一人さんの言葉 毎日セレクター
After=network.target

[Service]
Type=oneshot
ExecStart=$RUN_SCRIPT
StandardOutput=journal
StandardError=journal
EOF

    cat > "$unit_dir/daily-wisdom.timer" <<EOF
[Unit]
Description=毎朝 ${HOUR}:$(printf '%02d' $MINUTE) に daily-wisdom を実行

[Timer]
OnCalendar=*-*-* ${HOUR}:$(printf '%02d' $MINUTE):00
Persistent=true

[Install]
WantedBy=timers.target
EOF

    systemctl --user daemon-reload
    systemctl --user enable --now daily-wisdom.timer
    echo "[OK] systemd user timer を設定しました"
    echo "     毎朝 ${HOUR}:$(printf '%02d' $MINUTE) に自動実行されます"
    echo ""
    systemctl --user list-timers daily-wisdom.timer --no-pager
}

# ─────────────────────────────────────────────
# crontab（フォールバック）
# ─────────────────────────────────────────────
setup_crontab() {
    local cron_line="${MINUTE} ${HOUR} * * * $RUN_SCRIPT >> $SCRIPT_DIR/daily_wisdom.log 2>&1"
    local tmp
    tmp=$(mktemp)

    (crontab -l 2>/dev/null | grep -v "daily_wisdom" || true) > "$tmp"
    echo "$cron_line" >> "$tmp"
    crontab "$tmp"
    rm -f "$tmp"

    echo "[OK] crontab を設定しました"
    echo "     毎朝 ${HOUR}:$(printf '%02d' $MINUTE) に自動実行されます"
    crontab -l | grep daily_wisdom
}

# ─────────────────────────────────────────────
# Python スケジューラー（フォールバック）
# ─────────────────────────────────────────────
setup_python_scheduler() {
    local pid_file="$SCRIPT_DIR/wisdom_scheduler.pid"
    local log_file="$SCRIPT_DIR/daily_wisdom.log"

    # 既存プロセスを停止
    if [ -f "$pid_file" ]; then
        local old_pid
        old_pid=$(cat "$pid_file")
        if kill -0 "$old_pid" 2>/dev/null; then
            kill "$old_pid"
            echo "[INFO] 既存のスケジューラー (PID $old_pid) を停止しました"
        fi
    fi

    # バックグラウンドで起動
    nohup python3 "$SCRIPT_DIR/wisdom_scheduler.py" \
        --hour "$HOUR" --minute "$MINUTE" \
        >> "$log_file" 2>&1 &
    echo $! > "$pid_file"

    echo "[OK] Python スケジューラーをバックグラウンドで起動しました (PID $!)"
    echo "     毎朝 ${HOUR}:$(printf '%02d' $MINUTE) に自動実行されます"
    echo "     ログ: $log_file"
    echo ""
    echo "▶ 停止するには:"
    echo "    kill \$(cat $pid_file)"
}

# ─────────────────────────────────────────────
# メイン
# ─────────────────────────────────────────────
echo "=== 毎日の言葉セレクター スケジュールセットアップ ==="
echo "実行スクリプト: $RUN_SCRIPT"
echo "実行時刻: 毎朝 ${HOUR}:$(printf '%02d' $MINUTE)"
echo ""

if systemctl --user status > /dev/null 2>&1; then
    setup_systemd
elif command -v crontab > /dev/null 2>&1; then
    setup_crontab
else
    echo "[INFO] systemd/crontab が使用不可のため Python スケジューラーを使用します"
    setup_python_scheduler
fi

echo ""
echo "=== セットアップ完了 ==="
echo ""
echo "▶ すぐにテスト実行:"
echo "    bash $RUN_SCRIPT"
echo ""
echo "▶ 実行時刻を変更する場合（例: 6:30 AM）:"
echo "    WISDOM_HOUR=6 WISDOM_MIN=30 bash $SCRIPT_DIR/setup_schedule.sh"
