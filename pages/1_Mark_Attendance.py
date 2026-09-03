"""
pages/1_Mark_Attendance.py
---------------------------
Record daily check-in / check-out. Admins can mark for any employee;
regular employees can only mark their own attendance.
"""

from datetime import datetime, date

import streamlit as st

import config
from database.db_setup import get_session
from database.models import Employee, Attendance
from utils.auth import require_login, is_admin, current_employee_id
from utils.calculations import evaluate_attendance
from utils.timezone import local_now
from utils.ui import inject_global_css, render_sidebar_brand, hero, section_title, status_badge

st.set_page_config(page_title="Mark Attendance", page_icon="🕒", layout="wide")
inject_global_css()
require_login()
render_sidebar_brand(config.APP_NAME, config.APP_ICON)

hero("Mark Attendance", "Record check-in and check-out times.", icon="🕒")

session = get_session()

# ---------------------------------------------------------------------
# Choose employee (admin can pick anyone; employee is locked to self)
# ---------------------------------------------------------------------
if is_admin():
    employees = session.query(Employee).filter_by(is_active=True).order_by(Employee.full_name).all()
    if not employees:
        st.warning("No active employees found. Add employees from Employee Management first.")
        st.stop()
    names = [e.full_name for e in employees]
    selected_name = st.selectbox("Employee", names)
    employee = next(e for e in employees if e.full_name == selected_name)
else:
    employee = session.get(Employee, current_employee_id())
    if not employee:
        st.error("No employee profile linked to this account.")
        st.stop()
    st.markdown(f"Marking attendance for **{employee.full_name}**")

target_date = st.date_input("Date", value=date.today())

record = (
    session.query(Attendance)
    .filter_by(employee_id=employee.id, date=target_date)
    .first()
)

section_title("Today's Record", "📋")
col1, col2, col3 = st.columns(3)
col1.metric("Check In", record.check_in.strftime("%H:%M") if record and record.check_in else "—")
col2.metric("Check Out", record.check_out.strftime("%H:%M") if record and record.check_out else "—")
col3.metric("Hours Worked", f"{record.hours_worked:.2f}" if record else "0.00")

if record:
    st.markdown(status_badge(record.status), unsafe_allow_html=True)

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    if st.button("✅ Check In", width='stretch', type="primary",
                 disabled=bool(record and record.check_in)):
        if not record:
            record = Attendance(employee_id=employee.id, date=target_date)
            session.add(record)
        record.check_in = datetime.combine(target_date, local_now().time())
        result = evaluate_attendance(record.check_in, record.check_out, employee)
        for k, v in result.items():
            setattr(record, k, v)
        session.commit()
        st.success(f"Checked in at {record.check_in.strftime('%H:%M')}")
        st.rerun()

with c2:
    if st.button("🚪 Check Out", width='stretch',
                 disabled=not (record and record.check_in) or bool(record and record.check_out)):
        record.check_out = datetime.combine(target_date, local_now().time())
        result = evaluate_attendance(record.check_in, record.check_out, employee)
        for k, v in result.items():
            setattr(record, k, v)
        session.commit()
        st.success(f"Checked out at {record.check_out.strftime('%H:%M')}")
        st.rerun()

if is_admin():
    st.markdown("---")
    section_title("Manual Correction (Admin)", "🛠️")

    def _time_picker(label_prefix: str, existing_time):
        """12-hour Hour / Minute / AM-PM picker — avoids 24-hour format confusion."""
        if existing_time:
            default_hour_24 = existing_time.hour
            default_minute = existing_time.minute
            default_ampm = "PM" if default_hour_24 >= 12 else "AM"
            default_hour_12 = default_hour_24 % 12
            default_hour_12 = 12 if default_hour_12 == 0 else default_hour_12
        else:
            default_hour_12, default_minute, default_ampm = 12, 0, "AM"

        h1, h2, h3 = st.columns([1, 1, 1])
        hour = h1.selectbox(f"{label_prefix} Hour", list(range(1, 13)),
                             index=default_hour_12 - 1, key=f"{label_prefix}_hour")
        minute = h2.selectbox(f"{label_prefix} Minute", list(range(0, 60, 5)),
                               index=min(range(0, 60, 5), key=lambda m: abs(m - default_minute)) // 5,
                               key=f"{label_prefix}_minute")
        ampm = h3.selectbox(f"{label_prefix} AM/PM", ["AM", "PM"],
                             index=0 if default_ampm == "AM" else 1, key=f"{label_prefix}_ampm")

        hour_24 = hour % 12
        if ampm == "PM":
            hour_24 += 12
        from datetime import time as _time
        return _time(hour_24, minute)

    with st.form("manual_correction"):
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown("**Check-in time**")
            in_time = _time_picker("Check-in", record.check_in.time() if record and record.check_in else None)
        with mc2:
            st.markdown("**Check-out time**")
            out_time = _time_picker("Check-out", record.check_out.time() if record and record.check_out else None)

        clear_check_out = st.checkbox("Leave check-out empty (not checked out yet)")

        notes = st.text_area("Notes (optional)", value=record.notes if record else "")
        if st.form_submit_button("Save Correction"):
            new_check_in = datetime.combine(target_date, in_time) if in_time else None
            new_check_out = None if clear_check_out else (datetime.combine(target_date, out_time) if out_time else None)

            if new_check_in and new_check_out and new_check_out <= new_check_in:
                st.error(
                    "Check-out time is before check-in time. "
                    "Double-check the AM/PM selection for both times."
                )
            else:
                if not record:
                    record = Attendance(employee_id=employee.id, date=target_date)
                    session.add(record)
                record.check_in = new_check_in
                record.check_out = new_check_out
                record.notes = notes
                result = evaluate_attendance(record.check_in, record.check_out, employee)
                for k, v in result.items():
                    setattr(record, k, v)
                session.commit()
                st.success("Attendance record updated.")
                st.rerun()