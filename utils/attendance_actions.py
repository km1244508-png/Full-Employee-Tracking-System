"""
utils/attendance_actions.py
-----------------------------
Single source of truth for check-in / check-out logic, so manual
button clicks and QR-scan events always apply the exact same rules
(Present / Late / Half-Day evaluation, hours calculation, etc.).
"""

from datetime import datetime

from database.models import Attendance
from utils.calculations import evaluate_attendance
from utils.timezone import local_now


def get_or_create_today_record(session, employee, target_date):
    record = (
        session.query(Attendance)
        .filter_by(employee_id=employee.id, date=target_date)
        .first()
    )
    if not record:
        record = Attendance(employee_id=employee.id, date=target_date)
        session.add(record)
    return record


def perform_check_in(session, employee, target_date):
    record = get_or_create_today_record(session, employee, target_date)
    if record.check_in:
        return False, f"{employee.full_name} is already checked in.", record

    record.check_in = datetime.combine(target_date, local_now().time())
    result = evaluate_attendance(record.check_in, record.check_out, employee)
    for k, v in result.items():
        setattr(record, k, v)
    session.commit()
    return True, f"{employee.full_name} checked in at {record.check_in.strftime('%H:%M')}", record


def perform_check_out(session, employee, target_date):
    record = get_or_create_today_record(session, employee, target_date)
    if not record.check_in:
        return False, f"{employee.full_name} hasn't checked in yet today.", record
    if record.check_out:
        return False, f"{employee.full_name} is already checked out.", record

    record.check_out = datetime.combine(target_date, local_now().time())
    result = evaluate_attendance(record.check_in, record.check_out, employee)
    for k, v in result.items():
        setattr(record, k, v)
    session.commit()
    return True, f"{employee.full_name} checked out at {record.check_out.strftime('%H:%M')}", record


def perform_qr_scan(session, employee, target_date):
    """
    One scan = one action: not checked in yet -> check in.
    Checked in but not out -> check out. Both done -> report already-complete.
    """
    record = get_or_create_today_record(session, employee, target_date)
    if not record.check_in:
        return perform_check_in(session, employee, target_date)
    if not record.check_out:
        return perform_check_out(session, employee, target_date)
    return False, f"{employee.full_name} has already completed attendance for today.", record