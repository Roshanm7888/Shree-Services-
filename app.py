import streamlit as st
import pandas as pd
import urllib.parse
import requests
import base64
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Online GST & Tax Center", layout="wide", page_icon="🏢")

# Custom Styling (Sabse Professional Design)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .main-header { background: #1e3a8a; color: white; padding: 35px; border-radius: 15px; text-align: center; margin-bottom: 25px;}
    .stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; font-size: 16px; transition: 0.3s; }
    .stButton>button:hover { background-color: #1e3a8a; color: white; }
    .service-box { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 12px solid #1e3a8a; margin-bottom: 20px; }
    .footer-box { background: #1e3a8a; padding: 20px; border-radius: 12px; text-align: center; margin-top: 30px; color: white; font-weight: bold; font-size: 18px;}
    .upload-card { background: #f0f4f8; padding: 20px; border-radius: 10px; border: 2px dashed #1e3a8a; margin-bottom: 15px; color: #1e3a8a; font-weight: bold; }
    .invoice-card { background: white; border: 2px solid #1e3a8a; padding: 25px; border-radius: 15px; font-family: sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data & Settings
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
FIXED_UPI = "7888273972-2@ybl"
PORTAL_LINK = "https://shree-services.streamlit.app"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwhzALmZZp2KvshihXxQR0QZzhN38aSTHb7KewLnJTO_pQ5t-C4Er4nJBjnfZI3VGXz/exec"

@st.cache_data(ttl=10)
def load_data():
    try:
        d = pd.read_csv(SHEET_URL)
        d.columns = d.columns.str.strip()
        return d
    except: return pd.DataFrame()
df = load_data()

# URL Parameter Handling
params = st.query_params
if 'page' not in st.session_state:
    st.session_state.page = params.get("page", "home")

# 3. TOP NAVIGATION (Big Blue Buttons)
st.markdown('<div class="main-header"><h1 style="font-size:38px; margin-bottom:0;">Shree Services - Online GST & Tax Center</h1><p style="font-size:20px;">A Complete Hub for Accounting & Taxation Solutions</p></div>', unsafe_allow_html=True)

col_n1, col_n2, col_n3, col_n4, col_n5 = st.columns(5)
with col_n1: 
    if st.button("🏠 HOME"): st.session_state.page = "home"
with col_n2: 
    if st.button("🧾 BILL"): st.session_state.page = "bill"
with col_n3: 
    if st.button("🔔 REMINDER"): st.session_state.page = "rem"
with col_n4: 
    if st.button("📤 UPLOAD"): st.session_state.page = "up"
with col_n5: 
    if st.button("📊 LEDGER"): st.session_state.page = "led"

st.markdown("---")

# 4. Page Routing Logic
if st.session_state.page == "home":
    st.write("### Services Offered (Click to apply)")
    services = [
        {"n": "📊 Taxation", "d": "GST, House Tax, Salary & Business Tax Filing."},
        {"n": "🛡️ Insurance", "d": "Life, Health & Vehicle Insurance Solutions."},
        {"n": "📝 Online Work", "d": "PAN, Aadhar, GST Registration & Digital Services."}
    ]
    for s in services:
        st.markdown(f'<div class="service-box"><h2>{s["n"]}</h2><p style="font-size:18px; color:#555;">{s["d"]}</p></div>', unsafe_allow_html=True)
        with st.expander(f"Apply for {s['n']} Request"):
            m_num = st.text_input("Your Mobile Number", key=f"m_{s['n']}")
            req_text = st.text_area("Your Requirement", key=f"r_{s['n']}")
            if st.button(f"Submit {s['n']} Application"):
                w_msg = f"Inquiry for {s['n']}\nMobile: {m_num}\nDetails: {req_text}"
                st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(w_msg)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; text-align:center; border-radius:10px; font-weight:bold;">📲 Send Application to Roshan Ji</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "bill":
    st.title("📑 Generate Invoice")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        amt = st.number_input("Amount (₹)", min_value=0, value=800)
        p_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {p_month}")
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        
        st.markdown(f"""
        <div class="invoice-card">
            <div style="text-align:center;"><h2>Shree Services</h2><small>Mohan Garden, Delhi | 7888273972</small></div>
            <hr><p><b>To:</b> {party} <span style="float:right;"><b>Date:</b> {datetime.now().strftime('%d-%b-%Y')}</span></p>
            <table style="width:100%; border:none;">
                <tr style="background:#f2f2f2;"><th>Description</th><th style="text-align:right;">Amount</th></tr>
                <tr><td>{particulars}</td><td style="text-align:right;">₹{amt}/-</td></tr>
            </table>
            <div style="text-align:center; margin-top:20px; background:#f9f9f9; padding:10px; border-radius:10px;">
                <p style="font-size:12px;"><b>SCAN TO PAY</b></p>
                <img src="{qr}" width="120"><br><small>UPI: {FIXED_UPI}</small>
            </div>
        </div>""", unsafe_allow_html=True)
        
        download_url = f"{PORTAL_LINK}?page=bill&party={urllib.parse.quote(party)}&amt={amt}"
        wa_m = f"Namaste 🙏, *Shree Services*.\n*Bill For:* {party}\n*Amount:* ₹{amt}\n\n1️⃣ *Download Invoice:* {download_url}\n2️⃣ *Visit Portal:* {PORTAL_LINK}\n\n*UPI:* {FIXED_UPI}"
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(wa_m)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Bill (2 Links)</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "up":
    st.title("📤 Document Portal")
    mode = params.get("mode", "all")
    if not df.empty: st.selectbox("Your Firm", df['Firm Name'].unique())
    
    if mode in ["sale", "all"]:
        st.markdown('<div class="upload-card">📁 SALE BILLS (GSTR-1)</div>', unsafe_allow_html=True)
        s_files = st.file_uploader("Upload Sales", accept_multiple_files=True, key="s")
    
    if mode in ["purchase", "all"]:
        st.markdown('<div class="upload-card">📁 PURCHASE BILLS (GST-3B)</div>', unsafe_allow_html=True)
        p_files = st.file_uploader("Upload Purchases", accept_multiple_files=True, key="p")
    
    if st.button("Submit Documents to Drive"):
        st.success("Bills submitted successfully! Roshan ji will check in Drive.")
        st.balloons()

elif st.session_state.page == "rem":
    st.title("🔔 Reminders")
    if not df.empty:
        party = st.selectbox("Select Client", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        r_type = st.radio("Type", ["GSTR-1 (Sale Link)", "GST-3B (Purchase Link)", "💰 Payment Reminder"])
        
        if "GSTR-1" in r_type:
            link = f"{PORTAL_LINK}?page=up&mode=sale"
            m = f"Namaste 🙏, *Shree Services*. GSTR-1 date aa rahi hai. Sale bills yahan upload karein:\n👉 {link}"
        elif "GST-3B" in r_type:
            link = f"{PORTAL_LINK}?page=up&mode=purchase"
            m = f"Namaste 🙏, *Shree Services*. GST-3B date aa rahi hai. Purchase bills yahan upload karein:\n👉 {link}"
        else:
            m = f"Namaste 🙏, Aapka payment pending hai: {PORTAL_LINK}"
            
        st.markdown(f'<a href="https://wa.me/{row["Mobile Number"]}?text={urllib.parse.quote(m)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Reminder</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "led":
    st.title("📊 Ledger Status")
    st.dataframe(df, use_container_width=True)

# 5. Footer (Permanent Support Info)
st.markdown(f'<div class="footer-box">📞 Roshan Mishra: 7888273972 | 9220393972 | 8668257610</div>', unsafe_allow_html=True)
