import io
from datetime import datetime
from pathlib import Path

from fpdf import FPDF

FONT_CANDIDATES = [
    (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ),
    (
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ),
    (
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ),
]

LABEL_W = 52   # label ustuni kengligi (mm)


def resolve_pdf_fonts() -> tuple[str, str]:
    for regular, bold in FONT_CANDIDATES:
        if Path(regular).is_file() and Path(bold).is_file():
            return regular, bold
    searched = ", ".join(path for pair in FONT_CANDIDATES for path in pair)
    raise FileNotFoundError(
        f"PDF font fayllari topilmadi. Tekshirilgan yo'llar: {searched}"
    )


def generate_contract(
    contract_number: str,
    full_name: str,
    phone: str,
    jshshir: str,
    passport_id: str,
    level: str,
    direction: str,
    study_type: str,
    price: str,
    bank_account: str,
    bank_name: str,
    bank_mfo: str,
    date: str,
) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    font_path, font_bold = resolve_pdf_fonts()
    pdf.add_font("DJ", "", font_path)
    pdf.add_font("DJ", "B", font_bold)

    page_w = pdf.w - pdf.l_margin - pdf.r_margin   # ~190mm

    def h1(text):
        pdf.set_font("DJ", "B", 13)
        pdf.multi_cell(page_w, 8, text, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    def h2(text):
        pdf.set_font("DJ", "B", 10)
        pdf.multi_cell(page_w, 7, text, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    def body(text):
        pdf.set_font("DJ", "", 9)
        pdf.multi_cell(page_w, 6, text, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    def info_row(label, value):
        """Label va qiymatni bir qatorda chiqarish."""
        val_w = page_w - LABEL_W
        row_h = 6
        y = pdf.get_y()

        # Label
        pdf.set_font("DJ", "B", 9)
        pdf.set_xy(pdf.l_margin, y)
        pdf.cell(LABEL_W, row_h, label)

        # Value
        pdf.set_font("DJ", "", 9)
        pdf.set_xy(pdf.l_margin + LABEL_W, y)
        pdf.multi_cell(val_w, row_h, value, new_x="LMARGIN", new_y="NEXT")

    # ── Sarlavha ─────────────────────────────────────────────
    h1("ORIENTAL UNIVERSITETI")
    h1("TA'LIM XIZMATLARI KO'RSATISH SHARTNOMASI")

    pdf.set_font("DJ", "", 9)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_w, 6,
             f"Shartnoma No {contract_number}     Sana: {date}",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # ── Tomonlar jadvali ─────────────────────────────────────
    pdf.set_font("DJ", "B", 10)
    pdf.cell(page_w, 7, "TOMONLAR MA'LUMOTLARI", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(46, 134, 171)
    pdf.set_line_width(0.5)
    x0, x1 = pdf.l_margin, pdf.w - pdf.r_margin
    pdf.line(x0, pdf.get_y(), x1, pdf.get_y())
    pdf.ln(3)

    info_row("Universitet:",         "Oriental universiteti")
    info_row("Talaba (F.I.SH):",    full_name)
    info_row("Telefon:",             phone)
    info_row("JSHSHIR:",             jshshir if jshshir else "—")
    info_row("Pasport:",             passport_id if passport_id else "—")
    info_row("Ta'lim darajasi:",      level)
    info_row("Ta'lim yo'nalishi:",   direction)
    info_row("Ta'lim shakli:",       study_type)
    info_row("Yillik to'lov:",       price)
    info_row("Bank:",                bank_name)
    info_row("Hisob raqam (H/R):",   bank_account)
    info_row("MFO:",                 bank_mfo)
    pdf.ln(4)

    # ── I bo'lim ─────────────────────────────────────────────
    h2("I. SHARTNOMA MAZMUNI")
    body(
        "1.1. Mazkur shartnomaga muvofiq, Universitet Talabani belgilangan ta'lim standarti "
        "va o'quv rejasiga muvofiq o'qitish, Talaba esa shartnomada belgilangan tartib va "
        "miqdorda to'lov-kontrakt mablag'larini to'lash hamda Universitetning ichki "
        "tartib-qoidalariga rioya qilish majburiyatini oladi."
    )

    # ── II bo'lim ─────────────────────────────────────────────
    h2("II. TOMONLARNING HUQUQ VA MAJBURIYATLARI")
    body("2.1. Universitetning majburiyatlari:")
    body(
        "  \u2022  O'quv jarayonini qonunchilik hujjatlariga muvofiq malakali mutaxassislar "
        "yordamida tashkil etish;\n"
        "  \u2022  Talabani o'quv reja va dasturlarga muvofiq darsliklar, o'quv qo'llanmalari "
        "va axborot-resurs markazi xizmatlaridan foydalanishiga sharoit yaratish;\n"
        "  \u2022  O'quv rejasida ko'zda tutilgan amaliyotlarni o'tashini tashkil etish."
    )
    body("2.2. Talabaning majburiyatlari:")
    body(
        "  \u2022  O'quv intizomiga, Universitet ustavi va ichki tartib-qoidalariga qat'iy "
        "rioya qilish;\n"
        "  \u2022  Belgilangan o'quv rejadagi fanlarni o'zlashtirish va imtihonlarni topshirish;\n"
        "  \u2022  Shartnomada belgilangan to'lovlarni o'z vaqtida amalga oshirish."
    )

    # ── III bo'lim ────────────────────────────────────────────
    h2("III. TO'LOV MIQDORI VA TARTIBI")
    body(
        f"3.1. Bir o'quv yili uchun to'lov miqdori: {price}.\n"
        f"3.2. To'lovlar belgilangan muddatlarda bank muassasalari orqali Universitetning "
        f"hisob-raqamiga o'tkazilishi shart.\n"
        f"      Bank: {bank_name}\n"
        f"      H/R: {bank_account}   MFO: {bank_mfo}\n"
        "3.3. To'lov miqdori minimal ish haqi yoki bazaviy hisoblash miqdori o'zgarganda "
        "Universitet tomonidan bir tomonlama qayta ko'rib chiqilishi mumkin."
    )

    # ── IV bo'lim ─────────────────────────────────────────────
    h2("IV. SHARTNOMANI BEKOR QILISH")
    body(
        "4.1. Talaba o'z xohishiga ko'ra, o'qishdan chetlashtirilganda yoki boshqa oliy "
        "ta'lim muassasasiga ko'chirilganda shartnoma bekor qilinadi.\n"
        "4.2. Shartnoma majburiyatlari bajarilmaganda tomonlar qonunchilikda belgilangan "
        "tartibda javobgar bo'ladilar."
    )

    # ── Imzolar ──────────────────────────────────────────────
    pdf.ln(6)
    pdf.set_draw_color(46, 134, 171)
    pdf.line(x0, pdf.get_y(), x1, pdf.get_y())
    pdf.ln(4)

    col = page_w // 2
    pdf.set_font("DJ", "B", 9)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col, 6, "UNIVERSITET")
    pdf.cell(col, 6, "TALABA", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("DJ", "", 9)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col, 6, "Oriental universiteti")
    pdf.cell(col, 6, full_name, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)
    pdf.set_draw_color(150, 150, 150)
    pdf.line(x0,          pdf.get_y(), x0 + col - 5,  pdf.get_y())
    pdf.line(x0 + col + 5, pdf.get_y(), x1,            pdf.get_y())
    pdf.ln(4)
    pdf.set_font("DJ", "", 8)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col, 5, "Imzo / M.O.")
    pdf.cell(col, 5, "Imzo", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())


def make_contract_number(tg_id: int) -> str:
    year = datetime.now().year
    return f"OR-{year}-{tg_id % 100000:05d}"
