# アメブロ自動投稿ツール

Playwright を使ってアメブロ (アメーバブログ) へ自動ログイン・投稿を行う Python ツールです。

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

## 認証情報の設定方法

優先順位: コマンドライン引数 > 環境変数 > config.json

### config.json (推奨)

```json
{
  "username": "your_ameblo_id",
  "password": "your_password"
}
```

### 環境変数

```bash
export AMEBLO_USER="your_ameblo_id"
export AMEBLO_PASS="your_password"
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
