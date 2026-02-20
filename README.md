# アメブロ自動投稿ツール

Playwright を使ってアメブロ (アメーバブログ) へ自動ログイン・投稿を行う Python ツールです。
**Google Gemini AI** と連携して、プロンプトから記事本文を自動生成する機能も備えています。

## 必要環境

- Python 3.10 以上
- pip

## セットアップ

```bash
# 1. 依存パッケージのインストール
pip install -r requirements.txt

# 2. Playwright ブラウザのインストール
playwright install chromium

# 3. 設定ファイルの作成 (認証情報を記入)
cp config.json.example config.json
# config.json を編集して username / password を入力
```

## 使い方

### 基本的な投稿

```bash
python ameblo_poster.py \
  --title "今日のランチ" \
  --body "美味しいラーメンを食べました！"
```

### ファイルから本文を読み込む

```bash
python ameblo_poster.py \
  --title "旅行記" \
  --body-file article.txt
```

### カテゴリ指定・画像付き投稿

```bash
python ameblo_poster.py \
  --title "旅行記" \
  --body-file article.txt \
  --category "旅行" \
  --images photo1.jpg photo2.jpg
```

### 下書きとして保存

```bash
python ameblo_poster.py \
  --title "下書き記事" \
  --body "あとで編集します" \
  --draft
```

### ブラウザを表示して動作確認 (デバッグ)

```bash
python ameblo_poster.py \
  --title "テスト" \
  --body "動作確認" \
  --show-browser
```

## Gemini AI で記事本文を自動生成

`--gemini-prompt` オプションを使うと、Google Gemini AI がプロンプトをもとにブログ本文を自動生成します。

### セットアップ

[Google AI Studio](https://aistudio.google.com/) で API キーを取得し、`config.json` または環境変数に設定します。

```json
{
  "username": "your_ameblo_id",
  "password": "your_password",
  "gemini_api_key": "your_gemini_api_key"
}
```

または環境変数:

```bash
export GEMINI_API_KEY="your_gemini_api_key"
```

### 使い方

```bash
# Gemini AI で本文を自動生成して投稿
python ameblo_poster.py \
  --title "今日のカフェ巡り" \
  --gemini-prompt "東京のおしゃれなカフェを紹介するブログ記事を書いてください。"

# Gemini モデルを指定して生成 (デフォルト: gemini-1.5-flash)
python ameblo_poster.py \
  --title "AI近況" \
  --gemini-prompt "最新の AI トレンドについて日本語で書いてください。" \
  --gemini-model "gemini-1.5-pro"

# 生成した本文を下書きとして保存
python ameblo_poster.py \
  --title "週末の過ごし方" \
  --gemini-prompt "週末の充実した過ごし方を紹介するブログ記事を書いてください。" \
  --draft
```

### Gemini オプション

| オプション | 短縮形 | 説明 |
|---|---|---|
| `--gemini-prompt` | `-g` | Gemini AI に渡すプロンプト |
| `--gemini-api-key` | | Gemini API キー |
| `--gemini-model` | | モデル名 (デフォルト: `gemini-1.5-flash`) |

## 認証情報の設定方法

優先順位: コマンドライン引数 > 環境変数 > config.json

### config.json (推奨)

```json
{
  "username": "your_ameblo_id",
  "password": "your_password",
  "gemini_api_key": "your_gemini_api_key"
}
```

### 環境変数

```bash
export AMEBLO_USER="your_ameblo_id"
export AMEBLO_PASS="your_password"
export GEMINI_API_KEY="your_gemini_api_key"
```

### コマンドライン引数

```bash
python ameblo_poster.py --username myid --password mypass --title "..." --body "..."
```

## オプション一覧

| オプション | 短縮形 | 説明 |
|---|---|---|
| `--username` | `-u` | アメブロ ID |
| `--password` | `-p` | パスワード |
| `--title` | `-t` | 記事タイトル (必須) |
| `--body` | `-b` | 記事本文 (直接入力) |
| `--body-file` | `-f` | 本文ファイルパス |
| `--category` | `-c` | カテゴリ名 (部分一致) |
| `--images` | `-i` | 画像ファイルパス (複数可) |
| `--draft` | `-d` | 下書き保存 |
| `--gemini-prompt` | `-g` | Gemini AI プロンプト (本文自動生成) |
| `--gemini-api-key` | | Gemini API キー |
| `--gemini-model` | | Gemini モデル名 |
| `--config` | | 設定ファイルパス (デフォルト: config.json) |
| `--show-browser` | | ブラウザを表示して実行 |

## 出力ファイル

| ファイル | 内容 |
|---|---|
| `post_success.png` | 投稿成功時のスクリーンショット |
| `post_error.png` | エラー時のスクリーンショット |
| `login_error.png` | ログイン失敗時のスクリーンショット |

## 注意事項

- **利用規約**: アメブロの利用規約に従って使用してください。過度な自動アクセスは規約違反になる場合があります。
- **認証情報**: `config.json` はリポジトリにコミットしないでください (`.gitignore` に設定済み)。
- **2段階認証**: 2段階認証が有効な場合は、ログインが失敗することがあります。
- **UI変更**: アメブロの UI が変更された場合、セレクタの更新が必要になることがあります。
- **Gemini API**: Gemini API の利用には Google AI Studio での API キー取得が必要です。API の利用料金については Google の料金体系をご確認ください。
