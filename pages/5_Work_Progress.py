"""
pages/5_Work_Progress.py
--------------------------
Assign and track tasks per employee. Admins assign tasks to anyone;
employees view and update progress on their own tasks (with
automatic overdue flagging by due date).
"""

from datetime import date

import streamlit as st

import config
from database.db_setup import get_session
from database.models import Employee, Task
from utils.auth import require_login, is_admin, current_employee_id
from utils.ui import inject_global_css, render_sidebar_brand, hero, section_title, status_badge

st.set_page_config(page_title="Work Progress", page_icon="📋", layout="wide")
inject_global_css()
require_login()
render_sidebar_brand(config.APP_NAME, config.APP_ICON)
hero("Work Progress", "Assign and track tasks per employee.", icon="📋")

session = get_session()
STATUSES = [config.TASK_STATUS_NOT_STARTED, config.TASK_STATUS_IN_PROGRESS,
            config.TASK_STATUS_COMPLETED, config.TASK_STATUS_ON_HOLD]
today = date.today()


def render_task_list(tasks, show_employee_name: bool):
    """Shared task-list renderer used by both the admin and employee views."""
    if not tasks:
        st.info("No tasks found.")
        return
    for task in tasks:
        overdue = task.due_date and task.due_date < today and task.status != config.TASK_STATUS_COMPLETED
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1.3, 1.3])
            with c1:
                title_line = f"**{task.title}**"
                if show_employee_name:
                    title_line += f"  ·  _{task.employee.full_name}_"
                st.markdown(title_line)
                if task.description:
                    st.caption(task.description)
                due_txt = f"Due: {task.due_date}" if task.due_date else "No due date"
                if overdue:
                    due_txt += "  ⚠️ OVERDUE"
                st.caption(due_txt)
            with c2:
                st.markdown(status_badge(task.status), unsafe_allow_html=True)
                st.progress(task.progress_pct / 100 if task.progress_pct else 0)
            with c3:
                can_edit = is_admin() or task.employee_id == current_employee_id()
                if can_edit:
                    new_status = st.selectbox(
                        "Update status", STATUSES,
                        index=STATUSES.index(task.status) if task.status in STATUSES else 0,
                        key=f"status_{task.id}", label_visibility="collapsed",
                    )
                    new_progress = st.slider(
                        "Progress %", 0, 100,
                        value=task.progress_pct or 0, key=f"prog_{task.id}", label_visibility="collapsed",
                    )
                    if st.button("Save", key=f"save_{task.id}"):
                        task.status = new_status
                        task.progress_pct = new_progress
                        if new_status == config.TASK_STATUS_COMPLETED and not task.completed_date:
                            task.completed_date = today
                        elif new_status != config.TASK_STATUS_COMPLETED:
                            task.completed_date = None
                        session.commit()
                        st.rerun()


if is_admin():
    tab1, tab2 = st.tabs(["All Tasks", "Assign New Task"])

    with tab1:
        section_title("All Tasks", "📋")
        all_employees = session.query(Employee).order_by(Employee.full_name).all()
        emp_filter = st.selectbox("Filter by employee", ["All"] + [e.full_name for e in all_employees])
        q = session.query(Task)
        if emp_filter != "All":
            q = q.join(Employee).filter(Employee.full_name == emp_filter)
        tasks = q.order_by(Task.due_date.asc().nullslast()).all()
        render_task_list(tasks, show_employee_name=True)

    with tab2:
        section_title("Assign a New Task", "➕")
        employees = [e for e in all_employees if e.is_active]
        if not employees:
            st.warning("No active employees to assign tasks to.")
        else:
            with st.form("assign_task", clear_on_submit=True):
                emp = st.selectbox("Assign To", employees, format_func=lambda e: e.full_name)
                title = st.text_input("Task Title *")
                description = st.text_area("Description")
                due = st.date_input("Due Date", value=today)
                if st.form_submit_button("Assign Task", type="primary"):
                    if not title:
                        st.error("Task title is required.")
                    else:
                        task = Task(
                            employee_id=emp.id, title=title, description=description,
                            due_date=due, status=config.TASK_STATUS_NOT_STARTED,
                        )
                        session.add(task)
                        session.commit()
                        st.success(f"Task assigned to {emp.full_name}.")
                        st.rerun()
else:
    section_title("My Tasks", "📋")
    my_tasks = (
        session.query(Task)
        .filter_by(employee_id=current_employee_id())
        .order_by(Task.due_date.asc().nullslast())
        .all()
    )
    render_task_list(my_tasks, show_employee_name=False)
