"""
pages/2_Employee_Management.py
--------------------------------
Admin: add/edit/deactivate employees and manage login accounts.
Every user (admin or employee) can change their own password here too.
"""

import streamlit as st

import config
from database.db_setup import get_session
from database.models import Employee
from utils.auth import (
    require_login, is_admin, current_user_id, change_password,
    create_user_and_employee, set_employee_active, reset_password,
)
from utils.ui import inject_global_css, render_sidebar_brand, hero, section_title, status_badge

st.set_page_config(page_title="Employee Management", page_icon="👥", layout="wide")
inject_global_css()
require_login()
render_sidebar_brand(config.APP_NAME, config.APP_ICON)
hero("Employee Management", "Manage employee profiles and login accounts.", icon="👥")

session = get_session()

tab_names = ["Change My Password"]
if is_admin():
    tab_names = ["All Employees", "Add Employee", "Reset Employee Password"] + tab_names

tabs = st.tabs(tab_names)

# ---------------------------------------------------------------------
if is_admin():
    with tabs[0]:
        section_title("All Employees", "👥")
        employees = session.query(Employee).order_by(Employee.full_name).all()
        if not employees:
            st.info("No employees yet — add one in the next tab.")
        for emp in employees:
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 2, 1])
                with c1:
                    st.markdown(f"**{emp.full_name}**  \n{emp.designation or '-'} · {emp.department or '-'}")
                    st.caption(emp.email or "no email on file")
                with c2:
                    st.markdown(
                        status_badge("Present" if emp.is_active else "Absent")
                        .replace("Present", "Active").replace("Absent", "Inactive"),
                        unsafe_allow_html=True,
                    )
                    st.caption(f"username: {emp.user.username if emp.user else '—'}")
                with c3:
                    if emp.is_active:
                        if st.button("Deactivate", key=f"deact_{emp.id}"):
                            set_employee_active(emp.id, False)
                            st.rerun()
                    else:
                        if st.button("Reactivate", key=f"react_{emp.id}"):
                            set_employee_active(emp.id, True)
                            st.rerun()

    with tabs[1]:
        section_title("Add New Employee", "➕")
        with st.form("add_employee", clear_on_submit=True):
            c1, c2 = st.columns(2)
            full_name = c1.text_input("Full Name *")
            email = c2.text_input("Email")
            department = c1.text_input("Department")
            designation = c2.text_input("Designation")
            username = c1.text_input("Username *")
            password = c2.text_input("Temporary Password *", type="password")
            role = c1.selectbox("Role", [config.ROLE_EMPLOYEE, config.ROLE_ADMIN])
            shift_start = c2.text_input("Shift Start (HH:MM, optional)", placeholder=config.DEFAULT_SHIFT_START)
            shift_end = c1.text_input("Shift End (HH:MM, optional)", placeholder=config.DEFAULT_SHIFT_END)

            if st.form_submit_button("Create Employee", type="primary"):
                if not full_name or not username or not password:
                    st.error("Full name, username, and password are required.")
                else:
                    ok, msg = create_user_and_employee(
                        username=username, password=password, full_name=full_name,
                        role=role, email=email, department=department,
                        designation=designation, shift_start=shift_start, shift_end=shift_end,
                    )
                    (st.success if ok else st.error)(msg)
                    if ok:
                        st.rerun()

    with tabs[2]:
        section_title("Reset an Employee's Password", "🔑")
        employees = session.query(Employee).filter(Employee.user_id.isnot(None)).order_by(Employee.full_name).all()
        if employees:
            target = st.selectbox("Employee", employees, format_func=lambda e: e.full_name)
            new_pw = st.text_input("New Password", type="password", key="reset_pw")
            if st.button("Reset Password"):
                ok, msg = reset_password(target.user_id, new_pw)
                (st.success if ok else st.error)(msg)
        else:
            st.info("No employees available.")

# ---------------------------------------------------------------------
with tabs[-1]:
    section_title("Change My Password", "🔒")
    with st.form("change_pw"):
        old_pw = st.text_input("Current Password", type="password")
        new_pw = st.text_input("New Password", type="password")
        confirm_pw = st.text_input("Confirm New Password", type="password")
        if st.form_submit_button("Update Password", type="primary"):
            if new_pw != confirm_pw:
                st.error("New passwords do not match.")
            else:
                ok, msg = change_password(current_user_id(), old_pw, new_pw)
                (st.success if ok else st.error)(msg)
