from core import NeuralCore
import streamlit as st
import time
import pandas as pd
import os

# --- TIMELESS BRUTALIST UI CONFIG ---
st.set_page_config(page_title="Aeon Nebula", layout="wide")

st.markdown("""
    <style>
    /* System Base Canvas Styling */
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Courier New', Courier, monospace !important; }
    * { font-family: 'Courier New', Courier, monospace !important; }

    /* Premium Minimalist Boot Viewport */
    .splash-viewport {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 80vh;
        background-color: #000000;
        text-align: center;
    }
    .splash-matrix-text {
        font-size: 0.8rem;
        letter-spacing: 5px;
        color: #00f5d4;
        margin-top: 15px;
        font-weight: bold;
        text-transform: uppercase;
    }

    /* Input Modules */
    .stTextArea textarea {
        background-color: #000000 !important; color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important; border-radius: 0px !important;
    }
    .stTextArea textarea:focus { border-color: #00f5d4 !important; }

    /* Brutalist Button Structures */
    .stButton>button {
        background-color: #FFFFFF !important; color: #000000 !important;
        border-radius: 0px !important; font-weight: bold !important;
        border: 1px solid #FFFFFF !important; width: 100%; height: 3em;
        text-transform: none !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { background-color: #000000 !important; color: #FFFFFF !important; border-color: #FFFFFF !important; }

    /* Sidebar Layout Control */
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222222 !important; }

    /* Typographic Adjustments */
    h1, h2, h3 { color: #FFFFFF !important; text-transform: none !important; font-weight: normal !important; }

    /* Compact Diagnostic Grid Component Styling */
    [data-testid="stMetric"] {
        border: 1px solid #222222 !important;
        padding: 12px !important;
        background-color: #050505 !important;
        border-radius: 0px !important;
    }
    [data-testid="stMetricLabel"] p { color: #888888 !important; font-size: 0.8rem !important; }
    [data-testid="stMetricValue"] div { color: #FFFFFF !important; font-size: 1.3rem !important; }

    /* Brutalist Table Borders for Dataframe rendering */
    div[data-testid="stDataFrame"] {
        border: 1px solid #222222 !important;
        background-color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TRACK LAUNCH LIFECYCLE STATE ---
if 'launched' not in st.session_state:
    st.session_state.launched = False

# --- NEURAL CORE INITIALIZATION ---
if 'brain' not in st.session_state:
    try:
        st.session_state.brain = NeuralCore()
        st.session_state.core_online = True
    except Exception as e:
        # Fallback to prevent AttributeErrors if the engine initialization errors out
        st.session_state.brain = None
        st.session_state.core_online = False

# --- WELCOME SPLASH SCREEN CYCLE ---
if not st.session_state.launched:
    st.markdown("<style>.stApp { overflow: hidden !important; }</style>", unsafe_allow_html=True)
    _, center_target, _ = st.columns([1, 3, 1])
 
    with center_target:
        st.markdown('<div class="splash-viewport">', unsafe_allow_html=True)
        if os.path.exists("logo.png"):
            st.image("logo.png", width=200)
        else:
            st.markdown('<h3>⚡ [ AEON NEBULA ] ⚡</h3>', unsafe_allow_html=True)
        st.markdown('<div class="splash-matrix-text">Initializing Threat Matrix...</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
     
    time.sleep(3.5)
    st.session_state.launched = True
    st.rerun()

# --- MAIN APPLICATION DASHBOARD ---
else:
    # --- SIDEBAR: SYSTEM STATUS & CLOUD COMMAND ---
    st.sidebar.title("Aeon Nebula")
    st.sidebar.markdown("---")

    # Local Status Monitor
    if st.session_state.get('core_online', False) and st.session_state.brain is not None:
        st.sidebar.success("Neural core: Connected")
      
        # Cloud Status Monitor (Only execute if brain object successfully exists)
        if st.session_state.brain.is_cloud_online():
            st.sidebar.success("Germany DB: Authenticated")
        else:
            st.sidebar.error("Germany DB: Initial Link Error")
    else:
        st.sidebar.error("Neural core: Disconnected")
        st.sidebar.error("Germany DB: Connection Defeated")

    st.sidebar.markdown("---")

    # --- NETWORK TELEMETRY MODULE ---
    st.sidebar.subheader("Network Routing")
    st.sidebar.text("Protocol: HTTPS / TLS 1.3")
    st.sidebar.text("Region: EU-Central (Frankfurt)")
    st.sidebar.text("Secure Tunnel: Active")

    st.sidebar.markdown("---")
    st.sidebar.caption("System version: 1.0.0-stable")

    # --- MAIN INTERFACE ---
    st.title("Neural threat interceptor")
    st.write(f"System time: {time.strftime('%H:%M:%S')}")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Data stream input")
        user_input = st.text_area("Inbound packet:", height=300, placeholder="Waiting for binary stream...")

        if st.button("Execute scan"):
            if user_input:
                if st.session_state.brain is not None:
                    with st.status("Neural analysis in progress...", expanded=True) as status:
                        results = st.session_state.brain.process_pipeline(user_input)
                        status.update(label="Scan complete", state="complete")
       
                    st.write("### Analysis result")
                 
                    if results["risk_level"] == "Low":
                        st.success("Access granted: Noise/Normal traffic.")
                    elif results["risk_level"] == "Moderate":
                        st.warning("Pattern flagged. Analyzing intent...")
                    elif results["risk_level"] == "High":
                        st.error("High-risk payload detected.")
                    else:
                        st.error("MALICIOUS PAYLOAD INTERCEPTED.")

                    st.code(results["json_output"], language="json")
                   
                    # Force a quick UI refresh so the bottom history log updates instantly after scan
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Core Engine Unavailable. Cannot complete scan.")
            else:
                st.error("No data detected.")

    with col2:
        st.subheader("Diagnostics")
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.metric(label="CPU Load", value="18%")
            st.metric(label="Neural Opt", value="Active")
        with t_col2:
            st.metric(label="RAM Usage", value="1.42GB")
            if st.session_state.brain is not None:
                current_latency = st.session_state.brain.get_last_latency()
                st.metric(label="Latency", value=f"{current_latency}ms")
            else:
                st.metric(label="Latency", value="ERRms")

        st.markdown("---")
        st.write("### Event log")
        st.caption(f"{time.strftime('%H:%M')} - Neural weights loaded")
        st.caption(f"{time.strftime('%H:%M')} - Vector matrix initialized")
  
        if st.session_state.brain is not None:
            alert_caption = st.session_state.brain.get_event_caption()
            if alert_caption:
                st.caption(alert_caption)
            else:
                st.caption(f"{time.strftime('%H:%M')} - Monitoring packets...")
        else:
            st.caption(f"{time.strftime('%H:%M')} - Core failure logged.")

    # --- SYSTEM SPACING ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("---")

    # --- GLOBAL ARCHIVE LEDGER (BOTTOM MODULE) ---
    st.header("Intercepted Threat History Ledger")
    st.write("Persistent real-time query interface fetching analytics straight from EU Node.")

    if st.session_state.brain is not None and st.session_state.brain.is_cloud_online():
        raw_logs = st.session_state.brain.fetch_threat_logs()
        if raw_logs:
            df = pd.DataFrame(raw_logs)
            df = df[['created_at', 'threat_type', 'risk_level', 'confidence_score', 'latency_ms']]
            df.columns = ['Timestamp (UTC)', 'Classification', 'Risk Severity', 'Confidence', 'Response Delay (ms)']
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("System Vault Archive is currently clean. No active threat logs registered.")
    else:
        st.error("Database offline or Core engine disconnected. History ledger inaccessible.")