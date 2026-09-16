"""
utils/calculations.py
----------------------
Pure calculation logic for attendance status, hours worked, lateness,
and overtime. All thresholds are pulled from config.py — never
hardcoded here — so business-rule changes stay in one place.
"""

from datetime import datetime, date, time as dtime
from typing import Optional

import config
from utils.timezone import local_now


def _parse_hhmm(value: str) -> dtime:
    h, m = value.split(":")
    return dtime(int(h), int(m))


def get_shift_bounds(employee) -> tuple[dtime, dtime]:
    """Return (shift_start, shift_end) for an employee, falling back to config defaults."""
    start = _parse_hhmm(employee.shift_start) if getattr(employee, "shift_start", None) else _parse_hhmm(config.DEFAULT_SHIFT_START)
    end = _parse_hhmm(employee.shift_end) if getattr(employee, "shift_end", None) else _parse_hhmm(config.DEFAULT_SHIFT_END)
    return start, end


def is_working_day(d: date) -> bool:
    """Monday=0 ... Sunday=6, per config.WORKING_DAYS."""
    return d.weekday() in config.WORKING_DAYS


def compute_hours_worked(check_in: Optional[datetime], check_out: Optional[datetime]) -> float:
    """Final hours worked — only counted once check-out has happened.
    Returns 0.0 while a shift is still in progress. For a live/running
    total while the employee hasn't checked out yet, use
    compute_live_elapsed_hours() instead."""
    if not check_in or not check_out:
        return 0.0
    delta = check_out - check_in
    hours = delta.total_seconds() / 3600.0
    return round(max(hours, 0.0), 2)


def compute_live_elapsed_hours(check_in: Optional[datetime], check_out: Optional[datetime]) -> float:
    """Hours elapsed so far, live. If check_out exists, same as
    compute_hours_worked(). If the employee has checked in but not
    checked out yet, this counts up to *now* — use this for a
    real-time 'hours worked so far' display in the UI."""
    if not check_in:
        return 0.0
    end = check_out or local_now()
    delta = end - check_in
    hours = delta.total_seconds() / 3600.0
    return round(max(hours, 0.0), 2)


def compute_lateness_minutes(check_in: Optional[datetime], employee) -> float:
    """Minutes late relative to shift start. 0 or negative = on time/early."""
    if not check_in:
        return 0.0
    shift_start, _ = get_shift_bounds(employee)
    scheduled = datetime.combine(check_in.date(), shift_start)
    delta_minutes = (check_in - scheduled).total_seconds() / 60
    return round(delta_minutes, 2)


def compute_overtime(hours_worked: float) -> float:
    if hours_worked > config.OVERTIME_THRESHOLD_HOURS:
        return round(hours_worked - config.OVERTIME_THRESHOLD_HOURS, 2)
    return 0.0


def compute_status(check_in: Optional[datetime], check_out: Optional[datetime],
                    hours_worked: float, late_by_minutes: float) -> str:
    """
    Present / Absent (no check-in OR too late) / Half-Day.

    "Late" status removed — beyond GRACE_PERIOD_MINUTES, employee is
    marked Absent directly. Working hours are calculated completely
    separately (compute_hours_worked) and are NEVER zeroed out by
    this status — an employee marked Absent for lateness still gets
    their actual worked hours logged and shown.
    """
    if not check_in:
        return "Absent"

    if late_by_minutes > config.GRACE_PERIOD_MINUTES:
        return "Absent"

    if not check_out:
        return "Present"

    if hours_worked < config.HALF_DAY_THRESHOLD_HOURS:
        return "Half-Day"

    return "Present"


def evaluate_attendance(check_in: Optional[datetime], check_out: Optional[datetime], employee) -> dict:
    """Run the full pipeline and return all derived attendance fields."""
    hours_worked = compute_hours_worked(check_in, check_out)
    late_by_minutes = compute_lateness_minutes(check_in, employee)
    is_late = late_by_minutes > config.GRACE_PERIOD_MINUTES
    overtime = compute_overtime(hours_worked)
    status = compute_status(check_in, check_out, hours_worked, late_by_minutes)
    return {
        "hours_worked": hours_worked,
        "is_late": is_late,
        "late_by_minutes": late_by_minutes,
        "overtime_hours": overtime,
        "status": status,
    }


def task_progress_summary(tasks) -> dict:
    """Given a list of Task ORM objects, return counts + completion %."""
    total = len(tasks)
    if total == 0:
        return {"total": 0, "completed": 0, "in_progress": 0,
                "not_started": 0, "on_hold": 0, "completion_pct": 0.0,
                "overdue": 0}

    completed = sum(1 for t in tasks if t.status == config.TASK_STATUS_COMPLETED)
    in_progress = sum(1 for t in tasks if t.status == config.TASK_STATUS_IN_PROGRESS)
    not_started = sum(1 for t in tasks if t.status == config.TASK_STATUS_NOT_STARTED)
    on_hold = sum(1 for t in tasks if t.status == config.TASK_STATUS_ON_HOLD)

    today = date.today()
    overdue = sum(
        1 for t in tasks
        if t.due_date and t.due_date < today and t.status != config.TASK_STATUS_COMPLETED
    )

    return {
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "not_started": not_started,
        "on_hold": on_hold,
        "completion_pct": round((completed / total) * 100, 1),
        "overdue": overdue,
    }