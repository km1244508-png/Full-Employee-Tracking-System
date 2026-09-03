"""
utils/export_utils.py
-----------------------
Export a report DataFrame to Excel (.xlsx) or PDF, returned as raw
bytes so Streamlit's st.download_button can offer it directly —
nothing is written to disk on the server.
"""

import io

import pandas as pd
from fpdf import FPDF

import config


def _clean_text(text: str) -> str:
    """PDF ke liye special unicode characters ko safe standard characters mein convert karta hai."""
    if text is None:
        return ""
    text = str(text)
    # Unicode dashes ko safe ascii minus dash se replace karein
    text = text.replace("—", "-").replace("–", "-").replace("―", "-")
    # Baki unsupported characters ko handle karein
    return text.encode("latin-1", "replace").decode("latin-1")


def to_excel_bytes(df: pd.DataFrame, sheet_name: str = "Report") -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
        worksheet = writer.sheets[sheet_name[:31]]
        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max() if not df.empty else 0, len(str(col))) + 2
            worksheet.column_dimensions[chr(65 + i) if i < 26 else "A"].width = min(max_len, 40)
    buffer.seek(0)
    return buffer.getvalue()


class _ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(31, 56, 100)
        self.cell(0, 10, self.title_text, ln=True, align="C")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(102, 112, 127)
        self.cell(0, 6, _clean_text(config.COMPANY_NAME), ln=True, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def to_pdf_bytes(df: pd.DataFrame, title: str = "Attendance Report") -> bytes:
    pdf = _ReportPDF(orientation="L", unit="mm", format="A4")
    pdf.title_text = _clean_text(title)
    pdf.add_page()
    pdf.set_font("Helvetica", "", 8)

    if df.empty:
        pdf.cell(0, 10, "No data available for the selected range.", ln=True)
        return bytes(pdf.output())

    col_count = len(df.columns)
    page_width = pdf.w - 20
    col_width = page_width / col_count

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(46, 116, 181)
    pdf.set_text_color(255, 255, 255)
    for col in df.columns:
        pdf.cell(col_width, 8, _clean_text(str(col)), border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(30, 30, 30)
    fill = False
    for _, row in df.iterrows():
        pdf.set_fill_color(245, 247, 250) if fill else pdf.set_fill_color(255, 255, 255)
        for val in row:
            text = _clean_text(str(val))
            if len(text) > 22:
                text = text[:19] + "..."
            pdf.cell(col_width, 7, text, border=1, fill=True, align="C")
        pdf.ln()
        fill = not fill

    return bytes(pdf.output())