"""
database/db_setup.py
---------------------
Engine/session management + first-run table creation and default
admin seeding. Safe to call init_db() on every app start.
"""

import bcrypt
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import config
from database.models import Base, User, Employee

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

_connect_args = {}
if config.DATABASE_URL.startswith("sqlite"):
    # allow use across Streamlit's script-rerun threads
    _connect_args = {"check_same_thread": False}

engine = create_engine(config.DATABASE_URL, connect_args=_connect_args, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))


def get_session():
    """Return the shared scoped session (safe to call repeatedly)."""
    return SessionLocal


@st.cache_resource
def init_db():
    """
    Create all tables (idempotent) and seed a default admin user if
    the users table is empty. Cached so it only runs once per server
    process, not on every Streamlit rerun.
    """
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        if session.query(User).count() == 0:
            hashed = bcrypt.hashpw(
                DEFAULT_ADMIN_PASSWORD.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            admin_user = User(
                username=DEFAULT_ADMIN_USERNAME,
                password_hash=hashed,
                role=config.ROLE_ADMIN,
                is_active=True,
            )
            session.add(admin_user)
            session.flush()  # get admin_user.id

            admin_employee = Employee(
                user_id=admin_user.id,
                full_name="System Administrator",
                department="Management",
                designation="Administrator",
            )
            session.add(admin_employee)
            session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def default_admin_still_active() -> bool:
    """True if the seeded default admin account still has its default password."""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=DEFAULT_ADMIN_USERNAME).first()
        if not user:
            return False
        return bcrypt.checkpw(
            DEFAULT_ADMIN_PASSWORD.encode("utf-8"), user.password_hash.encode("utf-8")
        )
    finally:
        session.close()


def default_admin_notice() -> str:
    return (
        f"Default admin account is still active — username **{DEFAULT_ADMIN_USERNAME}**, "
        f"password **{DEFAULT_ADMIN_PASSWORD}**. Please change this password from "
        f"**Employee Management → Change My Password** before going live."
    )
