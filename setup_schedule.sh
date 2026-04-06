#!/usr/bin/env bash
# 毎朝7時に daily_wisdom.py を自動実行するスケジュールをセットアップする
# 対応方式: systemd user timer（優先）/ crontab（フォールバック）
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

    # .service ファイル
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

    # .timer ファイル
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

    # 既存のエントリを削除してから追加
    (crontab -l 2>/dev/null | grep -v "daily_wisdom" || true) > "$tmp"
    echo "$cron_line" >> "$tmp"
    crontab "$tmp"
    rm -f "$tmp"

    echo "[OK] crontab を設定しました"
    echo "     毎朝 ${HOUR}:$(printf '%02d' $MINUTE) に自動実行されます"
    crontab -l | grep daily_wisdom
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
    echo "[ERROR] systemd user / crontab のどちらも使用できません"
    echo "        手動で以下をスケジューラーに登録してください:"
    echo "        $RUN_SCRIPT"
    exit 1
fi

echo ""
echo "=== セットアップ完了 ==="
echo ""
echo "▶ すぐにテスト実行:"
echo "    bash $RUN_SCRIPT"
echo ""
echo "▶ 実行時刻を変更する場合（例: 6:30 AM）:"
echo "    WISDOM_HOUR=6 WISDOM_MIN=30 bash setup_schedule.sh"
echo ""
echo "▶ スケジュールを停止する場合:"
if systemctl --user status > /dev/null 2>&1; then
    echo "    systemctl --user disable --now daily-wisdom.timer"
else
    echo "    crontab -e  # daily_wisdom の行を削除"
fi
