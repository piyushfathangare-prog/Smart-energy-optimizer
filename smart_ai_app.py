"""
⚡ Smart AI Energy Optimizer - Advanced UI
------------------------------------------
Glassmorphism + Dark Mode + AI Intelligence
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
from ml_predictor import EnergyPredictor, calculate_peak_offpeak_cost, optimize_usage_schedule
from solar_calculator import SolarROICalculator
from advanced_features import AdvancedEnergyFeatures
from advanced_modules import (
    get_weather_forecast, predict_bill_with_weather,
    check_appliance_degradation, optimize_battery_schedule,
    nilm_detect, calculate_eco_score, generate_pdf_report
)

# Page config
st.set_page_config(
    page_title="⚡ Smart Energy Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# LOGIN SYSTEM
# ─────────────────────────────────────────────

# Predefined user credentials {username: password}
USERS = {
    "admin": "energy123",
    "user1": "smart2024",
    "demo":  "demo123"
}

def show_login_page():
    st.markdown("""
    <style>
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }
    .login-box {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        max-width: 420px;
        width: 100%;
        box-shadow: 0 8px 40px rgba(0,0,0,0.5);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; margin-bottom: 2rem;">
            <h1 style="font-size:3rem; background: linear-gradient(135deg, #10b981, #3b82f6);
                       -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                       font-weight:800; margin-bottom:0.25rem;">⚡ Smart Energy</h1>
            <p style="color:#94a3b8; font-size:1rem;">Optimizer — Sign In</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("🔐 Login", use_container_width=True)

            if submitted:
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")



# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# Gate: show login if not authenticated
if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# Initialize theme mode FIRST (before using it)
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

# Professional Dark Mode CSS - Restored & Improved
if st.session_state.theme_mode == "dark":
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@500;600;700;800&display=swap');
    
    /* ============================================
       GLOBAL STYLES - Professional & Clean
       ============================================ */
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.01em;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* ============================================
       DARK BACKGROUND - Improved Gradient
       ============================================ */
    
    .main {
        background: #0a0e1a;
        background-image: 
            radial-gradient(at 10% 10%, rgba(16, 185, 129, 0.12) 0px, transparent 50%),
            radial-gradient(at 90% 90%, rgba(59, 130, 246, 0.08) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(139, 92, 246, 0.05) 0px, transparent 50%);
        color: #e2e8f0;
        min-height: 100vh;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #0a0e1a;
        background-image: 
            radial-gradient(at 10% 10%, rgba(16, 185, 129, 0.12) 0px, transparent 50%),
            radial-gradient(at 90% 90%, rgba(59, 130, 246, 0.08) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(139, 92, 246, 0.05) 0px, transparent 50%);
    }
    
    /* ============================================
       HEADER - Professional & Centered
       ============================================ */
    
    .professional-header {
        text-align: center;
        padding: 2.5rem 2rem 2rem 2rem;
        margin-bottom: 2rem;
    }
    
    .professional-header h1 {
        font-size: 3.25rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.75rem;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    
    .professional-header p {
        color: #94a3b8;
        font-size: 1.125rem;
        font-weight: 400;
        margin: 0;
        letter-spacing: 0.02em;
    }
    
    /* ============================================
       NAVIGATION TABS - Improved Alignment
       ============================================ */
    
    .stButton > button {
        background: linear-gradient(135deg, #0f2027 0%, #1a2a3a 100%);
        color: #e2e8f0;
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 0.75rem 1.25rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        width: 100%;
        letter-spacing: 0.01em;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        border-color: transparent;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.35);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    /* ============================================
       CARDS - Professional Glassmorphism
       ============================================ */
    
    .premium-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        padding: 1.75rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.35);
        transition: all 0.25s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.12);
        border-color: rgba(16, 185, 129, 0.25);
    }
    
    /* ============================================
       METRIC CARDS - Better Alignment
       ============================================ */
    
    .metric-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(16, 185, 129, 0.15);
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 16px rgba(0,0,0,0.3);
        transition: all 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(16, 185, 129, 0.18);
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    .metric-card h3 {
        color: #64748b;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    .metric-card h2 {
        color: #10b981;
        font-size: 2rem;
        font-weight: 800;
        margin: 0.25rem 0;
        line-height: 1;
    }
    
    .metric-card p {
        color: #94a3b8;
        font-size: 0.8rem;
        margin: 0.4rem 0 0 0;
    }
    
    /* ============================================
       ENERGY SCORE - Improved Design
       ============================================ */
    
    .energy-score-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
    
    .energy-score {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 50%;
        width: 220px;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 
            0 0 0 8px rgba(16, 185, 129, 0.1),
            0 0 0 16px rgba(16, 185, 129, 0.05),
            0 12px 40px rgba(16, 185, 129, 0.3);
        border: 4px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .energy-score::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.05),
            transparent
        );
        transform: rotate(45deg);
        animation: shine 3s linear infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .energy-score h2 {
        font-size: 4rem;
        color: #FFFFFF;
        font-weight: 900;
        margin: 0;
        z-index: 1;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .energy-score p {
        font-size: 0.9375rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 600;
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        z-index: 1;
    }
    
    /* ============================================
       ALERT BANNERS - Professional
       ============================================ */
    
    .alert-banner {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        color: #FFFFFF;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .alert-banner h3 {
        color: #FFFFFF;
        font-size: 1.125rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    
    .alert-banner p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1rem;
        margin: 0;
        line-height: 1.6;
    }
    
    /* ============================================
       APPLIANCE CARDS - Better Layout
       ============================================ */
    
    .appliance-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        border-left: 3px solid #10b981;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.25);
    }
    
    .appliance-card:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
        border-left-color: #34d399;
        background: rgba(15, 23, 42, 0.75);
    }
    
    .smart-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.25);
        transition: all 0.2s ease;
    }
    
    .smart-card:hover {
        border-color: rgba(16, 185, 129, 0.2);
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.1);
    }
    
    /* ============================================
       PROGRESS BARS - Smooth Animation
       ============================================ */
    
    .progress-container {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 8px;
        height: 8px;
        overflow: hidden;
        margin-top: 0.75rem;
    }
    
    .progress-bar {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 8px;
        height: 8px;
        overflow: hidden;
        margin-top: 0.75rem;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s ease;
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
    }
    
    hr {
        border: none;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        margin: 1.5rem 0;
    }
    
    .ai-banner {
        background: linear-gradient(135deg, rgba(16,185,129,0.12) 0%, rgba(59,130,246,0.08) 100%);
        border: 1px solid rgba(16,185,129,0.2);
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        backdrop-filter: blur(10px);
    }
    
    /* ============================================
       SIDEBAR - Professional Dark
       ============================================ */
    
    [data-testid="stSidebar"] {
        background: #080d18;
        border-right: 1px solid rgba(16, 185, 129, 0.1);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: #080d18;
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #e2e8f0;
        font-size: 0.95rem;
        letter-spacing: 0.03em;
    }
    
    /* ============================================
       INPUT FIELDS - Modern Style
       ============================================ */
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 10px;
        color: #e2e8f0;
        padding: 0.75rem 1rem;
        font-size: 0.9375rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
        outline: none;
        background: rgba(30, 41, 59, 0.8);
    }
    
    /* ============================================
       SLIDER - Green Theme
       ============================================ */
    
    .stSlider > div > div > div > div {
        background: #10b981;
    }
    
    .stSlider > div > div > div {
        background: rgba(148, 163, 184, 0.2);
    }
    
    /* ============================================
       EXPANDER - Clean Accordion
       ============================================ */
    
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        padding: 0.875rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(30, 41, 59, 0.7);
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    /* ============================================
       INFO BOXES - Professional Alerts
       ============================================ */
    
    .stInfo {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        color: #93c5fd;
    }
    
    .stSuccess {
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10b981;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        color: #6ee7b7;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1);
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        color: #fcd34d;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        color: #fca5a5;
    }
    
    /* ============================================
       SCROLLBAR - Minimal Design
       ============================================ */
    
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 5px;
        border: 2px solid rgba(15, 23, 42, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
    
    /* ============================================
       HIDE STREAMLIT BRANDING
       ============================================ */
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ============================================
       RESPONSIVE DESIGN
       ============================================ */
    
    @media (max-width: 768px) {
        .professional-header h1 {
            font-size: 2.25rem;
        }
        
        .energy-score {
            width: 180px;
            height: 180px;
        }
        
        .energy-score h2 {
            font-size: 3rem;
        }
        
        .metric-card h2 {
            font-size: 1.875rem;
        }
    }
    
    /* ============================================
       SMOOTH ANIMATIONS
       ============================================ */
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .premium-card,
    .metric-card,
    .appliance-card {
        animation: fadeIn 0.4s ease-out;
    }
    
</style>
""", unsafe_allow_html=True)
else:
    # Light Mode CSS (keep existing)
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: #f8fafc;
        color: #1e293b;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #f8fafc;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Expanded Appliance database with 50+ appliances
APPLIANCE_DATABASE = {
    # Cooling & Climate Control
    "Air Conditioner (1.5 Ton)": {"icon": "❄️", "typical_power": 1500, "category": "Cooling", "efficiency_rating": 3},
    "Air Conditioner (2 Ton)": {"icon": "❄️", "typical_power": 2000, "category": "Cooling", "efficiency_rating": 3},
    "Air Conditioner (Window)": {"icon": "❄️", "typical_power": 1200, "category": "Cooling", "efficiency_rating": 3},
    "Air Cooler": {"icon": "💨", "typical_power": 200, "category": "Cooling", "efficiency_rating": 4},
    "Ceiling Fan": {"icon": "🌀", "typical_power": 75, "category": "Cooling", "efficiency_rating": 5},
    "Table Fan": {"icon": "🌀", "typical_power": 50, "category": "Cooling", "efficiency_rating": 5},
    "Exhaust Fan": {"icon": "🌀", "typical_power": 40, "category": "Cooling", "efficiency_rating": 5},
    
    # Refrigeration
    "Refrigerator (Single Door)": {"icon": "🧊", "typical_power": 100, "category": "Refrigeration", "efficiency_rating": 4},
    "Refrigerator (Double Door)": {"icon": "🧊", "typical_power": 150, "category": "Refrigeration", "efficiency_rating": 4},
    "Refrigerator (Side by Side)": {"icon": "🧊", "typical_power": 250, "category": "Refrigeration", "efficiency_rating": 3},
    "Deep Freezer": {"icon": "🧊", "typical_power": 300, "category": "Refrigeration", "efficiency_rating": 3},
    "Mini Fridge": {"icon": "🧊", "typical_power": 80, "category": "Refrigeration", "efficiency_rating": 4},
    
    # Washing & Cleaning
    "Washing Machine (Front Load)": {"icon": "🧺", "typical_power": 500, "category": "Cleaning", "efficiency_rating": 4},
    "Washing Machine (Top Load)": {"icon": "🧺", "typical_power": 400, "category": "Cleaning", "efficiency_rating": 4},
    "Dishwasher": {"icon": "🍽️", "typical_power": 1800, "category": "Cleaning", "efficiency_rating": 3},
    "Vacuum Cleaner": {"icon": "🧹", "typical_power": 1000, "category": "Cleaning", "efficiency_rating": 4},
    "Iron": {"icon": "👔", "typical_power": 1000, "category": "Cleaning", "efficiency_rating": 3},
    "Steam Iron": {"icon": "👔", "typical_power": 1200, "category": "Cleaning", "efficiency_rating": 3},
    
    # Kitchen Appliances
    "Microwave Oven": {"icon": "🔥", "typical_power": 1200, "category": "Cooking", "efficiency_rating": 4},
    "Oven (Electric)": {"icon": "🍳", "typical_power": 2000, "category": "Cooking", "efficiency_rating": 2},
    "Induction Cooktop": {"icon": "🍳", "typical_power": 2000, "category": "Cooking", "efficiency_rating": 4},
    "Electric Stove": {"icon": "🍳", "typical_power": 2500, "category": "Cooking", "efficiency_rating": 2},
    "Toaster": {"icon": "🍞", "typical_power": 800, "category": "Cooking", "efficiency_rating": 4},
    "Electric Kettle": {"icon": "☕", "typical_power": 1500, "category": "Cooking", "efficiency_rating": 4},
    "Coffee Maker": {"icon": "☕", "typical_power": 1000, "category": "Cooking", "efficiency_rating": 4},
    "Mixer Grinder": {"icon": "🥤", "typical_power": 500, "category": "Cooking", "efficiency_rating": 4},
    "Blender": {"icon": "🥤", "typical_power": 400, "category": "Cooking", "efficiency_rating": 4},
    "Food Processor": {"icon": "🍴", "typical_power": 600, "category": "Cooking", "efficiency_rating": 4},
    "Rice Cooker": {"icon": "🍚", "typical_power": 700, "category": "Cooking", "efficiency_rating": 4},
    "Air Fryer": {"icon": "🍟", "typical_power": 1500, "category": "Cooking", "efficiency_rating": 3},
    "Sandwich Maker": {"icon": "🥪", "typical_power": 800, "category": "Cooking", "efficiency_rating": 4},
    
    # Entertainment
    "TV (32 inch LED)": {"icon": "📺", "typical_power": 60, "category": "Entertainment", "efficiency_rating": 5},
    "TV (43 inch LED)": {"icon": "📺", "typical_power": 80, "category": "Entertainment", "efficiency_rating": 5},
    "TV (55 inch LED)": {"icon": "📺", "typical_power": 100, "category": "Entertainment", "efficiency_rating": 4},
    "TV (65 inch LED)": {"icon": "📺", "typical_power": 150, "category": "Entertainment", "efficiency_rating": 4},
    "Home Theater System": {"icon": "🔊", "typical_power": 300, "category": "Entertainment", "efficiency_rating": 4},
    "Soundbar": {"icon": "🔊", "typical_power": 50, "category": "Entertainment", "efficiency_rating": 5},
    "Gaming Console": {"icon": "🎮", "typical_power": 150, "category": "Entertainment", "efficiency_rating": 4},
    "Set-Top Box": {"icon": "📡", "typical_power": 15, "category": "Entertainment", "efficiency_rating": 5},
    
    # Computing
    "Desktop Computer": {"icon": "💻", "typical_power": 200, "category": "Electronics", "efficiency_rating": 4},
    "Laptop": {"icon": "💻", "typical_power": 60, "category": "Electronics", "efficiency_rating": 5},
    "Monitor (24 inch)": {"icon": "🖥️", "typical_power": 30, "category": "Electronics", "efficiency_rating": 5},
    "Printer": {"icon": "🖨️", "typical_power": 50, "category": "Electronics", "efficiency_rating": 4},
    "Router/WiFi": {"icon": "📶", "typical_power": 10, "category": "Electronics", "efficiency_rating": 5},
    "Modem": {"icon": "📶", "typical_power": 8, "category": "Electronics", "efficiency_rating": 5},
    
    # Heating
    "Room Heater": {"icon": "🌡️", "typical_power": 2000, "category": "Heating", "efficiency_rating": 2},
    "Water Heater (Geyser)": {"icon": "🚿", "typical_power": 2000, "category": "Heating", "efficiency_rating": 2},
    "Immersion Rod": {"icon": "🚿", "typical_power": 1500, "category": "Heating", "efficiency_rating": 2},
    "Hair Dryer": {"icon": "💇", "typical_power": 1500, "category": "Personal Care", "efficiency_rating": 3},
    
    # Lighting
    "LED Bulb (9W)": {"icon": "💡", "typical_power": 9, "category": "Lighting", "efficiency_rating": 5},
    "LED Bulb (12W)": {"icon": "💡", "typical_power": 12, "category": "Lighting", "efficiency_rating": 5},
    "CFL Bulb (15W)": {"icon": "💡", "typical_power": 15, "category": "Lighting", "efficiency_rating": 4},
    "Tube Light (LED)": {"icon": "💡", "typical_power": 20, "category": "Lighting", "efficiency_rating": 5},
    "Tube Light (Fluorescent)": {"icon": "💡", "typical_power": 40, "category": "Lighting", "efficiency_rating": 3},
    "Decorative Lights": {"icon": "✨", "typical_power": 50, "category": "Lighting", "efficiency_rating": 4},
    
    # Water & Pumps
    "Water Pump (0.5 HP)": {"icon": "💧", "typical_power": 370, "category": "Water", "efficiency_rating": 4},
    "Water Pump (1 HP)": {"icon": "💧", "typical_power": 750, "category": "Water", "efficiency_rating": 4},
    "Aquarium Pump": {"icon": "🐠", "typical_power": 50, "category": "Water", "efficiency_rating": 4},
    
    # Others
    "Electric Chimney": {"icon": "🏠", "typical_power": 200, "category": "Kitchen", "efficiency_rating": 4},
    "Sewing Machine": {"icon": "🧵", "typical_power": 100, "category": "Others", "efficiency_rating": 4},
    "Treadmill": {"icon": "🏃", "typical_power": 700, "category": "Fitness", "efficiency_rating": 3},
    "Electric Shaver": {"icon": "🪒", "typical_power": 15, "category": "Personal Care", "efficiency_rating": 5},
    "Electric Toothbrush": {"icon": "🪥", "typical_power": 2, "category": "Personal Care", "efficiency_rating": 5},
    "Humidifier": {"icon": "💨", "typical_power": 30, "category": "Climate", "efficiency_rating": 4},
    "Dehumidifier": {"icon": "💨", "typical_power": 300, "category": "Climate", "efficiency_rating": 3},
    "Air Purifier": {"icon": "🌬️", "typical_power": 50, "category": "Climate", "efficiency_rating": 4},
}

# Product recommendations
# Product recommendations - Expanded database
PRODUCT_RECOMMENDATIONS = {
    "Air Conditioner": [
        {"brand": "Voltas", "model": "185V JZJ", "star": 5, "capacity": "1.5 Ton", "power": 1050, "price": 38000, "savings": "30%", "payback": "2.5 years"},
        {"brand": "Daikin", "model": "FTKF50TV", "star": 5, "capacity": "1.5 Ton", "power": 1100, "price": 45000, "savings": "27%", "payback": "3 years"},
        {"brand": "LG", "model": "PS-Q19YNZE", "star": 5, "capacity": "1.5 Ton", "power": 1080, "price": 42000, "savings": "28%", "payback": "2.8 years"},
        {"brand": "Blue Star", "model": "IC518DBTU", "star": 5, "capacity": "1.5 Ton", "power": 1120, "price": 40000, "savings": "26%", "payback": "2.7 years"}
    ],
    "Refrigerator": [
        {"brand": "Whirlpool", "model": "FP 263D", "star": 5, "capacity": "245L", "power": 95, "price": 24000, "savings": "37%", "payback": "3 years"},
        {"brand": "Samsung", "model": "RT28T3922", "star": 5, "capacity": "253L", "power": 100, "price": 28000, "savings": "33%", "payback": "3.5 years"},
        {"brand": "LG", "model": "GL-T292RPZY", "star": 5, "capacity": "260L", "power": 98, "price": 26000, "savings": "35%", "payback": "3.2 years"},
        {"brand": "Haier", "model": "HRB-2764", "star": 4, "capacity": "256L", "power": 110, "price": 22000, "savings": "27%", "payback": "3.8 years"}
    ],
    "Washing Machine": [
        {"brand": "IFB", "model": "Senator Aqua SX", "star": 5, "capacity": "8 Kg", "power": 450, "price": 32000, "savings": "35%", "payback": "3 years"},
        {"brand": "Bosch", "model": "WAJ2846IN", "star": 5, "capacity": "8 Kg", "power": 480, "price": 35000, "savings": "32%", "payback": "3.2 years"},
        {"brand": "LG", "model": "FHM1408BDL", "star": 5, "capacity": "8 Kg", "power": 470, "price": 33000, "savings": "33%", "payback": "3.1 years"}
    ],
    "Television": [
        {"brand": "Samsung", "model": "Crystal 4K", "star": 5, "capacity": "55 inch", "power": 95, "price": 45000, "savings": "40%", "payback": "4 years"},
        {"brand": "LG", "model": "OLED C2", "star": 5, "capacity": "55 inch", "power": 90, "price": 85000, "savings": "42%", "payback": "5 years"},
        {"brand": "Sony", "model": "Bravia X80K", "star": 5, "capacity": "55 inch", "power": 100, "price": 65000, "savings": "38%", "payback": "4.5 years"}
    ],
    "Fan": [
        {"brand": "Atomberg", "model": "Efficio", "star": 5, "capacity": "1200mm", "power": 28, "price": 3500, "savings": "65%", "payback": "1.5 years"},
        {"brand": "Havells", "model": "Stealth Air", "star": 5, "capacity": "1200mm", "power": 32, "price": 4200, "savings": "60%", "payback": "1.8 years"},
        {"brand": "Orient", "model": "Aeroquiet", "star": 5, "capacity": "1200mm", "power": 35, "price": 3800, "savings": "55%", "payback": "2 years"}
    ],
    "Water Heater": [
        {"brand": "Racold", "model": "Omnis Lux", "star": 5, "capacity": "25L", "power": 1800, "price": 12000, "savings": "30%", "payback": "2.5 years"},
        {"brand": "AO Smith", "model": "HSE-SAS", "star": 5, "capacity": "25L", "power": 1850, "price": 15000, "savings": "28%", "payback": "3 years"},
        {"brand": "Bajaj", "model": "New Shakti", "star": 4, "capacity": "25L", "power": 1900, "price": 9000, "savings": "25%", "payback": "2.8 years"}
    ],
    "LED Bulb": [
        {"brand": "Philips", "model": "Stellar Bright", "star": 5, "capacity": "9W", "power": 9, "price": 250, "savings": "85%", "payback": "6 months"},
        {"brand": "Syska", "model": "SSK-SRL", "star": 5, "capacity": "9W", "power": 9, "price": 180, "savings": "85%", "payback": "5 months"},
        {"brand": "Wipro", "model": "Garnet", "star": 5, "capacity": "9W", "power": 9, "price": 200, "savings": "85%", "payback": "5.5 months"}
    ],
    "Microwave": [
        {"brand": "IFB", "model": "25SC4", "star": 4, "capacity": "25L", "power": 1100, "price": 12000, "savings": "20%", "payback": "3 years"},
        {"brand": "Samsung", "model": "MC28H5013AK", "star": 4, "capacity": "28L", "power": 1150, "price": 14000, "savings": "18%", "payback": "3.5 years"},
        {"brand": "LG", "model": "MC2146BG", "star": 4, "capacity": "21L", "power": 1050, "price": 10000, "savings": "22%", "payback": "2.8 years"}
    ]
}

# Generic recommendations by category for custom appliances
GENERIC_RECOMMENDATIONS = {
    "Cooling": {
        "tips": [
            "Look for 5-star rated models with inverter technology",
            "Choose appropriate capacity for your room size",
            "Consider split AC over window AC for better efficiency",
            "Check for eco-friendly refrigerants (R32, R410A)"
        ],
        "avg_savings": "25-35%",
        "brands": ["Voltas", "Daikin", "LG", "Blue Star", "Carrier"]
    },
    "Refrigeration": {
        "tips": [
            "Opt for 5-star rated models with inverter compressor",
            "Choose frost-free for convenience and efficiency",
            "Look for models with smart cooling technology",
            "Consider capacity based on family size"
        ],
        "avg_savings": "30-40%",
        "brands": ["Whirlpool", "Samsung", "LG", "Haier", "Godrej"]
    },
    "Cleaning": {
        "tips": [
            "Front-load machines are more efficient than top-load",
            "Look for 5-star rated models with inverter motor",
            "Choose appropriate capacity to avoid multiple loads",
            "Consider models with quick wash and eco modes"
        ],
        "avg_savings": "30-35%",
        "brands": ["IFB", "Bosch", "LG", "Samsung", "Whirlpool"]
    },
    "Cooking": {
        "tips": [
            "Induction cooktops are most efficient",
            "Look for convection microwaves for versatility",
            "Choose appropriate wattage for your needs",
            "Consider energy-saving modes"
        ],
        "avg_savings": "20-30%",
        "brands": ["IFB", "Samsung", "LG", "Panasonic", "Morphy Richards"]
    },
    "Entertainment": {
        "tips": [
            "LED/OLED TVs consume less power than LCD",
            "Choose appropriate screen size for viewing distance",
            "Look for 5-star rated models",
            "Enable eco/power saving modes"
        ],
        "avg_savings": "35-45%",
        "brands": ["Samsung", "LG", "Sony", "Mi", "OnePlus"]
    },
    "Electronics": {
        "tips": [
            "Look for Energy Star certified devices",
            "Choose laptops over desktops for lower consumption",
            "Enable power management features",
            "Consider energy-efficient power supplies"
        ],
        "avg_savings": "20-30%",
        "brands": ["Dell", "HP", "Lenovo", "Apple", "Asus"]
    },
    "Heating": {
        "tips": [
            "Choose appropriate capacity for your needs",
            "Look for models with thermostat control",
            "Consider instant heaters over storage types",
            "Check for 5-star ratings"
        ],
        "avg_savings": "25-30%",
        "brands": ["Racold", "AO Smith", "Bajaj", "Havells", "Crompton"]
    },
    "Lighting": {
        "tips": [
            "Replace all bulbs with LED",
            "Choose appropriate lumens for the space",
            "Look for high CRI (Color Rendering Index)",
            "Consider smart bulbs for automation"
        ],
        "avg_savings": "80-90%",
        "brands": ["Philips", "Syska", "Wipro", "Havells", "Crompton"]
    },
    "Water": {
        "tips": [
            "Choose appropriate HP for your building height",
            "Look for energy-efficient motors",
            "Consider variable speed pumps",
            "Regular maintenance improves efficiency"
        ],
        "avg_savings": "20-25%",
        "brands": ["Crompton", "Havells", "Kirloskar", "V-Guard", "Shakti"]
    },
    "Others": {
        "tips": [
            "Look for energy-efficient models",
            "Choose appropriate capacity/power",
            "Check for energy star ratings",
            "Consider usage patterns before buying"
        ],
        "avg_savings": "20-30%",
        "brands": ["Various brands available"]
    }
}

def get_smart_recommendations(appliance_name, current_power, category, hours_per_day, rate_avg):
    """Generate smart product recommendations for any appliance"""
    recommendations = []
    
    # Check if exact match exists in PRODUCT_RECOMMENDATIONS
    for key in PRODUCT_RECOMMENDATIONS.keys():
        if key.lower() in appliance_name.lower():
            return PRODUCT_RECOMMENDATIONS[key]
    
    # Generate generic recommendations based on category
    if category in GENERIC_RECOMMENDATIONS:
        generic = GENERIC_RECOMMENDATIONS[category]
        
        # Calculate potential savings
        avg_savings_pct = 30  # Default 30% savings
        if "avg_savings" in generic:
            avg_savings_range = generic["avg_savings"].replace("%", "").split("-")
            avg_savings_pct = (int(avg_savings_range[0]) + int(avg_savings_range[1])) / 2
        
        new_power = current_power * (1 - avg_savings_pct / 100)
        daily_savings_kwh = (current_power - new_power) * hours_per_day / 1000
        monthly_savings = daily_savings_kwh * 30 * rate_avg
        yearly_savings = monthly_savings * 12
        
        # Generate 3 recommendation tiers
        recommendations = [
            {
                "brand": generic["brands"][0] if len(generic["brands"]) > 0 else "Premium Brand",
                "model": "5-Star Rated Model",
                "star": 5,
                "capacity": "Appropriate Size",
                "power": int(new_power),
                "price": int(current_power * 15),  # Rough estimate
                "savings": f"{int(avg_savings_pct)}%",
                "payback": f"{(current_power * 15) / yearly_savings:.1f} years" if yearly_savings > 0 else "N/A",
                "monthly_savings": int(monthly_savings)
            },
            {
                "brand": generic["brands"][1] if len(generic["brands"]) > 1 else "Mid-Range Brand",
                "model": "4-Star Rated Model",
                "star": 4,
                "capacity": "Appropriate Size",
                "power": int(new_power * 1.1),
                "price": int(current_power * 12),
                "savings": f"{int(avg_savings_pct * 0.85)}%",
                "payback": f"{(current_power * 12) / (yearly_savings * 0.85):.1f} years" if yearly_savings > 0 else "N/A",
                "monthly_savings": int(monthly_savings * 0.85)
            },
            {
                "brand": generic["brands"][2] if len(generic["brands"]) > 2 else "Budget Brand",
                "model": "3-Star Rated Model",
                "star": 3,
                "capacity": "Appropriate Size",
                "power": int(new_power * 1.2),
                "price": int(current_power * 8),
                "savings": f"{int(avg_savings_pct * 0.7)}%",
                "payback": f"{(current_power * 8) / (yearly_savings * 0.7):.1f} years" if yearly_savings > 0 else "N/A",
                "monthly_savings": int(monthly_savings * 0.7)
            }
        ]
    
    return recommendations

# Initialize session state
if "ml_model" not in st.session_state:
    st.session_state.ml_model = EnergyPredictor()
if "appliance_data" not in st.session_state:
    st.session_state.appliance_data = {}
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "rate_peak" not in st.session_state:
    st.session_state.rate_peak = 12.0
if "rate_offpeak" not in st.session_state:
    st.session_state.rate_offpeak = 12.0
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "dashboard"
if "custom_appliances" not in st.session_state:
    st.session_state.custom_appliances = {}
if "show_add_appliance" not in st.session_state:
    st.session_state.show_add_appliance = False
# theme_mode already initialized at top of file
if "energy_goals" not in st.session_state:
    st.session_state.energy_goals = []
if "goal_tracker" not in st.session_state:
    from energy_goals import EnergyGoalTracker
    st.session_state.goal_tracker = EnergyGoalTracker()
if "advanced_features" not in st.session_state:
    st.session_state.advanced_features = AdvancedEnergyFeatures()
if "previous_month_kwh" not in st.session_state:
    st.session_state.previous_month_kwh = None
if "user_city" not in st.session_state:
    st.session_state.user_city = "Mumbai"

def calculate_energy_score(appliance_data, prediction):
    """Calculate energy efficiency score (0-100)"""
    if not appliance_data:
        return 50
    
    total_score = 0
    for appliance, data in appliance_data.items():
        efficiency = APPLIANCE_DATABASE[appliance]["efficiency_rating"]
        total_score += efficiency
    
    avg_efficiency = (total_score / len(appliance_data)) / 5 * 100
    
    # Adjust based on consumption
    daily_kwh = prediction.get('daily_total', 0)
    if daily_kwh < 20:
        consumption_score = 100
    elif daily_kwh < 40:
        consumption_score = 80
    elif daily_kwh < 60:
        consumption_score = 60
    else:
        consumption_score = 40
    
    final_score = (avg_efficiency * 0.6 + consumption_score * 0.4)
    return min(100, max(0, final_score))

def calculate_slab_based_bill(monthly_kwh):
    """
    Calculate electricity bill based on Maharashtra tariff slabs
    Slabs: 0-100, 101-300, 301-500, 501-1000, >1000
    """
    # Maharashtra Electricity Tariff (Residential - LT I)
    slabs = [
        {"min": 0, "max": 100, "rate": 4.28, "fixed": 130},
        {"min": 101, "max": 300, "rate": 11.10, "fixed": 130},
        {"min": 301, "max": 500, "rate": 15.38, "fixed": 130},
        {"min": 501, "max": 1000, "rate": 17.68, "fixed": 130},
        {"min": 1001, "max": float('inf'), "rate": 17.68, "fixed": 130}
    ]
    
    total_cost = 0
    remaining_units = monthly_kwh
    
    for slab in slabs:
        if remaining_units <= 0:
            break
        
        # Calculate units in this slab
        slab_min = slab["min"]
        slab_max = slab["max"]
        
        if monthly_kwh <= slab_min:
            continue
        
        # Units consumed in this slab
        if monthly_kwh <= slab_max:
            units_in_slab = monthly_kwh - slab_min + 1
        else:
            units_in_slab = slab_max - slab_min + 1
        
        # Cost for this slab
        slab_cost = units_in_slab * slab["rate"]
        total_cost += slab_cost
        
        remaining_units -= units_in_slab
    
    # Add fixed charges (only once)
    fixed_charge = slabs[0]["fixed"]
    
    # Electricity Duty (16% on energy charges)
    electricity_duty = total_cost * 0.16
    
    # Total bill
    total_bill = total_cost + fixed_charge + electricity_duty
    
    return {
        "energy_charges": total_cost,
        "fixed_charges": fixed_charge,
        "electricity_duty": electricity_duty,
        "total_bill": total_bill,
        "effective_rate": total_bill / monthly_kwh if monthly_kwh > 0 else 0
    }

def calculate_carbon_impact(daily_kwh):
    """Calculate carbon emissions (kg CO2)"""
    # Average: 0.82 kg CO2 per kWh in India
    daily_co2 = daily_kwh * 0.82
    monthly_co2 = daily_co2 * 30
    yearly_co2 = daily_co2 * 365
    
    # Trees equivalent (1 tree absorbs ~21 kg CO2/year)
    trees_equivalent = yearly_co2 / 21
    
    # km not driven (1 km = 0.12 kg CO2)
    km_equivalent = yearly_co2 / 0.12
    
    return {
        "daily_co2": daily_co2,
        "monthly_co2": monthly_co2,
        "yearly_co2": yearly_co2,
        "trees_equivalent": trees_equivalent,
        "km_equivalent": km_equivalent
    }

# Professional Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2.5rem; padding: 2rem 0;">
    <h1 style="font-size: 3.5rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;
                letter-spacing: -1px; margin-bottom: 0.5rem;">
        ⚡ Smart Energy Optimizer
    </h1>
    <p style="color: #94a3b8; font-size: 1.2rem; font-weight: 400; letter-spacing: 0.5px;">
        Professional Energy Intelligence Platform
    </p>
</div>
""", unsafe_allow_html=True)

# Tab Navigation - Row 1
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
with col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.current_tab = "dashboard"
        st.rerun()
with col2:
    if st.button("📊 Insights", use_container_width=True):
        st.session_state.current_tab = "insights"
        st.rerun()
with col3:
    if st.button("🔌 Appliances", use_container_width=True):
        st.session_state.current_tab = "appliances"
        st.rerun()
with col4:
    if st.button("🧪 Simulation", use_container_width=True):
        st.session_state.current_tab = "simulation"
        st.rerun()
with col5:
    if st.button("☀️ Solar ROI", use_container_width=True):
        st.session_state.current_tab = "solar"
        st.rerun()
with col6:
    if st.button("🌍 Impact", use_container_width=True):
        st.session_state.current_tab = "impact"
        st.rerun()
with col7:
    if st.button("🎯 Goals", use_container_width=True):
        st.session_state.current_tab = "goals"
        st.rerun()
with col8:
    if st.button("📈 Analytics", use_container_width=True):
        st.session_state.current_tab = "analytics"
        st.rerun()

# Tab Navigation - Row 2 (Advanced Features)
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🔋 Battery & ToU", use_container_width=True):
        st.session_state.current_tab = "battery"
        st.rerun()
with col2:
    if st.button("🔍 Smart Meter", use_container_width=True):
        st.session_state.current_tab = "nilm"
        st.rerun()
with col3:
    if st.button("🏆 Eco-Score", use_container_width=True):
        st.session_state.current_tab = "ecoscore"
        st.rerun()
with col4:
    if st.button("📄 PDF Report", use_container_width=True):
        st.session_state.current_tab = "report"
        st.rerun()

st.markdown("---")

# Sidebar Configuration
with st.sidebar:
    # User info + logout
    st.markdown(f"""
    <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.2);
                border-radius:10px; padding:0.75rem 1rem; margin-bottom:1rem;">
        <p style="margin:0; color:#10b981; font-size:0.85rem; font-weight:600;">
            👤 Logged in as: <span style="color:#e2e8f0;">{st.session_state.current_user}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()
    st.markdown("---")
    st.markdown("## ⚙️ Configuration")
    
    # Dark/Light Mode Toggle
    st.markdown("### 🎨 Theme")
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        if st.button("🌙 Dark", use_container_width=True, type="primary" if st.session_state.theme_mode == "dark" else "secondary"):
            st.session_state.theme_mode = "dark"
            st.rerun()
    with theme_col2:
        if st.button("☀️ Light", use_container_width=True, type="primary" if st.session_state.theme_mode == "light" else "secondary"):
            st.session_state.theme_mode = "light"
            st.rerun()
    
    st.markdown("---")
    
    # City Selection for Comparison
    st.markdown("### 📍 Your City")
    st.session_state.user_city = st.selectbox(
        "Select your city:",
        ["Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad"],
        index=["Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad"].index(st.session_state.user_city)
    )
    
    st.markdown("---")
    
    st.markdown("### 🔌 Select Appliances")
    
    # Merge custom appliances with database
    all_appliances = {**APPLIANCE_DATABASE, **st.session_state.custom_appliances}
    appliance_options = list(all_appliances.keys())
    
    filtered_options = appliance_options
    
    # Add Custom Appliance Button
    st.markdown("---")
    if st.button("➕ Add Custom Appliance", use_container_width=True, type="primary"):
        st.session_state.show_add_appliance = True
    
    # Custom Appliance Dialog
    if st.session_state.get("show_add_appliance", False):
        with st.form("add_custom_appliance_form"):
            st.markdown("#### ➕ Add New Appliance")
            
            custom_name = st.text_input("Appliance Name", placeholder="e.g., Old Fridge")
            
            col1, col2 = st.columns(2)
            with col1:
                custom_type = st.selectbox("Type", all_categories)
                custom_power = st.number_input("Current Wattage", min_value=1, value=100, step=10)
            with col2:
                custom_icon = st.text_input("Icon (emoji)", value="🔌", max_chars=2)
                custom_rating = st.slider("Efficiency Rating", 1, 5, 3)
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("✅ Save Appliance", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit and custom_name:
                # Add to custom appliances in session state
                st.session_state.custom_appliances[custom_name] = {
                    "icon": custom_icon,
                    "typical_power": custom_power,
                    "category": custom_type,
                    "efficiency_rating": custom_rating
                }
                st.session_state.show_add_appliance = False
                st.success(f"✅ Added {custom_name} successfully!")
                st.rerun()
            elif submit and not custom_name:
                st.error("⚠️ Please enter an appliance name!")
            
            if cancel:
                st.session_state.show_add_appliance = False
                st.rerun()
    
    st.markdown("---")
    
    # Select All / Clear All buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Select All", use_container_width=True):
            st.session_state.selected_appliances = filtered_options.copy()
    with col2:
        if st.button("❌ Clear All", use_container_width=True):
            st.session_state.selected_appliances = []
    
    # Initialize session state for selected appliances
    if "selected_appliances" not in st.session_state:
        st.session_state.selected_appliances = []
    
    # Multiselect with filtered options
    selected_appliances = st.multiselect(
        f"Choose appliances ({len(filtered_options)} available):",
        filtered_options,
        default=st.session_state.selected_appliances,
        help="Select all appliances in your home",
        key="appliance_selector"
    )
    
    # Update session state
    st.session_state.selected_appliances = selected_appliances
    
    st.markdown("---")
    
    # Show custom appliances count
    if st.session_state.custom_appliances:
        st.markdown(f"**Custom Appliances:** {len(st.session_state.custom_appliances)}")
        with st.expander("🗑️ Manage Custom Appliances"):
            for custom_name in list(st.session_state.custom_appliances.keys()):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(f"{st.session_state.custom_appliances[custom_name]['icon']} {custom_name}")
                with col2:
                    if st.button("🗑️", key=f"delete_{custom_name}"):
                        del st.session_state.custom_appliances[custom_name]
                        if custom_name in st.session_state.selected_appliances:
                            st.session_state.selected_appliances.remove(custom_name)
                        st.rerun()
    
    st.markdown("---")
    
    # Dynamic inputs
    appliance_data = {}
    for appliance in selected_appliances:
        icon = all_appliances[appliance]["icon"]
        typical_power = all_appliances[appliance]["typical_power"]
        
        with st.expander(f"{icon} {appliance}", expanded=False):
            power = st.number_input(
                "Power (W)",
                min_value=1,
                value=typical_power,
                key=f"{appliance}_power"
            )
            hours = st.slider(
                "Hours/Day",
                0.0, 24.0, 8.0,
                key=f"{appliance}_hours"
            )
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
                key=f"{appliance}_qty"
            )
            
            appliance_data[appliance] = {
                "power_watts": power,
                "hours_per_day": hours,
                "quantity": quantity
            }
    
    st.markdown("---")
    
    # Electricity rates - Slab-based billing info
    st.markdown("### 💰 Billing System")
    st.info("""
    **Maharashtra Tariff (LT I - Residential)**
    - 0-100 units: ₹4.28/unit
    - 101-300 units: ₹11.10/unit
    - 301-500 units: ₹15.38/unit
    - 501-1000 units: ₹17.68/unit
    - >1000 units: ₹17.68/unit
    
    + Fixed: ₹130/month
    + Duty: 16% on energy charges
    """)
    
    st.markdown("---")
    
    # Fixed average rate based on Maharashtra slab billing
    rate_peak = 12.0
    rate_offpeak = 12.0
    
    # Analyze button
    if st.button("⚡ Analyze with AI", use_container_width=True):
        if not selected_appliances:
            st.error("⚠️ Select at least one appliance!")
        else:
            st.session_state.appliance_data = appliance_data
            st.session_state.rate_peak = rate_peak
            st.session_state.rate_offpeak = rate_offpeak
            st.session_state.show_results = True
            
            # Train model
            with st.spinner("🤖 AI is analyzing your energy usage..."):
                result = st.session_state.ml_model.train(appliance_data)
                st.session_state.ml_result = result
            
            st.rerun()

# Main Content Based on Tab
if not st.session_state.show_results or not st.session_state.appliance_data:
    # Show welcome screen but also handle tab clicks gracefully
    if st.session_state.current_tab != "dashboard":
        st.info("⚡ Please select appliances from the sidebar and click **Analyze with AI** to view this tab.")
    else:
        pass  # Welcome screen shown in else block below

if st.session_state.show_results and st.session_state.appliance_data:
    appliance_data = st.session_state.appliance_data
    rate_peak = st.session_state.rate_peak
    rate_offpeak = st.session_state.rate_offpeak
    ml_model = st.session_state.ml_model
    
    prediction = ml_model.predict_monthly_consumption(appliance_data)
    energy_score = calculate_energy_score(appliance_data, prediction)
    carbon_impact = calculate_carbon_impact(prediction['daily_total'])
    
    # AI Insight Banner
    daily_change = np.random.randint(-15, 15)  # Simulated
    potential_savings = sum([data['power_watts'] * data['hours_per_day'] * 0.3 / 1000 for data in appliance_data.values()])
    savings_amount = potential_savings * 30 * ((rate_peak + rate_offpeak) / 2)
    
    # Get advanced features
    advanced = st.session_state.advanced_features
    
    try:
        peak_alert = advanced.check_peak_load_alert(prediction['daily_total'])
        waste_detection = advanced.detect_energy_waste(appliance_data)
        city_comparison = advanced.compare_with_city(prediction['monthly_total'], st.session_state.user_city)
        gamification = advanced.calculate_gamification_score(prediction['monthly_total'], st.session_state.previous_month_kwh)
    except Exception as e:
        st.error(f"Error loading advanced features: {str(e)}")
        peak_alert = {'alert': False}
        waste_detection = []
        city_comparison = {'status': '🟡', 'message': 'Comparison unavailable', 'city': st.session_state.user_city, 'city_average': 240, 'your_usage': prediction['monthly_total']}
        gamification = {'points_earned': 0, 'total_points': 0, 'level': 1, 'badges': [], 'new_badges': [], 'next_level_points': 200}
    
    # Peak Load Alert (if triggered)
    if peak_alert['alert']:
        alert_color = "#ef4444" if peak_alert['severity'] == "high" else "#f59e0b"
        st.markdown(f"""
        <div class="ai-banner" style="background: linear-gradient(135deg, {alert_color}22 0%, {alert_color}11 100%); border-left: 4px solid {alert_color};">
            <h3 style="margin: 0 0 0.5rem 0; color: {alert_color};">{peak_alert['message']}</h3>
            <p style="margin: 0 0 0.5rem 0; font-size: 1.05rem;">{peak_alert['details']}</p>
            <p style="margin: 0; font-size: 0.95rem; color: #94a3b8;">
                <strong>Suggested Actions:</strong><br>
                {'<br>'.join(['• ' + s for s in peak_alert['suggestions']])}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Gamification Banner
    st.markdown(f"""
    <div class="ai-banner" style="background: linear-gradient(135deg, #8b5cf622 0%, #8b5cf611 100%); border-left: 4px solid #8b5cf6;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="margin: 0 0 0.5rem 0; color: #8b5cf6;">🏆 Level {gamification['level']} Energy Saver</h3>
                <p style="margin: 0; font-size: 1.05rem;">
                    You earned <strong>{gamification['points_earned']} points</strong> this month! 
                    Total: {gamification['total_points']} points
                </p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #94a3b8;">
                    {gamification['next_level_points']} points to Level {gamification['level'] + 1}
                </p>
            </div>
            <div style="font-size: 3rem;">
                {''.join(gamification['badges'][:3])}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # City Comparison Banner
    st.markdown(f"""
    <div class="ai-banner">
        <h3 style="margin: 0 0 0.5rem 0;">📊 {city_comparison['city']} Comparison</h3>
        <p style="margin: 0; font-size: 1.05rem;">
            {city_comparison['status']} - {city_comparison['message']}
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #94a3b8;">
            Average {city_comparison['city']} Household: {city_comparison['city_average']} kWh/month | 
            Your Usage: {city_comparison['your_usage']:.0f} kWh/month
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="ai-banner">
        <h3 style="margin: 0 0 0.5rem 0;">🤖 AI Insight</h3>
        <p style="margin: 0; font-size: 1.1rem;">
            Your energy usage {'increased' if daily_change > 0 else 'decreased'} by {abs(daily_change)}% this week. 
            Reducing AC usage by 30 mins can save ₹{savings_amount:.0f}/month.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tab Content
    if st.session_state.current_tab == "dashboard":
        # Energy Score
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            score_color = "#10b981" if energy_score >= 70 else "#f59e0b" if energy_score >= 50 else "#ef4444"
            st.markdown(f"""
            <div class="energy-score" style="background: linear-gradient(135deg, {score_color} 0%, {score_color}dd 100%);">
                <h2 style="margin: 0; font-size: 3rem; font-weight: 900;">{energy_score:.0f}</h2>
                <p style="margin: 0; font-size: 1.2rem;">Energy Score</p>
                <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">
                    {'🟢 Efficient' if energy_score >= 70 else '🟡 Moderate' if energy_score >= 50 else '🔴 Needs Improvement'}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Professional Metric Cards
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate slab-based bill
        bill_details = calculate_slab_based_bill(prediction['monthly_total'])
        
        with col1:
            st.markdown(f"""
            <div class="smart-card" style="border-top: 3px solid #10b981;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                    <h3 style="color: #10b981; margin: 0; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Live Usage</h3>
                    <span style="font-size: 1.5rem;">⚡</span>
                </div>
                <h2 style="margin: 0; font-size: 2.25rem; font-weight: 700; color: #e2e8f0;">{prediction['daily_total']:.1f}</h2>
                <p style="margin: 0.25rem 0 0 0; color: #94a3b8; font-size: 0.875rem;">kWh per day</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="smart-card" style="border-top: 3px solid #10b981;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                    <h3 style="color: #10b981; margin: 0; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Monthly Bill</h3>
                    <span style="font-size: 1.5rem;">💰</span>
                </div>
                <h2 style="margin: 0; font-size: 2.25rem; font-weight: 700; color: #e2e8f0;">₹{bill_details['total_bill']:.0f}</h2>
                <p style="margin: 0.25rem 0 0 0; color: #94a3b8; font-size: 0.875rem;">{prediction['monthly_total']:.0f} units @ ₹{bill_details['effective_rate']:.2f}/unit</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="smart-card" style="border-top: 3px solid #10b981;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                    <h3 style="color: #10b981; margin: 0; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Carbon Impact</h3>
                    <span style="font-size: 1.5rem;">🌱</span>
                </div>
                <h2 style="margin: 0; font-size: 2.25rem; font-weight: 700; color: #e2e8f0;">{carbon_impact['monthly_co2']:.0f}</h2>
                <p style="margin: 0.25rem 0 0 0; color: #94a3b8; font-size: 0.875rem;">kg CO₂ per month</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            optimization_potential = 25  # Simulated
            st.markdown(f"""
            <div class="smart-card" style="border-top: 3px solid #f59e0b;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                    <h3 style="color: #f59e0b; margin: 0; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Save Potential</h3>
                    <span style="font-size: 1.5rem;">📉</span>
                </div>
                <h2 style="margin: 0; font-size: 2.25rem; font-weight: 700; color: #e2e8f0;">{optimization_potential}%</h2>
                <p style="margin: 0.25rem 0 0 0; color: #94a3b8; font-size: 0.875rem;">optimization available</p>
            </div>
            """, unsafe_allow_html=True)

        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Bill Breakdown Card
        st.markdown("### 💰 Bill Breakdown (Maharashtra Tariff)")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Energy Charges", f"₹{bill_details['energy_charges']:.2f}")
        with col2:
            st.metric("Fixed Charges", f"₹{bill_details['fixed_charges']:.2f}")
        with col3:
            st.metric("Electricity Duty (16%)", f"₹{bill_details['electricity_duty']:.2f}")
        with col4:
            st.metric("Total Bill", f"₹{bill_details['total_bill']:.2f}", delta=None)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Appliance Breakdown
        st.markdown("### 🔌 Appliance Energy Usage")
        
        # Merge custom appliances with database for display
        all_appliances_display = {**APPLIANCE_DATABASE, **st.session_state.custom_appliances}
        
        for appliance, daily_kwh in prediction['breakdown'].items():
            data = appliance_data[appliance]
            monthly_cost = daily_kwh * 30 * ((rate_peak + rate_offpeak) / 2)
            efficiency = all_appliances_display[appliance]["efficiency_rating"]
            
            st.markdown(f"""
            <div class="appliance-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #e2e8f0;">{all_appliances_display[appliance]['icon']} {appliance}</h4>
                        <p style="margin: 0.25rem 0; color: #94a3b8;">
                            {data['power_watts']}W × {data['hours_per_day']}h/day × {data['quantity']} unit(s)
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <h3 style="margin: 0; color: #3b82f6;">₹{monthly_cost:.0f}</h3>
                        <p style="margin: 0; color: #94a3b8;">/month</p>
                        <div style="margin-top: 0.5rem;">
                            {'⭐' * efficiency}
                        </div>
                    </div>
                </div>
                <div class="progress-bar" style="margin-top: 1rem;">
                    <div class="progress-fill" style="width: {(daily_kwh / prediction['daily_total'] * 100):.0f}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Energy Waste Detection
        if waste_detection:
            st.markdown("### ⚠️ Energy Waste Detection")
            st.info(f"Found {len(waste_detection)} potential energy waste issues")
            
            for waste in waste_detection:
                severity_color = "#ef4444" if waste['severity'] == "high" else "#f59e0b"
                st.markdown(f"""
                <div class="appliance-card" style="border-left: 4px solid {severity_color};">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0; color: {severity_color};">⚠️ {waste['appliance']}</h4>
                            <p style="margin: 0.5rem 0; color: #e2e8f0; font-size: 1.05rem;">
                                <strong>Issue:</strong> {waste['issue']}
                            </p>
                            <p style="margin: 0.5rem 0; color: #94a3b8;">
                                <strong>Recommendation:</strong> {waste['recommendation']}
                            </p>
                        </div>
                        <div style="text-align: right; min-width: 120px;">
                            <h3 style="margin: 0; color: #10b981;">₹{waste['potential_savings']:.0f}</h3>
                            <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">potential savings/year</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    elif st.session_state.current_tab == "insights":
        st.markdown("### 📊 Advanced Analytics Intelligence")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Comparison Mode
            st.markdown("#### 📈 Smart Comparison")
            comparison_mode = st.selectbox(
                "Select comparison:",
                ["This Month vs Last Month", "Household vs Average", "Projected vs Actual"]
            )
            
            if comparison_mode == "This Month vs Last Month":
                last_month = prediction['monthly_total'] * 1.08  # Simulated
                fig = go.Figure(data=[
                    go.Bar(x=['Last Month', 'This Month'], 
                           y=[last_month, prediction['monthly_total']],
                           marker_color=['#94a3b8', '#3b82f6'])
                ])
                fig.update_layout(
                    title='Monthly Comparison',
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11)
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap View
        st.markdown("#### 🔥 Time-Based Usage Heatmap")
        
        # Simulated hourly data
        hours = list(range(24))
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        heatmap_data = np.random.rand(7, 24) * prediction['daily_total'] / 24
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=hours,
            y=days,
            colorscale='Blues',
            text=heatmap_data,
            texttemplate='%{text:.1f}',
            textfont={"size": 10}
        ))
        fig.update_layout(
            title='Peak Usage Zones (kWh)',
            xaxis_title='Hour of Day',
            yaxis_title='Day of Week',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(16,30,50,0.4)',
            font=dict(color='#94a3b8', size=11)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.current_tab == "appliances":
        st.markdown("### 🔌 Smart Appliance Manager")
        
        # Merge custom appliances with database for display
        all_appliances_display = {**APPLIANCE_DATABASE, **st.session_state.custom_appliances}
        
        # Visual Appliance Cards
        for appliance in selected_appliances:
            data = appliance_data[appliance]
            daily_kwh = prediction['breakdown'][appliance]
            monthly_cost = daily_kwh * 30 * ((rate_peak + rate_offpeak) / 2)
            efficiency = all_appliances_display[appliance]["efficiency_rating"]
            
            with st.expander(f"{all_appliances_display[appliance]['icon']} {appliance} - ₹{monthly_cost:.0f}/month", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Current Configuration:**
                    - Power: {data['power_watts']}W
                    - Usage: {data['hours_per_day']}h/day
                    - Quantity: {data['quantity']}
                    - Daily Cost: ₹{daily_kwh * ((rate_peak + rate_offpeak) / 2):.2f}
                    - Efficiency: {'⭐' * efficiency}
                    """)
                
                with col2:
                    # Efficiency indicator
                    if efficiency >= 4:
                        st.success("✅ Efficient appliance")
                    elif efficiency >= 3:
                        st.warning("⚠️ Moderate efficiency")
                    else:
                        st.error("🔴 Low efficiency - Consider upgrade")
                
                # Smart Product Recommendations - Works for all appliances
                st.markdown("**🛒 Recommended Upgrades:**")
                
                # Get recommendations using smart function
                category = all_appliances_display[appliance]["category"]
                rate_avg = (rate_peak + rate_offpeak) / 2
                recommendations = get_smart_recommendations(
                    appliance, 
                    data['power_watts'], 
                    category, 
                    data['hours_per_day'], 
                    rate_avg
                )
                
                if recommendations:
                    for product in recommendations[:2]:
                        power_saving = data['power_watts'] - product['power']
                        monthly_saving = (power_saving * data['hours_per_day'] * 30 / 1000) * rate_avg
                        
                        st.markdown(f"""
                        <div style="background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #10b981;">
                            <strong>{product['brand']} {product['model']}</strong> - ⭐ {product['star']} Star<br>
                            💡 {product['power']}W (saves {power_saving}W) | 💰 ₹{product['price']:,}<br>
                            📉 Energy Savings: {product['savings']} | 💵 Monthly Savings: ₹{monthly_saving:.0f}<br>
                            ⏱️ Payback Period: {product['payback']}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Show energy saving tips for the category
                    if category in GENERIC_RECOMMENDATIONS:
                        with st.expander("💡 Energy Saving Tips"):
                            for tip in GENERIC_RECOMMENDATIONS[category]["tips"]:
                                st.markdown(f"• {tip}")
                else:
                    st.info("💡 Consider upgrading to a 5-star rated model for better efficiency")
        
        # AI Optimization Button
        if st.button("⚡ Optimize My Home", use_container_width=True):
            optimization = optimize_usage_schedule(appliance_data, rate_peak, rate_offpeak)
            
            st.markdown("### 💡 AI Optimization Results")
            if optimization['suggestions']:
                for suggestion in optimization['suggestions']:
                    st.markdown(f"""
                    <div class="smart-card">
                        <h4 style="color: #10b981;">{suggestion['appliance']}</h4>
                        <p>{suggestion['recommendation']}</p>
                        <p><strong>💰 Save ₹{suggestion['monthly_savings']:.0f}/month</strong></p>
                    </div>
                    """, unsafe_allow_html=True)

    
    elif st.session_state.current_tab == "simulation":
        st.markdown("### 🧪 What-If Simulation Lab")
        st.info("🔬 Adjust parameters below to see real-time impact on your energy consumption and costs")
        
        # Simulation Controls
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⚙️ Simulation Controls")
            
            # AC usage reduction
            ac_reduction = st.slider("Reduce AC usage by (hours):", 0.0, 5.0, 0.0, 0.5)
            
            # Fan upgrade
            fan_upgrade = st.checkbox("Upgrade to 5-star fan")
            
            # Washing frequency
            washing_reduction = st.slider("Reduce washing frequency by (%):", 0, 50, 0, 5)
            
            # Lighting efficiency
            led_upgrade = st.checkbox("Switch all lights to LED")
        
        with col2:
            st.markdown("#### 📊 Simulation Results")
            
            # Calculate simulated values
            simulated_daily = prediction['daily_total']
            current_bill = calculate_slab_based_bill(prediction['monthly_total'])
            
            # Apply reductions
            # Find any Air Conditioner variant
            ac_appliances = [app for app in appliance_data.keys() if "Air Conditioner" in app]
            if ac_appliances and ac_reduction > 0:
                for ac_app in ac_appliances:
                    ac_saving = (appliance_data[ac_app]['power_watts'] * ac_reduction / 1000)
                    simulated_daily -= ac_saving
            
            # Find any Fan variant
            fan_appliances = [app for app in appliance_data.keys() if "Fan" in app]
            if fan_upgrade and fan_appliances:
                for fan_app in fan_appliances:
                    fan_saving = appliance_data[fan_app]['power_watts'] * 0.6 * appliance_data[fan_app]['hours_per_day'] / 1000
                    simulated_daily -= fan_saving
            
            # Find any Washing Machine variant
            washing_appliances = [app for app in appliance_data.keys() if "Washing Machine" in app]
            if washing_appliances and washing_reduction > 0:
                for wash_app in washing_appliances:
                    washing_saving = prediction['breakdown'].get(wash_app, 0) * (washing_reduction / 100)
                    simulated_daily -= washing_saving
            
            # Find any LED/Light variant
            light_appliances = [app for app in appliance_data.keys() if "LED" in app or "Light" in app or "Bulb" in app or "Tube" in app]
            if led_upgrade and light_appliances:
                for light_app in light_appliances:
                    led_saving = appliance_data[light_app]['power_watts'] * 0.85 * appliance_data[light_app]['hours_per_day'] / 1000
                    simulated_daily -= led_saving
            
            simulated_monthly = simulated_daily * 30
            simulated_bill = calculate_slab_based_bill(simulated_monthly)
            
            savings = current_bill['total_bill'] - simulated_bill['total_bill']
            carbon_saved = (prediction['daily_total'] - simulated_daily) * 30 * 0.82
            
            # Display results
            st.markdown(f"""
            <div class="metric-glow">
                <h3 style="color: #3b82f6; margin: 0;">New Predicted Bill</h3>
                <h2 style="margin: 0.5rem 0; font-size: 2.5rem;">₹{simulated_bill['total_bill']:.0f}</h2>
                <p style="color: #10b981; margin: 0;">💰 Save ₹{savings:.0f}/month ({simulated_monthly:.0f} units)</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="impact-badge">
                🌱 Carbon Reduction: {carbon_saved:.1f} kg CO₂/month
            </div>
            """, unsafe_allow_html=True)
        
        # Live Graph
        st.markdown("#### 📈 Live Impact Visualization")
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Current',
            x=['Daily kWh', 'Monthly Cost', 'Carbon (kg)'],
            y=[prediction['daily_total'], current_bill['total_bill'], carbon_impact['monthly_co2']],
            marker_color='#94a3b8'
        ))
        fig.add_trace(go.Bar(
            name='After Optimization',
            x=['Daily kWh', 'Monthly Cost', 'Carbon (kg)'],
            y=[simulated_daily, simulated_bill['total_bill'], carbon_impact['monthly_co2'] - carbon_saved],
            marker_color='#10b981'
        ))
        fig.update_layout(
            barmode='group',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(16,30,50,0.4)',
            font=dict(color='#94a3b8', size=11)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.current_tab == "impact":
        st.markdown("### 🌍 Sustainability Impact Dashboard")
        
        # Environmental metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="smart-card" style="text-align: center;">
                <h2 style="color: #10b981; font-size: 3rem; margin: 0;">{carbon_impact['yearly_co2']:.0f}</h2>
                <p style="color: #94a3b8; margin: 0.5rem 0;">kg CO₂/year</p>
                <h4 style="color: #e2e8f0; margin-top: 1rem;">Total Carbon Footprint</h4>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="smart-card" style="text-align: center;">
                <h2 style="color: #10b981; font-size: 3rem; margin: 0;">{carbon_impact['trees_equivalent']:.0f}</h2>
                <p style="color: #94a3b8; margin: 0.5rem 0;">trees 🌳</p>
                <h4 style="color: #e2e8f0; margin-top: 1rem;">Equivalent Trees Needed</h4>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="smart-card" style="text-align: center;">
                <h2 style="color: #10b981; font-size: 3rem; margin: 0;">{carbon_impact['km_equivalent']:.0f}</h2>
                <p style="color: #94a3b8; margin: 0.5rem 0;">km 🚗</p>
                <h4 style="color: #e2e8f0; margin-top: 1rem;">Equivalent km Not Driven</h4>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Impact visualization
        st.markdown("#### 📊 Environmental Impact Over Time")
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        co2_data = [carbon_impact['monthly_co2'] * (1 + np.random.uniform(-0.1, 0.1)) for _ in range(12)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=co2_data,
            mode='lines+markers',
            name='CO₂ Emissions',
            line=dict(color='#ef4444', width=3),
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.2)'
        ))
        fig.update_layout(
            title='Monthly Carbon Emissions Trend',
            xaxis_title='Month',
            yaxis_title='CO₂ (kg)',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(16,30,50,0.4)',
            font=dict(color='#94a3b8', size=11)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Sustainability tips
        st.markdown("#### 💡 Sustainability Tips")
        
        tips = [
            "🌱 Plant trees to offset your carbon footprint",
            "☀️ Consider installing solar panels for renewable energy",
            "♻️ Recycle and reduce waste to minimize environmental impact",
            "🚴 Use public transport or cycle to reduce carbon emissions",
            "💧 Conserve water to save energy used in water treatment"
        ]
        
        for tip in tips:
            st.markdown(f"""
            <div class="smart-card">
                <p style="margin: 0; font-size: 1.1rem;">{tip}</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif st.session_state.current_tab == "solar":
        st.markdown("### ☀️ Solar Panel Investment Calculator")
        
        # Initialize solar calculator
        solar_calc = SolarROICalculator()
        
        # Create two columns for input and results
        col_input, col_results = st.columns([1, 1])
        
        with col_input:
            st.markdown("#### 📋 Enter Your Details")
            
            with st.form("solar_calculator_form"):
                # Basic inputs
                monthly_bill = st.number_input(
                    "💰 Monthly Electricity Bill (₹)",
                    min_value=0,
                    value=3000,
                    step=100,
                    help="Your average monthly electricity bill"
                )
                
                monthly_units = st.number_input(
                    "⚡ Average Units Consumed per Month (kWh)",
                    min_value=0,
                    value=300,
                    step=10,
                    help="Check your electricity bill for units consumed"
                )
                
                cost_per_unit = st.number_input(
                    "💵 Cost per Unit (₹/kWh)",
                    min_value=0.0,
                    value=10.0,
                    step=0.5,
                    help="Average cost per unit from your bill"
                )
                
                rooftop_area = st.number_input(
                    "🏠 Available Rooftop Area (sq ft)",
                    min_value=0,
                    value=500,
                    step=50,
                    help="Approximate rooftop space available for panels"
                )
                
                st.markdown("---")
                st.markdown("#### ⚙️ System Configuration")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    cost_per_kw = st.number_input(
                        "💰 Solar Panel Cost per kW (₹)",
                        min_value=0,
                        value=55000,
                        step=1000,
                        help="Average cost: ₹50,000-₹60,000 per kW"
                    )
                    
                    sunlight_hours = st.slider(
                        "☀️ Avg Sunlight Hours/Day",
                        min_value=3.0,
                        max_value=8.0,
                        value=5.0,
                        step=0.5,
                        help="Average productive sunlight hours"
                    )
                
                with col2:
                    subsidy_percent = st.number_input(
                        "🎁 Government Subsidy (%)",
                        min_value=0,
                        max_value=100,
                        value=30,
                        step=5,
                        help="Central/State government subsidy"
                    )
                    
                    maintenance_yearly = st.number_input(
                        "🔧 Maintenance Cost/Year (₹)",
                        min_value=0,
                        value=5000,
                        step=500,
                        help="Annual maintenance and cleaning"
                    )
                
                st.markdown("---")
                
                # Advanced options
                tariff_increase = st.checkbox("📈 Consider Increasing Electricity Tariff (5% yearly)")
                
                col1, col2 = st.columns(2)
                with col1:
                    calculate_btn = st.form_submit_button("🔍 Calculate ROI", use_container_width=True)
                with col2:
                    reset_btn = st.form_submit_button("🔄 Reset", use_container_width=True)
                
                if calculate_btn:
                    # Perform calculations
                    with st.spinner("⚡ Calculating solar ROI..."):
                        # System size
                        system_size = solar_calc.calculate_system_size(monthly_units, sunlight_hours)
                        
                        # Installation cost
                        cost_data = solar_calc.calculate_installation_cost(
                            system_size, cost_per_kw, subsidy_percent
                        )
                        
                        # Monthly generation
                        monthly_solar_units = solar_calc.calculate_monthly_generation(
                            system_size, sunlight_hours
                        )
                        
                        # Savings
                        savings_data = solar_calc.calculate_savings(
                            monthly_solar_units, cost_per_unit, maintenance_yearly
                        )
                        
                        # Payback period
                        payback_period = solar_calc.calculate_payback_period(
                            cost_data['final_cost'], savings_data['yearly_savings']
                        )
                        
                        # ROI calculation
                        tariff_inc = 5 if tariff_increase else 0
                        roi_data = solar_calc.calculate_roi(
                            cost_data['final_cost'],
                            savings_data['yearly_savings'],
                            years=25,
                            tariff_increase=tariff_inc
                        )
                        
                        # Carbon reduction
                        carbon_data = solar_calc.calculate_carbon_reduction(
                            monthly_solar_units, years=25
                        )
                        
                        # Recommendation
                        recommendation = solar_calc.get_recommendation(payback_period)
                        
                        # Optimal system suggestion
                        optimal_system = solar_calc.suggest_optimal_system(
                            monthly_units, rooftop_area, sunlight_hours
                        )
                        
                        # Battery suggestion
                        battery_data = solar_calc.suggest_battery(system_size)
                        
                        # Store in session state
                        st.session_state.solar_results = {
                            'system_size': system_size,
                            'cost_data': cost_data,
                            'monthly_solar_units': monthly_solar_units,
                            'savings_data': savings_data,
                            'payback_period': payback_period,
                            'roi_data': roi_data,
                            'carbon_data': carbon_data,
                            'recommendation': recommendation,
                            'optimal_system': optimal_system,
                            'battery_data': battery_data,
                            'tariff_increase': tariff_inc,
                            'monthly_bill': monthly_bill
                        }
                        
                        st.success("✅ Calculation complete!")
                        st.rerun()
        
        # Results column
        with col_results:
            if 'solar_results' in st.session_state:
                results = st.session_state.solar_results
                
                st.markdown("#### 📊 Investment Analysis")
                
                # Recommendation banner
                rec = results['recommendation']
                st.markdown(f"""
                <div style="background: {rec['color']}; padding: 1.5rem; border-radius: 16px; 
                            color: white; text-align: center; margin-bottom: 1.5rem;">
                    <h3 style="margin: 0; font-size: 1.5rem;">{rec['rating']}</h3>
                    <p style="margin: 0.5rem 0 0 0;">{rec['message']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Key metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "System Size",
                        f"{results['system_size']} kW",
                        help="Required solar panel capacity"
                    )
                
                with col2:
                    st.metric(
                        "Payback Period",
                        f"{results['payback_period']:.1f} years",
                        help="Time to recover investment"
                    )
                
                with col3:
                    st.metric(
                        "ROI (25 years)",
                        f"{results['roi_data']['roi_percent']:.1f}%",
                        help="Return on investment"
                    )
                
                st.markdown("---")
                
                # Financial breakdown
                st.markdown("#### 💰 Financial Breakdown")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Installation Costs:**
                    - Total Cost: ₹{results['cost_data']['total_cost']:,.0f}
                    - Subsidy: -₹{results['cost_data']['subsidy_amount']:,.0f}
                    - **Final Investment: ₹{results['cost_data']['final_cost']:,.0f}**
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Savings:**
                    - Monthly: ₹{results['savings_data']['monthly_savings']:,.0f}
                    - Yearly: ₹{results['savings_data']['yearly_savings']:,.0f}
                    - **25-Year Profit: ₹{results['roi_data']['net_profit']:,.0f}**
                    """)
                
                st.markdown("---")
                
                # Environmental impact
                st.markdown("#### 🌱 Environmental Impact")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "CO₂ Reduced (25 years)",
                        f"{results['carbon_data']['total_co2_reduced']:,.0f} kg"
                    )
                
                with col2:
                    st.metric(
                        "Trees Equivalent",
                        f"{results['carbon_data']['trees_equivalent']:.0f} trees"
                    )
                
                with col3:
                    st.metric(
                        "Yearly CO₂ Saved",
                        f"{results['carbon_data']['yearly_co2_reduced']:,.0f} kg"
                    )
            
            else:
                st.info("👈 Fill in the form and click 'Calculate ROI' to see results")
        
        # Visualizations (full width)
        if 'solar_results' in st.session_state:
            results = st.session_state.solar_results
            
            st.markdown("---")
            st.markdown("### 📈 Investment Visualization")
            
            # Generate data for graphs
            years_list, net_cumulative, gross_cumulative = solar_calc.generate_cumulative_savings_data(
                results['cost_data']['final_cost'],
                results['savings_data']['yearly_savings'],
                years=25,
                tariff_increase=results['tariff_increase']
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Cumulative savings graph
                fig1 = go.Figure()
                
                # Add break-even line
                fig1.add_hline(y=0, line_dash="dash", line_color="white", 
                              annotation_text="Break-even Point")
                
                # Add cumulative savings line
                fig1.add_trace(go.Scatter(
                    x=years_list,
                    y=net_cumulative,
                    mode='lines+markers',
                    name='Net Savings',
                    line=dict(color='#10b981', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(16, 185, 129, 0.2)'
                ))
                
                fig1.update_layout(
                    title='Cumulative Savings Over 25 Years',
                    xaxis_title='Years',
                    yaxis_title='Net Savings (₹)',
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11),
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Cost comparison bar chart
                without_solar = solar_calc.calculate_without_solar_cost(
                    results['monthly_bill'], years=25, tariff_increase=results['tariff_increase']
                )
                with_solar = solar_calc.calculate_with_solar_cost(
                    results['cost_data']['final_cost'],
                    results['savings_data']['yearly_savings'] * 0.1,  # Approximate maintenance
                    years=25
                )
                
                fig2 = go.Figure(data=[
                    go.Bar(
                        name='Without Solar',
                        x=['25-Year Cost'],
                        y=[without_solar],
                        marker_color='#ef4444',
                        text=[f"₹{without_solar:,.0f}"],
                        textposition='auto'
                    ),
                    go.Bar(
                        name='With Solar',
                        x=['25-Year Cost'],
                        y=[with_solar],
                        marker_color='#10b981',
                        text=[f"₹{with_solar:,.0f}"],
                        textposition='auto'
                    )
                ])
                
                fig2.update_layout(
                    title='Cost Comparison: With vs Without Solar',
                    yaxis_title='Total Cost (₹)',
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11),
                    showlegend=True
                )
                
                st.plotly_chart(fig2, use_container_width=True)
            
            # Additional recommendations
            st.markdown("---")
            st.markdown("### 💡 Smart Recommendations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔋 Battery Backup (Optional)")
                st.markdown(f"""
                <div class="smart-card">
                    <p><strong>Recommended Capacity:</strong> {results['battery_data']['recommended_capacity']} kWh</p>
                    <p><strong>Estimated Cost:</strong> ₹{results['battery_data']['estimated_cost']:,.0f}</p>
                    <p><strong>Backup Duration:</strong> {results['battery_data']['backup_hours']} hours</p>
                    <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;">
                        Battery provides backup during power cuts and stores excess solar energy
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### 📐 System Optimization")
                opt = results['optimal_system']
                st.markdown(f"""
                <div class="smart-card">
                    <p><strong>Optimal System Size:</strong> {opt['optimal_size']} kW</p>
                    <p><strong>Based on Consumption:</strong> {opt['consumption_based']} kW</p>
                    <p><strong>Based on Space:</strong> {opt['space_based']} kW</p>
                    <p style="color: {'#10b981' if opt['space_sufficient'] else '#f59e0b'}; margin-top: 0.5rem;">
                        {'✅ Sufficient rooftop space available' if opt['space_sufficient'] else '⚠️ Limited rooftop space - consider smaller system'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    elif st.session_state.current_tab == "goals":
        st.markdown("### 🎯 Goal-Based Energy Tracker")
        st.info("💡 Set consumption targets and track your progress with smart alerts")
        
        # Goal creation form
        with st.expander("➕ Create New Goal", expanded=False):
            with st.form("create_goal_form"):
                st.markdown("#### Set Your Energy Goal")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    goal_type = st.selectbox(
                        "Goal Type",
                        ["daily", "monthly", "bill", "carbon"],
                        format_func=lambda x: st.session_state.goal_tracker.goal_types[x]
                    )
                    
                    goal_name = st.text_input("Goal Name", placeholder="e.g., Reduce AC usage")
                
                with col2:
                    target_value = st.number_input(
                        "Target Value",
                        min_value=0.0,
                        value=100.0,
                        step=10.0,
                        help="Set your target (kWh for consumption, ₹ for bill, kg for carbon)"
                    )
                    
                    current_value = st.number_input(
                        "Current Value",
                        min_value=0.0,
                        value=0.0,
                        step=1.0,
                        help="Your current consumption/bill/carbon"
                    )
                
                submit_goal = st.form_submit_button("✅ Create Goal", use_container_width=True)
                
                if submit_goal and goal_name:
                    new_goal = {
                        'id': len(st.session_state.energy_goals) + 1,
                        'name': goal_name,
                        'type': goal_type,
                        'target': target_value,
                        'current': current_value,
                        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.energy_goals.append(new_goal)
                    st.success(f"✅ Goal '{goal_name}' created successfully!")
                    st.rerun()
        
        st.markdown("---")
        
        # Display existing goals
        if st.session_state.energy_goals:
            st.markdown("### 📋 Your Active Goals")
            
            # Overall performance summary
            goals_summary = st.session_state.goal_tracker.generate_goal_summary(st.session_state.energy_goals)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Goals", goals_summary['total_goals'])
            with col2:
                st.metric("On Track", goals_summary['achieved'], delta="Good")
            with col3:
                st.metric("In Progress", goals_summary['in_progress'])
            with col4:
                st.metric("Overall Score", f"{goals_summary['overall_performance']:.0f}%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Individual goal cards
            for goal in st.session_state.energy_goals:
                progress = st.session_state.goal_tracker.calculate_progress(goal['current'], goal['target'])
                status = st.session_state.goal_tracker.get_status(goal['current'], goal['target'])
                remaining = st.session_state.goal_tracker.calculate_remaining(goal['current'], goal['target'])
                recommendations = st.session_state.goal_tracker.get_recommendations(goal['current'], goal['target'], goal['type'])
                
                with st.expander(f"{status['icon']} {goal['name']} - {progress:.1f}%", expanded=True):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Progress bar
                        st.markdown(f"""
                        <div class="progress-bar" style="height: 20px; margin-bottom: 1rem;">
                            <div class="progress-fill" style="width: {min(progress, 100):.0f}%; background: {status['color']};"></div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        **Status:** {status['status']}  
                        **Current:** {goal['current']:.1f} / **Target:** {goal['target']:.1f}  
                        **Remaining:** {remaining:.1f}  
                        **Type:** {st.session_state.goal_tracker.goal_types[goal['type']]}
                        """)
                        
                        st.markdown(f"_{status['message']}_")
                    
                    with col2:
                        # Alert message
                        alert_msg = st.session_state.goal_tracker.get_alert_message(progress, goal['type'])
                        
                        if progress > 100:
                            st.error(alert_msg)
                        elif progress > 90:
                            st.warning(alert_msg)
                        elif progress > 70:
                            st.info(alert_msg)
                        else:
                            st.success(alert_msg)
                        
                        # Delete button
                        if st.button(f"🗑️ Delete", key=f"delete_goal_{goal['id']}"):
                            st.session_state.energy_goals = [g for g in st.session_state.energy_goals if g['id'] != goal['id']]
                            st.rerun()
                    
                    # Recommendations
                    st.markdown("**💡 Recommendations:**")
                    for rec in recommendations[:3]:
                        st.markdown(f"• {rec}")
                    
                    # Update current value
                    with st.form(f"update_goal_{goal['id']}"):
                        new_current = st.number_input(
                            "Update Current Value",
                            min_value=0.0,
                            value=goal['current'],
                            step=1.0,
                            key=f"update_input_{goal['id']}"
                        )
                        
                        if st.form_submit_button("🔄 Update Progress"):
                            for g in st.session_state.energy_goals:
                                if g['id'] == goal['id']:
                                    g['current'] = new_current
                            st.success("✅ Progress updated!")
                            st.rerun()
            
            # Visualization
            st.markdown("---")
            st.markdown("### 📊 Goals Overview")
            
            # Create progress chart
            goal_names = [g['name'] for g in st.session_state.energy_goals]
            goal_progress = [st.session_state.goal_tracker.calculate_progress(g['current'], g['target']) for g in st.session_state.energy_goals]
            goal_colors = [st.session_state.goal_tracker.get_status(g['current'], g['target'])['color'] for g in st.session_state.energy_goals]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=goal_names,
                    y=goal_progress,
                    marker_color=goal_colors,
                    text=[f"{p:.1f}%" for p in goal_progress],
                    textposition='auto'
                )
            ])
            
            fig.add_hline(y=100, line_dash="dash", line_color="white", annotation_text="Target")
            
            fig.update_layout(
                title='Goal Progress Overview',
                xaxis_title='Goals',
                yaxis_title='Progress (%)',
                height=380,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(16,30,50,0.4)',
                font=dict(color='#94a3b8', size=11)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("📝 No goals set yet. Create your first goal above to start tracking!")
    
    elif st.session_state.current_tab == "analytics":
        st.markdown("### 📈 Advanced Analytics Dashboard")
        st.info("🔍 Deep dive into your energy consumption patterns with advanced data analysis")
        
        if not st.session_state.appliance_data:
            st.warning("⚠️ Please configure appliances and analyze to view analytics")
        else:
            # Merge custom appliances with database for display
            all_appliances_display = {**APPLIANCE_DATABASE, **st.session_state.custom_appliances}
            
            # Data preparation
            appliance_names = list(prediction['breakdown'].keys())
            daily_consumption = list(prediction['breakdown'].values())
            monthly_consumption = [d * 30 for d in daily_consumption]
            
            # Calculate costs
            rate_avg = (rate_peak + rate_offpeak) / 2
            monthly_costs = [d * 30 * rate_avg for d in daily_consumption]
            
            # Statistical Analysis
            st.markdown("### 📊 Statistical Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Mean Daily Usage", f"{np.mean(daily_consumption):.2f} kWh")
            with col2:
                st.metric("Median Daily Usage", f"{np.median(daily_consumption):.2f} kWh")
            with col3:
                st.metric("Peak Appliance", f"{max(daily_consumption):.2f} kWh")
            with col4:
                st.metric("Std Deviation", f"{np.std(daily_consumption):.2f} kWh")
            
            st.markdown("---")
            
            # Quick Tips Section
            st.markdown("### 💡 Quick Energy-Saving Tips")
            
            # Generate personalized tips based on data
            tips = []
            
            # Find highest consumer
            max_consumer_idx = np.argmax(daily_consumption)
            max_consumer = appliance_names[max_consumer_idx]
            max_consumption = daily_consumption[max_consumer_idx]
            
            tips.append(f"🔴 **High Usage Alert:** {max_consumer} uses {max_consumption:.1f} kWh/day. Consider reducing usage by 1-2 hours to save ₹{max_consumption * 30 * rate_avg * 0.2:.0f}/month.")
            
            # Check for AC usage
            ac_appliances = [app for app in appliance_names if 'Air Conditioner' in app or 'AC' in app]
            if ac_appliances:
                tips.append("❄️ **AC Tip:** Set temperature to 24-25°C instead of 18-20°C. Each degree higher saves 3-5% energy!")
            
            # Check for water heater
            heater_appliances = [app for app in appliance_names if 'Heater' in app or 'Geyser' in app]
            if heater_appliances:
                tips.append("🚿 **Water Heater Tip:** Use a timer to heat water only when needed. Can save up to 30% energy!")
            
            # Check for refrigerator
            fridge_appliances = [app for app in appliance_names if 'Refrigerator' in app or 'Fridge' in app]
            if fridge_appliances:
                tips.append("🧊 **Fridge Tip:** Keep fridge at 3-4°C and freezer at -18°C. Defrost regularly to maintain efficiency.")
            
            # General tips
            tips.append("💡 **LED Tip:** Replace all old bulbs with LED. They use 75% less energy and last 25x longer!")
            tips.append("🌙 **Off-Peak Tip:** Run washing machine, dishwasher during off-peak hours (10 PM - 6 AM) to save on electricity rates.")
            tips.append("🔌 **Standby Tip:** Unplug devices when not in use. Standby mode still consumes 5-10% energy!")
            
            # Display tips in cards
            col1, col2, col3 = st.columns(3)
            
            for i, tip in enumerate(tips[:6]):  # Show max 6 tips
                with [col1, col2, col3][i % 3]:
                    st.markdown(f"""
                    <div class="smart-card" style="min-height: 150px; display: flex; align-items: center;">
                        <p style="margin: 0; color: #e2e8f0; font-size: 0.95rem; line-height: 1.6;">
                            {tip}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Visualization Grid
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                # Bar Chart - Appliance-wise consumption
                st.markdown("#### 📊 Appliance-wise Energy Consumption")
                
                colors = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899', '#84cc16']
                bar_colors = [colors[i % len(colors)] for i in range(len(appliance_names))]
                
                fig1 = go.Figure(data=[
                    go.Bar(
                        x=appliance_names,
                        y=monthly_consumption,
                        marker=dict(
                            color=bar_colors,
                            line=dict(color='rgba(255,255,255,0.1)', width=1)
                        ),
                        text=[f"{c:.1f}" for c in monthly_consumption],
                        textposition='outside',
                        textfont=dict(size=11, color='#e2e8f0')
                    )
                ])
                
                fig1.update_layout(
                    xaxis_title='',
                    yaxis_title='kWh/month',
                    height=380,
                    margin=dict(l=40, r=20, t=20, b=60),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11),
                    xaxis=dict(tickangle=-30, tickfont=dict(size=10)),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                    bargap=0.3
                )
                
                st.plotly_chart(fig1, use_container_width=True)
                
                # Text explanation
                st.info("""
                **📖 How to Read:**
                - Each bar represents one appliance
                - Taller bars = higher monthly consumption
                - Compare bars to identify your biggest energy users
                - Focus on reducing usage of the tallest bars
                """)
            
            with col2:
                # Pie Chart - Percentage share
                st.markdown("#### 🥧 Consumption Distribution")
                
                fig2 = go.Figure(data=[
                    go.Pie(
                        labels=appliance_names,
                        values=monthly_consumption,
                        hole=0.5,
                        marker=dict(
                            colors=['#10b981','#3b82f6','#8b5cf6','#f59e0b','#ef4444','#06b6d4','#ec4899','#84cc16'],
                            line=dict(color='#0a0e1a', width=2)
                        ),
                        textinfo='percent',
                        textfont=dict(size=11),
                        hovertemplate='<b>%{label}</b><br>%{value:.1f} kWh<br>%{percent}<extra></extra>'
                    )
                ])
                
                fig2.update_layout(
                    height=380,
                    margin=dict(l=10, r=10, t=20, b=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8', size=11),
                    showlegend=True,
                    legend=dict(font=dict(size=10), bgcolor='rgba(0,0,0,0)')
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
                # Text explanation
                st.info("""
                **📖 How to Read:**
                - Each slice shows percentage of total energy used
                - Larger slices = appliances using more energy
                - Hover over slices to see exact percentages
                - Target the largest slices for savings
                """)
            
            # Second row
            col1, col2 = st.columns(2)
            
            with col1:
                # Line Chart - Monthly trend (simulated)
                st.markdown("#### 📈 Monthly Usage Trend")
                
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                trend_data = [prediction['monthly_total'] * (1 + np.random.uniform(-0.15, 0.15)) for _ in range(12)]
                
                fig3 = go.Figure()
                
                fig3.add_trace(go.Scatter(
                    x=months,
                    y=trend_data,
                    mode='lines+markers',
                    name='Monthly Usage',
                    line=dict(color='#10b981', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(16, 185, 129, 0.2)'
                ))
                
                # Add trend line
                z = np.polyfit(range(12), trend_data, 1)
                p = np.poly1d(z)
                fig3.add_trace(go.Scatter(
                    x=months,
                    y=p(range(12)),
                    mode='lines',
                    name='Trend',
                    line=dict(color='#ef4444', width=2, dash='dash')
                ))
                
                fig3.update_layout(
                    xaxis_title='',
                    yaxis_title='kWh',
                    height=380,
                    margin=dict(l=40, r=20, t=20, b=40),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11),
                    legend=dict(font=dict(size=10), bgcolor='rgba(0,0,0,0)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.03)')
                )
                
                st.plotly_chart(fig3, use_container_width=True)
                
                # Text explanation
                st.info("""
                **📖 How to Read:**
                - Green line shows your monthly usage over the year
                - Red dashed line shows the overall trend
                - Upward trend = increasing consumption
                - Downward trend = decreasing consumption (good!)
                """)
            
            with col2:
                # Histogram - Distribution
                st.markdown("#### 📊 Daily Consumption Distribution")
                
                # Simulate daily data
                daily_data = np.random.normal(prediction['daily_total'], prediction['daily_total'] * 0.15, 30)
                
                fig4 = go.Figure()
                
                # Elegant histogram with gradient-like effect
                fig4.add_trace(go.Histogram(
                    x=daily_data,
                    nbinsx=12,
                    marker=dict(
                        color='#3b82f6',
                        opacity=0.85,
                        line=dict(color='rgba(255,255,255,0.1)', width=1)
                    ),
                    name='Daily Usage'
                ))
                
                # Add mean line
                fig4.add_vline(
                    x=prediction['daily_total'],
                    line_dash='dash',
                    line_color='#10b981',
                    line_width=2,
                    annotation_text=f"Avg: {prediction['daily_total']:.1f}",
                    annotation_font_color='#10b981',
                    annotation_font_size=11
                )
                
                fig4.update_layout(
                    xaxis_title='kWh/day',
                    yaxis_title='Days',
                    height=380,
                    margin=dict(l=40, r=20, t=20, b=40),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11),
                    bargap=0.05,
                    yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                    showlegend=False
                )
                
                st.plotly_chart(fig4, use_container_width=True)
                
                # Text explanation
                st.info("""
                **📖 How to Read:**
                - Shows how often you use certain amounts of energy
                - Taller bars = more days with that usage level
                - Helps identify your typical daily consumption
                - Outliers indicate unusual usage days
                """)
            
            # Data Analysis Insights
            st.markdown("---")
            st.markdown("### 🔍 Data Analysis Insights")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 📉 Outlier Detection")
                
                # Simple outlier detection using IQR
                q1 = np.percentile(daily_consumption, 25)
                q3 = np.percentile(daily_consumption, 75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                outliers = [name for name, val in zip(appliance_names, daily_consumption) if val > upper_bound or val < lower_bound]
                
                if outliers:
                    st.warning(f"⚠️ High consumption detected:")
                    for outlier in outliers:
                        st.markdown(f"• {outlier}")
                else:
                    st.success("✅ No outliers detected")
            
            with col2:
                st.markdown("#### 📊 Consumption Trend")
                
                # Analyze trend
                trend_slope = z[0] if 'z' in locals() else 0
                
                if trend_slope > 0:
                    st.warning(f"📈 Increasing trend: +{abs(trend_slope):.2f} kWh/month")
                    st.markdown("Consider energy-saving measures")
                elif trend_slope < 0:
                    st.success(f"📉 Decreasing trend: -{abs(trend_slope):.2f} kWh/month")
                    st.markdown("Great job on reducing consumption!")
                else:
                    st.info("➡️ Stable consumption pattern")
            
            with col3:
                st.markdown("#### 💰 Savings Analysis")
                
                # Calculate potential savings
                total_monthly_cost = sum(monthly_costs)
                potential_savings = total_monthly_cost * 0.25  # 25% potential
                
                st.markdown(f"""
                **Current Monthly Cost:** ₹{total_monthly_cost:.0f}  
                **Potential Savings:** ₹{potential_savings:.0f}  
                **Yearly Savings:** ₹{potential_savings * 12:.0f}
                """)
                
                st.success("💡 Optimize high-usage appliances")
            
            # NEW ADVANCED VISUALIZATIONS
            st.markdown("---")
            st.markdown("### 📊 Advanced Visualizations")
            
            # Third row - More advanced charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Scatter Plot - Power vs Usage Hours
                st.markdown("#### 🔵 Power vs Usage Pattern")
                
                # Get power and hours data
                power_data = [appliance_data[app]['power_watts'] for app in appliance_names]
                hours_data = [appliance_data[app]['hours_per_day'] for app in appliance_names]
                
                fig5 = go.Figure()
                
                fig5.add_trace(go.Scatter(
                    x=power_data,
                    y=hours_data,
                    mode='markers+text',
                    marker=dict(
                        size=[d * 0.5 for d in daily_consumption],  # Size based on consumption
                        color=daily_consumption,
                        colorscale='Greens',
                        showscale=True,
                        colorbar=dict(title="Daily kWh"),
                        line=dict(width=2, color='white')
                    ),
                    text=[name[:15] for name in appliance_names],  # Truncate long names
                    textposition='top center',
                    textfont=dict(size=9),
                    hovertemplate='<b>%{text}</b><br>Power: %{x}W<br>Hours: %{y}h<br><extra></extra>'
                ))
                
                fig5.update_layout(
                    xaxis_title='Power Rating (Watts)',
                    yaxis_title='Usage Hours per Day',
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11)
                )
                
                st.plotly_chart(fig5, use_container_width=True)
                
                # Text explanation
                st.info("""
                **📖 How to Read:**
                - Each bubble is one appliance
                - X-axis = power rating (watts)
                - Y-axis = hours used per day
                - Bubble size = total daily consumption
                - Larger bubbles in top-right = highest energy users
                """)
            
            with col2:
                # Donut Chart - Cost Distribution
                st.markdown("#### 💰 Cost Distribution by Appliance")
                
                fig6 = go.Figure(data=[
                    go.Pie(
                        labels=appliance_names,
                        values=monthly_costs,
                        hole=0.5,
                        marker=dict(
                            colors=px.colors.sequential.Teal,
                            line=dict(color='white', width=2)
                        ),
                        textinfo='label+percent',
                        textfont=dict(size=10),
                        hovertemplate='<b>%{label}</b><br>Cost: ₹%{value:.0f}<br>%{percent}<extra></extra>'
                    )
                ])
                
                fig6.update_layout(
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8', size=11),
                    showlegend=False,
                    annotations=[dict(
                        text=f'₹{sum(monthly_costs):.0f}<br>Total',
                        x=0.5, y=0.5,
                        font_size=20,
                        showarrow=False
                    )]
                )
                
                st.plotly_chart(fig6, use_container_width=True)
                
                # Text explanation
                st.info("""
                **📖 How to Read:**
                - Donut chart shows cost distribution
                - Each segment = one appliance's monthly cost
                - Larger segments = more expensive to run
                - Center shows total monthly cost
                - Optimize the largest segments to save money
                """)
            
            # Fourth row - More charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Box Plot - Consumption Distribution
                st.markdown("#### 📦 Consumption Distribution (Box Plot)")
                
                fig7 = go.Figure()
                
                fig7.add_trace(go.Box(
                    y=daily_consumption,
                    x=appliance_names,
                    marker_color='#10b981',
                    boxmean='sd',  # Show mean and standard deviation
                    hovertemplate='<b>%{x}</b><br>Value: %{y:.2f} kWh<extra></extra>'
                ))
                
                fig7.update_layout(
                    xaxis_title='Appliances',
                    yaxis_title='Daily Consumption (kWh)',
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11),
                    xaxis_tickangle=-45,
                    showlegend=False
                )
                
                st.plotly_chart(fig7, use_container_width=True)
                
                # Text explanation
                st.info("""
                **📖 How to Read:**
                - Box shows the middle 50% of data
                - Line in box = median (middle value)
                - Whiskers (lines) show the range
                - Dots outside = outliers (unusual values)
                - Helps identify which appliances vary most in usage
                """)
            
            with col2:
                # Waterfall Chart - Cost Breakdown
                st.markdown("#### 💧 Cost Waterfall Analysis")
                
                # Prepare waterfall data
                waterfall_labels = appliance_names + ['Total']
                waterfall_values = monthly_costs + [sum(monthly_costs)]
                waterfall_measures = ['relative'] * len(appliance_names) + ['total']
                
                fig8 = go.Figure(go.Waterfall(
                    x=waterfall_labels,
                    y=waterfall_values,
                    measure=waterfall_measures,
                    text=[f"₹{v:.0f}" for v in waterfall_values],
                    textposition='outside',
                    connector=dict(line=dict(color='rgb(63, 63, 63)')),
                    increasing=dict(marker=dict(color='#10b981')),
                    totals=dict(marker=dict(color='#3b82f6'))
                ))
                
                fig8.update_layout(
                    xaxis_title='Appliances',
                    yaxis_title='Monthly Cost (₹)',
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11),
                    xaxis_tickangle=-45,
                    showlegend=False
                )
                
                st.plotly_chart(fig8, use_container_width=True)
                
                # Text explanation
                st.info("""
                **📖 How to Read:**
                - Shows how each appliance adds to your total bill
                - Green bars = individual appliance costs
                - Blue bar at end = total monthly bill
                - Read left to right to see cost buildup
                - Helps visualize which appliances contribute most
                """)
            
            # Fifth row - NEW Easy-to-Understand Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Simple Area Chart - Daily Usage Pattern
                st.markdown("#### 📅 Daily Usage Pattern (Last 30 Days)")
                
                # Simulate 30 days of data
                days = list(range(1, 31))
                daily_pattern = [prediction['daily_total'] * (1 + np.random.uniform(-0.2, 0.2)) for _ in range(30)]
                
                fig9 = go.Figure()
                
                fig9.add_trace(go.Scatter(
                    x=days,
                    y=daily_pattern,
                    mode='lines',
                    name='Daily Usage',
                    line=dict(color='#10b981', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(16, 185, 129, 0.3)',
                    hovertemplate='Day %{x}<br>Usage: %{y:.1f} kWh<extra></extra>'
                ))
                
                # Add average line
                avg_usage = np.mean(daily_pattern)
                fig9.add_hline(
                    y=avg_usage,
                    line_dash="dash",
                    line_color="#f59e0b",
                    annotation_text=f"Average: {avg_usage:.1f} kWh",
                    annotation_position="right"
                )
                
                fig9.update_layout(
                    xaxis_title='Day of Month',
                    yaxis_title='Energy Usage (kWh)',
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11),
                    showlegend=False
                )
                
                st.plotly_chart(fig9, use_container_width=True)
                
                # Text explanation
                st.info("""
                **📖 How to Read:**
                - Green area shows your daily energy usage
                - Orange dashed line is your average
                - Higher peaks = days with more usage
                - Use this to identify unusual consumption days
                """)
            
            with col2:
                # Top 5 Energy Consumers - Horizontal Bar
                st.markdown("#### 🏆 Top 5 Energy Consumers")
                
                # Get top 5
                top_5_indices = np.argsort(monthly_consumption)[-5:]
                top_5_names = [appliance_names[i] for i in top_5_indices]
                top_5_values = [monthly_consumption[i] for i in top_5_indices]
                top_5_costs = [monthly_costs[i] for i in top_5_indices]
                
                fig10 = go.Figure()
                
                fig10.add_trace(go.Bar(
                    y=top_5_names,
                    x=top_5_values,
                    orientation='h',
                    marker=dict(
                        color=top_5_values,
                        colorscale='Reds',
                        showscale=False
                    ),
                    text=[f"{v:.1f} kWh<br>₹{c:.0f}/mo" for v, c in zip(top_5_values, top_5_costs)],
                    textposition='auto',
                    hovertemplate='<b>%{y}</b><br>Usage: %{x:.1f} kWh<extra></extra>'
                ))
                
                fig10.update_layout(
                    xaxis_title='Monthly Consumption (kWh)',
                    yaxis_title='',
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11),
                    showlegend=False
                )
                
                st.plotly_chart(fig10, use_container_width=True)
                
                # Text explanation
                st.warning("""
                **📖 How to Read:**
                - These are your biggest energy users
                - Longer bars = higher consumption
                - Focus on optimizing these appliances first
                - Upgrading these will save the most money
                """)
            
            # Sixth row - Sunburst and Treemap
            col1, col2 = st.columns(2)
            
            with col1:
                # Sunburst Chart - Hierarchical View
                st.markdown("#### ☀️ Hierarchical Energy View")
                
                # Create hierarchical data by category
                categories = {}
                for app in appliance_names:
                    category = all_appliances_display[app]['category']
                    if category not in categories:
                        categories[category] = []
                    idx = appliance_names.index(app)
                    categories[category].append({
                        'name': app,
                        'value': monthly_consumption[idx]
                    })
                
                # Prepare sunburst data
                labels = ['Total']
                parents = ['']
                values = [sum(monthly_consumption)]
                
                for category, apps in categories.items():
                    labels.append(category)
                    parents.append('Total')
                    values.append(sum([a['value'] for a in apps]))
                    
                    for app in apps:
                        labels.append(app['name'])
                        parents.append(category)
                        values.append(app['value'])
                
                fig11 = go.Figure(go.Sunburst(
                    labels=labels,
                    parents=parents,
                    values=values,
                    branchvalues='total',
                    marker=dict(
                        colorscale='Greens',
                        cmid=np.mean(values)
                    ),
                    hovertemplate='<b>%{label}</b><br>Consumption: %{value:.1f} kWh<br>%{percentParent}<extra></extra>'
                ))
                
                fig11.update_layout(
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8', size=11)
                )
                
                st.plotly_chart(fig11, use_container_width=True)
                
                # Text explanation
                st.info("""
                **📖 How to Read:**
                - Center = total consumption
                - Inner ring = categories (Cooling, Cooking, etc.)
                - Outer ring = individual appliances
                - Click on segments to zoom in
                - Larger segments = higher consumption
                """)
            
            with col2:
                # Treemap - Proportional View
                st.markdown("#### 🗺️ Consumption Treemap")
                
                fig12 = go.Figure(go.Treemap(
                    labels=labels,
                    parents=parents,
                    values=values,
                    textinfo='label+value+percent parent',
                    marker=dict(
                        colorscale='Teal',
                        cmid=np.mean(values),
                        line=dict(width=2, color='white')
                    ),
                    hovertemplate='<b>%{label}</b><br>Consumption: %{value:.1f} kWh<br>%{percentParent}<extra></extra>'
                ))
                
                fig12.update_layout(
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8', size=11)
                )
                
                st.plotly_chart(fig12, use_container_width=True)
                
                # Text explanation
                st.info("""
                **📖 How to Read:**
                - Each box = one appliance or category
                - Box size = energy consumption
                - Larger boxes = higher usage
                - Colors show relative consumption levels
                - Easy way to spot your biggest energy users at a glance
                """)
            
            # Export data option
            st.markdown("---")
            st.markdown("### 💡 Quick Savings Tools")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Weekly Comparison Widget
                st.markdown("#### 📅 This Week vs Last Week")
                
                # Simulate weekly data
                this_week_total = prediction['daily_total'] * 7
                last_week_total = this_week_total * (1 + np.random.uniform(-0.15, 0.15))
                week_change = ((this_week_total - last_week_total) / last_week_total) * 100
                
                # Display comparison
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.metric(
                        "This Week",
                        f"{this_week_total:.1f} kWh",
                        delta=f"{week_change:.1f}%",
                        delta_color="inverse"
                    )
                
                with col_b:
                    st.metric(
                        "Last Week",
                        f"{last_week_total:.1f} kWh"
                    )
                
                # Visual comparison
                fig_week = go.Figure()
                
                fig_week.add_trace(go.Bar(
                    x=['Last Week', 'This Week'],
                    y=[last_week_total, this_week_total],
                    marker_color=['#94a3b8', '#10b981' if week_change < 0 else '#ef4444'],
                    text=[f"{last_week_total:.1f} kWh", f"{this_week_total:.1f} kWh"],
                    textposition='auto'
                ))
                
                fig_week.update_layout(
                    height=380,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(16,30,50,0.4)',
                    font=dict(color='#94a3b8', size=11),
                    showlegend=False,
                    yaxis_title='Energy Usage (kWh)'
                )
                
                st.plotly_chart(fig_week, use_container_width=True)
                
                # Interpretation
                if week_change < 0:
                    st.success(f"✅ Great! You reduced usage by {abs(week_change):.1f}% this week!")
                elif week_change > 10:
                    st.error(f"⚠️ Usage increased by {week_change:.1f}%. Check high-usage appliances.")
                else:
                    st.info(f"📊 Usage changed by {week_change:.1f}%. Keep monitoring.")
            
            with col2:
                # Interactive Savings Calculator
                st.markdown("#### 💰 Savings Calculator")
                st.caption("Calculate potential savings by reducing appliance usage")
                
                # Select appliance to optimize
                optimize_appliance = st.selectbox(
                    "Select appliance to optimize:",
                    appliance_names,
                    key="optimize_select"
                )
                
                if optimize_appliance:
                    current_hours = appliance_data[optimize_appliance]['hours_per_day']
                    current_power = appliance_data[optimize_appliance]['power_watts']
                    
                    # Slider to reduce hours
                    new_hours = st.slider(
                        "Reduce daily usage to (hours):",
                        0.0,
                        current_hours,
                        current_hours * 0.7,  # Default 30% reduction
                        0.5,
                        key="hours_slider"
                    )
                    
                    # Calculate savings
                    hours_saved = current_hours - new_hours
                    daily_kwh_saved = (current_power * hours_saved) / 1000
                    monthly_kwh_saved = daily_kwh_saved * 30
                    monthly_money_saved = monthly_kwh_saved * rate_avg
                    yearly_money_saved = monthly_money_saved * 12
                    
                    # Display results
                    st.markdown("**💡 Potential Savings:**")
                    
                    col_x, col_y = st.columns(2)
                    
                    with col_x:
                        st.metric(
                            "Monthly Savings",
                            f"₹{monthly_money_saved:.0f}",
                            delta=f"{monthly_kwh_saved:.1f} kWh"
                        )
                    
                    with col_y:
                        st.metric(
                            "Yearly Savings",
                            f"₹{yearly_money_saved:.0f}",
                            delta=f"{monthly_kwh_saved * 12:.1f} kWh"
                        )
                    
                    # Progress bar showing reduction
                    reduction_pct = (hours_saved / current_hours) * 100 if current_hours > 0 else 0
                    
                    st.markdown(f"""
                    <div style="margin-top: 1rem;">
                        <p style="color: #94a3b8; margin-bottom: 0.5rem;">Usage Reduction: {reduction_pct:.0f}%</p>
                        <div class="progress-bar" style="height: 12px;">
                            <div class="progress-fill" style="width: {reduction_pct:.0f}%; background: #10b981;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Actionable tip
                    if reduction_pct > 0:
                        st.success(f"💡 Tip: Reduce {optimize_appliance} usage by {hours_saved:.1f} hours/day to save ₹{yearly_money_saved:.0f}/year!")
                    else:
                        st.info("👆 Use the slider above to see potential savings")
            
            # Export data option
            st.markdown("---")
            st.markdown("### 📥 Export Data")
            
            # Create DataFrame
            df = pd.DataFrame({
                'Appliance': appliance_names,
                'Daily kWh': daily_consumption,
                'Monthly kWh': monthly_consumption,
                'Monthly Cost (₹)': monthly_costs
            })
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(df, use_container_width=True)
            
            with col2:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="energy_analytics.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                st.info("💡 Download your data for further analysis in Excel or other tools")

    elif st.session_state.current_tab == "battery":
        st.markdown("### 🔋 Battery & Time-of-Use Optimization")
        
        col1, col2 = st.columns(2)
        with col1:
            battery_cap = st.slider("Battery Capacity (kWh)", 2.0, 20.0, 5.0, 0.5)
        with col2:
            solar_kwh = st.slider("Daily Solar Generation (kWh)", 0.0, 20.0, 0.0, 0.5)
        
        batt = optimize_battery_schedule(prediction['daily_total'], battery_cap, solar_kwh)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div class="smart-card" style="border-top:3px solid #10b981;">
                <h3 style="color:#10b981;margin:0;font-size:0.9rem;text-transform:uppercase;">Daily Savings</h3>
                <h2 style="margin:0.5rem 0;font-size:2.5rem;color:#e2e8f0;">₹{batt['daily_savings']:.1f}</h2>
                <p style="color:#94a3b8;margin:0;">With battery optimization</p>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="smart-card" style="border-top:3px solid #3b82f6;">
                <h3 style="color:#3b82f6;margin:0;font-size:0.9rem;text-transform:uppercase;">Monthly Savings</h3>
                <h2 style="margin:0.5rem 0;font-size:2.5rem;color:#e2e8f0;">₹{batt['monthly_savings']:.0f}</h2>
                <p style="color:#94a3b8;margin:0;">Estimated savings</p>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="smart-card" style="border-top:3px solid #f59e0b;">
                <h3 style="color:#f59e0b;margin:0;font-size:0.9rem;text-transform:uppercase;">Yearly Savings</h3>
                <h2 style="margin:0.5rem 0;font-size:2.5rem;color:#e2e8f0;">₹{batt['yearly_savings']:.0f}</h2>
                <p style="color:#94a3b8;margin:0;">Annual benefit</p>
            </div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### ⏰ 24-Hour Battery Schedule")
        
        hours = [s['hour'] for s in batt['schedule']]
        soc = [s['battery_soc'] for s in batt['schedule']]
        rates = [s['rate'] for s in batt['schedule']]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=soc, name='Battery SoC (kWh)',
                                  fill='tozeroy', fillcolor='rgba(16,185,129,0.2)',
                                  line=dict(color='#10b981', width=2)))
        fig.add_trace(go.Scatter(x=hours, y=rates, name='Rate (₹/kWh)', yaxis='y2',
                                  line=dict(color='#ef4444', width=2, dash='dash')))
        fig.update_layout(
            height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(16,30,50,0.4)',
            font=dict(color='#94a3b8', size=11), margin=dict(l=40,r=40,t=20,b=40),
            xaxis=dict(title='Hour of Day', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='SoC (kWh)', gridcolor='rgba(255,255,255,0.05)'),
            yaxis2=dict(title='Rate (₹)', overlaying='y', side='right'),
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig, use_container_width=True)

    elif st.session_state.current_tab == "nilm":
        st.markdown("### 🔍 Virtual Smart Meter (NILM)")
        st.info("Non-Intrusive Load Monitoring — detects which appliances are running from total power draw")
        
        total_watts = st.slider("Total Current Power Draw (Watts)", 100, 5000, 
                                 int(sum(d['power_watts'] for d in appliance_data.values())), 50)
        
        result = nilm_detect(total_watts)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class="smart-card" style="border-top:3px solid #10b981;">
                <h3 style="color:#10b981;margin:0;">Total Input</h3>
                <h2 style="margin:0.5rem 0;color:#e2e8f0;">{result['total_input']}W</h2>
                <p style="color:#94a3b8;margin:0;">Accounted: {result['accounted_watts']}W | 
                Unaccounted: {result['unaccounted_watts']}W</p>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="smart-card" style="border-top:3px solid #3b82f6;">
                <h3 style="color:#3b82f6;margin:0;">Detected Appliances</h3>
                <h2 style="margin:0.5rem 0;color:#e2e8f0;">{len(result['detected'])}</h2>
                <p style="color:#94a3b8;margin:0;">Running right now</p>
            </div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🔌 Detected Running Appliances")
        
        for item in result['detected']:
            conf_color = "#10b981" if item['confidence'] >= 70 else "#f59e0b"
            st.markdown(f"""<div class="appliance-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <h4 style="margin:0;color:#e2e8f0;">🔌 {item['name']}</h4>
                        <p style="margin:0.25rem 0;color:#94a3b8;">~{item['estimated_watts']}W estimated</p>
                    </div>
                    <div style="text-align:right;">
                        <h3 style="margin:0;color:{conf_color};">{item['confidence']}%</h3>
                        <p style="margin:0;color:#94a3b8;font-size:0.85rem;">confidence</p>
                    </div>
                </div>
                <div class="progress-bar" style="margin-top:0.75rem;">
                    <div class="progress-fill" style="width:{item['confidence']}%;background:{conf_color};"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    elif st.session_state.current_tab == "ecoscore":
        st.markdown("### 🏆 Eco-Score")
        
        col1, col2 = st.columns(2)
        with col1:
            renewable_pct = st.slider("Renewable Energy Mix (%)", 0, 100, 0)
        with col2:
            avg_efficiency = np.mean([APPLIANCE_DATABASE.get(a, {}).get('efficiency_rating', 3) 
                                       for a in appliance_data.keys()])
        
        city_avg = st.session_state.advanced_features.CITY_AVERAGES.get(st.session_state.user_city, 240)
        eco = calculate_eco_score(prediction['monthly_total'], city_avg, renewable_pct, avg_efficiency)
        
        score_color = "#10b981" if eco['score'] >= 650 else "#f59e0b" if eco['score'] >= 400 else "#ef4444"
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown(f"""<div class="energy-score" style="background:linear-gradient(135deg,{score_color} 0%,{score_color}cc 100%);">
                <h2 style="margin:0;font-size:3.5rem;font-weight:900;">{eco['score']}</h2>
                <p style="margin:0;font-size:1.3rem;">/ 1000</p>
                <p style="margin:0.5rem 0 0 0;font-size:1.1rem;">Grade: {eco['grade']} · {eco['label']}</p>
            </div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Consumption Score", f"{eco['consumption_score']}/400")
        with col2:
            st.metric("Renewable Score", f"{eco['renewable_score']}/300")
        with col3:
            st.metric("Efficiency Score", f"{eco['efficiency_score']}/300")

    elif st.session_state.current_tab == "report":
        st.markdown("### 📄 PDF Energy Audit Report")
        st.info("Generate a professional PDF report of your energy analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            renewable_pct = st.slider("Renewable Energy Mix (%)", 0, 100, 0, key="report_renewable")
        with col2:
            st.markdown(f"**City:** {st.session_state.user_city}")
            st.markdown(f"**Appliances:** {len(appliance_data)}")
        
        if st.button("📥 Generate & Download PDF Report", use_container_width=True):
            with st.spinner("Generating PDF..."):
                city_avg = st.session_state.advanced_features.CITY_AVERAGES.get(st.session_state.user_city, 240)
                avg_eff = np.mean([APPLIANCE_DATABASE.get(a, {}).get('efficiency_rating', 3) for a in appliance_data.keys()])
                eco = calculate_eco_score(prediction['monthly_total'], city_avg, renewable_pct, avg_eff)
                bill_details = calculate_slab_based_bill(prediction['monthly_total'])
                
                pdf_bytes, error = generate_pdf_report(
                    appliance_data, prediction, bill_details, carbon_impact, eco, st.session_state.user_city
                )
                
                if error:
                    st.error(f"❌ {error}")
                    st.code("pip install reportlab")
                else:
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"energy_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("✅ PDF generated successfully!")

else:
    # Professional Welcome Screen
    st.markdown("""
    <div style="text-align: center; padding: 5rem 2rem; background: rgba(30, 41, 59, 0.5); 
                border-radius: 24px; backdrop-filter: blur(20px); border: 1px solid rgba(148, 163, 184, 0.1);
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);">
        <h2 style="color: #10b981; margin-bottom: 1rem; font-size: 2.75rem; font-weight: 700; letter-spacing: -0.5px;">
            Welcome to Smart Energy Optimizer
        </h2>
        <p style="font-size: 1.25rem; color: #94a3b8; margin-bottom: 3rem; font-weight: 400;">
            Professional-grade energy intelligence powered by advanced AI
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-top: 3rem; max-width: 1000px; margin-left: auto; margin-right: auto;">
            <div style="text-align: center; padding: 2rem; background: rgba(16, 185, 129, 0.1); border-radius: 16px; border: 1px solid rgba(16, 185, 129, 0.2);">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🤖</div>
                <div style="font-weight: 600; color: #e2e8f0; font-size: 1.25rem; margin-bottom: 0.5rem;">AI Intelligence</div>
                <div style="font-size: 0.95rem; color: #94a3b8;">Smart predictions & insights</div>
            </div>
            <div style="text-align: center; padding: 2rem; background: rgba(16, 185, 129, 0.1); border-radius: 16px; border: 1px solid rgba(16, 185, 129, 0.2);">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">📊</div>
                <div style="font-weight: 600; color: #e2e8f0; font-size: 1.25rem; margin-bottom: 0.5rem;">Analytics</div>
                <div style="font-size: 0.95rem; color: #94a3b8;">Real-time monitoring</div>
            </div>
            <div style="text-align: center; padding: 2rem; background: rgba(16, 185, 129, 0.1); border-radius: 16px; border: 1px solid rgba(16, 185, 129, 0.2);">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🧪</div>
                <div style="font-weight: 600; color: #e2e8f0; font-size: 1.25rem; margin-bottom: 0.5rem;">Simulation</div>
                <div style="font-size: 0.95rem; color: #94a3b8;">What-if scenarios</div>
            </div>
            <div style="text-align: center; padding: 2rem; background: rgba(16, 185, 129, 0.1); border-radius: 16px; border: 1px solid rgba(16, 185, 129, 0.2);">
                <div style="font-size: 3.5rem; margin-bottom: 1rem;">🌍</div>
                <div style="font-weight: 600; color: #e2e8f0; font-size: 1.25rem; margin-bottom: 0.5rem;">Impact</div>
                <div style="font-size: 0.95rem; color: #94a3b8;">Carbon tracking</div>
            </div>
        </div>
        <div style="margin-top: 3.5rem; padding: 1.5rem; background: rgba(16, 185, 129, 0.15); border-radius: 16px; border: 1px solid rgba(16, 185, 129, 0.3);">
            <p style="color: #10b981; font-size: 1.15rem; margin: 0; font-weight: 500;">
                👈 Configure your appliances in the sidebar to begin your energy optimization journey
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Professional Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 1.5rem; margin-top: 2rem;">
    <p style="font-size: 0.9rem; margin: 0; font-weight: 500; letter-spacing: 0.5px;">
        ⚡ Smart Energy Optimizer | Powered by Advanced Machine Learning
    </p>
    <p style="font-size: 0.8rem; margin: 0.5rem 0 0 0; color: #475569;">
        Professional Energy Intelligence Platform
    </p>
</div>
""", unsafe_allow_html=True)
