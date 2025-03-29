from io import BytesIO
from fpdf import FPDF


def download_meal_plan_txt(text, filename="meal_plan.txt"):
    return BytesIO(text.encode("utf-8"))


def download_meal_plan_pdf(text, filename="meal_plan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    # Output PDF as string and convert to BytesIO
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return BytesIO(pdf_bytes)
