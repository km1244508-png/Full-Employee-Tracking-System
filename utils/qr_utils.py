"""
utils/qr_utils.py
------------------
Generates and manages each employee's permanent attendance QR code.

The QR encodes a random, unguessable token (NOT the raw employee ID),
stored on Employee.qr_token, so nobody can forge a code just by
knowing someone's employee ID. The token never changes once created,
so the printed/screenshotted QR keeps working forever.
"""

import io
import secrets

import qrcode

from database.db_setup import get_session
from database.models import Employee


def get_or_create_qr_token(employee: Employee) -> str:
    """Return the employee's permanent QR token, creating one the first
    time it's needed (covers employees added before this feature existed)."""
    if employee.qr_token:
        return employee.qr_token

    session = get_session()
    # Re-fetch inside the active session in case `employee` came from a
    # different session instance.
    db_employee = session.get(Employee, employee.id)
    token = secrets.token_hex(16)
    db_employee.qr_token = token
    session.commit()
    employee.qr_token = token
    return token


def make_qr_png(data: str) -> bytes:
    """Render a QR code for `data` and return PNG image bytes."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# Alias — some pages import this function under this name.
def generate_qr_image_bytes(data: str) -> bytes:
    return make_qr_png(data)


def find_employee_by_token(token: str):
    """Look up the active employee owning this QR token, or None."""
    session = get_session()
    return session.query(Employee).filter_by(qr_token=token, is_active=True).first()