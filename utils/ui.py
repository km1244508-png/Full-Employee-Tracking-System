"""
utils/ui.py
-----------
Shared design system: global CSS, KPI cards, hero banners, section
titles, sidebar branding, and status badges. Keep all color/style
constants here so branding can be changed from one place.

Visual language: deep-slate "premium SaaS" dark theme (Deel / Linear /
Stripe style) — slate-900 canvas, slate-800 surfaces, ultra-subtle
borders, soft ambient shadows, Inter type, and a small semantic accent
set (indigo = primary/brand, emerald = active/positive, amber = pending,
rose = negative).
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Palette — deep slate dark theme
# ---------------------------------------------------------------------------
BG = "#0B1220"           # app canvas (near slate-950)
SURFACE = "#141B2D"      # cards, containers (slate-900/800 blend)
SURFACE_2 = "#1B2436"    # slightly raised surface (hover, sidebar footer)
BORDER = "rgba(255,255,255,0.08)"
BORDER_STRONG = "rgba(255,255,255,0.14)"

TEXT_PRIMARY = "#F1F5F9"   # slate-100
TEXT_MUTED = "#94A3B8"     # slate-400
TEXT_FAINT = "#64748B"     # slate-500

PRIMARY = "#6366F1"        # indigo-500 — brand / primary actions
PRIMARY_HOVER = "#7C7FF2"
EMERALD = "#10B981"        # active / positive
AMBER = "#F59E0B"          # pending / warning
ROSE = "#F43F5E"           # negative / absent

# Kept for backward-compat imports elsewhere in the codebase.
NAVY = SURFACE
NAVY_DARK = BG
BLUE = PRIMARY
LIGHT_BG = BG
TEXT_DARK = TEXT_PRIMARY

# A small curated accent palette used to give repeating card grids
# (Quick Navigation, KPI rows, etc.) visual variety without breaking
# the overall dark/indigo brand identity. Chosen to stay legible on a
# dark surface.
ACCENT_PALETTE = ["#6366F1", "#10B981", "#38BDF8", "#F59E0B", "#F472B6", "#2DD4BF"]

STATUS_COLORS = {
    "Present": EMERALD,
    "Late": AMBER,
    "Half-Day": "#FB923C",
    "Absent": ROSE,
    "Not Started": TEXT_FAINT,
    "In Progress": "#38BDF8",
    "Completed": EMERALD,
    "On Hold": AMBER,
}


def inject_global_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, .stApp, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }}

        html, body, .stApp {{
            color-scheme: dark !important;
        }}

        .stApp {{ background-color: {BG}; }}
        #MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; }}

        .block-container {{
            padding-top: 2.2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1220px;
        }}

        /* Slim, unobtrusive dark scrollbars — small polish detail that
           matches the rest of the premium-dark aesthetic. */
        ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 8px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #475569; }}

        /* ---------------------------------------------------------------
           Equal-height card rows: whenever cards are laid out with
           st.columns(), stretch every column to the tallest one in that
           row so cards with shorter text don't end up visually shorter.
           This is what keeps every "tracking box" the same size.
        --------------------------------------------------------------- */
        div[data-testid="stHorizontalBlock"] {{
            align-items: stretch !important;
            gap: 16px;
        }}

        /* Text colors — ensure everything is readable on dark bg */
        .stApp, .stMarkdown, p, span, label, li {{
            color: {TEXT_PRIMARY} !important;
        }}

        /* Tab styling */
        button[data-baseweb="tab"] {{
            color: {TEXT_MUTED} !important;
            border-bottom: 2px solid transparent !important;
        }}
        button[data-baseweb="tab"] p {{
            color: {TEXT_MUTED} !important;
            font-size: 14px !important;
            font-weight: 600 !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            border-bottom-color: {PRIMARY} !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] p {{
            color: {PRIMARY} !important;
            font-weight: 700 !important;
        }}

        /* Input fields */
        input, textarea, select {{
            background-color: {SURFACE} !important;
            color: {TEXT_PRIMARY} !important;
            border: 1px solid {BORDER_STRONG} !important;
            border-radius: 6px !important;
        }}
        input::placeholder {{
            color: {TEXT_FAINT} !important;
        }}

        /* Primary buttons */
        .stButton > button {{
            background-color: {PRIMARY} !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            transition: background-color 0.2s ease !important;
        }}
        .stButton > button:hover {{
            background-color: {PRIMARY_HOVER} !important;
        }}

        /* Download buttons */
        .stDownloadButton button {{
            background-color: {PRIMARY} !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
        }}
        .stDownloadButton button:hover {{
            background-color: {PRIMARY_HOVER} !important;
        }}

        /* Cards and containers */
        .element-container {{
            background-color: {SURFACE} !important;
            border-radius: 8px !important;
        }}

        /* Hero banner */
        .hero-banner {{
            background: linear-gradient(135deg, {PRIMARY} 0%, #818CF8 100%);
            color: white;
            padding: 32px;
            border-radius: 12px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.15);
        }}
        .hero-banner h1 {{
            color: white !important;
            font-size: 1.8rem;
            margin: 0 0 8px 0;
            font-weight: 800;
        }}
        .hero-banner p {{
            color: white !important;
            margin: 0;
            opacity: 0.95;
            font-size: 1rem;
        }}

        /* KPI Cards with color accent */
        .kpi-card {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 10px;
            padding: 18px;
            border-left: 4px solid var(--kpi-color, {PRIMARY});
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: all 0.2s ease;
            min-height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        .kpi-card:hover {{ 
            transform: translateY(-2px);
            border-left-color: var(--kpi-color, {PRIMARY});
        }}
        .kpi-icon {{ 
            font-size: 2rem;
            margin-bottom: 8px;
        }}
        .kpi-title {{
            font-weight: 700;
            color: {TEXT_PRIMARY} !important;
            font-size: 1rem;
            margin-bottom: 6px;
        }}
        .kpi-desc {{
            color: {TEXT_MUTED} !important;
            font-size: 0.85rem;
            line-height: 1.5;
        }}

        /* Section title */
        .section-title {{
            font-weight: 800;
            color: {TEXT_PRIMARY} !important;
            font-size: 1.25rem;
            margin: 24px 0 16px 0;
            letter-spacing: -0.5px;
        }}

        /* Status badge */
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: white !important;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: {SURFACE};
            border-right: 1px solid {BORDER};
        }}
        section[data-testid="stSidebar"] * {{
            color: {TEXT_PRIMARY} !important;
        }}
        section[data-testid="stSidebar"] button {{
            color: {TEXT_MUTED} !important;
        }}
        section[data-testid="stSidebar"] button:hover {{
            color: {TEXT_PRIMARY} !important;
            background-color: {SURFACE_2} !important;
        }}

        /* Expander */
        details {{
            background-color: {SURFACE} !important;
            border: 1px solid {BORDER} !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }}

        /* Table */
        .stDataFrame {{
            background-color: {SURFACE} !important;
        }}
        .stDataFrame th {{
            background-color: {SURFACE_2} !important;
            color: {TEXT_PRIMARY} !important;
        }}
        .stDataFrame td {{
            color: {TEXT_PRIMARY} !important;
            border-color: {BORDER} !important;
        }}

        /* Metrics */
        .stMetric {{
            background-color: {SURFACE};
            padding: 12px;
            border-radius: 8px;
            border: 1px solid {BORDER};
        }}

        /* Info/Warning/Error boxes */
        .stAlert {{
            background-color: {SURFACE};
            border: 1px solid {BORDER};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle_html: str, icon: str = "🕒"):
    st.markdown(
        f"""
        <div class="hero-banner">
            <h1>{icon} {title}</h1>
            <p>{subtitle_html}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text: str, icon: str = ""):
    st.markdown(
        f'<div class="section-title">{icon} {text}</div>',
        unsafe_allow_html=True,
    )


def render_sidebar_brand(app_name: str, app_icon: str):
    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align:center;padding:16px 0 24px 0;">
                <div style="font-size:2.2rem;margin-bottom:8px;">{app_icon}</div>
                <div style="font-weight:800;font-size:1.1rem;color:{TEXT_PRIMARY};line-height:1.3;">{app_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def status_badge(status: str) -> str:
    color = STATUS_COLORS.get(status, TEXT_FAINT)
    return f'<span class="status-badge" style="background-color:{color};">{status}</span>'


def kpi_card(icon: str, label: str, value, color: str = PRIMARY):
    st.markdown(
        f"""
        <div class="kpi-card" style="--kpi-color:{color};">
            <div class="kpi-icon">{icon}</div>
            <div style="font-weight:700;color:{TEXT_PRIMARY};font-size:1.6rem;margin-bottom:4px;">{value}</div>
            <div style="color:{TEXT_MUTED};font-size:0.85rem;">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )