import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==========================================
# 1. KONFIGURASI HALAMAN & DESIGN SYSTEM (CSS)
# ==========================================
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* =========================================================
   DESIGN TOKENS — Modern Blue Analytics
   ========================================================= */
:root {
    color-scheme: light;
    --primary-color: #2563EB;
    --background-color: #EAF3FF;
    --secondary-background-color: #FFFFFF;
    --text-color: #172554;

    --bg-main: #EAF3FF;
    --bg-secondary: #F3F7FD;
    --surface: #FFFFFF;
    --blue-primary: #2563EB;
    --blue-deep: #1E40AF;
    --blue-navy: #172554;
    --blue-sky: #60A5FA;
    --blue-soft: #BFDBFE;
    --blue-light: #DBEAFE;
    --cyan: #38BDF8;
    --teal: #0D9488;
    --indigo: #6366F1;
    --text-primary: #172554;
    --text-secondary: #64748B;
    --border: #D8E6F7;

    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --shadow-sm: 0 1px 2px rgba(23, 37, 84, 0.04), 0 2px 8px rgba(23, 37, 84, 0.04);
    --shadow-md: 0 2px 4px rgba(23, 37, 84, 0.04), 0 8px 24px rgba(37, 99, 235, 0.08);
    --shadow-lg: 0 4px 8px rgba(23, 37, 84, 0.05), 0 16px 32px rgba(37, 99, 235, 0.14);
    --ease: cubic-bezier(0.22, 0.61, 0.36, 1);
    --font: 'Inter', 'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif;
}

/* =========================================================
   KEYFRAMES (hanya opacity + transform, tanpa looping)
   ========================================================= */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

/* =========================================================
   BASE: PAGE, BACKGROUND & TYPOGRAPHY
   ========================================================= */
.stApp {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: var(--font);
    -webkit-font-smoothing: antialiased;
}
.stApp p,
.stApp label,
.stApp li,
.stApp button,
.stApp input,
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
[data-testid="stMarkdownContainer"],
[data-testid="stCaptionContainer"] {
    font-family: var(--font);
}
header[data-testid="stHeader"] {
    background: transparent !important;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1340px;
    animation: fadeIn 0.45s var(--ease) both;
}

/* Heading di dalam kartu grafik */
div[data-testid="stVerticalBlockBorderWrapper"] h3 {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em;
    color: var(--blue-navy) !important;
    padding: 0 0 0.15rem 0 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] h4 {
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: var(--blue-navy) !important;
}
div[data-testid="stCaptionContainer"],
div[data-testid="stCaptionContainer"] p {
    color: var(--text-secondary) !important;
    font-size: 0.82rem !important;
    line-height: 1.5;
}

/* =========================================================
   SIDEBAR — PANEL KONTROL
   ========================================================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E1EDFC 0%, #EAF3FF 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
    animation: none;
}
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 14px;
    margin-bottom: 1.1rem;
    box-shadow: var(--shadow-sm);
    animation: fadeUp 0.5s var(--ease) both;
}
.sidebar-brand-mark {
    flex: 0 0 auto;
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--blue-deep) 0%, var(--blue-primary) 100%);
    color: #FFFFFF;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.28);
}
.sidebar-brand-title {
    font-size: 0.98rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--blue-navy);
    line-height: 1.25;
    margin: 0;
}
.sidebar-brand-sub {
    font-size: 0.76rem;
    color: var(--text-secondary);
    line-height: 1.4;
    margin-top: 2px;
}
.sidebar-section-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-secondary);
    margin: 0.2rem 0 0.4rem 2px;
}
section[data-testid="stSidebar"] hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent 0%, #C6DAF3 20%, #C6DAF3 80%, transparent 100%) !important;
    margin: 1.1rem 0 !important;
}

/* Label widget */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: var(--blue-navy) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.005em;
}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    margin-bottom: 0.15rem;
}
section[data-testid="stSidebar"] [data-testid="stElementContainer"] {
    margin-bottom: 0.15rem;
}

/* Input, date input, multiselect */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
section[data-testid="stSidebar"] div[data-baseweb="input"],
section[data-testid="stSidebar"] div[data-baseweb="base-input"] {
    background-color: var(--surface) !important;
    border-color: var(--border) !important;
    border-radius: var(--radius-sm) !important;
    transition: border-color 0.2s var(--ease), box-shadow 0.2s var(--ease);
}
section[data-testid="stSidebar"] div[data-baseweb="input"] input {
    color: var(--blue-navy) !important;
    font-weight: 500;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover,
section[data-testid="stSidebar"] div[data-baseweb="input"]:hover {
    border-color: var(--blue-sky) !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within,
section[data-testid="stSidebar"] div[data-baseweb="input"]:focus-within {
    border-color: var(--blue-primary) !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.16) !important;
}

/* Tag multiselect */
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color: var(--blue-primary) !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
}
section[data-testid="stSidebar"] span[data-baseweb="tag"] span,
section[data-testid="stSidebar"] span[data-baseweb="tag"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

/* =========================================================
   BUTTONS — rounded rectangle, konsisten
   Secondary (Reset Filter) : putih + border biru
   Primary   (Unduh CSV)    : biru solid + teks putih
   ========================================================= */
.stButton > button,
.stDownloadButton > button {
    min-height: 2.6rem;
    padding: 0.5rem 1.1rem !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font);
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.005em;
    cursor: pointer;
    transition: background-color 0.22s var(--ease),
                color 0.22s var(--ease),
                border-color 0.22s var(--ease),
                box-shadow 0.22s var(--ease),
                transform 0.22s var(--ease) !important;
}
.stButton > button p,
.stDownloadButton > button p {
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: inherit !important;
}

/* Secondary */
.stButton > button {
    background-color: var(--surface) !important;
    color: var(--blue-deep) !important;
    border: 1px solid var(--blue-sky) !important;
    box-shadow: 0 1px 2px rgba(23, 37, 84, 0.05) !important;
}
.stButton > button:hover {
    background-color: var(--blue-light) !important;
    color: var(--blue-deep) !important;
    border-color: var(--blue-primary) !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.18) !important;
    transform: translateY(-1px);
}

/* Primary */
.stDownloadButton > button {
    background-color: var(--blue-primary) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--blue-primary) !important;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.28) !important;
}
.stDownloadButton > button:hover {
    background-color: var(--blue-deep) !important;
    border-color: var(--blue-deep) !important;
    color: #FFFFFF !important;
    box-shadow: 0 6px 16px rgba(30, 64, 175, 0.32) !important;
    transform: translateY(-1px);
}

/* Pressed, focus, disabled */
.stButton > button:active,
.stDownloadButton > button:active {
    transform: translateY(0) scale(0.985) !important;
    box-shadow: 0 1px 2px rgba(23, 37, 84, 0.12) !important;
}
.stButton > button:focus-visible,
.stDownloadButton > button:focus-visible {
    outline: 3px solid rgba(37, 99, 235, 0.38) !important;
    outline-offset: 2px !important;
}
.stButton > button:disabled,
.stDownloadButton > button:disabled {
    opacity: 0.55;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
}

/* =========================================================
   HERO
   ========================================================= */
.hero-card {
    position: relative;
    background: linear-gradient(120deg, #FFFFFF 0%, #E8F1FF 52%, #CFE1FD 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 28px 32px 26px 32px;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-md);
    overflow: hidden;
    animation: fadeUp 0.6s var(--ease) both;
}
.hero-card::before {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 5px;
    background: linear-gradient(180deg, var(--blue-primary) 0%, var(--cyan) 100%);
}
.hero-kicker {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--blue-primary);
    margin-bottom: 8px;
}
.hero-title {
    font-size: 2.05rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    line-height: 1.15;
    color: var(--blue-navy);
    margin: 0 0 8px 0;
}
.hero-desc {
    font-size: 0.95rem;
    line-height: 1.6;
    color: #475569;
    max-width: 780px;
    margin: 0;
}
.filter-pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 20px;
    padding-top: 18px;
    border-top: 1px solid rgba(37, 99, 235, 0.14);
}
.filter-pill {
    display: inline-flex;
    flex-direction: column;
    gap: 1px;
    background-color: rgba(255, 255, 255, 0.85);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 7px 14px;
    box-shadow: 0 1px 2px rgba(23, 37, 84, 0.04);
    transition: border-color 0.22s var(--ease), box-shadow 0.22s var(--ease), transform 0.22s var(--ease);
}
.filter-pill:hover {
    border-color: var(--blue-sky);
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.12);
    transform: translateY(-1px);
}
.pill-key {
    font-size: 0.64rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-secondary);
}
.pill-val {
    font-size: 0.84rem;
    font-weight: 600;
    color: var(--blue-deep);
    line-height: 1.35;
}

/* =========================================================
   KPI CARDS
   ========================================================= */
.kpi-card {
    --accent: #2563EB;
    --accent-soft: #DBEAFE;
    position: relative;
    height: 100%;
    background: radial-gradient(130% 120% at 100% 0%, var(--accent-soft) 0%, #FFFFFF 58%);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px 22px 18px 22px;
    box-shadow: var(--shadow-sm);
    overflow: hidden;
    opacity: 0;
    animation: fadeUp 0.55s var(--ease) both;
    animation-delay: var(--d, 0ms);
    transition: transform 0.28s var(--ease), box-shadow 0.28s var(--ease), border-color 0.28s var(--ease);
}
.kpi-card::before {
    content: "";
    position: absolute;
    left: 22px; top: 0;
    width: 36px; height: 3px;
    border-radius: 0 0 3px 3px;
    background-color: var(--accent);
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
    border-color: var(--accent);
}
.kpi-label {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-secondary);
    margin: 4px 0 8px 0;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
    color: var(--blue-navy);
    line-height: 1.15;
    margin-bottom: 14px;
}
.kpi-badge {
    display: inline-block;
    background-color: var(--accent-soft);
    color: var(--accent);
    font-size: 0.74rem;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
}
.kpi-teal   { --accent: #0D9488; --accent-soft: #CCFBF1; }
.kpi-sky    { --accent: #0369A1; --accent-soft: #E0F2FE; }
.kpi-indigo { --accent: #4F46E5; --accent-soft: #E0E7FF; }

/* KPI utama: satu-satunya kartu dengan gradient solid sebagai penekanan */
.kpi-primary {
    background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%);
    border-color: #1E40AF;
}
.kpi-primary::before { background-color: #93C5FD; }
.kpi-primary .kpi-label { color: #BFDBFE; }
.kpi-primary .kpi-value { color: #FFFFFF; }
.kpi-primary .kpi-badge {
    background-color: rgba(255, 255, 255, 0.16);
    color: #FFFFFF;
}
.kpi-primary:hover { border-color: #60A5FA; }

/* =========================================================
   TABS NAVIGATION
   ========================================================= */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background-color: var(--blue-light);
    padding: 6px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    overflow-x: auto;
    scrollbar-width: none;
}
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
    background-color: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    position: relative;
    flex: 0 0 auto;
    white-space: nowrap;
    border-radius: var(--radius-sm) !important;
    padding: 9px 18px !important;
    height: auto !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: #475569 !important;
    background-color: transparent !important;
    border: none !important;
    transition: background-color 0.22s var(--ease), color 0.22s var(--ease),
                box-shadow 0.22s var(--ease) !important;
}
.stTabs [data-baseweb="tab"] p {
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: inherit !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(255, 255, 255, 0.75) !important;
    color: var(--blue-deep) !important;
}
.stTabs [data-baseweb="tab"]:focus-visible {
    outline: 3px solid rgba(37, 99, 235, 0.38) !important;
    outline-offset: 1px;
}
.stTabs [aria-selected="true"] {
    background-color: var(--blue-primary) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3) !important;
}
.stTabs [aria-selected="true"] p { color: #FFFFFF !important; }
.stTabs [aria-selected="true"]::after {
    content: "";
    position: absolute;
    left: 50%; bottom: 3px;
    width: 18px; height: 2px;
    margin-left: -9px;
    border-radius: 2px;
    background-color: rgba(255, 255, 255, 0.7);
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.2rem;
    animation: fadeUp 0.35s var(--ease) both;
}

/* =========================================================
   KARTU GRAFIK, INSIGHT, MINI STAT
   ========================================================= */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 20px 22px !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.28s var(--ease), border-color 0.28s var(--ease);
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: var(--shadow-md) !important;
    border-color: var(--blue-soft) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"] img,
div[data-testid="stVerticalBlockBorderWrapper"] img {
    max-width: 100%;
    height: auto;
    margin-top: 0.5rem;
}

.sky-insight {
    background-color: var(--blue-light);
    border: 1px solid #C3D9F7;
    border-left: 4px solid var(--blue-primary);
    padding: 16px 20px;
    border-radius: var(--radius-md);
    color: var(--blue-navy);
    font-size: 0.9rem;
    line-height: 1.7;
    margin-top: 1rem;
    animation: fadeUp 0.5s var(--ease) both;
    animation-delay: 120ms;
}
.sky-insight strong {
    color: var(--blue-deep);
    font-weight: 600;
}

.mini-stat-box {
    --accent: #38BDF8;
    position: relative;
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 18px 14px 18px;
    text-align: left;
    box-shadow: var(--shadow-sm);
    overflow: hidden;
    animation: fadeUp 0.5s var(--ease) both;
    animation-delay: var(--d, 0ms);
    transition: transform 0.28s var(--ease), box-shadow 0.28s var(--ease), border-color 0.28s var(--ease);
}
.mini-stat-box::before {
    content: "";
    position: absolute;
    left: 0; top: 14px; bottom: 14px;
    width: 3px;
    border-radius: 0 3px 3px 0;
    background-color: var(--accent);
}
.mini-stat-box:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--accent);
}
.mini-stat-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
.mini-stat-value {
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    font-variant-numeric: tabular-nums;
    color: var(--blue-navy);
    margin-top: 6px;
}
.mini-blue   { --accent: #2563EB; }
.mini-teal   { --accent: #0D9488; }
.mini-sky    { --accent: #38BDF8; }
.mini-indigo { --accent: #6366F1; }

/* =========================================================
   TABEL AGREGASI
   ========================================================= */
.table-wrapper {
    max-height: 400px;
    overflow: auto;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    margin: 0.6rem 0 1.2rem 0;
    background-color: var(--surface);
    scrollbar-width: thin;
    scrollbar-color: #A9C6EE #EEF4FC;
}
.table-wrapper::-webkit-scrollbar { width: 10px; height: 10px; }
.table-wrapper::-webkit-scrollbar-track { background: #EEF4FC; }
.table-wrapper::-webkit-scrollbar-thumb {
    background-color: #A9C6EE;
    border-radius: 8px;
    border: 2px solid #EEF4FC;
}
.table-wrapper::-webkit-scrollbar-thumb:hover { background-color: var(--blue-sky); }
.styled-table {
    width: 100%;
    min-width: 680px;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.86rem;
    background-color: var(--surface);
}
.styled-table thead th {
    position: sticky;
    top: 0;
    z-index: 1;
    background-color: var(--blue-light);
    color: var(--blue-navy);
    font-weight: 600;
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    text-align: left;
    padding: 13px 16px;
    border-bottom: 1px solid #B9D3F4;
    white-space: nowrap;
}
.styled-table tbody td {
    padding: 11px 16px;
    border-bottom: 1px solid #E6EEF9;
    color: #1E293B;
    font-weight: 500;
    font-variant-numeric: tabular-nums;
    transition: background-color 0.18s var(--ease);
}
.styled-table thead th:nth-child(n+4),
.styled-table tbody td:nth-child(n+4) {
    text-align: right;
}
.styled-table tbody tr:nth-child(even) { background-color: var(--bg-secondary); }
.styled-table tbody tr:hover td { background-color: #E4EFFD; }
.styled-table tbody tr:last-child td { border-bottom: none; }

/* =========================================================
   RESPONSIVE
   ========================================================= */
@media (max-width: 992px) {
    .block-container { padding-left: 1.25rem; padding-right: 1.25rem; }
    div[data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        min-width: calc(50% - 1rem) !important;
    }
    /* Kolom di dalam kartu (grafik + panduan) ditumpuk */
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        min-width: 100% !important;
    }
    .hero-title { font-size: 1.7rem; }
}
@media (max-width: 640px) {
    .block-container { padding-top: 3.25rem; padding-left: 0.9rem; padding-right: 0.9rem; }
    .hero-card { padding: 22px 20px 20px 22px; }
    .hero-title { font-size: 1.45rem; }
    .hero-desc { font-size: 0.9rem; }
    .kpi-value { font-size: 1.7rem; }
    .kpi-card { padding: 16px 18px; }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        min-width: 100% !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] { padding: 14px !important; }
    .stTabs [data-baseweb="tab"] { padding: 8px 14px !important; }
    .stButton > button, .stDownloadButton > button { width: 100%; }
}

/* =========================================================
   REDUCED MOTION
   ========================================================= */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-delay: 0ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
    .kpi-card { opacity: 1; }
}

/* =========================================================
   KOMPATIBILITAS STREAMLIT TERBARU (komponen react-aria)
   Selector di atas tetap dipakai untuk versi berbasis baseweb.
   ========================================================= */
/* Kartu ber-border (st.container(border=True)) */
div[data-testid="stVerticalBlock"][data-test-scroll-behavior] {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 20px 22px !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.28s var(--ease), border-color 0.28s var(--ease);
}
div[data-testid="stVerticalBlock"][data-test-scroll-behavior]:hover {
    box-shadow: var(--shadow-md) !important;
    border-color: var(--blue-soft) !important;
}
div[data-testid="stVerticalBlock"][data-test-scroll-behavior] [data-testid="stImage"] img {
    max-width: 100%;
    height: auto;
    margin-top: 0.5rem;
}
div[data-testid="stHeading"] h3 {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em;
    line-height: 1.35 !important;
    color: var(--blue-navy) !important;
    padding: 0 0 0.15rem 0 !important;
}
div[data-testid="stVerticalBlock"][data-test-scroll-behavior] h4 {
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: var(--blue-navy) !important;
}
[data-testid="stHeadingActionElements"],
[data-testid="stHeaderActionElements"] { display: none !important; }

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {
    gap: 6px;
    background-color: var(--blue-light);
    padding: 6px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    overflow-x: auto;
    scrollbar-width: none;
}
[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar { display: none; }
[data-testid="stTab"] {
    position: relative;
    flex: 0 0 auto;
    white-space: nowrap;
    border-radius: var(--radius-sm) !important;
    padding: 9px 18px !important;
    height: auto !important;
    color: #475569 !important;
    background-color: transparent !important;
    border: none !important;
    cursor: pointer;
    transition: background-color 0.22s var(--ease), color 0.22s var(--ease),
                box-shadow 0.22s var(--ease) !important;
}
[data-testid="stTab"] p {
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: inherit !important;
    margin: 0 !important;
}
/* Garis indikator bawaan (merah) disembunyikan; diganti penanda halus */
[data-testid="stTab"] > div:not([data-testid]) { display: none !important; }
[data-testid="stTab"]:hover {
    background-color: rgba(255, 255, 255, 0.75) !important;
    color: var(--blue-deep) !important;
}
[data-testid="stTab"]:focus-visible {
    outline: 3px solid rgba(37, 99, 235, 0.38) !important;
    outline-offset: 1px;
}
[data-testid="stTab"][aria-selected="true"] {
    background-color: var(--blue-primary) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3) !important;
}
[data-testid="stTab"][aria-selected="true"]::after {
    content: "";
    position: absolute;
    left: 50%; bottom: 3px;
    width: 18px; height: 2px;
    margin-left: -9px;
    border-radius: 2px;
    background-color: rgba(255, 255, 255, 0.7);
}
[data-testid="stTabPanel"] {
    padding-top: 1.2rem;
    animation: fadeUp 0.35s var(--ease) both;
}

/* Input sidebar: multiselect & date input */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] div[role="group"],
section[data-testid="stSidebar"] [data-testid="stDateInputField"] {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    transition: border-color 0.2s var(--ease), box-shadow 0.2s var(--ease);
}
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] div[role="group"]:hover,
section[data-testid="stSidebar"] [data-testid="stDateInputField"]:hover {
    border-color: var(--blue-sky) !important;
}
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] div[role="group"]:focus-within,
section[data-testid="stSidebar"] [data-testid="stDateInputField"]:focus-within {
    border-color: var(--blue-primary) !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.16) !important;
}
section[data-testid="stSidebar"] [data-testid="stDateInputField"],
section[data-testid="stSidebar"] [data-testid="stDateInputField"] [role="spinbutton"],
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] input {
    color: var(--blue-navy) !important;
    font-weight: 500;
}
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-tag] {
    background-color: var(--blue-primary) !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
}
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-tag] span,
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-tag] button,
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-tag] svg {
    color: #FFFFFF !important;
}

@media (max-width: 992px) {
    div[data-testid="stVerticalBlock"][data-test-scroll-behavior] div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        min-width: 100% !important;
    }
}
@media (max-width: 640px) {
    div[data-testid="stVerticalBlock"][data-test-scroll-behavior] { padding: 14px !important; }
    [data-testid="stTab"] { padding: 8px 14px !important; }
}
</style>
""", unsafe_allow_html=True)

# Gaya grafik Matplotlib & Seaborn (selaras dengan design system)
NAVY = "#172554"
SLATE = "#64748B"
GRID = "#E3EDF9"
AXIS_EDGE = "#D0DFF3"
LEGEND_FACE = "#F3F7FD"
LEGEND_EDGE = "#D8E6F7"

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = AXIS_EDGE
plt.rcParams["axes.linewidth"] = 0.9
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["text.color"] = NAVY
plt.rcParams["axes.labelcolor"] = SLATE
plt.rcParams["xtick.color"] = SLATE
plt.rcParams["ytick.color"] = SLATE
plt.rcParams["xtick.labelsize"] = 10.5
plt.rcParams["ytick.labelsize"] = 10.5
plt.rcParams["legend.fontsize"] = 10
plt.rcParams["legend.title_fontsize"] = 10.5
sns.set_style("whitegrid", {
    "grid.color": GRID,
    "grid.linestyle": "--",
    "grid.linewidth": 0.8,
    "axes.edgecolor": AXIS_EDGE,
    "axes.labelcolor": SLATE,
    "text.color": NAVY,
    "xtick.color": SLATE,
    "ytick.color": SLATE,
    "axes.facecolor": "white",
    "figure.facecolor": "white",
})

BLUE_MAIN = "#2563EB"       # Primary Blue
BLUE_BRIGHT = "#38BDF8"     # Cyan / Sky
TEAL_BRIGHT = "#14B8A6"     # Teal
BLUE_SOFT = "#93C5FD"       # Soft Blue


# ==========================================
# 2. PEMUATAN DATA
# ==========================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    return df


main_df = load_data()

# ==========================================
# 3. SIDEBAR: PANEL FILTER SELARAS
# ==========================================
min_date = main_df["date"].min().date()
max_date = main_df["date"].max().date()
season_options = ["Spring", "Summer", "Fall", "Winter"]
day_type_options = ["Working Day", "Holiday/Weekend"]
weather_options = ["Clear/Partly Cloudy", "Mist/Cloudy", "Light Snow/Rain", "Heavy Rain/Ice"]

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-mark">BS</div>
            <div>
                <div class="sidebar-brand-title">Filter & Kontrol Data</div>
                <div class="sidebar-brand-sub">Sesuaikan parameter untuk memperbarui grafik secara real-time.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Reset Semua Filter", use_container_width=True):
        st.session_state["date_filter"] = [min_date, max_date]
        st.session_state["season_filter"] = season_options
        st.session_state["day_filter"] = day_type_options
        st.session_state["weather_filter"] = weather_options
        st.rerun()

    st.markdown("---")

    st.markdown('<div class="sidebar-section-label">Parameter Filter</div>', unsafe_allow_html=True)

    date_range = st.date_input(
        label="Rentang Tanggal",
        min_value=min_date,
        max_value=max_date,
        value=st.session_state.get("date_filter", [min_date, max_date]),
        key="date_filter"
    )

    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range[0], date_range[1]
    else:
        start_date, end_date = min_date, max_date

    selected_seasons = st.multiselect(
        label="Musim (Season)",
        options=season_options,
        default=st.session_state.get("season_filter", season_options),
        key="season_filter"
    )

    selected_day_types = st.multiselect(
        label="Kategori Hari",
        options=day_type_options,
        default=st.session_state.get("day_filter", day_type_options),
        key="day_filter"
    )

    selected_weathers = st.multiselect(
        label="Kondisi Cuaca",
        options=weather_options,
        default=st.session_state.get("weather_filter", weather_options),
        key="weather_filter"
    )

    st.markdown("---")
    st.caption("Bike Sharing Dataset (2011–2012) • Dicoding Data Analytics")

# Terapkan filter ke DataFrame
filtered_df = main_df[
    (main_df["date"].dt.date >= start_date) &
    (main_df["date"].dt.date <= end_date) &
    (main_df["season"].isin(selected_seasons)) &
    (main_df["workingday"].isin(selected_day_types)) &
    (main_df["weather"].isin(selected_weathers))
].copy()

if filtered_df.empty:
    st.warning("Data kosong untuk kombinasi filter yang dipilih. Klik 'Reset Semua Filter' pada sidebar untuk mengembalikan tampilan.")
    st.stop()

# ==========================================
# 4. HERO BANNER & FILTER PILLS
# ==========================================
st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-kicker">Operational & Demand Intelligence</div>
        <div class="hero-title">Bike Sharing Analytics Dashboard</div>
        <div class="hero-desc">Pemantauan performa penyewaan sepeda, perilaku pelanggan, pola jam puncak, serta klaster beban operasional.</div>
        <div class="filter-pill-row">
            <span class="filter-pill"><span class="pill-key">Periode</span><span class="pill-val">{start_date.strftime('%d %b %Y')} – {end_date.strftime('%d %b %Y')}</span></span>
            <span class="filter-pill"><span class="pill-key">Musim Aktif</span><span class="pill-val">{', '.join(selected_seasons)}</span></span>
            <span class="filter-pill"><span class="pill-key">Kategori Hari</span><span class="pill-val">{', '.join(selected_day_types)}</span></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 5. CUSTOM KPI SUMMARY CARDS
# ==========================================
daily_filtered_df = filtered_df.groupby(["date", "year", "month", "workingday", "season"], as_index=False).agg({
    "casual": "sum",
    "registered": "sum",
    "total_rentals": "sum"
})

total_all_rentals = int(daily_filtered_df["total_rentals"].sum())
total_registered = int(daily_filtered_df["registered"].sum())
total_casual = int(daily_filtered_df["casual"].sum())
avg_daily_rentals = daily_filtered_df["total_rentals"].mean()

reg_share = (total_registered / total_all_rentals * 100) if total_all_rentals > 0 else 0
cas_share = (total_casual / total_all_rentals * 100) if total_all_rentals > 0 else 0

col1, col2, col3, col4 = st.columns(4, gap="medium")
with col1:
    st.markdown(
        f"""
        <div class="kpi-card kpi-primary" style="--d: 60ms;">
            <div class="kpi-label">Total Penyewaan</div>
            <div class="kpi-value">{total_all_rentals:,}</div>
            <span class="kpi-badge">● {len(daily_filtered_df)} Hari Operasional</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"""
        <div class="kpi-card kpi-teal" style="--d: 140ms;">
            <div class="kpi-label">Penyewa Registered</div>
            <div class="kpi-value">{total_registered:,}</div>
            <span class="kpi-badge">▲ {reg_share:.1f}% Kontribusi Total</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        f"""
        <div class="kpi-card kpi-sky" style="--d: 220ms;">
            <div class="kpi-label">Penyewa Casual</div>
            <div class="kpi-value">{total_casual:,}</div>
            <span class="kpi-badge">● {cas_share:.1f}% Kontribusi Total</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with col4:
    st.markdown(
        f"""
        <div class="kpi-card kpi-indigo" style="--d: 300ms;">
            <div class="kpi-label">Rata-Rata Sewa / Hari</div>
            <div class="kpi-value">{avg_daily_rentals:,.0f}</div>
            <span class="kpi-badge">● Unit Sepeda / Hari</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 0.9rem;'></div>", unsafe_allow_html=True)

# ==========================================
# 6. NAVIGASI TABS UTAMA
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Ringkasan & Segmentasi Pengguna",
    "Pola Jam Puncak & Cuaca",
    "Klaster Permintaan Operasional",
    "Data & Ekspor Laporan"
])

# ------------------------------------------
# TAB 1: RINGKASAN TREN & SEGMENTASI PENGGUNA
# ------------------------------------------
with tab1:
    col_t1_left, col_t1_right = st.columns([1.15, 1], gap="medium")

    with col_t1_left:
        with st.container(border=True):
            st.subheader("Perbandingan Registered vs Casual")
            st.caption("Rata-rata penyewaan harian berdasarkan hari kerja dan akhir pekan/hari libur.")

            avg_user_df = daily_filtered_df.groupby("workingday")[["casual", "registered"]].mean().reset_index()
            avg_user_melted = avg_user_df.melt(
                id_vars="workingday",
                value_vars=["casual", "registered"],
                var_name="User Type",
                value_name="Average Daily Rentals"
            )
            avg_user_melted["User Type"] = avg_user_melted["User Type"].str.capitalize()

            fig1, ax1 = plt.subplots(figsize=(7.5, 4.4))
            sns.barplot(
                data=avg_user_melted,
                x="workingday",
                y="Average Daily Rentals",
                hue="User Type",
                palette={"Casual": BLUE_BRIGHT, "Registered": BLUE_MAIN},
                width=0.52,
                ax=ax1
            )

            for container in ax1.containers:
                ax1.bar_label(container, fmt="%.0f", padding=5, fontsize=11.5, fontweight="bold", color=NAVY)

            ax1.set_title("Rata-Rata Penyewaan Harian per Kategori Hari", fontsize=12.5, fontweight="bold", pad=14, color=NAVY, loc="left")
            ax1.set_xlabel("")
            ax1.set_ylabel("Rata-Rata Penyewaan / Hari", fontsize=11, fontweight="bold", color=SLATE)
            ax1.set_ylim(0, avg_user_melted["Average Daily Rentals"].max() * 1.22)
            ax1.legend(title="Tipe Pengguna", frameon=True, facecolor=LEGEND_FACE, edgecolor=LEGEND_EDGE)
            sns.despine(top=True, right=True)
            plt.tight_layout()
            st.pyplot(fig1)

    with col_t1_right:
        with st.container(border=True):
            st.subheader("Tren Rata-Rata Penyewaan Bulanan")
            st.caption("Perbandingan performa rata-rata harian antar bulan pada tahun 2011 dan 2012.")

            month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            monthly_trend = daily_filtered_df.groupby(["month", "year"], as_index=False)["total_rentals"].mean()
            monthly_trend["month"] = pd.Categorical(monthly_trend["month"], categories=month_order, ordered=True)
            monthly_trend = monthly_trend.sort_values("month")

            fig_m, ax_m = plt.subplots(figsize=(7.5, 4.4))
            sns.lineplot(
                data=monthly_trend,
                x="month",
                y="total_rentals",
                hue="year",
                palette={2011: BLUE_BRIGHT, 2012: BLUE_MAIN},
                marker="o",
                linewidth=2.5,
                ax=ax_m
            )

            ax_m.set_title("Pertumbuhan Rata-Rata Sewa Harian (2011 vs 2012)", fontsize=12.5, fontweight="bold", pad=14, color=NAVY, loc="left")
            ax_m.set_xlabel("")
            ax_m.set_ylabel("Rata-Rata Penyewaan / Hari", fontsize=11, fontweight="bold", color=SLATE)
            ax_m.legend(title="Tahun", frameon=True, facecolor=LEGEND_FACE, edgecolor=LEGEND_EDGE)
            sns.despine(top=True, right=True)
            plt.tight_layout()
            st.pyplot(fig_m)

    st.markdown(
        """
        <div class="sky-insight">
        <strong>Insight Segmentasi & Pertumbuhan:</strong> Penyewa <strong>Registered</strong> mendominasi aktivitas pada <em>Working Day</em> untuk kebutuhan komuter rutin, sedangkan penyewa <strong>Casual</strong> melonjak signifikan pada <em>Holiday/Weekend</em>. Secara keseluruhan, volume penyewaan tahun 2012 tumbuh konsisten lebih tinggi dibandingkan 2011 dengan puncak pada pertengahan hingga awal musim gugur.
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------
# TAB 2: POLA JAM PUNCAK & SENSITIVITAS CUACA
# ------------------------------------------
with tab2:
    hourly_summary = filtered_df.groupby(["workingday", "hour"])["total_rentals"].mean().reset_index()
    wd_data = hourly_summary[hourly_summary["workingday"] == "Working Day"]
    we_data = hourly_summary[hourly_summary["workingday"] == "Holiday/Weekend"]

    wd_peak_hr = f"{int(wd_data.loc[wd_data['total_rentals'].idxmax(), 'hour']):02d}:00" if not wd_data.empty else "-"
    wd_peak_val = f"{wd_data['total_rentals'].max():.0f} sewa/jam" if not wd_data.empty else "-"
    we_peak_hr = f"{int(we_data.loc[we_data['total_rentals'].idxmax(), 'hour']):02d}:00" if not we_data.empty else "-"
    we_peak_val = f"{we_data['total_rentals'].max():.0f} sewa/jam" if not we_data.empty else "-"

    m1, m2, m3, m4 = st.columns(4, gap="medium")
    with m1:
        st.markdown(f'<div class="mini-stat-box mini-blue" style="--d: 40ms;"><div class="mini-stat-label">Jam Tersibuk Working Day</div><div class="mini-stat-value">{wd_peak_hr}</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="mini-stat-box mini-indigo" style="--d: 100ms;"><div class="mini-stat-label">Puncak Sewa Working Day</div><div class="mini-stat-value">{wd_peak_val}</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="mini-stat-box mini-teal" style="--d: 160ms;"><div class="mini-stat-label">Jam Tersibuk Weekend</div><div class="mini-stat-value">{we_peak_hr}</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="mini-stat-box mini-sky" style="--d: 220ms;"><div class="mini-stat-label">Puncak Sewa Weekend</div><div class="mini-stat-value">{we_peak_val}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 0.9rem;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
        with st.container(border=True):
            st.subheader("Pola Penyewaan Per Jam (24 Jam)")
            st.caption("Perbandingan ritme permintaan antara hari kerja dan akhir pekan/hari libur.")

            fig2, ax2 = plt.subplots(figsize=(7.5, 4.6))
            sns.lineplot(
                data=hourly_summary,
                x="hour",
                y="total_rentals",
                hue="workingday",
                palette={"Working Day": BLUE_MAIN, "Holiday/Weekend": TEAL_BRIGHT},
                marker="o",
                markersize=5,
                linewidth=2.5,
                ax=ax2
            )
            ax2.axvspan(7.5, 8.5, color=BLUE_MAIN, alpha=0.10, label="Morning Peak (08:00)")
            ax2.axvspan(16.5, 18.5, color=BLUE_MAIN, alpha=0.10, label="Evening Peak (17:00–18:00)")

            ax2.set_title("Rata-Rata Penyewaan Berdasarkan Jam Operasional", fontsize=12.5, fontweight="bold", pad=14, color=NAVY, loc="left")
            ax2.set_xlabel("Jam (00:00 – 23:00)", fontsize=11, fontweight="bold", color=SLATE)
            ax2.set_ylabel("Rata-Rata Penyewaan / Jam", fontsize=11, fontweight="bold", color=SLATE)
            ax2.set_xticks(range(0, 24, 2))
            ax2.legend(title="Kategori Hari", frameon=True, facecolor=LEGEND_FACE, edgecolor=LEGEND_EDGE)
            sns.despine(top=True, right=True)
            plt.tight_layout()
            st.pyplot(fig2)

    with col_right:
        with st.container(border=True):
            st.subheader("Sensitivitas Cuaca di Tiap Musim")
            st.caption("Dampak kondisi cuaca terhadap rata-rata volume penyewaan.")

            weather_season_df = filtered_df[filtered_df["weather"] != "Heavy Rain/Ice"].groupby(
                ["season", "weather"], as_index=False
            )["total_rentals"].mean()

            fig3, ax3 = plt.subplots(figsize=(7.5, 4.6))
            sns.barplot(
                data=weather_season_df,
                x="season",
                y="total_rentals",
                hue="weather",
                order=[s for s in ["Spring", "Summer", "Fall", "Winter"] if s in selected_seasons],
                palette={
                    "Clear/Partly Cloudy": BLUE_MAIN,
                    "Mist/Cloudy": BLUE_BRIGHT,
                    "Light Snow/Rain": BLUE_SOFT
                },
                ax=ax3
            )

            ax3.set_title("Rata-Rata Penyewaan Berdasarkan Cuaca & Musim", fontsize=12.5, fontweight="bold", pad=14, color=NAVY, loc="left")
            ax3.set_xlabel("Musim (Season)", fontsize=11, fontweight="bold", color=SLATE)
            ax3.set_ylabel("Rata-Rata Penyewaan / Jam", fontsize=11, fontweight="bold", color=SLATE)
            ax3.legend(title="Kondisi Cuaca", frameon=True, facecolor=LEGEND_FACE, edgecolor=LEGEND_EDGE)
            sns.despine(top=True, right=True)
            plt.tight_layout()
            st.pyplot(fig3)

# ------------------------------------------
# TAB 3: ANALISIS LANJUTAN (CLUSTERING)
# ------------------------------------------
with tab3:
    with st.container(border=True):
        st.subheader("Klaster Intensitas Permintaan Sewa (Manual Grouping)")
        st.caption("Pengelompokan jam operasional ke dalam kategori Low, Medium, dan High Demand berdasarkan distribusi kuartil.")

        q1_global = main_df["total_rentals"].quantile(0.25)
        q3_global = main_df["total_rentals"].quantile(0.75)

        def categorize_time_of_day(hour):
            if 0 <= hour < 6:
                return "Late Night (00:00–05:59)"
            elif 6 <= hour < 12:
                return "Morning (06:00–11:59)"
            elif 12 <= hour < 18:
                return "Afternoon (12:00–17:59)"
            else:
                return "Evening (18:00–23:59)"

        def categorize_demand(rentals):
            if rentals <= q1_global:
                return "Low Demand"
            elif rentals <= q3_global:
                return "Medium Demand"
            else:
                return "High Demand"

        filtered_df["time_segment"] = filtered_df["hour"].apply(categorize_time_of_day)
        filtered_df["demand_cluster"] = filtered_df["total_rentals"].apply(categorize_demand)

        cluster_pct = pd.crosstab(
            index=filtered_df["time_segment"],
            columns=filtered_df["demand_cluster"],
            normalize="index"
        ) * 100

        for col in ["Low Demand", "Medium Demand", "High Demand"]:
            if col not in cluster_pct.columns:
                cluster_pct[col] = 0.0

        cluster_pct = cluster_pct[["Low Demand", "Medium Demand", "High Demand"]]
        segment_order = [
            "Late Night (00:00–05:59)",
            "Morning (06:00–11:59)",
            "Afternoon (12:00–17:59)",
            "Evening (18:00–23:59)"
        ]
        cluster_pct = cluster_pct.reindex([s for s in segment_order if s in cluster_pct.index])

        col_chart3, col_info3 = st.columns([2.2, 1], gap="large")

        with col_chart3:
            fig4, ax4 = plt.subplots(figsize=(8.2, 4.4))
            cluster_pct.plot(
                kind="bar",
                stacked=True,
                color={"Low Demand": BLUE_SOFT, "Medium Demand": BLUE_BRIGHT, "High Demand": BLUE_MAIN},
                edgecolor="white",
                width=0.52,
                ax=ax4
            )

            # Label putih pada segmen biru tua agar kontras tetap terbaca
            label_colors = {"Low Demand": NAVY, "Medium Demand": NAVY, "High Demand": "#FFFFFF"}
            for c in ax4.containers:
                labels = [f"{v:.1f}%" if v >= 6 else "" for v in c.datavalues]
                ax4.bar_label(
                    c, labels=labels, label_type="center",
                    color=label_colors.get(c.get_label(), NAVY),
                    fontweight="bold", fontsize=9
                )

            ax4.set_title("Proporsi Klaster Permintaan per Segmen Waktu", fontsize=12.5, fontweight="bold", pad=14, color=NAVY, loc="left")
            ax4.set_xlabel("")
            ax4.set_ylabel("Persentase Jam Operasional (%)", fontsize=11, fontweight="bold", color=SLATE)
            ax4.set_xticklabels(ax4.get_xticklabels(), rotation=10)
            ax4.legend(title="Klaster Permintaan", bbox_to_anchor=(1.01, 1), loc="upper left", frameon=True, facecolor=LEGEND_FACE, edgecolor=LEGEND_EDGE)
            sns.despine(top=True, right=True)
            plt.tight_layout()
            st.pyplot(fig4)

        with col_info3:
            st.markdown("#### Panduan Operasional")
            st.markdown(
                f"""
                <div class="sky-insight" style="margin-top: 0.4rem;">
                <strong>Ambang Batas Kuartil:</strong><br>
                • <strong>Low Demand:</strong> ≤ {q1_global:.0f} sewa/jam<br>
                • <strong>Medium Demand:</strong> {q1_global+1:.0f}–{q3_global:.0f} sewa/jam<br>
                • <strong>High Demand:</strong> &gt; {q3_global:.0f} sewa/jam<br><br>
                <strong>Strategi Armada:</strong><br>
                Segmen <em>Afternoon</em> memiliki konsentrasi beban tertinggi, sedangkan <em>Late Night</em> merupakan waktu paling ideal untuk perawatan unit dan redistribusi sepeda ke titik stasiun komuter.
                </div>
                """,
                unsafe_allow_html=True
            )

# ------------------------------------------
# TAB 4: TABEL AGREGASI & EKSPOR CSV
# ------------------------------------------
with tab4:
    with st.container(border=True):
        st.subheader("Tabel Agregasi Harian")
        st.caption("Menampilkan rincian data harian sesuai filter aktif dengan tampilan kontras tinggi.")

        display_daily = daily_filtered_df[["date", "workingday", "season", "casual", "registered", "total_rentals"]].sort_values(
            by="date", ascending=False
        ).copy()
        display_daily["date"] = display_daily["date"].dt.strftime("%Y-%m-%d")
        display_daily["casual"] = display_daily["casual"].map("{:,}".format)
        display_daily["registered"] = display_daily["registered"].map("{:,}".format)
        display_daily["total_rentals"] = display_daily["total_rentals"].map("{:,}".format)
        display_daily.columns = ["Tanggal", "Kategori Hari", "Musim", "Penyewa Casual", "Penyewa Registered", "Total Penyewaan"]

        html_table = display_daily.to_html(index=False, classes="styled-table", border=0)
        st.markdown(f'<div class="table-wrapper">{html_table}</div>', unsafe_allow_html=True)

        export_df = daily_filtered_df[["date", "workingday", "season", "casual", "registered", "total_rentals"]].sort_values(
            by="date", ascending=False
        ).copy()
        export_df["date"] = export_df["date"].dt.strftime("%Y-%m-%d")
        export_df.columns = ["Tanggal", "Kategori Hari", "Musim", "Penyewa Casual", "Penyewa Registered", "Total Penyewaan"]

        csv_data = export_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Unduh Laporan CSV",
            data=csv_data,
            file_name=f"bikesharing_report_{start_date}_to_{end_date}.csv",
            mime="text/csv"
        )