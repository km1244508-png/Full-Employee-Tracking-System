"""
database/models.py
-------------------
SQLAlchemy ORM models: User, Employee, Attendance, Task.
"""

from datetime import datetime, date as _date, timezone

from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime, Boolean,
    ForeignKey, Text
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """Login account. Every Employee has exactly one linked User (1:1)."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(20), nullable=False, default="Employee")  # Admin / Employee
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    employee = relationship("Employee", back_populates="user", uselist=False)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String(120), nullable=False)
    email = Column(String(120))
    department = Column(String(80))
    designation = Column(String(80))
    date_joined = Column(Date, default=_date.today)
    shift_start = Column(String(5))  # "HH:MM", overrides config default if set
    shift_end = Column(String(5))
    is_active = Column(Boolean, default=True, nullable=False)
    qr_token = Column(String(64), unique=True, index=True)  # permanent attendance QR

    user = relationship("User", back_populates="employee")
    attendance_records = relationship(
        "Attendance", back_populates="employee", cascade="all, delete-orphan"
    )
    tasks = relationship(
        "Task", back_populates="employee", cascade="all, delete-orphan"
    )


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    hours_worked = Column(Float, default=0.0)
    status = Column(String(20), default="Absent")  # Present/Half-Day/Absent
    is_late = Column(Boolean, default=False)
    overtime_hours = Column(Float, default=0.0)
    notes = Column(Text)

    employee = relationship("Employee", back_populates="attendance_records")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="Not Started")
    assigned_date = Column(Date, default=_date.today)
    due_date = Column(Date)
    completed_date = Column(Date)
    progress_pct = Column(Integer, default=0)  # 0-100

    employee = relationship("Employee", back_populates="tasks")