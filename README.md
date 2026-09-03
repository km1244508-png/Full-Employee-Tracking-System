# Employee Attendance & Working Hours Tracking System

A full-stack, production-ready Streamlit application for tracking employee
attendance, working hours, and task progress — with a modern, "top-company"
style dashboard UI.

## Features

- 🕒 **Mark Attendance** — check-in/out, auto-calculated hours, lateness, status
- 👥 **Employee Management** — add/edit/deactivate employees, manage login accounts
- 📊 **Dashboard** — KPI cards, weekly/monthly charts, attendance %, work-progress snapshot
- 📑 **Reports** — Daily / Weekly / Monthly / Individual / Comparative, exportable to Excel & PDF
- 📋 **Work Progress** — task assignment, progress tracking, automatic overdue flagging
- 🔐 Role-based access (Admin / Employee), bcrypt password hashing
- 🎨 Custom design system: branded sidebar, KPI cards, status badges, themed charts

## 1. Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

**Default login:** username `admin` / password `admin123`
→ Change this immediately under **Employee Management → Change My Password**.

## 2. Switch to a production database (PostgreSQL)

By default the app uses a local SQLite file (`attendance.db`). For deployment
on Streamlit Community Cloud (which does not persist local files across
restarts), point it at a free PostgreSQL instance (Supabase or Neon):

```bash
export DATABASE_URL="postgresql://user:password@host:5432/dbname"
```

No code changes are needed — every database call goes through SQLAlchemy.

## 3. Deploy to Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Point it at your repo, branch, and `app.py` as the entry point.
4. Under **Advanced settings → Secrets**, add:
   ```toml
   DATABASE_URL = "postgresql://user:password@host:5432/dbname"
   ```
5. Deploy. First load will auto-create tables and the default admin account.

## 4. Project structure

```
config.py                    # all business rules (grace period, overtime, etc.)
database/models.py           # Employee, Attendance, User, Task tables
database/db_setup.py         # connection, session, first-run setup
utils/auth.py                # login, roles, access control
utils/calculations.py        # hours/lateness/status/task-progress logic
utils/report_generator.py    # builds every report as a DataFrame
utils/export_utils.py        # Excel (.xlsx) / PDF export
utils/ui.py                  # shared design system (CSS, KPI cards, charts)
pages/                       # 5 app screens (Streamlit auto-navigation)
app.py                       # login screen + landing page
```

## 5. Making changes safely

- **Business rule change** (e.g. grace period, overtime threshold) → edit
  `config.py` only.
- **New report type** → add a function to `utils/report_generator.py`,
  add a tab in `pages/4_Reports.py`.
- **New field on Attendance/Employee/Task** → add the column in
  `database/models.py`; for SQLite dev, delete `attendance.db` to
  regenerate, or write a migration for production Postgres.
- **Styling / branding** → edit `utils/ui.py` (`NAVY`, `BLUE` color
  constants, `inject_global_css()`).

## 6. Security checklist before go-live

- [ ] Change the default admin password
- [ ] Enable HTTPS on your hosting provider
- [ ] Restrict database network access to the app only
- [ ] Set a password-rotation policy for Admin accounts
