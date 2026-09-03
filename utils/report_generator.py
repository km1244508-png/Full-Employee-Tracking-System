"""
utils/report_generator.py
--------------------------
Builds every report as a pandas DataFrame, ready to render in
Streamlit or hand off to utils/export_utils.py for Excel/PDF export.
"""

from datetime import date, timedelta

import pandas as pd

from database.db_setup import get_session
from database.models import Attendance, Employee


def _base_query(session, start: date, end: date, employee_id: int | None = None):
    q = (
        session.query(Attendance, Employee)
        .join(Employee, Attendance.employee_id == Employee.id)
        .filter(Attendance.date >= start, Attendance.date <= end)
    )
    if employee_id:
        q = q.filter(Attendance.employee_id == employee_id)
    return q.order_by(Attendance.date.asc())


def _to_dataframe(rows) -> pd.DataFrame:
    records = []
    for att, emp in rows:
        records.append({
            "Date": att.date,
            "Employee": emp.full_name,
            "Department": emp.department or "-",
            "Check In": att.check_in.strftime("%H:%M") if att.check_in else "-",
            "Check Out": att.check_out.strftime("%H:%M") if att.check_out else "-",
            "Hours Worked": att.hours_worked or 0.0,
            "Overtime": att.overtime_hours or 0.0,
            "Status": att.status,
        })
    return pd.DataFrame(records)


def daily_report(target_date: date, employee_id: int | None = None) -> pd.DataFrame:
    session = get_session()
    rows = _base_query(session, target_date, target_date, employee_id).all()
    return _to_dataframe(rows)


def weekly_report(week_start: date, employee_id: int | None = None) -> pd.DataFrame:
    session = get_session()
    week_end = week_start + timedelta(days=6)
    rows = _base_query(session, week_start, week_end, employee_id).all()
    return _to_dataframe(rows)


def monthly_report(year: int, month: int, employee_id: int | None = None) -> pd.DataFrame:
    session = get_session()
    start = date(year, month, 1)
    end = date(year + 1, 1, 1) - timedelta(days=1) if month == 12 else date(year, month + 1, 1) - timedelta(days=1)
    rows = _base_query(session, start, end, employee_id).all()
    return _to_dataframe(rows)


def individual_report(employee_id: int, start: date, end: date) -> pd.DataFrame:
    session = get_session()
    rows = _base_query(session, start, end, employee_id).all()
    return _to_dataframe(rows)


def comparative_report(start: date, end: date) -> pd.DataFrame:
    """One row per employee: totals + attendance % over the date range."""
    session = get_session()
    rows = _base_query(session, start, end).all()
    df = _to_dataframe(rows)
    if df.empty:
        return df

    total_working_days = (end - start).days + 1

    summary = (
        df.groupby(["Employee", "Department"])
        .agg(
            Days_Present=("Status", lambda s: (s == "Present").sum() + (s == "Late").sum() + (s == "Half-Day").sum()),
            Days_Late=("Status", lambda s: (s == "Late").sum()),
            Days_Absent=("Status", lambda s: (s == "Absent").sum()),
            Total_Hours=("Hours Worked", "sum"),
            Total_Overtime=("Overtime", "sum"),
        )
        .reset_index()
    )
    summary["Attendance %"] = round(
        (summary["Days_Present"] / total_working_days) * 100, 1
    )
    return summary.sort_values("Attendance %", ascending=False)
