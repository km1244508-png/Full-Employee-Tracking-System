"""
pages/3_Dashboard.py
----------------------
Real-time overview.
Admin: org-wide KPIs (present/late/absent today, active employees,
avg hours), today's live attendance table, work-progress snapshot,
and a 7-day attendance trend chart.
Employee: personal today's status + live hours, personal task
snapshot, and a 7-day personal hours chart.
"""

from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

import config
from database.db_setup import get_session
from database.models import Employee, Attendance, Task
from utils.auth import require_login, is_admin, current_employee_id
from utils.calculations import compute_live_elapsed_hours, task_progress_summary
from utils.ui import (
    inject_global_css, render_sidebar_brand, hero, section_title,
    status_badge, kpi_card, ACCENT_PALETTE, PRIMARY, EMERALD, AMBER, ROSE,
)

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
inject_global_css()
require_login()
render_sidebar_brand(config.APP_NAME, config.APP_ICON)

session = get_session()
today = date.today()


def _plotly_dark(fig):
    """Match the plotly chart chrome to the app's dark theme."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#F1F5F9",
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")
    return fig


# ===========================================================================
# ADMIN DASHBOARD
# ===========================================================================
if is_admin():
    hero("Dashboard", "Real-time attendance and work-progress overview.", icon="📊")

    employees = session.query(Employee).filter_by(is_active=True).order_by(Employee.full_name).all()
    today_records = {
        r.employee_id: r
        for r in session.query(Attendance).filter_by(date=today).all()
    }

    present = sum(1 for e in employees if today_records.get(e.id) and today_records[e.id].status in ("Present",))
    late = sum(1 for e in employees if today_records.get(e.id) and today_records[e.id].status == "Late")
    half_day = sum(1 for e in employees if today_records.get(e.id) and today_records[e.id].status == "Half-Day")
    absent = len(employees) - sum(1 for e in employees if e.id in today_records)

    checked_in_hours = [
        compute_live_elapsed_hours(r.check_in, r.check_out)
        for r in today_records.values() if r.check_in
    ]
    avg_hours = round(sum(checked_in_hours) / len(checked_in_hours), 2) if checked_in_hours else 0.0

    section_title("Today's Overview", "📌")
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: kpi_card("👥", "Active Employees", len(employees), color=PRIMARY)
    with k2: kpi_card("✅", "Present Today", present, color=EMERALD)
    with k3: kpi_card("⏰", "Late Today", late, color=AMBER)
    with k4: kpi_card("🚫", "Absent Today", absent, color=ROSE)
    with k5: kpi_card("🕒", "Avg Hours (live)", avg_hours, color="#38BDF8")

    section_title("Today's Attendance", "🕒")
    if not employees:
        st.info("No active employees found. Add employees from Employee Management first.")
    else:
        rows = []
        for e in employees:
            r = today_records.get(e.id)
            rows.append({
                "Employee": e.full_name,
                "Department": e.department or "-",
                "Status": r.status if r else "Absent",
                "Check In": r.check_in.strftime("%H:%M") if r and r.check_in else "-",
                "Check Out": r.check_out.strftime("%H:%M") if r and r.check_out else "-",
                "Hours (live)": compute_live_elapsed_hours(r.check_in, r.check_out) if r and r.check_in else 0.0,
            })
        df_today = pd.DataFrame(rows)
        for _, row in df_today.iterrows():
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([2.5, 1.3, 2, 1.2])
                c1.markdown(f"**{row['Employee']}**  \n_{row['Department']}_")
                c2.markdown(status_badge(row["Status"]), unsafe_allow_html=True)
                c3.markdown(f"In: {row['Check In']}  ·  Out: {row['Check Out']}")
                c4.metric("Hours", f"{row['Hours (live)']:.2f}", label_visibility="collapsed")

    section_title("Work Progress Snapshot", "📋")
    all_tasks = session.query(Task).all()
    summary = task_progress_summary(all_tasks)
    t1, t2, t3, t4, t5 = st.columns(5)
    with t1: kpi_card("📋", "Total Tasks", summary["total"], color=PRIMARY)
    with t2: kpi_card("✅", "Completed", summary["completed"], color=EMERALD)
    with t3: kpi_card("🔄", "In Progress", summary["in_progress"], color="#38BDF8")
    with t4: kpi_card("⏸️", "On Hold / Not Started", summary["on_hold"] + summary["not_started"], color=AMBER)
    with t5: kpi_card("⚠️", "Overdue", summary["overdue"], color=ROSE)
    st.progress(summary["completion_pct"] / 100 if summary["total"] else 0,
                text=f"Overall completion: {summary['completion_pct']}%")

    section_title("Last 7 Days — Attendance Trend", "📈")
    week_start = today - timedelta(days=6)
    week_records = (
        session.query(Attendance)
        .filter(Attendance.date >= week_start, Attendance.date <= today)
        .all()
    )
    trend_rows = []
    for d in [week_start + timedelta(days=i) for i in range(7)]:
        day_recs = [r for r in week_records if r.date == d]
        trend_rows.append({
            "Date": d.strftime("%a %d"),
            "Present": sum(1 for r in day_recs if r.status == "Present"),
            "Late": sum(1 for r in day_recs if r.status == "Late"),
            "Half-Day": sum(1 for r in day_recs if r.status == "Half-Day"),
        })
    df_trend = pd.DataFrame(trend_rows)
    if df_trend[["Present", "Late", "Half-Day"]].sum().sum() > 0:
        fig = px.bar(
            df_trend, x="Date", y=["Present", "Late", "Half-Day"],
            barmode="stack",
            color_discrete_map={"Present": EMERALD, "Late": AMBER, "Half-Day": "#FB923C"},
        )
        fig.update_layout(legend_title_text="")
        st.plotly_chart(_plotly_dark(fig), width='stretch')
    else:
        st.info("No attendance data yet for the last 7 days.")

# ===========================================================================
# EMPLOYEE (PERSONAL) DASHBOARD
# ===========================================================================
else:
    emp_id = current_employee_id()
    employee = session.get(Employee, emp_id) if emp_id else None

    hero(f"Welcome back, {employee.full_name if employee else 'there'} 👋",
         "Your personal attendance and work-progress overview.", icon="📊")

    if not employee:
        st.error("No employee profile linked to this account.")
        st.stop()

    today_record = session.query(Attendance).filter_by(employee_id=emp_id, date=today).first()
    live_hours = compute_live_elapsed_hours(
        today_record.check_in if today_record else None,
        today_record.check_out if today_record else None,
    )

    section_title("Today", "📌")
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("📅", "Status", today_record.status if today_record else "Absent", color=PRIMARY)
    with k2: kpi_card("🕒", "Hours (live)", f"{live_hours:.2f}", color="#38BDF8")
    with k3: kpi_card("➡️", "Check In", today_record.check_in.strftime("%H:%M") if today_record and today_record.check_in else "-", color=EMERALD)
    with k4: kpi_card("⬅️", "Check Out", today_record.check_out.strftime("%H:%M") if today_record and today_record.check_out else "-", color=AMBER)

    section_title("My Work Progress", "📋")
    my_tasks = session.query(Task).filter_by(employee_id=emp_id).all()
    summary = task_progress_summary(my_tasks)
    t1, t2, t3, t4 = st.columns(4)
    with t1: kpi_card("📋", "Total Tasks", summary["total"], color=PRIMARY)
    with t2: kpi_card("✅", "Completed", summary["completed"], color=EMERALD)
    with t3: kpi_card("🔄", "In Progress", summary["in_progress"], color="#38BDF8")
    with t4: kpi_card("⚠️", "Overdue", summary["overdue"], color=ROSE)
    st.progress(summary["completion_pct"] / 100 if summary["total"] else 0,
                text=f"My completion: {summary['completion_pct']}%")

    section_title("Last 7 Days — My Hours", "📈")
    week_start = today - timedelta(days=6)
    week_records = (
        session.query(Attendance)
        .filter(Attendance.employee_id == emp_id, Attendance.date >= week_start, Attendance.date <= today)
        .all()
    )
    by_date = {r.date: r for r in week_records}
    trend_rows = []
    for d in [week_start + timedelta(days=i) for i in range(7)]:
        r = by_date.get(d)
        trend_rows.append({
            "Date": d.strftime("%a %d"),
            "Hours": compute_live_elapsed_hours(r.check_in, r.check_out) if r and r.check_in else 0.0,
        })
    df_trend = pd.DataFrame(trend_rows)
    if df_trend["Hours"].sum() > 0:
        fig = px.bar(df_trend, x="Date", y="Hours", color_discrete_sequence=[PRIMARY])
        st.plotly_chart(_plotly_dark(fig), width='stretch')
    else:
        st.info("No attendance data yet for the last 7 days.")
