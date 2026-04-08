import streamlit as st
import requests
import json
import os
from datetime import datetime

# --- Config ---
WEBHOOK_URL = "https://n8n.srv1093761.hstgr.cloud/webhook/competitor-blogs"
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")

# --- Page Config ---
st.set_page_config(
    page_title="Pelvi AI Hub - Competitor Analyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* ===== GLOBAL ===== */
    *, *::before, *::after { box-sizing: border-box; }

    .stApp {
        background: #f8f9fc !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        color: #1e293b;
    }

    .main .block-container {
        padding: 2rem 2.5rem 3rem 2.5rem;
        max-width: 1300px;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 7px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

    /* ===== HIDE DEFAULTS ===== */
    #MainMenu, footer, .stDeployButton, header[data-testid="stHeader"] { display: none !important; }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e2e8f0;
        box-shadow: 2px 0 12px rgba(0,0,0,0.04);
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    /* Sidebar Brand/Logo */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 1rem 0.5rem 1.8rem 0.5rem;
        border-bottom: 2px solid #f1f5f9;
        margin-bottom: 1.5rem;
    }
    .sidebar-brand-icon {
        width: 60px; height: 60px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        font-size: 30px;
        font-weight: 800;
        color: white;
        box-shadow: 0 4px 14px rgba(99,102,241,0.3);
        flex-shrink: 0;
    }
    .sidebar-brand-text {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .sidebar-brand-sub {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 500;
        margin-top: 3px;
    }

    /* Sidebar Section Title */
    .sidebar-section-title {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #94a3b8;
        padding: 0.5rem 0.5rem 0.8rem 0.5rem;
    }

    /* Sidebar Clear History Button */
    section[data-testid="stSidebar"] .stButton > button {
        background: #f8f9fc !important;
        border: 1.5px solid #e2e8f0 !important;
        box-shadow: none !important;
        color: #334155 !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
        font-size: 0.9rem !important;
        border-radius: 10px !important;
        text-align: left !important;
        transition: all 0.2s ease !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #ede9fe !important;
        border-color: #a78bfa !important;
        color: #5b21b6 !important;
        transform: none !important;
    }

    /* History item card style */
    .hist-card {
        background: #f8f9fc;
        border: 1.5px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
    }
    .hist-card:hover {
        background: #ede9fe;
        border-color: #a78bfa;
    }
    .hist-card-info {
        flex: 1;
        min-width: 0;
    }
    .hist-card-niche {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0f172a;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .hist-card-date {
        font-size: 0.78rem;
        color: #94a3b8;
        font-weight: 500;
        margin-top: 2px;
    }
    .hist-card-del {
        width: 32px; height: 32px;
        border-radius: 8px;
        border: 1.5px solid #e2e8f0;
        background: white;
        color: #94a3b8;
        font-size: 14px;
        font-weight: 700;
        display: flex; align-items: center; justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
        flex-shrink: 0;
    }
    .hist-card-del:hover {
        background: #fef2f2;
        border-color: #fecaca;
        color: #ef4444;
    }

    /* ===== HERO SECTION ===== */
    .hero {
        position: relative;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%);
        border-radius: 24px;
        padding: 3.5rem 3rem;
        margin-bottom: 2.5rem;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(99,102,241,0.25);
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%; right: -15%;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero::after {
        content: '';
        position: absolute;
        bottom: -40%; left: -10%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-content {
        position: relative;
        z-index: 2;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 24px;
        padding: 7px 18px;
        font-size: 0.88rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1.2rem;
    }
    .hero-badge-dot {
        width: 8px; height: 8px;
        background: #4ade80;
        border-radius: 50%;
        animation: pulse-dot 2s infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
    .hero h1 {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        margin: 0 0 0.8rem 0;
        letter-spacing: -1.5px;
        line-height: 1.1;
    }
    .hero p {
        font-size: 1.15rem;
        color: rgba(255,255,255,0.85);
        margin: 0;
        max-width: 600px;
        line-height: 1.7;
        font-weight: 400;
    }

    /* ===== SEARCH AREA ===== */
    .search-label {
        font-size: 1.15rem;
        font-weight: 700;
        color: #334155;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
        display: block;
    }

    /* Input */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 14px 20px !important;
        font-size: 1.1rem !important;
        color: #0f172a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
        font-weight: 400 !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 4px rgba(99,102,241,0.12) !important;
        background: #ffffff !important;
    }

    /* Align input and button vertically */
    .stTextInput { margin-bottom: 0 !important; }
    [data-testid="stHorizontalBlock"] {
        align-items: flex-end !important;
    }

    /* Main Analyze Button - same height as input */
    .main .stButton > button,
    [data-testid="stMainBlockContainer"] .stButton > button,
    .main .stButton > button[kind="secondary"],
    .main .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        height: 44px !important;
        padding: 0 32px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(99,102,241,0.35) !important;
        letter-spacing: 0.3px;
        cursor: pointer;
    }
    .main .stButton > button:hover,
    [data-testid="stMainBlockContainer"] .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(99,102,241,0.45) !important;
    }

    /* ===== RESULT BADGE ===== */
    .result-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: #ecfdf5;
        border: 2px solid #a7f3d0;
        border-radius: 12px;
        padding: 10px 20px;
        margin-bottom: 1.8rem;
    }
    .result-badge-dot {
        width: 10px; height: 10px;
        background: #22c55e;
        border-radius: 50%;
    }
    .result-badge-text {
        font-size: 1rem;
        font-weight: 700;
        color: #166534;
    }

    /* ===== METRIC CARDS ===== */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 1.5rem;
    }
    @media (max-width: 768px) {
        .metrics-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .m-card {
        background: white;
        border: 2px solid #f1f5f9;
        border-radius: 14px;
        padding: 1rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .m-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }
    .m-card-icon {
        font-size: 1.3rem;
        margin-bottom: 0.3rem;
    }
    .m-card-value {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 0.25rem;
    }
    .m-card-label {
        font-size: 0.72rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .m-card.blue { border-left: 4px solid #3b82f6; }
    .m-card.blue .m-card-value { color: #2563eb; }
    .m-card.green { border-left: 4px solid #22c55e; }
    .m-card.green .m-card-value { color: #16a34a; }
    .m-card.red { border-left: 4px solid #f97316; }
    .m-card.red .m-card-value { color: #ea580c; }
    .m-card.purple { border-left: 4px solid #8b5cf6; }
    .m-card.purple .m-card-value { color: #7c3aed; }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 14px;
        padding: 6px;
        gap: 6px;
        border: 2px solid #f1f5f9;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        color: #64748b !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #6366f1 !important;
        color: white !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #1e293b !important;
        background: #f1f5f9 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"]:hover {
        color: white !important;
        background: #6366f1 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ===== SECTION HEADER ===== */
    .sec-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 1.8rem 0 1.5rem 0;
    }
    .sec-header-line {
        width: 5px;
        height: 28px;
        background: linear-gradient(180deg, #6366f1, #8b5cf6);
        border-radius: 3px;
    }
    .sec-header h3 {
        margin: 0;
        font-size: 1.4rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.5px;
    }

    /* ===== GENERATED TITLES ===== */
    .gen-title {
        background: white;
        border: 2px solid #f1f5f9;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 12px;
        display: flex;
        align-items: flex-start;
        gap: 14px;
        transition: all 0.25s ease;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }
    .gen-title:hover {
        border-color: #c7d2fe;
        background: #faf5ff;
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(99,102,241,0.1);
    }
    .gen-num {
        min-width: 34px; height: 34px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.85rem;
        font-weight: 800;
        color: white;
        flex-shrink: 0;
    }
    .gen-text {
        font-size: 1.05rem;
        color: #1e293b;
        font-weight: 600;
        line-height: 1.5;
        padding-top: 4px;
    }

    /* ===== COMPETITOR GROUP ===== */
    .comp-group {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        margin-bottom: 20px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .comp-group:hover {
        border-color: #c7d2fe;
        box-shadow: 0 4px 16px rgba(99,102,241,0.08);
    }
    .comp-group-body {
        padding: 16px 20px;
    }

    /* ===== BLOG CARDS ===== */
    .blog-card {
        background: #f8f9fc;
        border: 1.5px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 10px;
        transition: all 0.25s ease;
    }
    .blog-card:hover {
        border-color: #c7d2fe;
        background: #f1f5f9;
    }
    .blog-card:last-child {
        margin-bottom: 0;
    }
    .blog-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
    }
    .blog-card-title a {
        color: #0f172a;
        text-decoration: none;
        transition: color 0.2s;
    }
    .blog-card-title a:hover {
        color: #6366f1;
    }
    .blog-card-snippet {
        font-size: 0.95rem;
        color: #64748b;
        line-height: 1.7;
        margin-bottom: 8px;
    }
    .blog-card-date {
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 600;
    }

    /* ===== SHORTS CARDS ===== */
    .short-card {
        background: #fef2f2;
        border: 2px solid #fecaca;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 12px;
        transition: all 0.25s ease;
    }
    .short-card:hover {
        border-color: #f87171;
        box-shadow: 0 4px 12px rgba(239,68,68,0.1);
    }
    .short-card-title a {
        font-size: 1.05rem;
        font-weight: 700;
        color: #dc2626;
        text-decoration: none;
    }
    .short-card-title a:hover {
        color: #b91c1c;
    }
    .short-card-topic {
        font-size: 0.92rem;
        color: #64748b;
        margin-top: 6px;
    }
    .short-card-date {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 4px;
        font-weight: 500;
    }

    /* ===== COMPETITOR HEADER ===== */
    .comp-header {
        background: #f8f9fc;
        border: 2px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }
    .comp-name {
        font-size: 1.2rem;
        font-weight: 800;
        color: #0f172a;
    }
    .comp-links {
        display: flex;
        gap: 10px;
        align-items: center;
    }
    .comp-link {
        font-size: 0.88rem;
        padding: 6px 16px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        transition: all 0.2s;
    }
    .comp-link.web {
        background: #ede9fe;
        color: #6366f1;
        border: 1.5px solid #c7d2fe;
    }
    .comp-link.web:hover {
        background: #6366f1;
        color: white;
    }
    .comp-link.yt {
        background: #fef2f2;
        color: #dc2626;
        border: 1.5px solid #fecaca;
    }
    .comp-link.yt:hover {
        background: #dc2626;
        color: white;
    }
    .comp-blog-count {
        font-size: 0.82rem;
        background: #e0e7ff;
        padding: 4px 14px;
        border-radius: 20px;
        color: #4338ca;
        font-weight: 700;
    }

    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 14px !important;
        border: 2px solid #e2e8f0 !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 16px 20px !important;
    }
    .streamlit-expanderHeader:hover {
        border-color: #a78bfa !important;
        background: #faf5ff !important;
    }
    .streamlit-expanderContent {
        border: 2px solid #f1f5f9 !important;
        border-top: none !important;
        border-radius: 0 0 14px 14px !important;
        background: #fafbfe !important;
        padding: 16px 20px !important;
    }
    [data-testid="stExpander"] {
        border: none !important;
        box-shadow: none !important;
        margin-bottom: 12px;
    }

    /* ===== COMPETITOR LIST CARD ===== */
    .comp-list-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        margin-bottom: 16px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.25s ease;
    }
    .comp-list-card:hover {
        border-color: #a78bfa;
        box-shadow: 0 6px 20px rgba(99,102,241,0.1);
    }
    .comp-list-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
        padding: 20px 24px;
        background: linear-gradient(135deg, #f8f9fc, #f1f5f9);
        border-bottom: 2px solid #e2e8f0;
    }
    .comp-list-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .comp-list-avatar {
        width: 44px; height: 44px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem;
        font-weight: 800;
        color: white;
        flex-shrink: 0;
    }
    .comp-list-name {
        font-size: 1.15rem;
        font-weight: 800;
        color: #0f172a;
    }
    .comp-list-count {
        font-size: 0.8rem;
        background: #e0e7ff;
        color: #4338ca;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: 700;
    }
    .comp-list-zero {
        font-size: 0.8rem;
        background: #fef2f2;
        color: #dc2626;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: 700;
    }
    .comp-list-links {
        display: flex;
        gap: 8px;
    }
    .comp-list-link {
        font-size: 0.85rem;
        padding: 7px 18px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 700;
        transition: all 0.2s;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .comp-list-link.web {
        background: #ede9fe;
        color: #6366f1;
        border: 1.5px solid #c7d2fe;
    }
    .comp-list-link.web:hover {
        background: #6366f1;
        color: white;
    }
    .comp-list-link.yt {
        background: #fef2f2;
        color: #dc2626;
        border: 1.5px solid #fecaca;
    }
    .comp-list-link.yt:hover {
        background: #dc2626;
        color: white;
    }
    .comp-list-blogs {
        padding: 16px 24px 20px 24px;
    }
    .comp-list-empty {
        padding: 20px 24px;
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 500;
        text-align: center;
        font-style: italic;
    }

    /* ===== DOWNLOAD BUTTON ===== */
    .stDownloadButton > button {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        color: #475569 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 12px 24px !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .stDownloadButton > button:hover {
        background: #ede9fe !important;
        border-color: #a78bfa !important;
        color: #5b21b6 !important;
        transform: none !important;
    }

    /* ===== EMPTY STATE ===== */
    .empty-state {
        text-align: center;
        padding: 5rem 2rem;
        background: white;
        border: 2px dashed #e2e8f0;
        border-radius: 24px;
        margin-top: 1rem;
    }
    .empty-icon {
        font-size: 4rem;
        margin-bottom: 1.2rem;
    }
    .empty-state h3 {
        color: #0f172a;
        font-weight: 800;
        font-size: 1.6rem;
        margin: 0 0 0.6rem 0;
    }
    .empty-state p {
        color: #64748b;
        font-size: 1.1rem;
        margin: 0;
        line-height: 1.7;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero { padding: 2.5rem 1.8rem; }
        .hero h1 { font-size: 2rem; }
        .hero p { font-size: 1rem; }
        .main .block-container { padding: 1rem; }
        .search-wrapper { padding: 1.2rem; }
        .sec-header h3 { font-size: 1.1rem; }
    }
</style>
""", unsafe_allow_html=True)


# --- History Functions ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_to_history(niche, data):
    history = load_history()
    entry = {
        "id": len(history) + 1,
        "niche": niche,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": data,
    }
    history.insert(0, entry)
    history = history[:50]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    return entry


def delete_history_item(idx):
    history = load_history()
    if 0 <= idx < len(history):
        history.pop(idx)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)


def clear_all_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)


# --- API Call ---
def analyze_niche(niche):
    try:
        response = requests.post(
            WEBHOOK_URL,
            json={"niche": niche},
            headers={"Content-Type": "application/json"},
            timeout=180,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None


# --- Render Results ---
def render_results(data):
    if not data:
        st.warning("No data to display.")
        return

    competitor_data = data.get("competitor_data", [])
    generated = data.get("generated_new_titles", [])

    total_competitors = len(competitor_data)
    total_blogs = sum(len(c.get("blogs_last_30_days") or []) for c in competitor_data)
    total_shorts = sum(len(c.get("youtube_shorts_last_30_days") or []) for c in competitor_data)
    yt_channels = sum(1 for c in competitor_data if c.get("youtube_channel"))

    st.markdown(f"""
    <div class="metrics-grid">
        <div class="m-card blue">
            <div class="m-card-icon">&#127970;</div>
            <div class="m-card-value">{total_competitors}</div>
            <div class="m-card-label">Competitors</div>
        </div>
        <div class="m-card green">
            <div class="m-card-icon">&#128221;</div>
            <div class="m-card-value">{total_blogs}</div>
            <div class="m-card-label">Blog Posts</div>
        </div>
        <div class="m-card red">
            <div class="m-card-icon">&#127909;</div>
            <div class="m-card-value">{yt_channels}</div>
            <div class="m-card-label">YT Channels</div>
        </div>
        <div class="m-card purple">
            <div class="m-card-icon">&#10024;</div>
            <div class="m-card-value">{len(generated)}</div>
            <div class="m-card-label">Generated Titles</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "  Generated Titles  ",
        "  Competitor Blogs  ",
        "  YouTube Shorts  ",
        "  Raw Data  "
    ])

    with tab1:
        st.markdown("""
        <div class="sec-header">
            <div class="sec-header-line"></div>
            <h3>AI-Generated Blog Title Ideas</h3>
        </div>
        """, unsafe_allow_html=True)

        if generated:
            col_a, col_b = st.columns(2)
            half = (len(generated) + 1) // 2
            for i, title in enumerate(generated):
                target = col_a if i < half else col_b
                with target:
                    st.markdown(f"""
                    <div class="gen-title">
                        <div class="gen-num">{i+1}</div>
                        <div class="gen-text">{title}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            all_titles_text = "\n".join(f"{i+1}. {t}" for i, t in enumerate(generated))
            st.download_button(
                "Download All Titles (.txt)",
                all_titles_text,
                file_name="generated_titles.txt",
                mime="text/plain",
            )
        else:
            st.info("No titles were generated.")

    with tab2:
        st.markdown("""
        <div class="sec-header">
            <div class="sec-header-line"></div>
            <h3>Competitor Blog Posts (Last 30 Days)</h3>
        </div>
        """, unsafe_allow_html=True)

        if competitor_data:
            for comp in competitor_data:
                name = comp.get("competitor_name", "Unknown")
                website = comp.get("competitor_website", "")
                blogs = comp.get("blogs_last_30_days") or []
                yt = comp.get("youtube_channel")
                initial = name[0].upper() if name else "?"

                links_html = f'<a href="{website}" target="_blank" class="comp-list-link web">Website</a>'
                if yt:
                    links_html += f'<a href="{yt}" target="_blank" class="comp-list-link yt">YouTube</a>'

                count_class = "comp-list-count" if len(blogs) > 0 else "comp-list-zero"
                count_text = f"{len(blogs)} posts" if len(blogs) > 0 else "0 posts"

                # Build header HTML
                header_html = f"""
                <div class="comp-group">
                    <div class="comp-list-top" style="border-radius:12px 12px 0 0;">
                        <div class="comp-list-left">
                            <div class="comp-list-avatar">{initial}</div>
                            <div>
                                <div class="comp-list-name">{name}</div>
                                <span class="{count_class}">{count_text}</span>
                            </div>
                        </div>
                        <div class="comp-list-links">{links_html}</div>
                    </div>
                    <div class="comp-group-body">
                """

                # Render header
                st.markdown(header_html, unsafe_allow_html=True)

                if blogs:
                    for blog in blogs:
                        b_title = blog.get("title", "No title")
                        b_url = blog.get("url", "#")
                        b_snippet = blog.get("snippet", "")
                        b_date = blog.get("date", "")
                        st.markdown(f"""<div class="blog-card"><div class="blog-card-title"><a href="{b_url}" target="_blank">{b_title}</a></div><div class="blog-card-snippet">{b_snippet}</div><div class="blog-card-date">{b_date}</div></div>""", unsafe_allow_html=True)
                else:
                    st.markdown('<div class="comp-list-empty">No blog posts found in the last 30 days</div>', unsafe_allow_html=True)

                # Close wrapper
                st.markdown("</div></div>", unsafe_allow_html=True)
        else:
            st.info("No competitor data available.")

    with tab3:
        st.markdown("""
        <div class="sec-header">
            <div class="sec-header-line"></div>
            <h3>YouTube Shorts (Last 30 Days)</h3>
        </div>
        """, unsafe_allow_html=True)

        has_shorts = False
        for comp in competitor_data:
            shorts = comp.get("youtube_shorts_last_30_days") or []
            if shorts:
                has_shorts = True
                name = comp.get("competitor_name", "Unknown")
                initial = name[0].upper() if name else "?"

                header_html = f"""
                <div class="comp-group" style="border-color:#fecaca;">
                    <div class="comp-list-top" style="background:linear-gradient(135deg,#fef2f2,#fff1f2);border-radius:12px 12px 0 0;">
                        <div class="comp-list-left">
                            <div class="comp-list-avatar" style="background:linear-gradient(135deg,#ef4444,#dc2626);">{initial}</div>
                            <div>
                                <div class="comp-list-name">{name}</div>
                                <span class="comp-list-count" style="background:#fef2f2;color:#dc2626;">{len(shorts)} shorts</span>
                            </div>
                        </div>
                    </div>
                    <div class="comp-group-body">
                """

                # Render header
                st.markdown(header_html, unsafe_allow_html=True)

                # Render each short individually
                for s in shorts:
                    s_title = s.get("title", "No title")
                    s_url = s.get("url", "#")
                    s_topic = s.get("topic", "")
                    s_date = s.get("date", "")
                    topic_html = f'<div class="short-card-topic">{s_topic}</div>' if s_topic else ''
                    date_html = f'<div class="short-card-date">{s_date}</div>' if s_date else ''
                    st.markdown(f"""<div class="short-card"><div class="short-card-title"><a href="{s_url}" target="_blank">{s_title}</a></div>{topic_html}{date_html}</div>""", unsafe_allow_html=True)

                # Close wrapper
                st.markdown("</div></div>", unsafe_allow_html=True)

        if not has_shorts:
            st.info("No YouTube Shorts found for any competitor.")

    with tab4:
        st.markdown("""
        <div class="sec-header">
            <div class="sec-header-line"></div>
            <h3>Complete API Response</h3>
        </div>
        """, unsafe_allow_html=True)
        st.json(data)
        st.download_button(
            "Download Full JSON",
            json.dumps(data, indent=2, ensure_ascii=False),
            file_name="competitor_analysis.json",
            mime="application/json",
        )


# ===================================================================
# SIDEBAR
# ===================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">P</div>
        <div>
            <div class="sidebar-brand-text">Pelvi AI Hub</div>
            <div class="sidebar-brand-sub">Competitor Analyzer</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">Search History</div>', unsafe_allow_html=True)

    history = load_history()

    if history:
        if st.button("Clear All History", use_container_width=True):
            clear_all_history()
            if "result_data" in st.session_state:
                del st.session_state["result_data"]
            if "loaded_niche" in st.session_state:
                del st.session_state["loaded_niche"]
            st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        for idx, entry in enumerate(history):
            niche_name = entry['niche']
            timestamp = entry['timestamp']
            date_part = timestamp.split(" ")[0]
            time_part = timestamp.split(" ")[1] if " " in timestamp else ""

            if st.button(
                f"{niche_name}   |   {date_part}  {time_part}",
                key=f"hist_{idx}",
                use_container_width=True,
            ):
                st.session_state["result_data"] = entry["data"]
                st.session_state["loaded_niche"] = entry["niche"]
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;padding:2.5rem 1rem;color:#94a3b8;font-size:1rem;">
            No history yet.<br><span style="font-size:0.88rem;">Run your first analysis to see results here.</span>
        </div>
        """, unsafe_allow_html=True)


# ===================================================================
# MAIN CONTENT
# ===================================================================

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <div class="hero-badge">
            <div class="hero-badge-dot"></div>
            AI-Powered Analysis
        </div>
        <h1>Competitor Blog Analyzer</h1>
        <p>Discover what your competitors are publishing, find their YouTube presence, and get AI-generated blog title ideas — all in one click.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Search Bar
st.markdown('<span class="search-label">Enter Your Niche</span>', unsafe_allow_html=True)
col_input, col_btn = st.columns([4, 1])
with col_input:
    niche = st.text_input(
        "niche",
        placeholder="e.g. pelvic floor therapy, AI marketing, SaaS tools, fitness coaching...",
        label_visibility="collapsed",
    )
with col_btn:
    analyze_btn = st.button("Analyze", use_container_width=True)

# Process
if analyze_btn and niche.strip():
    with st.status("Analyzing competitors...", expanded=True) as status:
        st.write("Searching for top competitors...")
        st.write("Fetching blog posts from last 30 days...")
        st.write("Finding YouTube channels & shorts...")
        st.write("Generating AI blog title ideas...")
        result = analyze_niche(niche.strip())
        if result:
            status.update(label="Analysis complete!", state="complete", expanded=False)
        else:
            status.update(label="Analysis failed", state="error", expanded=False)

    if result:
        save_to_history(niche.strip(), result)
        st.session_state["result_data"] = result
        st.session_state["loaded_niche"] = niche.strip()
        st.rerun()

elif analyze_btn:
    st.warning("Please enter a niche to analyze.")

# Show Results
if "result_data" in st.session_state:
    loaded_niche = st.session_state.get("loaded_niche", "")
    if loaded_niche:
        st.markdown(f"""
        <div class="result-badge">
            <div class="result-badge-dot"></div>
            <span class="result-badge-text">Results for: {loaded_niche}</span>
        </div>
        """, unsafe_allow_html=True)
    render_results(st.session_state["result_data"])
else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">&#128301;</div>
        <h3>Ready to Discover Insights</h3>
        <p>Enter your niche above and hit Analyze.<br>We'll find competitors, their blogs, YouTube shorts, and generate fresh title ideas for you.</p>
    </div>
    """, unsafe_allow_html=True)
