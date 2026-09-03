"""
utils/timezone.py
------------------
Streamlit Cloud's server runs in UTC. This file makes sure the app
always uses Pakistan time instead.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

APP_TZ = ZoneInfo("Asia/Karachi")


def local_now() -> datetime:
    return datetime.now(APP_TZ).replace(tzinfo=None)


def local_today():
    return local_now().date()