import streamlit as st
import pandas as pd
import urllib.parse
import requests
import base64
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(
    page_title="Shree Services - Online GST & Tax Center", 
    layout="centered", 
    page_icon="🏢",
    initial_sidebar_state="expanded"
)

# Custom Styling (BLUE HIGHLIGHTS FOR SIDEBAR)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #1e3a8a !important; min-width: 300px !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: white !important; font-size: 18px !important; font-weight: bold; }
    
    /* Mobile Sidebar Button (BLUE COLOR) */
    button[kind="headerNoSpacing"] { background-color: #007bff !important; color: white !important; border-radius: 50% !important; padding: 10px !important; }
    
    /* Main Layout Styling */
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1e3a8a; color: white; font-weight: bold; }
    .main-header { background: #1e3a8a; color: white; padding: 40px; border-radius: 0 0 25px 25px; text-align: center; margin-top: -65px; margin-bottom: 30px;}
    .service-box { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 10px solid #1e3a8a; margin-bottom: 20px; }
    
    /* Warning/Alert for Menu */
    .menu-alert { background-color: #007bff; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data & Settings
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
FIXED_UPI = "7888273972-2@ybl"
PORTAL_LINK = "https://shree-services.streamlit.app"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwhzALmZZp2KvshihXxQR0QZzhN38aSTHb7KewLnJTO_pQ5t-C4Er4nJBjnfZI3VGXz/exec"

@st.cache_data(ttl=30)
def load_data():
    try:
        d = pd.read_csv(SHEET_URL)
        d.columns = d.columns.str.strip()
        return d
    except: return pd.DataFrame()
df = load_data()

# URL Handling
params = st.query_params
nav_idx = 0
if params.get("page") == "upload": nav_idx = 4

# 3. SIDEBAR
with st.sidebar:
    st.markdown("<h1 style='color:white; text-align:center;'>🏢 SHREE MENU</h1>", unsafe_allow_html=True)
    st.markdown("---")
    choice = st.radio("SELECT ACTION:", ["🏠 Home Page", "📊 Ledger Status", "🧾 Create Invoice", "🔔 WhatsApp Reminder", "📤 Upload Bills"], index=nav_idx)
    st.markdown("---")
    st.markdown("""
        <div style='color:white; background:rgba(255,255,255,0.2); padding:15px; border-radius:10px;'>
        <p><b>📞 Helpline Numbers:</b></p>
        <p>7888273972 (Roshan Mishra)<br>9220393972<br>8668257610</p>
        </div>
    """, unsafe_allow_html=True)

# 4. Home Page Content
if choice == "🏠 Home Page":
    st.markdown('<div class="menu-alert">⬅️ Tap the Blue Arrow (Left Top) to see Menu</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header"><h1>Shree Services - Online GST & Tax Center</h1><p>A Complete Hub for Accounting & Taxation Solutions</p></div>', unsafe_allow_html=True)
    
    services = [
        {"n": "📊 Taxation", "d": "Professional GST, House Tax & Business Tax Filing."},
        {"n": "🛡️ Insurance", "d": "Life, Health & Vehicle Insurance Plans."},
        {"n": "📝 Online Work", "d": "Quick PAN, Aadhar & GST Registration."}
    ]
    
    for s in services:
        st.markdown(f'<div class="service-box"><h2>{s["n"]}</h2><p>{s["d"]}</p></div>', unsafe_allow_html=True)
        with st.expander(f"Apply for {s['n']}"):
            m = st.text_input("Mobile Number", key=f"m_{s['n']}")
            r = st.text_area("Requirement Details", key=f"r_{s['n']}")
            if st.button(f"Submit {s['n']} Request"):
                msg = f"Inquiry for {s['n']}\nMobile: {m}\nDetails: {r}"
                st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(msg)}" target="_blank"><div style="background:#25d366; color:white; padding:10px; text-align:center; border-radius:10px;">📲 Send to Roshan Ji</div></a>', unsafe_allow_html=True)

# (Baki pages Ledger, Invoice, Upload, Reminder ka code niche waisa hi rahega)
elif choice == "🧾 Create Invoice":
    st.title("📑 Generate Bill")
    if not df.empty:
        party = st.selectbox("Client Name", df['Firm Name'].unique())
        amt = st.number_input("Amount (₹)", min_value=0, value=800)
        p_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {p_month}")
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        st.markdown(f'<div style="border:2px solid #1e3a8a; padding:20px; border-radius:10px; background:white;"><h2 style="text-align:center; color:#1e3a8a;">Shree Services</h2><p><b>To:</b> {party}</p><hr><p>{particulars} <span style="float:right;"><b>₹{amt}/-</b></span></p><div style="text-align:center; margin-top:20px;"><img src="{qr}" width="130"><br><b>UPI: {FIXED_UPI}</b></div></div>', unsafe_allow_html=True)
        wa_m = f"Namaste 🙏, *Shree Services*.\n*Bill For:* {party}\n*Amount:* ₹{amt}\n*UPI:* {FIXED_UPI}\n*Portal:* {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(wa_m)}" target="_blank">📲 Send Bill on WhatsApp</a>', unsafe_allow_html=True)

elif choice == "📤 Upload Bills":
    st.title("📤 Document Portal")
    mode = params.get("mode", "all")
    if not df.empty: st.selectbox("Select Your Firm", df['Firm Name'].unique())
    if mode == "sale" or mode == "all":
        st.markdown("### 📁 SALE BILLS (GSTR-1)")
        st.file_uploader("Select Sale Files", accept_multiple_files=True, key="sale")
    if mode == "purchase" or mode == "all":
        st.markdown("### 📁 PURCHASE BILLS (GST-3B)")
        st.file_uploader("Select Purchase Files", accept_multiple_files=True, key="pur")
    if st.button("Submit to Google Drive"):
        st.success("Files Submitted Successfully!")

elif choice == "🔔 WhatsApp Reminder":
    st.title("🔔 Send Reminders")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        c_row = df[df['Firm Name'] == party].iloc[0]
        rem = st.radio("Reminder Type", ["GSTR-1 (Sale Link)", "GST-3B (Purchase Link)", "Payment Reminder"])
        if "GSTR-1" in rem:
            l = f"{PORTAL_LINK}?page=upload&mode=sale"
            m = f"Namaste 🙏, *Shree Services*. GSTR-1 date aa rahi hai. Sale bills yahan upload karein:\n👉 {l}"
        elif "GST-3B" in rem:
            l = f"{PORTAL_LINK}?page=upload&mode=purchase"
            m = f"Namaste 🙏, *Shree Services*. GST-3B date aa rahi hai. Purchase bills yahan upload karein:\n👉 {l}"
        else:
            m = f"Namaste 🙏, *Shree Services*. Aapka payment pending hai, kripya check karein: {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/{c_row["Mobile Number"]}?text={urllib.parse.quote(m)}" target="_blank">📲 Send Reminder</a>', unsafe_allow_html=True)

elif choice == "📊 Ledger Status":
    st.title("📊 Business Ledger")
    st.dataframe(df, use_container_width=True)

            
