#!/usr/bin/env python3
"""
アメブロ自動投稿ツール
Ameblo (アメーバブログ) への自動ログイン・投稿を行うツール
"""

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

import google.generativeai as genai
from playwright.async_api import async_playwright, Page, Browser, TimeoutError as PlaywrightTimeout


# ─────────────────────────────────────────────
# 定数
# ─────────────────────────────────────────────
LOGIN_URL = "https://www.ameba.jp/login/"
NEW_POST_URL = "https://blog.ameba.jp/ucs/entry/srventryinsertform.do"
DEFAULT_TIMEOUT = 30_000  # ms


# ─────────────────────────────────────────────
# ユーティリティ
# ─────────────────────────────────────────────
def load_config(config_path: str = "config.json") -> dict:
    """設定ファイルを読み込む。環境変数で上書き可能。"""
    config: dict = {}

    if Path(config_path).exists():
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

    # 環境変数で上書き
    if os.environ.get("AMEBLO_USER"):
        config["username"] = os.environ["AMEBLO_USER"]
    if os.environ.get("AMEBLO_PASS"):
        config["password"] = os.environ["AMEBLO_PASS"]
    if os.environ.get("GEMINI_API_KEY"):
        config["gemini_api_key"] = os.environ["GEMINI_API_KEY"]

    return config


def read_file_content(path: str) -> str:
    """ファイルからテキストを読み込む。"""
    with open(path, encoding="utf-8") as f:
        return f.read()


def generate_content_with_gemini(
    prompt: str,
    api_key: str,
    model: str = "gemini-1.5-flash",
) -> str:
    """Gemini API を使ってブログ本文を生成する。

    Args:
        prompt: 生成指示プロンプト
        api_key: Gemini API キー
        model: 使用するモデル名 (デフォルト: gemini-1.5-flash)

    Returns:
        生成されたテキスト
    """
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel(model)
    print(f"[INFO] Gemini ({model}) でコンテンツを生成中...")
    response = gemini_model.generate_content(prompt)
    text = response.text
    print(f"[INFO] Gemini 生成完了 ({len(text)} 文字)")
    return text


# ─────────────────────────────────────────────
# コアロジック
# ─────────────────────────────────────────────
class AmebloPoster:
    """アメブロ自動投稿クラス。"""

    def __init__(self, username: str, password: str, headless: bool = True):
        self.username = username
        self.password = password
        self.headless = headless
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None

    # ── ブラウザ管理 ──────────────────────────
    async def __aenter__(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        context = await self._browser.new_context(
            locale="ja-JP",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        self._page = await context.new_page()
        self._page.set_default_timeout(DEFAULT_TIMEOUT)
        return self

    async def __aexit__(self, *_):
        if self._browser:
            await self._browser.close()
        await self._playwright.stop()

    # ── ログイン ─────────────────────────────
    async def login(self) -> bool:
        """アメブロにログインする。成功時 True を返す。"""
        page = self._page
        print(f"[INFO] ログインページへアクセス: {LOGIN_URL}")
        await page.goto(LOGIN_URL, wait_until="domcontentloaded")

        try:
            # ユーザー名入力
            await page.wait_for_selector('input[name="accountId"]', timeout=DEFAULT_TIMEOUT)
            await page.fill('input[name="accountId"]', self.username)

            # パスワード入力
            await page.fill('input[name="password"]', self.password)

            # ログインボタンクリック
            await page.click('button[type="submit"]')

            # ログイン完了を待機 (URLが変わるかホームへリダイレクト)
            await page.wait_for_url("https://www.ameba.jp/**", timeout=DEFAULT_TIMEOUT)
            print("[INFO] ログイン成功")
            return True

        except PlaywrightTimeout:
            # 2段階認証やエラーページの可能性をチェック
            current_url = page.url
            if "login" in current_url or "auth" in current_url:
                print(f"[ERROR] ログイン失敗。現在のURL: {current_url}")
                await page.screenshot(path="login_error.png")
                print("[INFO] スクリーンショット保存: login_error.png")
                return False
            # リダイレクト先がログインでなければ成功とみなす
            print("[INFO] ログイン成功 (別URLへリダイレクト)")
            return True

    # ── 投稿 ─────────────────────────────────
    async def post(
        self,
        title: str,
        body: str,
        category_name: Optional[str] = None,
        draft: bool = False,
        image_paths: Optional[list[str]] = None,
    ) -> bool:
        """
        アメブロに記事を投稿する。

        Args:
            title: 記事タイトル
            body: 記事本文 (プレーンテキストまたは HTML)
            category_name: カテゴリ名 (省略可)
            draft: True の場合は下書き保存
            image_paths: 添付画像ファイルパスのリスト (省略可)

        Returns:
            成功時 True
        """
        page = self._page
        print(f"[INFO] 投稿ページへアクセス: {NEW_POST_URL}")
        await page.goto(NEW_POST_URL, wait_until="domcontentloaded")

        # ── タイトル入力 ──────────────────────
        try:
            title_selector = 'input#entry-title, input[name="title"], input.entry-title'
            await page.wait_for_selector(title_selector, timeout=DEFAULT_TIMEOUT)
            await page.fill(title_selector, title)
            print(f"[INFO] タイトル入力: {title}")
        except PlaywrightTimeout:
            print("[ERROR] タイトル欄が見つかりません")
            await page.screenshot(path="post_error.png")
            return False

        # ── 本文入力 ──────────────────────────
        # アメブロはリッチエディタ (iframe) を使用している場合がある
        try:
            # まず通常のテキストエリアを試す
            body_selector = 'textarea#entry-body, textarea[name="body"]'
            if await page.query_selector(body_selector):
                await page.fill(body_selector, body)
                print("[INFO] 本文入力 (textarea)")
            else:
                # iframe 内の contenteditable エディタを試す
                iframe_selector = 'iframe#body-frame, iframe.editor-frame, iframe[id*="body"]'
                frame_elem = await page.wait_for_selector(iframe_selector, timeout=10_000)
                frame = await frame_elem.content_frame()
                editor = await frame.wait_for_selector(
                    'body[contenteditable="true"], div[contenteditable="true"]',
                    timeout=10_000,
                )
                await editor.click()
                # 既存テキストをクリアして入力
                await editor.evaluate("el => el.innerHTML = ''")
                await editor.type(body, delay=10)
                print("[INFO] 本文入力 (iframe contenteditable)")
        except Exception as e:
            print(f"[ERROR] 本文入力に失敗: {e}")
            await page.screenshot(path="post_error.png")
            return False

        # ── カテゴリ選択 ──────────────────────
        if category_name:
            try:
                cat_selector = 'select#entry-category, select[name="themeId"]'
                select_elem = await page.query_selector(cat_selector)
                if select_elem:
                    options = await select_elem.query_selector_all("option")
                    for opt in options:
                        text = await opt.inner_text()
                        if category_name in text:
                            val = await opt.get_attribute("value")
                            await page.select_option(cat_selector, value=val)
                            print(f"[INFO] カテゴリ選択: {text.strip()}")
                            break
                    else:
                        print(f"[WARN] カテゴリ '{category_name}' が見つかりません。スキップします。")
            except Exception as e:
                print(f"[WARN] カテゴリ選択中にエラー: {e}")

        # ── 画像添付 ──────────────────────────
        if image_paths:
            await self._attach_images(image_paths)

        # ── 投稿 / 下書き保存 ─────────────────
        if draft:
            btn_selector = (
                'button#draft-btn, button[name="draftSave"], '
                'input[value*="下書"], button:has-text("下書き")'
            )
            action_label = "下書き保存"
        else:
            btn_selector = (
                'button#publish-btn, button[name="submit"], '
                'input[value*="投稿"], button:has-text("投稿する")'
            )
            action_label = "投稿"

        try:
            await page.wait_for_selector(btn_selector, timeout=DEFAULT_TIMEOUT)
            await page.click(btn_selector)
            print(f"[INFO] {action_label}ボタンをクリック")

            # 完了ページへの遷移を待機
            await page.wait_for_load_state("domcontentloaded", timeout=DEFAULT_TIMEOUT)
            await asyncio.sleep(2)

            # 確認ダイアログが出る場合に備えて OK クリック
            ok_btn = await page.query_selector('button:has-text("OK"), button:has-text("はい")')
            if ok_btn:
                await ok_btn.click()
                await page.wait_for_load_state("domcontentloaded")

            current_url = page.url
            print(f"[INFO] {action_label}完了。現在のURL: {current_url}")
            await page.screenshot(path="post_success.png")
            print("[INFO] スクリーンショット保存: post_success.png")
            return True

        except PlaywrightTimeout:
            print(f"[ERROR] {action_label}ボタンが見つかりません")
            await page.screenshot(path="post_error.png")
            return False

    # ── 画像添付 (内部) ──────────────────────
    async def _attach_images(self, image_paths: list[str]):
        page = self._page
        try:
            # 画像アップロードボタンを探してクリック
            upload_btn = await page.query_selector(
                'button[id*="photo"], button[class*="photo"], '
                'label[for*="image"], button:has-text("画像")'
            )
            if not upload_btn:
                print("[WARN] 画像アップロードボタンが見つかりません。スキップします。")
                return

            for img_path in image_paths:
                if not Path(img_path).exists():
                    print(f"[WARN] 画像ファイルが見つかりません: {img_path}")
                    continue

                # ファイル選択ダイアログをインターセプト
                async with page.expect_file_chooser() as fc_info:
                    await upload_btn.click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(img_path)
                await asyncio.sleep(1)
                print(f"[INFO] 画像添付: {img_path}")

        except Exception as e:
            print(f"[WARN] 画像添付中にエラー: {e}")


# ─────────────────────────────────────────────
# CLI エントリポイント
# ─────────────────────────────────────────────
async def async_main(args: argparse.Namespace) -> int:
    config = load_config(args.config)

    username = args.username or config.get("username", "")
    password = args.password or config.get("password", "")

    if not username or not password:
        print(
            "[ERROR] ユーザー名・パスワードを指定してください。\n"
            "  --username / --password オプション、config.json、"
            "または環境変数 AMEBLO_USER / AMEBLO_PASS を使用してください。"
        )
        return 1

    # Gemini API キーの解決
    gemini_api_key = args.gemini_api_key or config.get("gemini_api_key", "") or os.environ.get("GEMINI_API_KEY", "")

    # 本文の取得
    if args.body_file:
        body = read_file_content(args.body_file)
    elif args.body:
        body = args.body
    elif args.gemini_prompt:
        if not gemini_api_key:
            print(
                "[ERROR] Gemini API キーを指定してください。\n"
                "  --gemini-api-key オプション、config.json の gemini_api_key、"
                "または環境変数 GEMINI_API_KEY を使用してください。"
            )
            return 1
        body = generate_content_with_gemini(
            prompt=args.gemini_prompt,
            api_key=gemini_api_key,
            model=args.gemini_model,
        )
    else:
        print("[ERROR] 本文を --body、--body-file、または --gemini-prompt で指定してください。")
        return 1

    # 画像リスト
    images = args.images if args.images else []

    async with AmebloPoster(username, password, headless=not args.show_browser) as poster:
        ok = await poster.login()
        if not ok:
            return 1

        ok = await poster.post(
            title=args.title,
            body=body,
            category_name=args.category,
            draft=args.draft,
            image_paths=images,
        )
        return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser(
        description="アメブロ自動投稿ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 直接指定
  python ameblo_poster.py --username myid --password mypass \\
      --title "テスト投稿" --body "こんにちは！"

  # config.json を使用
  python ameblo_poster.py --title "テスト投稿" --body-file article.txt

  # 下書き保存
  python ameblo_poster.py --title "下書き" --body "本文" --draft

  # 画像付き投稿
  python ameblo_poster.py --title "旅行記" --body "楽しかった！" \\
      --images photo1.jpg photo2.jpg

  # Gemini AI で本文を自動生成して投稿
  python ameblo_poster.py --title "今日のカフェ巡り" \\
      --gemini-prompt "東京のおしゃれなカフェを紹介するブログ記事を書いてください。"

  # Gemini モデルを指定して生成
  python ameblo_poster.py --title "AI近況" \\
      --gemini-prompt "最新の AI トレンドについて日本語で書いてください。" \\
      --gemini-model "gemini-1.5-pro"
""",
    )

    # 認証
    auth = parser.add_argument_group("認証")
    auth.add_argument("--username", "-u", help="アメブロ ID (省略時は config.json / 環境変数)")
    auth.add_argument("--password", "-p", help="パスワード (省略時は config.json / 環境変数)")

    # 投稿内容
    content = parser.add_argument_group("投稿内容")
    content.add_argument("--title", "-t", required=True, help="記事タイトル")
    content.add_argument("--body", "-b", help="記事本文 (直接入力)")
    content.add_argument("--body-file", "-f", help="記事本文ファイルパス (.txt / .html)")
    content.add_argument("--category", "-c", help="カテゴリ名 (部分一致)")
    content.add_argument(
        "--images", "-i", nargs="+", metavar="IMAGE", help="添付画像ファイルパス (複数可)"
    )
    content.add_argument(
        "--draft", "-d", action="store_true", help="下書き保存する (デフォルト: 公開投稿)"
    )

    # Gemini AI
    gemini = parser.add_argument_group("Gemini AI (本文自動生成)")
    gemini.add_argument(
        "--gemini-prompt", "-g",
        metavar="PROMPT",
        help="Gemini AI に渡すプロンプト。指定すると --body / --body-file の代わりに本文を自動生成します。",
    )
    gemini.add_argument(
        "--gemini-api-key",
        metavar="KEY",
        help="Gemini API キー (省略時は config.json の gemini_api_key / 環境変数 GEMINI_API_KEY)",
    )
    gemini.add_argument(
        "--gemini-model",
        metavar="MODEL",
        default="gemini-1.5-flash",
        help="使用する Gemini モデル名 (デフォルト: gemini-1.5-flash)",
    )

    # その他
    misc = parser.add_argument_group("その他")
    misc.add_argument("--config", default="config.json", help="設定ファイルパス (デフォルト: config.json)")
    misc.add_argument(
        "--show-browser", action="store_true", help="ブラウザを表示して実行する (デバッグ用)"
    )

    args = parser.parse_args()
    sys.exit(asyncio.run(async_main(args)))


if __name__ == "__main__":
    main()
