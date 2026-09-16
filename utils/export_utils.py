"""
utils/export_utils.py
----------------------
Converts reports (pandas DataFrames) to formatted Excel (.xlsx) and
printable PDF files, returned as in-memory bytes so Streamlit's
download_button can serve them directly (no disk writes needed).
"""

import io
from datetime import datetime

import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from fpdf import FPDF

import config


def _sanitize_for_pdf(text) -> str:
    """
    The PDF core fonts (Helvetica) only support Latin-1. Report titles and
    data can contain characters like em-dashes, curly quotes, or bullets
    that would otherwise crash PDF generation. Replace the common ones
    with safe ASCII equivalents and strip anything else unsupported.
    """
    text = str(text)
    replacements = {
        "\u2014": "-", "\u2013": "-",   # em dash, en dash
        "\u2018": "'", "\u2019": "'",   # curly single quotes
        "\u201c": '"', "\u201d": '"',   # curly double quotes
        "\u2026": "...",                # ellipsis
        "\u2022": "-",                  # bullet
        "\u00a0": " ",                  # non-breaking space
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    # Drop any remaining characters the core font can't render.
    return text.encode("latin-1", "replace").decode("latin-1")


def _sanitize_sheet_name(name: str) -> str:
    """Excel sheet names can't contain : \\ / ? * [ ] and are capped at 31 chars."""
    invalid = ':\\/?*[]'
    for ch in invalid:
        name = name.replace(ch, "-")
    name = name.strip() or "Report"
    return name[:31]


def dataframe_to_excel_bytes(df: pd.DataFrame, sheet_name: str = "Report") -> bytes:
    sheet_name = _sanitize_sheet_name(sheet_name)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        ws = writer.sheets[sheet_name]

        header_fill = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid")
        header_font = Font(color="FFFFFF", bold=True)
        for col_idx, col_name in enumerate(df.columns, start=1):
            cell = ws.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")

        for col_idx, col_name in enumerate(df.columns, start=1):
            max_len = max(
                [len(str(col_name))] + [len(str(v)) for v in df[col_name].astype(str).tolist()]
            ) if len(df) else len(str(col_name))
            ws.column_dimensions[get_column_letter(col_idx)].width = min(max_len + 4, 40)

        ws.freeze_panes = "A2"

    buffer.seek(0)
    return buffer.getvalue()


class _ReportPDF(FPDF):
    def __init__(self, title: str):
        super().__init__(orientation="L", unit="mm", format="A4")
        self.report_title = title
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(31, 56, 100)  # navy
        self.cell(0, 10, _sanitize_for_pdf(config.APP_NAME), ln=1, align="C")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(80, 80, 80)
        self.cell(0, 7, _sanitize_for_pdf(self.report_title), ln=1, align="C")
        self.set_draw_color(46, 116, 181)
        self.line(10, self.get_y() + 1, self.w - 10, self.get_y() + 1)
        self.ln(6)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}  |  Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="C")


def dataframe_to_pdf_bytes(df: pd.DataFrame, title: str = "Report") -> bytes:
    pdf = _ReportPDF(_sanitize_for_pdf(title))
    pdf.add_page()

    if df.empty:
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 10, "No records found for the selected filters.", ln=1)
        return bytes(pdf.output(dest="S"))

    usable_width = pdf.w - 20
    n_cols = len(df.columns)
    col_width = usable_width / n_cols

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(31, 56, 100)
    pdf.set_text_color(255, 255, 255)
    for col in df.columns:
        pdf.cell(col_width, 8, _sanitize_for_pdf(col)[:28], border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(20, 20, 20)
    fill = False
    for _, row in df.iterrows():
        if pdf.get_y() > pdf.h - 20:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(31, 56, 100)
            pdf.set_text_color(255, 255, 255)
            for col in df.columns:
                pdf.cell(col_width, 8, _sanitize_for_pdf(col)[:28], border=1, align="C", fill=True)
            pdf.ln()
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(20, 20, 20)

        pdf.set_fill_color(237, 242, 248) if fill else pdf.set_fill_color(255, 255, 255)
        for val in row:
            text = _sanitize_for_pdf(val)
            if len(text) > 30:
                text = text[:27] + "..."
            pdf.cell(col_width, 7, text, border=1, align="C", fill=True)
        pdf.ln()
        fill = not fill

    return bytes(pdf.output(dest="S"))
# Aliases for backward compatibility with pages/4_Reports.py imports
to_excel_bytes = dataframe_to_excel_bytes
to_pdf_bytes = dataframe_to_pdf_bytes
