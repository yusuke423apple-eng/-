from fpdf import FPDF
from fpdf.enums import XPos, YPos

FONT  = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
INPUT = "/root/.claude/skills/bupura-sales/SKILL.md"
OUT   = "/home/user/-/BUPURA_skill_report.pdf"

# ── helpers ─────────────────────────────────────────────────────────────────

class PDF(FPDF):
    def header(self):
        self.set_fill_color(20, 50, 100)
        self.set_text_color(255, 255, 255)
        self.set_font("ja", "B", 9)
        self.cell(0, 9, "  小顔専門店 BUPURA（ブプラ）事業運営スキルファイル",
                  fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("ja", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"作成日：2026年5月5日　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　Page {self.page_no()}", align="C")


def h1(pdf, text):
    pdf.ln(4)
    pdf.set_fill_color(20, 50, 100)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("ja", "B", 12)
    pdf.cell(0, 10, f"  {text}", fill=True,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)


def h2(pdf, text):
    pdf.ln(3)
    pdf.set_fill_color(200, 215, 240)
    pdf.set_text_color(20, 50, 100)
    pdf.set_font("ja", "B", 10)
    pdf.cell(0, 8, f"  {text}", fill=True,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)


def h3(pdf, text):
    pdf.ln(2)
    pdf.set_text_color(20, 50, 100)
    pdf.set_font("ja", "B", 9)
    pdf.cell(0, 7, f"  {text}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)


def body(pdf, text, indent=3):
    pdf.set_font("ja", "", 9)
    pdf.set_text_color(40, 40, 40)
    pdf.set_x(pdf.l_margin + indent)
    pdf.multi_cell(0, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def note(pdf, text, bg=(255, 245, 220), fg=(160, 90, 0)):
    pdf.set_font("ja", "B", 9)
    pdf.set_text_color(*fg)
    pdf.set_fill_color(*bg)
    pdf.multi_cell(0, 7, f"  [!] {text}", border="L", fill=True,
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)


def table(pdf, headers, rows, col_widths):
    pdf.set_fill_color(50, 80, 140)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("ja", "B", 8)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 7, f" {h}", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_font("ja", "", 8)
    for ri, row in enumerate(rows):
        fill = ri % 2 == 0
        pdf.set_fill_color(235, 242, 255) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(30, 30, 30)
        for i, cell in enumerate(row):
            pdf.cell(col_widths[i], 6, f" {cell}", border=1, fill=fill)
        pdf.ln()
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)


def code_block(pdf, lines):
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font("ja", "", 8)
    pdf.set_text_color(50, 50, 50)
    for line in lines:
        pdf.set_x(pdf.l_margin + 3)
        pdf.cell(0, 5.5, line, fill=True,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)


def bullet(pdf, items, indent=6):
    pdf.set_font("ja", "", 9)
    pdf.set_text_color(40, 40, 40)
    for item in items:
        pdf.set_x(pdf.l_margin + indent)
        pdf.multi_cell(0, 5.5, f"・{item}",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def check_list(pdf, items):
    pdf.set_font("ja", "", 9)
    pdf.set_text_color(40, 40, 40)
    for item in items:
        pdf.set_x(pdf.l_margin + 4)
        pdf.cell(8, 6, "[ ]")
        pdf.multi_cell(0, 6, item,
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)


# ── build ────────────────────────────────────────────────────────────────────

pdf = PDF(orientation="P", unit="mm", format="A4")
pdf.add_font("ja", "",  FONT)
pdf.add_font("ja", "B", FONT)
pdf.set_margins(15, 20, 15)
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# cover
pdf.set_fill_color(10, 35, 80)
pdf.rect(0, 0, 210, 55, "F")
pdf.set_y(12)
pdf.set_text_color(255, 255, 255)
pdf.set_font("ja", "B", 17)
pdf.cell(0, 11, "小顔専門店 BUPURA（ブプラ）", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("ja", "B", 13)
pdf.cell(0, 10, "事業運営スキルファイル", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("ja", "", 8)
pdf.cell(0, 7, "開業日：2026年6月5日　｜　オーナー：芝浦工業大学職員（兼業）　｜　施術士：28歳女性", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_text_color(0, 0, 0)
pdf.ln(16)

# ── Part 1 ──────────────────────────────────────────────────────────────────
h1(pdf, "Part 1. 事業概要・収支シミュレーション")

h2(pdf, "基本情報")
table(pdf,
    ["項目", "内容"],
    [
        ["FC本部", "株式会社SPEEDspring（2026年3月 エアトリ連結子会社化）"],
        ["加盟店数", "197店舗（業界最大級）"],
        ["施術メソッド", "頭蓋骨小顔リフト3TS法（手技ベース・HIFU規制対象外）"],
        ["ロイヤリティ", "月額10〜11万円（固定）"],
        ["初期投資", "500万円〜（物件費込みで600〜780万円になる可能性あり）"],
        ["契約期間", "3年"],
    ],
    [45, 135]
)

h2(pdf, "収支シミュレーション")
table(pdf,
    ["シナリオ", "月商", "月次経費", "月次利益", "投資回収"],
    [
        ["楽観", "130万円", "約61万円", "約69万円", "約9ヶ月"],
        ["現実", "80万円",  "約61万円", "約19万円", "約26ヶ月"],
        ["悲観", "50万円",  "約61万円", "赤字",     "回収不能"],
    ],
    [30, 28, 30, 28, 64]
)
body(pdf, "損益分岐点：月60万円（1日2名 × 客単価12,000円 × 25日）")

h2(pdf, "総合判定：条件付きで可能性あり（60点/100点）")
note(pdf, "最大リスク：施術士1名体制。施術士が離職した翌日から売上ゼロ。全ての計画がここに集約する。",
     bg=(255, 235, 235), fg=(180, 30, 30))

# ── Part 2 ──────────────────────────────────────────────────────────────────
h1(pdf, "Part 2. 事業成功アクションプラン")

h2(pdf, "Phase 1（開業前）：基盤構築")
bullet(pdf, [
    "FC条件変更なしの書面をエアトリ買収後に取得",
    "施術士と競業避止条項付き雇用契約を締結",
    "業績連動ボーナス（月商80万円超で+3万円等）を事前合意",
    "開業前モニター10名を確保しGoogleレビューの種を作る",
])

h2(pdf, "Phase 2（6〜9月）：集客立ち上げ")
bullet(pdf, [
    "HOT PEPPER Beauty でオープン記念クーポン（初回60%OFF）",
    "Instagram リール投稿でBefore/After動画を週2本発信",
    "施術後に全員へGoogleレビュー依頼QRカードを配布",
])

h2(pdf, "Phase 3（10月〜）：安定・定着")
bullet(pdf, [
    "回数券・月額サブスクでLTV（顧客生涯価値）向上",
    "施術士2名体制への移行計画を開始",
])

h2(pdf, "KPI目標（開業6ヶ月時点）")
table(pdf,
    ["指標", "目標"],
    [
        ["月間来店数", "80名"],
        ["リピート率", "60%以上"],
        ["客単価", "12,000円以上"],
        ["月間売上", "80万円以上"],
        ["Googleレビュー", "30件以上（★4.5以上）"],
        ["Instagramフォロワー", "500人以上"],
    ],
    [80, 100]
)

# ── Part 3 ──────────────────────────────────────────────────────────────────
pdf.add_page()
h1(pdf, "Part 3. 開業前残タスク（オーナー自身が動くもの）")
note(pdf, "第1・2・4週および直前タスクは完了 or 本部対応済み。以下が残タスク。",
     bg=(235, 245, 255), fg=(20, 60, 140))

h2(pdf, "第3週タスク（5月19日〜25日）")
check_list(pdf, [
    "開業前モニター客10名の募集・予約確定（最優先）",
    "Googleレビュー依頼QRコードカードの作成・印刷",
    "近隣500m以内へのポスティング",
    "カウンセリング〜クロージングのロールプレイを3回実施",
    "カルテフォーマットの最終確定",
    "予約受付フローと1日の受付上限を決定",
])

h2(pdf, "追加タスク（本部対応外）")
table(pdf,
    ["タスク", "期限"],
    [
        ["スマホで売上・予約をリアルタイム確認できる設定", "5/25"],
        ["施術士との「毎日18時に1行報告」ルール合意", "5/11"],
        ["業績連動ボーナス条件の口頭合意", "5/11"],
        ["週次MTGのスケジュール設定（毎週土曜or日曜）", "5/11"],
        ["店舗総合保険（施術事故賠償）の加入", "5/31"],
        ["施術士のInstagram開設を促す", "5/25"],
    ],
    [140, 40]
)

# ── Part 4 ──────────────────────────────────────────────────────────────────
h1(pdf, "Part 4. 売上向上スキル集")

h2(pdf, "4-1. カウンセリングスキル（成約率向上）")
h3(pdf, "初回カウンセリングの黄金フロー（30分）")
code_block(pdf, [
    "①ヒアリング（10分）",
    "  ・「今一番気になっているお顔のお悩みは何ですか？」",
    "  ・「いつ頃からお悩みですか？」",
    "  ・「どんな状態になりたいですか？（理想のイメージ）」",
    "",
    "②ビフォー写真撮影（2分）：正面・横・斜め45度の3枚",
    "",
    "③体験施術（15分）",
    "  ・施術中に感触を言語化させる",
    "  ・変化が出た瞬間に鏡を見せる",
    "",
    "④クロージング（3分）",
    "  ・アフター写真を並べて変化を視覚化",
    "  ・「今日の変化を定着させるには◯回が必要です」と具体的回数を提示",
    "  ・回数券・サブスクを自然な流れで提案",
])

h3(pdf, "失敗しないクロージングの3原則")
bullet(pdf, [
    "比較提示：「10回券 = 98,000円、バラで買うより2万円お得です」",
    "期間提示：「月2回ペースで5ヶ月で理想に近づきます」",
    "損失回避：「今日の変化は72時間以内に戻りやすいので、次回は〇日以内がベストです」",
])

h2(pdf, "4-2. リピート率向上スキル")
h3(pdf, "次回予約を必ず取る習慣")
bullet(pdf, [
    "施術終了後、施術台の上で次回日程を提案する",
    "「次は2週間後の◯曜日はいかがですか？」と具体的に",
])

h3(pdf, "LINE公式アカウント活用")
table(pdf,
    ["タイミング", "配信内容"],
    [
        ["来店3日後", "「変化は続いていますか？」フォローメッセージ"],
        ["来店7日後", "自宅ケアのアドバイス"],
        ["次回予約7日前", "リマインド"],
        ["誕生月", "誕生日特典クーポン"],
        ["2ヶ月未来店", "再来店促進メッセージ"],
    ],
    [45, 135]
)

h2(pdf, "4-3. 客単価アップスキル")
bullet(pdf, [
    "アフター写真を見た感動の瞬間にサブスク・回数券を提案",
    "「首・デコルテのコリが小顔に影響しています」→ セットメニューへ誘導（+3,000〜5,000円）",
    "来店客の20%に物販提案 → 客単価+2,000〜3,000円",
])

pdf.add_page()
h2(pdf, "4-4. 新規集客スキル")
h3(pdf, "Instagram 投稿設計")
table(pdf,
    ["投稿タイプ", "頻度", "目的"],
    [
        ["Before/After（許可取得必須）", "週1", "効果の証明"],
        ["施術の一場面（リール）", "週2", "親近感・信頼感"],
        ["お客様の声", "週1", "社会的証明"],
        ["スタッフの日常・人柄", "週1", "ファン化"],
    ],
    [90, 25, 65]
)

h3(pdf, "Googleレビュー獲得スクリプト")
note(pdf,
     "「こちらのQRコードから30秒で書けます。★の数だけでも大丈夫です。」　目標：月5件以上・返信は24時間以内",
     bg=(240, 255, 245), fg=(20, 120, 60))

h3(pdf, "紹介プログラム")
note(pdf,
     "「ご紹介のお友達には初回30%OFF、ご紹介者様には3,000円分のポイントをプレゼントしています。」",
     bg=(240, 255, 245), fg=(20, 120, 60))

h2(pdf, "4-5. 接客・コミュニケーションスキル")
h3(pdf, "NGワード と 言い換え")
table(pdf,
    ["NGワード", "言い換え"],
    [
        ["「効果には個人差があります」", "「◯◯さんの場合は〜が期待できます」"],
        ["「たぶん大丈夫です」",         "「ご安心ください。〜です」"],
        ["「以上になります」",           "「施術は以上です」"],
    ],
    [90, 90]
)

h2(pdf, "4-6. 数字で管理するスキル")
h3(pdf, "毎日チェックする3つの数字")
bullet(pdf, [
    "当日の来店数：目標 3〜4名/日",
    "次回予約取得率：目標 80%以上",
    "リピート比率：60%以上を維持",
])

h3(pdf, "売上が落ちたときの診断チェック")
code_block(pdf, [
    "[ ] 新規が減った       → SNS・HOT PEPPERを見直す",
    "[ ] リピートが減った   → カウンセリング・接客を振り返る",
    "[ ] 客単価が下がった   → クロージングを練習する",
    "[ ] キャンセルが増えた → リマインド配信を強化する",
])

h2(pdf, "4-7. セルフブランディングスキル（施術士向け）")
bullet(pdf, [
    "Instagram で小顔知識・豆知識を定期投稿（専門性の発信）",
    "「◯◯サロン勤務の小顔スペシャリスト」とプロフィールに明記",
    "指名客を育てることが施術士定着の動機にもなる",
])

# ── Part 5 ──────────────────────────────────────────────────────────────────
h1(pdf, "Part 5. オーナーのリモート管理スキル")

h2(pdf, "平日不在でも回る仕組み")
table(pdf,
    ["管理項目", "方法", "頻度"],
    [
        ["売上・予約確認", "POSアプリをスマホに設定", "毎日"],
        ["施術士への報告依頼", "毎日18時にLINEで1行報告", "毎日"],
        ["課題・改善の共有", "週次MTG（土日営業後30分）", "週1回"],
        ["収支レビュー", "月次で確認", "月1回"],
    ],
    [55, 90, 35]
)

h2(pdf, "緊急時の連絡フロー")
code_block(pdf, [
    "施術中トラブル → 施術士がまず対応",
    "  → 対応困難な場合  → オーナーにLINE（即レス）",
    "  → 解決困難な場合  → FC本部サポート窓口に連絡",
])

pdf.ln(4)
pdf.set_font("ja", "", 8)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 6, "本スキルファイルは月次で見直し、数字に基づいてアップデートすること。", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.output(OUT)
print(f"PDF generated: {OUT}")
