"""
config.py
---------
Single source of truth for all business rules and app-wide settings.
Change a rule here and it applies everywhere in the app — no need to
touch calculation logic, pages, or reports.
"""

import os
from dotenv import load_dotenv

# Load variables from a local .env file if present (e.g. DATABASE_URL).
# In production (Streamlit Cloud, etc.) set these as real environment
# variables / secrets instead of shipping a .env file.
load_dotenv()

# ---------------------------------------------------------------------------
# App identity
# ---------------------------------------------------------------------------
APP_NAME = "Employee Attendance & Working Hours Tracking System"
APP_ICON = "🕒"
COMPANY_NAME = os.environ.get("COMPANY_NAME", "Your Company")

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL") or "sqlite:///attendance.db"

# ---------------------------------------------------------------------------
# Attendance business rules
# ---------------------------------------------------------------------------
DEFAULT_SHIFT_START = "09:00"   # 24hr HH:MM
DEFAULT_SHIFT_END = "18:00"     # 24hr HH:MM

# Minutes of lateness allowed before an employee is marked "Absent".
GRACE_PERIOD_MINUTES = 10

OVERTIME_THRESHOLD_HOURS = 8.0
HALF_DAY_THRESHOLD_HOURS = 4.0
WORKING_DAYS = [0, 1, 2, 3, 4, 5]  # Mon-Sat; change to [0,1,2,3,4] for Mon-Fri

# ---------------------------------------------------------------------------
# QR Attendance (employee QR codes, USB scanner check-in/check-out)
# ---------------------------------------------------------------------------
# CRITICAL: this must be a long random secret, and must NOT be committed
# to git. Set it as a real environment variable / Streamlit secret in
# production. If this leaks, someone could forge QR tokens.
QR_SECRET_KEY = os.environ.get("QR_SECRET_KEY", "change-this-in-production")

# ---------------------------------------------------------------------------
# Work Progress (task tracking) rules
# ---------------------------------------------------------------------------
TASK_STATUS_NOT_STARTED = "Not Started"
TASK_STATUS_IN_PROGRESS = "In Progress"
TASK_STATUS_COMPLETED = "Completed"
TASK_STATUS_ON_HOLD = "On Hold"

# ---------------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------------
ROLE_ADMIN = "Admin"
ROLE_EMPLOYEE = "Employee"

# ---------------------------------------------------------------------------
# Export settings
# ---------------------------------------------------------------------------
EXPORT_DIR = os.environ.get("EXPORT_DIR", "exports")

# QR Attendance secret
QR_SECRET_KEY = os.environ.get("QR_SECRET_KEY", "change-this-in-production")