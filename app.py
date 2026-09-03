"""
app.py
------
Login / Sign-Up screen and landing page — entry point of the app.
"""

import streamlit as st

import config
from database.db_setup import init_db, default_admin_notice, default_admin_still_active
from utils.auth import login, logout, is_logged_in, is_admin, create_user_and_employee
from utils.cookies import block_until_ready
from utils.ui import (
    inject_global_css, hero, section_title, render_sidebar_brand,
    ACCENT_PALETTE, TEXT_PRIMARY, TEXT_MUTED,
)

st.set_page_config(
    page_title=config.APP_NAME,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",  # FIX: sidebar was hidden by default
)

# Show loading indicator immediately
st.markdown("⏳ Initializing app...")

inject_global_css()

# The cookie component responds asynchronously — it isn't ready on the
# very first script run. This shows a brief spinner and reruns itself
# rather than freezing the page blank.
block_until_ready()

# Create tables + seed default admin on first run (safe to call every time).
init_db()


def render_login():
    st.markdown("<div style='height:4vh'></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.15, 1])
    with col:
        st.markdown(
            f"""
            <div style="text-align:center;margin-bottom:18px;">
                <div style="font-size:2.6rem;">{config.APP_ICON}</div>
                <div style="font-size:1.5rem;font-weight:800;color:{TEXT_PRIMARY};margin-top:4px;">
                    {config.APP_NAME}
                </div>
                <div style="color:{TEXT_MUTED};font-size:0.95rem;margin-top:4px;">
                    Sign in to your workspace
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])

            with tab_login:
                with st.form("login_form", clear_on_submit=False):
                    username = st.text_input("Username", placeholder="e.g. admin")
                    password = st.text_input("Password", type="password", placeholder="••••••••")
                    submitted = st.form_submit_button("Log In →", type="primary", width='stretch')

                if submitted:
                    if login(username, password):
                        st.success("Login successful.")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

            with tab_signup:
                with st.form("signup_form", clear_on_submit=False):
                    full_name = st.text_input("Full Name", placeholder="e.g. Ali Raza")
                    new_username = st.text_input("Choose a Username", placeholder="e.g. ali.raza")
                    new_password = st.text_input("Choose a Password", type="password", placeholder="At least 6 characters")
                    confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")
                    email = st.text_input("Email (optional)", placeholder="you@example.com")
                    signed_up = st.form_submit_button("Sign Up →", type="primary", width='stretch')

                if signed_up:
                    if not full_name or not new_username or not new_password:
                        st.error("Full name, username, and password are required.")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        ok, msg = create_user_and_employee(
                            username=new_username,
                            password=new_password,
                            full_name=full_name,
                            role=config.ROLE_EMPLOYEE,
                            email=email,
                        )
                        if ok:
                            st.success("Account created! You can now log in from the Log In tab.")
                        else:
                            st.error(msg)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        if default_admin_still_active():
            st.info(default_admin_notice())


def render_landing():
    render_sidebar_brand(config.APP_NAME, config.APP_ICON)

    role = st.session_state.get("auth_role")
    username = st.session_state.get("auth_username")

    hero(
        f"Welcome back, {username} 👋",
        f"You're signed in as <b>{role}</b>. Use the sidebar to navigate the workspace.",
        icon=config.APP_ICON,
    )

    # FIX: each card now includes its real page path so it can be turned
    # into an actual clickable navigation link (previously these were
    # just decorative HTML divs with no click action at all).
    if is_admin():
        cards = [
            ("🕒", "Mark Attendance", "Record daily check-in / check-out for employees.", "pages/1_Mark_Attendance.py"),
            ("👥", "Employee Management", "Add, edit, or deactivate employees and login accounts.", "pages/2_Employee_Management.py"),
            ("📊", "Dashboard", "Real-time attendance and work-progress overview.", "pages/3_Dashboard.py"),
            ("📑", "Reports", "Daily, weekly, monthly, individual & comparative reports.", "pages/4_Reports.py"),
            ("📋", "Work Progress", "Assign and track tasks per employee.", "pages/5_Work_Progress.py"),
        ]
    else:
        cards = [
            ("📊", "Dashboard", "Your personal attendance overview.", "pages/3_Dashboard.py"),
            ("📑", "Reports", "Your own attendance history, exportable anytime.", "pages/4_Reports.py"),
            ("📋", "Work Progress", "View and update your assigned tasks.", "pages/5_Work_Progress.py"),
        ]

    section_title("Quick Navigation", "🧭")
    cols = st.columns(len(cards))
    for c, (icon, label, desc, page_path), color in zip(cols, cards, ACCENT_PALETTE):
        with c:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="border-left:4px solid {color};padding-left:12px;">
                        <div style="font-size:2rem;">{icon}</div>
                        <div style="font-weight:700;color:{TEXT_PRIMARY};margin:4px 0;">{label}</div>
                        <div style="color:{TEXT_MUTED};font-size:0.85rem;margin-bottom:10px;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # This is the actual clickable navigation — st.page_link
                # is Streamlit's built-in way to jump to another page.
                st.page_link(page_path, label="Open →")


if not is_logged_in():
    render_login()
else:
    render_landing()