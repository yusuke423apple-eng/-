from fpdf import FPDF
from fpdf.enums import XPos, YPos
import datetime

FONT_PATH = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
OUTPUT = "/home/user/-/BUPURA_feasibility_report.pdf"

class PDF(FPDF):
    def header(self):
        self.set_font("ja", "B", 9)
        self.set_fill_color(30, 60, 114)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "小顔専門店 BUPURA（ブプラ）事業可能性精査レポート", border=0, fill=True,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("ja", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, f"作成日：2026年5月5日　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　Page {self.page_no()}", align="C")


def add_section_title(pdf, text):
    pdf.ln(4)
    pdf.set_fill_color(30, 60, 114)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("ja", "B", 11)
    pdf.cell(0, 9, f"  {text}", border=0, fill=True,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)


def add_subsection(pdf, text):
    pdf.ln(2)
    pdf.set_fill_color(220, 230, 245)
    pdf.set_text_color(30, 60, 114)
    pdf.set_font("ja", "B", 10)
    pdf.cell(0, 8, f"  {text}", border=0, fill=True,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)


def add_body(pdf, text, indent=0):
    pdf.set_font("ja", "", 9)
    pdf.set_text_color(40, 40, 40)
    pdf.set_x(pdf.l_margin + indent)
    pdf.multi_cell(0, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def add_note(pdf, text, color=(200, 50, 50)):
    pdf.set_font("ja", "B", 9)
    pdf.set_text_color(*color)
    pdf.set_fill_color(255, 245, 245)
    pdf.multi_cell(0, 7, f"  [!] {text}", border="L", fill=True,
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)


def add_table(pdf, headers, rows, col_widths=None):
    if col_widths is None:
        w = (pdf.w - pdf.l_margin - pdf.r_margin) / len(headers)
        col_widths = [w] * len(headers)

    # header row
    pdf.set_fill_color(60, 90, 150)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("ja", "B", 8)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 7, f" {h}", border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("ja", "", 8)
    for ri, row in enumerate(rows):
        fill = ri % 2 == 0
        pdf.set_fill_color(240, 245, 255) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(30, 30, 30)
        for i, cell in enumerate(row):
            pdf.cell(col_widths[i], 6, f" {cell}", border=1, fill=fill, align="L")
        pdf.ln()
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)


def add_verdict_box(pdf, score, verdict, color=(30, 130, 80)):
    pdf.ln(3)
    pdf.set_fill_color(*color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("ja", "B", 13)
    pdf.cell(0, 12, f"  総合判定：{verdict}　　スコア：{score} / 100点",
             border=0, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)


def add_check_item(pdf, text, checked=False):
    mark = "[v]" if checked else "[ ]"
    pdf.set_font("ja", "", 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(10, 6, mark)
    pdf.multi_cell(0, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


# ── Build PDF ────────────────────────────────────────────────
pdf = PDF(orientation="P", unit="mm", format="A4")
pdf.add_font("ja", "", FONT_PATH)
pdf.add_font("ja", "B", FONT_PATH)
pdf.set_margins(15, 20, 15)
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# ── Cover block ──────────────────────────────────────────────
pdf.set_fill_color(15, 40, 90)
pdf.rect(0, 0, 210, 60, style="F")
pdf.set_y(14)
pdf.set_text_color(255, 255, 255)
pdf.set_font("ja", "B", 18)
pdf.cell(0, 12, "小顔専門店 BUPURA（ブプラ）", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("ja", "B", 14)
pdf.cell(0, 10, "事業可能性精査レポート", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("ja", "", 9)
pdf.cell(0, 7, "調査日：2026年5月5日　｜　運営本部：株式会社SPEEDspring（エアトリ傘下）", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_text_color(0, 0, 0)
pdf.ln(18)

# ── 0. 前提条件 ──────────────────────────────────────────────
add_section_title(pdf, "0. 調査対象・前提条件")
add_table(pdf,
    ["項目", "内容"],
    [
        ["事業形態", "フランチャイズ加盟"],
        ["オーナー", "芝浦工業大学職員（年収800万円）兼業"],
        ["開業予定", "2026年6月"],
        ["施術士", "28歳女性（1名体制）"],
        ["把握済み初期支出", "500万円"],
        ["調査ソース", "公式HP・FCポータル複数・矢野経済研究所市場調査"],
    ],
    [50, 130]
)

# ── 1. 本部実態 ──────────────────────────────────────────────
add_section_title(pdf, "1. BUPURA本部の実態")
add_table(pdf,
    ["項目", "内容"],
    [
        ["運営会社", "株式会社SPEEDspring"],
        ["設立", "2021年9月（約4.5年の若い会社）"],
        ["代表", "軸丸真衣"],
        ["本社", "福岡市東区"],
        ["資本金", "500万円"],
        ["加盟店数", "197店舗（業界最大級・2026年3月時点）"],
        ["親会社", "株式会社エアトリ（2026年3月に連結子会社化）"],
        ["口コミ評価", "平均☆4.90"],
    ],
    [55, 125]
)

add_note(pdf,
    "2026年3月、旅行・IT大手エアトリがSPEEDspringを買収。大手資本の集客力が期待できる反面、"
    "FC条件変更リスクあり。開業前に「条件変更なし」の書面取得が必須。"
)

# ── 2. 費用の実態 ────────────────────────────────────────────
add_section_title(pdf, "2. FC加盟費用の実態検証")
add_table(pdf,
    ["費目", "本部資料A", "本部資料B", "備考"],
    [
        ["加盟金", "220万円", "270万円", "資料により異なる"],
        ["研修費", "80万円", "含む", ""],
        ["設備・内装費", "300万円", "約200万円〜", "物件次第で変動"],
        ["合計目安", "600万円", "470万円〜", ""],
        ["ロイヤリティ", "月額11万円（固定）", "月額10万円（固定）", "売上連動でなく固定"],
        ["契約期間", "3年", "3年", ""],
    ],
    [40, 42, 42, 56]
)

add_note(pdf,
    "オーナーが把握の「500万円」は最低ライン。物件の礼金・保証金が上乗せされると"
    "実際の総投資額は600〜780万円になる可能性あり。今すぐ本部に書面で上限確認を。"
)

# ── 3. 収益性 ────────────────────────────────────────────────
add_section_title(pdf, "3. 収益性の精査")

add_subsection(pdf, "本部主張（公式資料）vs 現実的試算")
add_table(pdf,
    ["シナリオ", "月商", "主な月次経費", "月次利益", "投資回収期間"],
    [
        ["本部主張（最良）", "130〜150万円", "約50〜60万円", "70〜82万円", "10ヶ月〜1.5年"],
        ["現実（中間）", "80万円", "約61万円", "約19万円", "約26ヶ月"],
        ["悲観", "50万円", "約61万円", "▲約11万円（赤字）", "回収不能"],
    ],
    [32, 28, 52, 28, 40]
)

add_note(pdf,
    "本部数値は第三者検証なし・失敗事例の開示なし。現実シナリオでの投資回収は18〜30ヶ月が目安。",
    color=(180, 80, 0)
)

add_subsection(pdf, "損益分岐点")
add_body(pdf,
    "固定費概算：人件費25万円 ＋ 家賃10万円 ＋ ロイヤリティ11万円 ＋ その他5万円 ＝ 月51万円\n"
    "変動費率：約15%（消耗品・予約手数料等）\n"
    "損益分岐売上 ＝ 51万円 ÷（1 − 0.15）≒ 月60万円\n"
    "  → 客単価12,000円 × 50名 ＝ 1日2名ペースで達成可能", indent=3
)

pdf.add_page()

# ── 4. 市場環境 ──────────────────────────────────────────────
add_section_title(pdf, "4. 市場環境の精査")
add_table(pdf,
    ["指標", "数値・内容"],
    [
        ["国内エステ市場（2024年度）", "3,043億円（5年連続縮小）"],
        ["2025年度予測", "3,046億円（横ばい回復）"],
        ["女性向け施術市場", "1,918億円（前年比97.4%）"],
        ["HIFU規制（2024年6月）", "非医療従事者によるHIFU機器使用を全面禁止"],
        ["BUPURAへの影響", "手技ベース施術のため規制対象外 → 競合流入のチャンス"],
    ],
    [75, 105]
)

add_note(pdf,
    "HIFU禁止により競合エステが小顔メニューから撤退。BUPURAは手技ベースで規制外のため、"
    "需要の受け皿になれる絶好のタイミング。",
    color=(30, 100, 50)
)

# ── 5. SWOT ──────────────────────────────────────────────────
add_section_title(pdf, "5. SWOT分析")

swot_data = [
    {
        "title": "強み (Strengths)",
        "title_bg": (30, 90, 160),
        "body_bg": (235, 242, 255),
        "items": [
            "197店舗・口コミ☆4.90の実績ブランド",
            "手技ベースでHIFU規制の影響ゼロ",
            "エアトリ傘下で集客基盤が強化",
            "サブスクモデルで月次収益が安定",
            "オーナーの安定収入でリスク耐性あり",
        ],
    },
    {
        "title": "弱み (Weaknesses)",
        "title_bg": (200, 60, 60),
        "body_bg": (255, 240, 240),
        "items": [
            "施術士1名体制 → 離職即廃業リスク",
            "オーナーが平日日中不在",
            "本部設立4.5年で長期実績なし",
            "固定ロイヤリティで赤字時の負担大",
            "初期費用が過少見積もりの可能性",
        ],
    },
    {
        "title": "機会 (Opportunities)",
        "title_bg": (30, 140, 80),
        "body_bg": (235, 255, 242),
        "items": [
            "HIFU禁止で手技系小顔需要が流入",
            "競合サロン淘汰後の市場シェア獲得",
            "エアトリのマーケ・集客支援",
            "高所得層が多いエリアへの訴求",
        ],
    },
    {
        "title": "脅威 (Threats)",
        "title_bg": (180, 120, 30),
        "body_bg": (255, 248, 230),
        "items": [
            "エステ市場の長期縮小トレンド",
            "エアトリ買収後のFC条件変更",
            "美容クリニック（医療小顔）との競合",
            "施術士採用・定着の難化",
        ],
    },
]

full_w = pdf.w - pdf.l_margin - pdf.r_margin
col_w = full_w / 2 - 1

for i in range(0, 4, 2):
    left  = swot_data[i]
    right = swot_data[i + 1]

    # measure heights: title(7) + items*6 + bottom_pad(2)
    left_h  = 7 + len(left["items"])  * 6 + 2
    right_h = 7 + len(right["items"]) * 6 + 2
    box_h   = max(left_h, right_h)

    start_y = pdf.get_y()

    for col_idx, box in enumerate([left, right]):
        x = pdf.l_margin + col_idx * (col_w + 2)
        y = start_y

        # title bar
        pdf.set_xy(x, y)
        pdf.set_fill_color(*box["title_bg"])
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("ja", "B", 9)
        pdf.cell(col_w, 7, f"  {box['title']}", border=1, fill=True,
                 new_x=XPos.LEFT, new_y=YPos.NEXT)

        # body rows
        pdf.set_fill_color(*box["body_bg"])
        pdf.set_text_color(30, 30, 30)
        pdf.set_font("ja", "", 8)
        for item in box["items"]:
            pdf.set_x(x)
            pdf.cell(col_w, 6, f"  ・{item}", border="LR", fill=True,
                     new_x=XPos.LEFT, new_y=YPos.NEXT)

        # fill remaining height to align columns
        drawn_h = 7 + len(box["items"]) * 6
        remaining = box_h - drawn_h
        if remaining > 0:
            pdf.set_x(x)
            pdf.cell(col_w, remaining, "", border="LR", fill=True,
                     new_x=XPos.LEFT, new_y=YPos.NEXT)

        # bottom border
        pdf.set_x(x)
        pdf.cell(col_w, 0, "", border="B",
                 new_x=XPos.LEFT, new_y=YPos.NEXT)

    pdf.set_y(start_y + box_h + 3)

# ── 6. 総合判定 ──────────────────────────────────────────────
pdf.add_page()
add_verdict_box(pdf, 60, "条件付きで可能性あり", color=(30, 90, 160))
add_body(pdf,
    "ブランド力・市場ポジション・HIFU規制追い風は本物。ただし「施術士1名体制」という"
    "人的集中リスクが全ての前提を崩し得る最大のリスク。本部の謳う10ヶ月回収は楽観シナリオ。"
    "現実的には18〜30ヶ月での回収を想定して計画を立てるべき。"
)

# ── 7. 必須アクション ────────────────────────────────────────
add_section_title(pdf, "7. 事業成功のための必須アクション（優先順位順）")

add_subsection(pdf, "【最優先】施術士の確保・定着戦略")
add_body(pdf,
    "1. 雇用契約に競業避止条項・秘密保持条項を明記（退職後の独立開業防止）\n"
    "2. 業績連動ボーナス制度を開業前に設計（月商80万円超で+3万円等）\n"
    "3. 副施術士候補を今から1名リストアップ（緊急時の代替要員）\n"
    "4. 月次面談を必ず実施し不満を早期把握", indent=3
)

add_subsection(pdf, "【重要】本部への確認事項（開業前に書面取得）")
add_body(pdf,
    "1. エアトリ買収後のFC条件変更有無の確認書面\n"
    "2. 総投資額の上限（物件費込み）の書面確認\n"
    "3. 解約条件・違約金の詳細\n"
    "4. 本部紹介でない既存FCオーナー3名以上への直接ヒアリング", indent=3
)

add_subsection(pdf, "【重要】財務管理")
add_body(pdf,
    "1. 開業後6ヶ月分の固定費（約300万円）を手元に確保してから開業\n"
    "2. 月次で損益を管理し、3ヶ月連続赤字で集客施策を抜本見直し\n"
    "3. オーナー収入からの補填限度額を事前に設定（例：月20万円まで）", indent=3
)

# ── 8. 開業前チェックリスト ──────────────────────────────────
add_section_title(pdf, "8. 開業前チェックリスト")
items = [
    "エアトリ買収後の新FC条件を書面で確認済み",
    "実際の総投資額（物件費込み）が600万円以下に収まることを確認",
    "施術士と雇用契約（競業避止・秘密保持含む）締結済み",
    "既存FCオーナー（本部紹介外）へのヒアリング実施済み",
    "開業後6ヶ月の固定費相当（300万円）が手元に確保されている",
    "損益分岐（月60万円）の達成見込みを開業前モニターで確認",
    "Googleビジネスプロフィール・Instagram開設済み",
    "LINE公式アカウント開設・初回配信準備完了",
]
for item in items:
    add_check_item(pdf, item)

# ── KPI ──────────────────────────────────────────────────────
add_section_title(pdf, "9. KPIダッシュボード（月次チェック項目）")
add_table(pdf,
    ["指標", "目標値（開業6ヶ月時点）"],
    [
        ["月間来店客数", "60〜80名"],
        ["新規客数", "20〜30名/月"],
        ["リピート率", "60%以上"],
        ["客単価", "12,000円以上"],
        ["月間売上", "80万円以上"],
        ["Googleレビュー数", "30件以上（★4.5以上）"],
        ["Instagramフォロワー", "500人以上"],
    ],
    [80, 100]
)

# ── 情報ソース ────────────────────────────────────────────────
add_section_title(pdf, "調査情報ソース")
sources = [
    "BUPURA公式HP：https://bupura.jp/",
    "フランチャイズ比較ネット：https://www.fc-hikaku.net/bupura_fc",
    "フランチャイズの窓口：https://www.fc-mado.com/detail/3846",
    "フランチャイズWEBリポート：https://web-repo.jp/fc/10845",
    "ビジェント（BUPURA）：https://www.bgent.net/view/3162",
    "エアトリ プレスリリース（買収発表）：https://prtimes.jp/main/html/rd/p/000000088.000006481.html",
    "矢野経済研究所 エステ市場2025年調査：https://www.yano.co.jp/press-release/show/press_id/3764",
]
for s in sources:
    add_body(pdf, f"・{s}", indent=3)

pdf.output(OUTPUT)
print(f"PDF generated: {OUTPUT}")
