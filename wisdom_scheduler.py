#!/usr/bin/env python3
"""
毎日の言葉セレクター - Python スケジューラー
systemd/crontab が使えない環境向けのフォールバック常駐プロセス
"""

import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
RUN_SCRIPT = SCRIPT_DIR / "run_daily_wisdom.sh"


def next_run_time(hour: int, minute: int) -> datetime:
    """次の実行時刻（今日の指定時刻、過ぎていたら明日）を返す。"""
    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return target


def run_wisdom():
    """run_daily_wisdom.sh を実行する。"""
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 実行開始", flush=True)
    result = subprocess.run(
        ["bash", str(RUN_SCRIPT)],
        capture_output=False,
    )
    if result.returncode != 0:
        print(f"[WARN] 終了コード: {result.returncode}", flush=True)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="毎朝の言葉セレクター スケジューラー")
    parser.add_argument("--hour",   type=int, default=7, help="実行時（デフォルト: 7）")
    parser.add_argument("--minute", type=int, default=0, help="実行分（デフォルト: 0）")
    parser.add_argument("--run-now", action="store_true", help="起動時に即時実行してからスケジュール待機")
    args = parser.parse_args()

    print(f"=== 毎日の言葉スケジューラー 起動 ===")
    print(f"毎朝 {args.hour}:{args.minute:02d} に実行します")
    print(f"停止するには Ctrl+C を押してください")
    print()

    if args.run_now:
        run_wisdom()

    try:
        while True:
            target = next_run_time(args.hour, args.minute)
            wait_sec = (target - datetime.now()).total_seconds()
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 次回実行: {target:%Y-%m-%d %H:%M:%S} "
                  f"（{wait_sec/3600:.1f}時間後）", flush=True)
            time.sleep(max(wait_sec, 0))
            run_wisdom()
    except KeyboardInterrupt:
        print("\nスケジューラーを停止しました")


if __name__ == "__main__":
    main()
