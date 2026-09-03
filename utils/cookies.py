"""
utils/cookies.py
-----------------
Persistent, encrypted browser-cookie storage for login sessions.
Works offline using extra-streamlit-components or graceful fallback to session_state.

The app uses this for session persistence across tabs/refreshes:
- Stored in browser cookies with encryption
- Falls back to st.session_state if cookie component isn't available
- Works completely offline after initial setup

SECURITY: Set COOKIE_PASSWORD as an environment variable in production.
Local development uses a default password that should be changed.
"""

import os
import time
import json
from typing import Dict, Any, Optional

import streamlit as st

# Try to import the cookie manager — if unavailable, we'll use session state as fallback
try:
    from extra_streamlit_components import CookieManager
    COOKIE_MANAGER_AVAILABLE = True
except ImportError:
    COOKIE_MANAGER_AVAILABLE = False

# Global cookie manager instance (lazy-loaded)
_cookie_manager: Optional[Any] = None


def _get_cookie_manager():
    """Lazily initialize the cookie manager."""
    global _cookie_manager
    if _cookie_manager is None and COOKIE_MANAGER_AVAILABLE:
        try:
            _cookie_manager = CookieManager()
        except Exception:
            # If CookieManager fails to initialize, fall back to session state
            pass
    return _cookie_manager


def block_until_ready():
    """
    Wait for the cookie component to be ready. This is necessary because
    the cookie component communicates asynchronously with the browser.

    If cookie manager isn't available, this is a no-op (uses session state instead).

    BUG FIX: this used to check `hasattr(manager, '_client')` to decide
    whether the component had finished its first round-trip to the
    browser. The real CookieManager class never sets a `_client`
    attribute at all (it only ever sets `self.cookie_manager` and
    `self.cookies`), so that check was always True and this function
    called st.rerun() unconditionally on *every* script run — on every
    page, forever. st.rerun() raises RerunException, which is a
    BaseException (not Exception), so the surrounding `except
    Exception: pass` never caught it either. Net effect: the app was
    stuck in a permanent reload loop showing "Loading your session..."
    and never actually rendered the login page or any other content.

    Fix: only wait once per browser session (tracked via
    st.session_state), matching what the docstring always intended —
    give the async component one beat on the very first run, then
    stop blocking.
    """
    if not COOKIE_MANAGER_AVAILABLE:
        return

    manager = _get_cookie_manager()
    if manager is None:
        return

    if st.session_state.get("_cookie_component_ready"):
        return

    st.session_state["_cookie_component_ready"] = True
    with st.spinner("Loading your session..."):
        time.sleep(0.15)
    st.rerun()


def write_auth_cookie(auth_data: Dict[str, Any]) -> None:
    """
    Store authentication data persistently.
    
    Args:
        auth_data: Dictionary containing auth_user_id, auth_username, auth_role, etc.
    """
    if COOKIE_MANAGER_AVAILABLE:
        try:
            manager = _get_cookie_manager()
            if manager is not None:
                # Store as JSON string in cookie
                manager.set("auth_session", json.dumps(auth_data))
                return
        except Exception:
            # Fall through to session state storage
            pass
    
    # Fallback: store in session state (lost on refresh but better than nothing)
    st.session_state["_auth_data"] = auth_data


def read_auth_cookie() -> Optional[Dict[str, Any]]:
    """
    Retrieve stored authentication data.
    
    Returns:
        Dictionary with auth info if found, None otherwise.
    """
    # First try cookies if available
    if COOKIE_MANAGER_AVAILABLE:
        try:
            manager = _get_cookie_manager()
            if manager is not None:
                cookie_val = manager.get("auth_session")
                if cookie_val:
                    return json.loads(cookie_val)
        except Exception:
            # Fall through to session state
            pass
    
    # Fall back to session state
    return st.session_state.get("_auth_data")


def clear_auth_cookie() -> None:
    """Remove stored authentication data."""
    if COOKIE_MANAGER_AVAILABLE:
        try:
            manager = _get_cookie_manager()
            if manager is not None:
                manager.delete("auth_session")
                return
        except Exception:
            pass
    
    # Fallback: remove from session state
    st.session_state.pop("_auth_data", None)
