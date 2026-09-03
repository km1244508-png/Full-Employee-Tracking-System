"""
utils/auth.py
--------------
Login, logout, session state, role checks, and password management.
Passwords are hashed with bcrypt — never stored or compared in plaintext.

Session persistence: on top of st.session_state (fast, in-memory, but
tab-scoped), the same auth info is mirrored into an encrypted cookie via
utils/cookies.py. That way switching tabs, refreshing, or reopening the
app restores the session instead of forcing a re-login every time.
"""

import bcrypt
import streamlit as st

import config
from database.db_setup import get_session
from database.models import User, Employee
from utils.cookies import block_until_ready, read_auth_cookie, write_auth_cookie, clear_auth_cookie

_AUTH_KEYS = (
    "auth_user_id", "auth_username", "auth_role",
    "auth_employee_id", "auth_employee_name",
)


def _hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _check_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def login(username: str, password: str) -> bool:
    """Validate credentials and populate session state + persistent cookie on success."""
    if not username or not password:
        return False

    session = get_session()
    user = session.query(User).filter_by(username=username.strip()).first()

    if not user or not user.is_active:
        return False
    if not _check_password(password, user.password_hash):
        return False

    employee = session.query(Employee).filter_by(user_id=user.id).first()

    st.session_state["auth_user_id"] = user.id
    st.session_state["auth_username"] = user.username
    st.session_state["auth_role"] = user.role
    st.session_state["auth_employee_id"] = employee.id if employee else None
    st.session_state["auth_employee_name"] = employee.full_name if employee else user.username

    # Mirror into a persistent cookie so other tabs / a refresh /
    # reopening the browser pick the session back up automatically.
    write_auth_cookie({
        "auth_user_id": user.id,
        "auth_username": user.username,
        "auth_role": user.role,
        "auth_employee_id": employee.id if employee else None,
        "auth_employee_name": employee.full_name if employee else user.username,
    })

    return True


def logout():
    for key in _AUTH_KEYS:
        st.session_state.pop(key, None)
    clear_auth_cookie()


def _restore_session_from_cookie():
    """If session_state is empty (new tab / refresh / new session) but a
    valid login cookie exists, rehydrate session_state from it."""
    if "auth_user_id" in st.session_state:
        return
    data = read_auth_cookie()
    if not data or not data.get("auth_user_id"):
        return
    st.session_state["auth_user_id"] = data.get("auth_user_id")
    st.session_state["auth_username"] = data.get("auth_username")
    st.session_state["auth_role"] = data.get("auth_role")
    st.session_state["auth_employee_id"] = data.get("auth_employee_id")
    st.session_state["auth_employee_name"] = data.get("auth_employee_name")


def is_logged_in() -> bool:
    _restore_session_from_cookie()
    return "auth_user_id" in st.session_state


def is_admin() -> bool:
    return st.session_state.get("auth_role") == config.ROLE_ADMIN


def current_user_id():
    return st.session_state.get("auth_user_id")


def current_employee_id():
    return st.session_state.get("auth_employee_id")


def require_login():
    """Call at the top of a page to guard it; stops execution if not logged in.
    Also waits for the cookie component to be ready — it responds
    asynchronously, so it isn't available on the very first script run."""
    block_until_ready()
    if not is_logged_in():
        st.warning("Please log in first.")
        st.stop()


def require_admin():
    """Call at the top of an admin-only page."""
    require_login()
    if not is_admin():
        st.error("You don't have permission to view this page.")
        st.stop()


def change_password(user_id: int, old_password: str, new_password: str) -> tuple[bool, str]:
    session = get_session()
    user = session.get(User, user_id)
    if not user:
        return False, "User not found."
    if not _check_password(old_password, user.password_hash):
        return False, "Current password is incorrect."
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters."
    user.password_hash = _hash_password(new_password)
    session.commit()
    return True, "Password updated successfully."


def create_user_and_employee(
    username: str, password: str, full_name: str, role: str = "Employee",
    email: str = "", department: str = "", designation: str = "",
    shift_start: str = "", shift_end: str = "",
) -> tuple[bool, str]:
    """Admin-only: create a new login + employee record together."""
    session = get_session()
    if session.query(User).filter_by(username=username.strip()).first():
        return False, "Username already exists."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    user = User(
        username=username.strip(),
        password_hash=_hash_password(password),
        role=role,
        is_active=True,
    )
    session.add(user)
    session.flush()

    employee = Employee(
        user_id=user.id,
        full_name=full_name.strip(),
        email=email.strip(),
        department=department.strip(),
        designation=designation.strip(),
        shift_start=shift_start or None,
        shift_end=shift_end or None,
        is_active=True,
    )
    session.add(employee)
    session.commit()
    return True, "Employee account created."


def set_employee_active(employee_id: int, active: bool):
    """Deactivate/reactivate an employee AND their login in one step."""
    session = get_session()
    employee = session.get(Employee, employee_id)
    if not employee:
        return
    employee.is_active = active
    if employee.user:
        employee.user.is_active = active
    session.commit()


def reset_password(user_id: int, new_password: str) -> tuple[bool, str]:
    """Admin-only: force-reset another user's password (no old password needed)."""
    session = get_session()
    user = session.get(User, user_id)
    if not user:
        return False, "User not found."
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters."
    user.password_hash = _hash_password(new_password)
    session.commit()
    return True, "Password reset."