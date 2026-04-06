#!/usr/bin/env python3
"""
斎藤一人さんの88の言葉 - 毎日の知恵セレクター
その日の気分・状況に合わせて最適な言葉を選んで表示する
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

import anthropic

# ─────────────────────────────────────────────
# 斎藤一人さんの88の言葉
# ─────────────────────────────────────────────
WISDOM_LIST = [
    {"no": 1,  "text": "人の心に灯をともすと自分の心に灯がともる。愛がないと人間て生きられないね。"},
    {"no": 2,  "text": "天に豊作を祈り、手は田を耕す。ありがとうを言おう、わくわく冒険しよう。"},
    {"no": 3,  "text": "人生は弱気になったら負けですよ。勇気をだして、知恵だして。"},
    {"no": 4,  "text": "今日一日だけ一生けん命いきよう。明日のことは考えないで。"},
    {"no": 5,  "text": "自分にたりないものは、人をほめる努力。"},
    {"no": 6,  "text": "魅力があれば、すべてがうまくいくから不思議。"},
    {"no": 7,  "text": "カンペキ主義はつかれるな。不カンペキ主義は楽しいな。楽しいからいつもニコニコ。"},
    {"no": 8,  "text": "本も読まないでのりこえられる時代じゃないですよ。"},
    {"no": 9,  "text": "よく考えて行えば成功まちがいないですよ。安心安心。"},
    {"no": 10, "text": "笑顔で仕事をしていると、どこに勉強に行くより頭が良くなる。"},
    {"no": 11, "text": "やりたい事は今やらないと、いつまでも出来ませんよ。"},
    {"no": 12, "text": "幸せっていっぱい言うと幸せになる。目があって幸せ、耳があって幸せ、命があって幸せ。"},
    {"no": 13, "text": "仲間がいるから楽しい。仲間がいるから前進できる。"},
    {"no": 14, "text": "足元を見て歩くと、道のすみに咲く花に気づけるし、人にやさしくできる。"},
    {"no": 15, "text": "元気なら一生働ける。よかったよかった。"},
    {"no": 16, "text": "人生にはいろいろな宝物があるけど、そのなかで最高の宝物は今日も元気で働けること。"},
    {"no": 17, "text": "困ったことがおきたら「面白いことがおきた」と言ってみな。奇跡がおきるから。"},
    {"no": 18, "text": "あなたの行く所に必ず日がさしますよ。だいじょうぶ、だいじょうぶ。"},
    {"no": 19, "text": "秋になると、なべ物がおいしい、紅葉がきれい。生まれてきてよかったよかった。"},
    {"no": 20, "text": "お金がないと愛する人を助けることができない。だから仕事をしよう。"},
    {"no": 21, "text": "なんにもないとき「ついてる」。こまったときは「ありがとう」。いいことあったら「かんしゃします」。これでしあわせ。"},
    {"no": 22, "text": "困った時に「ついてる」って言えないよね。だから口癖にするといいよ。"},
    {"no": 23, "text": "あなたにとって今が修行時です。笑顔でのりこえましょう。"},
    {"no": 24, "text": "あなたの笑顔は人も自分も助けるよ。"},
    {"no": 25, "text": "私は自分を信じています。信じているからどんな問題ものりこえられる。"},
    {"no": 26, "text": "みんな元気ですか。身体の具合の悪いとき、完ペキ主義になっていませんか。ありがとうはたりていますか。もう一度、頭に浮かんだ人に「ありがとう、ありがとう」。"},
    {"no": 27, "text": "やってやれないことはない。やらずにできるわけがない。"},
    {"no": 28, "text": "人は愛する人のためならガンバレル。"},
    {"no": 29, "text": "私は前進します。みんなが待っている所まで。"},
    {"no": 30, "text": "みんな元気ですか。ひとりさんも元気です。今日はいいことありますよ。"},
    {"no": 31, "text": "今起きている事は、私を成功に導くチャンスです。"},
    {"no": 32, "text": "闇夜に太陽を待つように、今みんなの笑顔を待っている人がたくさんいます。"},
    {"no": 33, "text": "明るく明るく、今日も明るく、明日も明るく。"},
    {"no": 34, "text": "笑顔でいること、愛のある言葉を話すことは、みんな自分のため。"},
    {"no": 35, "text": "ツイテル人はなにをやってもうまくいくが、ついてない人はなにをやってもうまくいかない。"},
    {"no": 36, "text": "命令するより指導する。競争するより協力する。みんな仲間だから。"},
    {"no": 37, "text": "こわくても平気だよ、なんにもおきないから。"},
    {"no": 38, "text": "うまくいっている人のまねをしてごらん。それだけで人生はうまくいくから。"},
    {"no": 39, "text": "自分ひとりだけでも「ガンバル」って言う人がみんなを助けるんだね。"},
    {"no": 40, "text": "幸せって小さな幸せを見つけて、また一歩階段を登る自分にありがとう。"},
    {"no": 41, "text": "楽しいから成功するんで、成功したから楽しいんじゃないですよ。"},
    {"no": 42, "text": "ありがとうって言うだけでこんなに幸せになるなんて。ありがとうが今日も幸せを運んでくれる。"},
    {"no": 43, "text": "明日よいことがあると思ってごらん。今幸せになるよ。"},
    {"no": 44, "text": "いつも笑顔でいるあなたに、悪い事は絶対におきない。"},
    {"no": 45, "text": "ますますいい笑顔で人助けしなくっちゃと思いました。みんなありがとう。"},
    {"no": 46, "text": "お米に感謝するとご飯がおいしい。ご飯がおいしいと一日たのしい。とくした、とくした。"},
    {"no": 47, "text": "がんばって働いた日はご飯がおいしいな。"},
    {"no": 48, "text": "いい日とは、自分に「ありがとう」を言える日。"},
    {"no": 49, "text": "ツイテいる人はどこまでもツイテいる。"},
    {"no": 50, "text": "思いやりのある言葉っていいよな。今日は少し話せたような気がする。"},
    {"no": 51, "text": "すぐ怒るやつは馬鹿だ。この言葉を世界に広げよう。"},
    {"no": 52, "text": "来るものこばまず、去るものおわず。バイバイ。"},
    {"no": 53, "text": "人生は気合いだ。りくつが通らないこともたまにはあるよね。"},
    {"no": 54, "text": "笑いながら食事をすると、健康になるよ。"},
    {"no": 55, "text": "ずぶとくいこう。負けたらだめだよ。"},
    {"no": 56, "text": "おめでとう。みんなの努力がすてきな奇跡をおこします。"},
    {"no": 57, "text": "みんなただガンバルだけではだめですよ。楽しくガンバッた人だけが不況に勝ち残る人ですよ。笑って笑って。"},
    {"no": 58, "text": "いいことが山ほどくる。"},
    {"no": 59, "text": "まだまだ頭がよくなるよ。だってそんなに使ってないもん。"},
    {"no": 60, "text": "毎日生きていることが魂の修行。むだなことはなにもない。"},
    {"no": 61, "text": "人生って楽しいことばかりじゃないけれど、苦しいことやつらいことをのりこえて、ほっとした時いつも心に浮かぶのはこの一言です。「母さん、私を生んでくれてありがとう」。"},
    {"no": 62, "text": "一寸先は光だ。明日が楽しみだな。"},
    {"no": 63, "text": "次はうまくいくからだいじょうぶ。"},
    {"no": 64, "text": "涙がながれる日もあるけど、次の日はなぜかいい日だ。"},
    {"no": 65, "text": "ありがとうを言うから人間。"},
    {"no": 66, "text": "ハイはみごとなハイ、笑顔はみごとな笑顔。それが商人。"},
    {"no": 67, "text": "私には福の神がついている。"},
    {"no": 68, "text": "頭がどんどんよくなる。自分の頭が大好き。"},
    {"no": 69, "text": "ついてる。"},
    {"no": 70, "text": "神様は私を絶対に見すてない。ありがとう、ありがとう。"},
    {"no": 71, "text": "マナーを守るあなたは素敵な人ですよ。"},
    {"no": 72, "text": "何があっても大丈夫。天があなたを守っているから。"},
    {"no": 73, "text": "今は考えることより行動です。自信を持ってね。"},
    {"no": 74, "text": "いいことは分けてあげる。みんなよろこぶから。"},
    {"no": 75, "text": "みんなで幸せになろうよ。人間だもん。"},
    {"no": 76, "text": "ありがとう、ありがとうを一日100回は言おうね。"},
    {"no": 77, "text": "ついているから、あわてない、あわてない。"},
    {"no": 78, "text": "つらくても、最後にはあなたが必ず勝ちますよ。"},
    {"no": 79, "text": "商人は定年がないから一生働ける。よかったよかった。"},
    {"no": 80, "text": "いいこと聞いたらすぐ実行。ほんとにすぐだぜ。"},
    {"no": 81, "text": "今日一日ひとにやさしく、自分にやさしくでいこう。"},
    {"no": 82, "text": "いい考えは明るさから生まれる。"},
    {"no": 83, "text": "生きてるだけで幸せって思える時が一番幸せ。"},
    {"no": 84, "text": "全員が暗いから、私は明るくいく。"},
    {"no": 85, "text": "小さな幸せを数えだしたら、大きな安心が手に入った。手があって幸せ、足があって幸せ、今日があって幸せ。"},
    {"no": 86, "text": "やさしさより強いものはないですよ。"},
    {"no": 87, "text": "今、神の愛により全ての事がうまくいっています。"},
    {"no": 88, "text": "幸せは全て自分の心から生まれる。"},
]

# ─────────────────────────────────────────────
# 佑輔の信条候補（貼り出し用）
# ─────────────────────────────────────────────
YUSUKE_MOTTOS = [3, 4, 11, 17, 25, 27, 31, 41, 73, 80, 84, 88]

# ─────────────────────────────────────────────
# 今日の言葉セレクター
# ─────────────────────────────────────────────
def select_wisdom(context: str = "", ameblo_recent: str = "") -> dict:
    """
    Claude APIを使い、今日の気分・文脈に最適な言葉を選ぶ。

    Args:
        context: 今日の気分や状況のメモ (任意)
        ameblo_recent: 最近のアメブロ記事内容 (任意)

    Returns:
        選ばれた言葉の辞書 {"no": int, "text": str, "reason": str}
    """
    client = anthropic.Anthropic()

    wisdom_text = "\n".join(
        f"[{w['no']}] {w['text']}" for w in WISDOM_LIST
    )

    today_str = date.today().strftime("%Y年%m月%d日")

    prompt_parts = [
        f"今日は {today_str} です。",
        "以下は斎藤一人さんの88の言葉です。",
        "",
        wisdom_text,
        "",
        "佑輔は起業家・ブロガーとして活動しており、前向きで行動力のある生き方を大切にしています。",
    ]

    if ameblo_recent:
        prompt_parts += [
            "",
            "【最近のアメブロ記事の内容】",
            ameblo_recent,
        ]

    if context:
        prompt_parts += [
            "",
            "【今日の佑輔の状況・気分】",
            context,
        ]

    prompt_parts += [
        "",
        "上記88の言葉の中から、今日の佑輔に最もふさわしい言葉を1つ選んでください。",
        "以下のJSON形式で回答してください（他のテキストは不要）:",
        '{"no": <番号>, "text": "<言葉>", "reason": "<選んだ理由（1〜2文）>"}',
    ]

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        messages=[
            {"role": "user", "content": "\n".join(prompt_parts)}
        ],
    )

    raw = message.content[0].text.strip()
    # JSON部分を抽出
    start = raw.find("{")
    end = raw.rfind("}") + 1
    result = json.loads(raw[start:end])
    return result


# ─────────────────────────────────────────────
# 表示ヘルパー
# ─────────────────────────────────────────────
BORDER = "=" * 60

def print_daily_wisdom(wisdom: dict):
    today_str = date.today().strftime("%Y年%m月%d日")
    print(BORDER)
    print(f"  斎藤一人さんの言葉  【{today_str}】")
    print(BORDER)
    print(f"\n  No.{wisdom['no']}")
    print(f"\n  「{wisdom['text']}」")
    if wisdom.get("reason"):
        print(f"\n  ▶ {wisdom['reason']}")
    print(f"\n{BORDER}\n")


def print_mottos():
    mottos = [w for w in WISDOM_LIST if w["no"] in YUSUKE_MOTTOS]
    print(BORDER)
    print("  佑輔の信条候補 ― 壁に貼っておきたい言葉")
    print(BORDER)
    for w in mottos:
        print(f"\n  No.{w['no']}")
        print(f"  「{w['text']}」")
    print(f"\n{BORDER}\n")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="斎藤一人さんの88の言葉 - 毎日の知恵セレクター",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 今日の言葉を選ぶ（コンテキストなし）
  python daily_wisdom.py

  # 今日の気分を伝えて選ぶ
  python daily_wisdom.py --context "新しいプロジェクトを始めた。少し不安もある。"

  # アメブロ記事内容も参考にする
  python daily_wisdom.py --context "..." --ameblo-file latest_post.txt

  # 佑輔の信条候補を表示（貼り出し用）
  python daily_wisdom.py --mottos
""",
    )
    parser.add_argument(
        "--context", "-c",
        default="",
        help="今日の状況・気分のメモ（任意）",
    )
    parser.add_argument(
        "--ameblo-file", "-a",
        default="",
        metavar="FILE",
        help="最近のアメブロ記事ファイルパス（任意）",
    )
    parser.add_argument(
        "--mottos",
        action="store_true",
        help="佑輔の信条候補リストを表示して終了",
    )
    parser.add_argument(
        "--no-api",
        action="store_true",
        help="Claude APIを使わず日付ベースで言葉を選ぶ（APIキー不要）",
    )
    args = parser.parse_args()

    if args.mottos:
        print_mottos()
        return

    ameblo_text = ""
    if args.ameblo_file:
        path = Path(args.ameblo_file)
        if path.exists():
            ameblo_text = path.read_text(encoding="utf-8")
        else:
            print(f"[WARN] ファイルが見つかりません: {args.ameblo_file}")

    if args.no_api:
        # APIなし: 日付から決定論的に選ぶ
        idx = date.today().toordinal() % len(WISDOM_LIST)
        w = WISDOM_LIST[idx]
        wisdom = {"no": w["no"], "text": w["text"], "reason": ""}
    else:
        try:
            wisdom = select_wisdom(context=args.context, ameblo_recent=ameblo_text)
        except Exception as e:
            print(f"[WARN] Claude API 呼び出し失敗: {e}")
            print("[INFO] 日付ベースのフォールバックモードで実行します")
            idx = date.today().toordinal() % len(WISDOM_LIST)
            w = WISDOM_LIST[idx]
            wisdom = {"no": w["no"], "text": w["text"], "reason": ""}

    print_daily_wisdom(wisdom)


if __name__ == "__main__":
    main()
