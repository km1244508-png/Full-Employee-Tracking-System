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
# Local/dev default: SQLite file in the project folder.
# Production: set DATABASE_URL env var to a PostgreSQL connection string
# (e.g. Supabase / Neon). No code changes needed anywhere else.
DATABASE_URL = os.environ.get("DATABASE_URL") or "sqlite:///attendance.db"

# ---------------------------------------------------------------------------
# Attendance business rules
# ---------------------------------------------------------------------------
# Standard shift start time used when an employee has no custom shift set.
DEFAULT_SHIFT_START = "09:00"   # 24hr HH:MM
DEFAULT_SHIFT_END = "18:00"     # 24hr HH:MM

# Minutes of lateness allowed before an employee is marked "Late".
GRACE_PERIOD_MINUTES = 10

# Hours worked beyond this in a single day count as overtime.
OVERTIME_THRESHOLD_HOURS = 8.0

# An employee who works fewer than this many hours (but more than 0)
# is marked "Half-Day" instead of "Present".
HALF_DAY_THRESHOLD_HOURS = 4.0

# Days of the week considered working days (0=Monday ... 6=Sunday).
WORKING_DAYS = [0, 1, 2, 3, 4, 5]  # Mon-Sat; change to [0,1,2,3,4] for Mon-Fri

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
