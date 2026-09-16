"""
pages/6_QR_Attendance.py
--------------------------
Camera-based QR attendance scanner.

How it works:
- Uses the `streamlit-qrcode-scanner` component (pip install
  streamlit-qrcode-scanner) which opens the browser camera and scans
  QR codes using the html5-qrcode library.
- Unlike a raw components.html() + jsQR approach, this is a proper
  bidirectional Streamlit component: the scanned value is returned
  directly into Python (no page-navigation trick needed, so it isn't
  blocked by Streamlit's iframe sandbox).
- The moment an employee's QR is recognised, Streamlit reruns with
  the scanned value available immediately. We check the employee
  in/out and show a big status card, then loop back to scanning.

SETUP REQUIRED (run once in your project's terminal):
    pip install streamlit-qrcode-scanner
"""

from datetime import datetime

import streamlit as st

import config
from database.db_setup import get_session
from database.models import Employee, Attendance
from utils.auth import require_login
from utils.calculations import evaluate_attendance
from utils.timezone import local_now
from utils.ui import inject_global_css, render_sidebar_brand, hero, status_badge

try:
    from streamlit_qrcode_scanner import qrcode_scanner
except ImportError:
    qrcode_scanner = None

st.set_page_config(page_title="QR Attendance", page_icon="📷", layout="wide")
inject_global_css()
require_login()
render_sidebar_brand(config.APP_NAME, config.APP_ICON)

hero(
    "QR Attendance Scanner",
    "Apna QR camera ke saamne karein — check-in / check-out khud-ba-khud ho jayega.",
    icon="📷",
)

if qrcode_scanner is None:
    st.error(
        "⚠️ Zaroori package install nahi hai. Terminal mein ye chalayein:\n\n"
        "`pip install streamlit-qrcode-scanner`\n\n"
        "phir app ko restart karein."
    )
    st.stop()

session = get_session()

# ---------------------------------------------------------------------
# Result of the last scan, kept for 3 seconds so the badge is visible
# before we go back to live scanning.
# ---------------------------------------------------------------------
if "last_scan_result" not in st.session_state:
    st.session_state.last_scan_result = None
if "last_scan_time" not in st.session_state:
    st.session_state.last_scan_time = None

# If we're showing a result and 3 seconds have passed, clear it so the
# scanner becomes live again.
if st.session_state.last_scan_time:
    elapsed = (local_now() - st.session_state.last_scan_time).total_seconds()
    if elapsed > 3:
        st.session_state.last_scan_result = None
        st.session_state.last_scan_time = None

# ---------------------------------------------------------------------
# Showing the result of a just-completed scan.
# ---------------------------------------------------------------------
if st.session_state.last_scan_result:
    st.markdown("<div style='padding:24px 0;'>", unsafe_allow_html=True)
    kind, message, badge_html = st.session_state.last_scan_result
    if kind == "success":
        st.success(message)
    elif kind == "info":
        st.info(message)
    elif kind == "warning":
        st.warning(message)
    else:
        st.error(message)
    if badge_html:
        st.markdown(badge_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Scanner 3 second mein khud reset ho jayega...")
    st_autorefresh_ms = 3200
    st.markdown(
        f"<script>setTimeout(function(){{window.location.reload();}}, {st_autorefresh_ms});</script>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------
# Idle state — live camera, scanning continuously.
# ---------------------------------------------------------------------
else:
    st.markdown(
        """
        <div style="background:#141B2D;border:1px solid rgba(255,255,255,0.08);
                    border-radius:12px;padding:18px 20px;margin-bottom:16px;">
            <b>📡 Scanner live hai</b> — QR code ko camera ke saamne rakhein,
            khud detect ho kar check-in/check-out ho jayega. Kuch type ya
            click karne ki zaroorat nahi.
        </div>
        """,
        unsafe_allow_html=True,
    )

    scan_token = qrcode_scanner(key="attendance_qr_scanner")

    if scan_token:
        employee = (
            session.query(Employee)
            .filter_by(qr_token=scan_token, is_active=True)
            .first()
        )

        if not employee:
            st.session_state.last_scan_result = (
                "error",
                "❌ Ye QR pehchana nahi gaya. Mark Attendance page se dobara QR generate karwayein.",
                None,
            )
        else:
            today = local_now().date()
            record = (
                session.query(Attendance)
                .filter_by(employee_id=employee.id, date=today)
                .first()
            )
            if not record:
                record = Attendance(employee_id=employee.id, date=today)
                session.add(record)

            if not record.check_in:
                record.check_in = datetime.combine(today, local_now().time())
                action = "in"
            elif not record.check_out:
                record.check_out = datetime.combine(today, local_now().time())
                action = "out"
            else:
                action = "done"

            if action != "done":
                result = evaluate_attendance(record.check_in, record.check_out, employee)
                for k, v in result.items():
                    setattr(record, k, v)
                session.commit()

            if action == "in":
                st.session_state.last_scan_result = (
                    "success",
                    f"✅ **{employee.full_name}** checked IN at {record.check_in.strftime('%I:%M %p')}",
                    status_badge(record.status),
                )
            elif action == "out":
                st.session_state.last_scan_result = (
                    "info",
                    f"🚪 **{employee.full_name}** checked OUT at {record.check_out.strftime('%I:%M %p')} "
                    f"— {record.hours_worked:.2f} hours worked",
                    status_badge(record.status),
                )
            else:
                st.session_state.last_scan_result = (
                    "warning",
                    f"⚠️ **{employee.full_name}** ka aaj check-in aur check-out dono ho chuke hain.",
                    status_badge(record.status),
                )

        st.session_state.last_scan_time = local_now()
        st.rerun()