import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
import folium
from streamlit_folium import st_folium
from sklearn.cluster import KMeans
import mysql.connector


# Page Configuration
st.set_page_config(
    page_title="StreeTranam - Safety First",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with rose/coral accents
st.markdown("""
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #1a1625 0%, #1e1a2e 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #13111c 0%, #1a1625 100%);
        border-right: 1px solid #2d2640;
    }
    
    /* Cards */
    .card {
        background: linear-gradient(145deg, #231f35 0%, #1e1a2e 100%);
        border: 1px solid #2d2640;
        border-radius: 16px;
        padding: 24px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .card-header {
        color: #f0e6ff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Primary button */
    .primary-btn {
        background: linear-gradient(135deg, #e85a8f 0%, #d64577 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        display: inline-block;
    }
    
    .primary-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(232, 90, 143, 0.4);
    }
    
    /* SOS Button */
    .sos-button {
        background: linear-gradient(135deg, #ff4757 0%, #ff3344 100%);
        color: white;
        padding: 20px 40px;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        cursor: pointer;
        animation: pulse 2s infinite;
        box-shadow: 0 0 40px rgba(255, 71, 87, 0.5);
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 20px rgba(255, 71, 87, 0.5); }
        50% { box-shadow: 0 0 40px rgba(255, 71, 87, 0.8); }
        100% { box-shadow: 0 0 20px rgba(255, 71, 87, 0.5); }
    }
    
    /* Safe indicator */
    .safe-indicator {
        background: linear-gradient(135deg, #2ed573 0%, #26ab5f 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Warning indicator */
    .warning-indicator {
        background: linear-gradient(135deg, #ffa502 0%, #ff8c00 100%);
        color: #1a1625;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Metric card */
    .metric-card {
        background: linear-gradient(145deg, #2d2640 0%, #231f35 100%);
        border: 1px solid #3d3555;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e85a8f 0%, #ff8a9b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: #9d95b8;
        font-size: 0.85rem;
        margin-top: 4px;
    }
    
    /* Guardian card */
    .guardian-card {
        background: linear-gradient(145deg, #2d2640 0%, #231f35 100%);
        border: 1px solid #3d3555;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .guardian-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #e85a8f 0%, #d64577 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    /* Status badge */
    .status-active {
        background: #2ed573;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        animation: blink 1.5s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Map placeholder */
    .map-container {
        background: linear-gradient(145deg, #1e1a2e 0%, #13111c 100%);
        border: 2px solid #3d3555;
        border-radius: 16px;
        height: 400px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    
    .map-grid {
        position: absolute;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(61, 53, 85, 0.3) 1px, transparent 1px),
            linear-gradient(90deg, rgba(61, 53, 85, 0.3) 1px, transparent 1px);
        background-size: 40px 40px;
    }
    
    .location-marker {
        width: 20px;
        height: 20px;
        background: #e85a8f;
        border-radius: 50%;
        position: relative;
        z-index: 10;
        box-shadow: 0 0 20px rgba(232, 90, 143, 0.6);
    }
    
    .location-marker::after {
        content: '';
        position: absolute;
        width: 40px;
        height: 40px;
        border: 2px solid #e85a8f;
        border-radius: 50%;
        top: -10px;
        left: -10px;
        animation: ripple 2s infinite;
    }
    
    @keyframes ripple {
        0% { transform: scale(1); opacity: 1; }
        100% { transform: scale(2); opacity: 0; }
    }
    
    /* Trip route line */
    .route-line {
        position: absolute;
        height: 4px;
        background: linear-gradient(90deg, #2ed573, #e85a8f, #ff4757);
        border-radius: 2px;
        width: 60%;
        z-index: 5;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: #231f35;
        border: 1px solid #3d3555;
        border-radius: 8px;
        color: #f0e6ff;
    }
    
    .stSelectbox > div > div {
        background: #231f35;
        border: 1px solid #3d3555;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #231f35;
        border-radius: 8px;
        color: #9d95b8;
        border: 1px solid #3d3555;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #e85a8f 0%, #d64577 100%);
        color: white;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #e85a8f, #ff8a9b);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #231f35;
        border-radius: 8px;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e85a8f 0%, #ff8a9b 50%, #2ed573 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 8px;
    }
    
    .subtitle {
        color: #9d95b8;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 24px;
    }
    
    /* Feature card */
    .feature-card {
        background: linear-gradient(145deg, #231f35 0%, #1e1a2e 100%);
        border: 1px solid #3d3555;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: #e85a8f;
        box-shadow: 0 12px 40px rgba(232, 90, 143, 0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 12px;
    }
    
    .feature-title {
        color: #f0e6ff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .feature-desc {
        color: #9d95b8;
        font-size: 0.85rem;
    }
    
    /* Quote card */
    .quote-card {
        background: linear-gradient(145deg, #2d2640 0%, #231f35 100%);
        border-left: 4px solid #e85a8f;
        border-radius: 0 12px 12px 0;
        padding: 20px 24px;
        margin: 16px 0;
        font-style: italic;
        color: #d4cce8;
    }
    
    .quote-author {
        color: #e85a8f;
        font-style: normal;
        font-weight: 600;
        margin-top: 12px;
        text-align: right;
    }
    
    /* Breathing circle */
    .breathing-circle {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: linear-gradient(135deg, #4ecdc4 0%, #2ed573 100%);
        margin: 20px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        animation: breathe 8s infinite ease-in-out;
    }
    
    @keyframes breathe {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    /* Incident severity */
    .severity-low { border-left: 4px solid #2ed573; }
    .severity-medium { border-left: 4px solid #ffa502; }
    .severity-high { border-left: 4px solid #ff4757; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'guardian_mode_active' not in st.session_state:
    st.session_state.guardian_mode_active = False
if 'guardians' not in st.session_state:
    st.session_state.guardians = [
        {"name": "Mom", "phone": "+91 98765 43210", "active": True},
        {"name": "Best Friend", "phone": "+91 87654 32109", "active": True},
    ]
if 'trip_active' not in st.session_state:
    st.session_state.trip_active = False
if 'check_ins' not in st.session_state:
    st.session_state.check_ins = 0
if 'safety_score' not in st.session_state:
    st.session_state.safety_score = 87
if 'incidents' not in st.session_state:
    st.session_state.incidents = []

# Sidebar Navigation
# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 2.5rem;">🛡️</div>
        <div class="main-title" style="font-size: 1.5rem;">StreeTranam</div>
        <div class="subtitle" style="font-size: 0.8rem; margin-bottom: 0;">
            Safety First, Always
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation pages
    pages = {
        "dashboard": ("📊", "Dashboard"),
        "guardian": ("👁️", "Guardian Mode"),
        "trip": ("🗺️", "Trip Analyzer"),
        "map_page": ("🗺️", "Safety Map"),
        "emergency": ("🚨", "Emergency SOS"),
        "report": ("📝", "Report Incident"),
        "safety_form": ("📋", "Safety Form"),
        "support": ("💜", "Support & Care"),
        "settings": ("⚙️", "Settings"),
    }

    # Sidebar buttons (FIXED KEYS)
    for page_key, (icon, label) in pages.items():
        if st.button(
            f"{icon} {label}",
            key=f"sidebar_nav_{page_key}",   # ✅ UNIQUE KEY FIX
            use_container_width=True
        ):
            st.session_state.current_page = page_key
            st.rerun()

    st.markdown("---")

    # SOS Button
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <div style="color: #9d95b8; font-size: 0.8rem; margin-bottom: 8px;">
            Quick Emergency
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "🚨 SOS",
        key="sidebar_sos_unique",   # ✅ UNIQUE KEY FIX
        use_container_width=True
    ):
        st.session_state.current_page = 'emergency'
        st.rerun()

# Main Content Area
def render_dashboard():
    st.markdown('<h1 class="main-title">Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your safety overview at a glance</p>', unsafe_allow_html=True)

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.safety_score}%</div>
            <div class="metric-label">Safety Score</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.guardians)}</div>
            <div class="metric-label">Active Guardians</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.check_ins}</div>
            <div class="metric-label">Check-ins Today</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        guardian_status = "Active" if st.session_state.guardian_mode_active else "Inactive"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size: 1.2rem;">{guardian_status}</div>
            <div class="metric-label">Guardian Mode</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Actions
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-header">⚡ Quick Actions</div>
        </div>
        """, unsafe_allow_html=True)

        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button("🚨 Emergency SOS", use_container_width=True, type="primary"):
                st.session_state.current_page = 'emergency'
                st.rerun()
            if st.button("👁️ Start Guardian", use_container_width=True):
                st.session_state.current_page = 'guardian'
                st.rerun()

    # Emergency Helplines
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <div class="card-header">📞 Emergency Helplines</div>
    </div>
    """, unsafe_allow_html=True)

    helpline_cols = st.columns(4)
    helplines = [
        ("🚔", "Police", "100"),
        ("🚑", "Ambulance", "102"),
        ("👩", "Women Helpline", "1091"),
        ("🆘", "Emergency", "112"),
    ]

    for col, (icon, name, number) in zip(helpline_cols, helplines):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="color: #f0e6ff; font-weight: 600; margin: 8px 0;">{name}</div>
                <div style="color: #e85a8f; font-size: 1.3rem; font-weight: 700;">{number}</div>
            </div>
            """, unsafe_allow_html=True)

def render_guardian_mode():
    st.markdown('<h1 class="main-title">Guardian Mode</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Real-time location sharing with your trusted contacts</p>', unsafe_allow_html=True)

    # Status banner
    if st.session_state.guardian_mode_active:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2ed573 0%, #26ab5f 100%); 
                    border-radius: 12px; padding: 16px; text-align: center; margin-bottom: 20px;">
            <span class="status-active"></span>
            <span style="color: white; font-weight: 600;">Guardian Mode is ACTIVE - Your guardians are watching</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3d3555 0%, #2d2640 100%); 
                    border-radius: 12px; padding: 16px; text-align: center; margin-bottom: 20px; border: 1px solid #4d4565;">
            <span style="color: #9d95b8; font-weight: 600;">Guardian Mode is INACTIVE - Enable to start sharing</span>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:

        # Trip controls
        st.markdown("<br>", unsafe_allow_html=True)

        if not st.session_state.trip_active:
            st.markdown("""
            <div class="card">
                <div class="card-header">📍 Start a Trip</div>
            </div>
            """, unsafe_allow_html=True)

            with st.form("trip_form"):
                start_loc = st.text_input("Starting Location", placeholder="Current location or enter address")
                dest_loc = st.text_input("Destination", placeholder="Where are you going?")
                travel_mode = st.selectbox("Travel Mode", ["Walking", "Public Transport", "Cab/Taxi", "Personal Vehicle"])

                if st.form_submit_button("🚀 Start Trip", use_container_width=True, type="primary"):
                    if start_loc and dest_loc:
                        st.session_state.trip_active = True
                        st.session_state.guardian_mode_active = True
                        st.success("Trip started! Your guardians have been notified.")
                        st.rerun()
                    else:
                        st.error("Please enter both starting and destination locations")
        else:
            trip_col1, trip_col2, trip_col3 = st.columns(3)
            with trip_col1:
                if st.button("✅ I'm Safe", use_container_width=True):
                    st.session_state.check_ins += 1
                    st.success("Check-in recorded!")
            with trip_col2:
                if st.button("📍 Update Location", use_container_width=True):
                    st.info("Location updated!")
            with trip_col3:
                if st.button("🛑 End Trip", use_container_width=True, type="secondary"):
                    st.session_state.trip_active = False
                    st.session_state.guardian_mode_active = False
                    st.info("Trip ended. Guardians notified.")
                    st.rerun()

    with col2:
        # Guardian Mode Toggle
        st.markdown("""
        <div class="card">
            <div class="card-header">⚡ Quick Controls</div>
        </div>
        """, unsafe_allow_html=True)

        guardian_toggle = st.toggle("Enable Guardian Mode", value=st.session_state.guardian_mode_active)
        if guardian_toggle != st.session_state.guardian_mode_active:
            st.session_state.guardian_mode_active = guardian_toggle
            st.rerun()

        check_in_interval = st.selectbox("Check-in Reminder", ["Every 5 min", "Every 10 min", "Every 15 min", "Every 30 min"])

        st.markdown("<br>", unsafe_allow_html=True)

        # Guardians list
        st.markdown("""
        <div class="card">
            <div class="card-header">👥 Your Guardians</div>
        </div>
        """, unsafe_allow_html=True)

        for guardian in st.session_state.guardians:
            initial = guardian["name"][0].upper()
            st.markdown(f"""
            <div class="guardian-card">
                <div class="guardian-avatar">{initial}</div>
                <div>
                    <div style="color: #f0e6ff; font-weight: 600;">{guardian["name"]}</div>
                    <div style="color: #9d95b8; font-size: 0.85rem;">{guardian["phone"]}</div>
                </div>
                <div style="margin-left: auto;">
                    <span class="status-active"></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Add guardian form
        with st.expander("➕ Add Guardian"):
            new_name = st.
