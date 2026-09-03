"""
pages/4_Reports.py
--------------------
Daily / Weekly / Monthly / Individual / Comparative reports,
exportable to Excel and PDF. Employees are restricted to their own
individual report; admins get all report types.
"""

from datetime import date, timedelta

import streamlit as st

import config
from database.db_setup import get_session
from database.models import Employee
from utils.auth import require_login, is_admin, current_employee_id
from utils.ui import inject_global_css, render_sidebar_brand, hero, section_title
from utils import report_generator as rg
from utils.export_utils import to_excel_bytes, to_pdf_bytes

st.set_page_config(page_title="Reports", page_icon="📑", layout="wide")
inject_global_css()
require_login()
render_sidebar_brand(config.APP_NAME, config.APP_ICON)
hero("Reports", "Daily, weekly, monthly, individual & comparative reports.", icon="📑")

session = get_session()


def _export_buttons(df, filename_prefix, title):
    if df.empty:
        st.info("No data for this selection.")
        return
    st.dataframe(df, width='stretch', hide_index=True)
    c1, c2 = st.columns(2)
    c1.download_button(
        "⬇️ Download Excel", data=to_excel_bytes(df, sheet_name=filename_prefix[:31]),
        file_name=f"{filename_prefix}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    c2.download_button(
        "⬇️ Download PDF", data=to_pdf_bytes(df, title=title),
        file_name=f"{filename_prefix}.pdf", mime="application/pdf",
    )


if is_admin():
    tabs = st.tabs(["Daily", "Weekly", "Monthly", "Individual", "Comparative"])

    with tabs[0]:
        section_title("Daily Report", "📅")
        d = st.date_input("Date", value=date.today(), key="daily_date")
        df = rg.daily_report(d)
        _export_buttons(df, f"daily_report_{d}", f"Daily Report — {d}")

    with tabs[1]:
        section_title("Weekly Report", "📅")
        week_start = st.date_input("Week Starting (Monday)", value=date.today() - timedelta(days=date.today().weekday()), key="weekly_date")
        df = rg.weekly_report(week_start)
        _export_buttons(df, f"weekly_report_{week_start}", f"Weekly Report — starting {week_start}")

    with tabs[2]:
        section_title("Monthly Report", "📅")
        c1, c2 = st.columns(2)
        year = c1.number_input("Year", min_value=2000, max_value=2100, value=date.today().year)
        month = c2.number_input("Month", min_value=1, max_value=12, value=date.today().month)
        df = rg.monthly_report(int(year), int(month))
        _export_buttons(df, f"monthly_report_{year}_{month:02d}", f"Monthly Report — {year}-{month:02d}")

    with tabs[3]:
        section_title("Individual Report", "👤")
        employees = session.query(Employee).order_by(Employee.full_name).all()
        if employees:
            emp = st.selectbox("Employee", employees, format_func=lambda e: e.full_name, key="ind_emp")
            c1, c2 = st.columns(2)
            start = c1.date_input("From", value=date.today() - timedelta(days=30), key="ind_start")
            end = c2.date_input("To", value=date.today(), key="ind_end")
            df = rg.individual_report(emp.id, start, end)
            _export_buttons(df, f"individual_report_{emp.full_name}_{start}_{end}", f"Individual Report — {emp.full_name}")
        else:
            st.info("No employees found.")

    with tabs[4]:
        section_title("Comparative Report", "📊")
        c1, c2 = st.columns(2)
        start = c1.date_input("From", value=date.today() - timedelta(days=30), key="comp_start")
        end = c2.date_input("To", value=date.today(), key="comp_end")
        df = rg.comparative_report(start, end)
        _export_buttons(df, f"comparative_report_{start}_{end}", "Comparative Attendance Report")

else:
    section_title("My Attendance History", "👤")
    c1, c2 = st.columns(2)
    start = c1.date_input("From", value=date.today() - timedelta(days=30))
    end = c2.date_input("To", value=date.today())
    df = rg.individual_report(current_employee_id(), start, end)
    _export_buttons(df, f"my_attendance_{start}_{end}", "My Attendance Report")
