import streamlit as st
import pandas as pd
import urllib.parse
import requests
import base64
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services", layout="wide", page_icon="🏢")

# Custom Styling - Sidebar ko hide karke buttons ko upar set kiya hai
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; } /* Sidebar ko pura hata diya */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    .main-header { background: #1e3a8a; color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
    .stButton>button { border-radius: 8px; height: 3em; font-weight: bold; border: 2px solid #1e3a8a; }
    .nav-active { background-color: #1e3a8a !important; color: white !important; }
    .service-box { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-left: 10px solid #1e3a8a; margin-bottom: 15px; }
    .footer-box { background: #f1f5f9; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px; border: 1px solid #1e3a8a; color: #1e3a8a; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 2. Settings & Data
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
FIXED_UPI = "7888273972-2@ybl"
PORTAL_LINK = "https://shree-services.streamlit.app"

@st.cache_data(ttl=10)
def load_data():
    try:
        d = pd.read_csv(SHEET_URL)
        d.columns = d.columns.str.strip()
        return d
    except: return pd.DataFrame()
df = load_data()

# 3. TOP NAVIGATION MENU (Instead of Sidebar)
st.markdown('<div class="main-header"><h1>Shree Services - Online GST & Tax Center</h1><p>A Complete Hub for Accounting & Taxation Solutions</p></div>', unsafe_allow_html=True)

# Navigation Buttons in a Row
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

# Default Page
if 'page' not in st.session_state:
    st.session_state.page = "home"

# 4. Page Logic
if st.session_state.page == "home":
    st.info("Choose a service below and submit your request.")
    services = [
        {"n": "📊 Taxation", "d": "GST, House Tax & Income Tax Filing."},
        {"n": "🛡️ Insurance", "d": "Life, Health & Vehicle Insurance."},
        {"n": "📝 Online Work", "d": "PAN, Aadhar & GST Registration."}
    ]
    for s in services:
        st.markdown(f'<div class="service-box"><h3>{s["n"]}</h3><p>{s["d"]}</p></div>', unsafe_allow_html=True)
        with st.expander(f"Apply for {s['n']}"):
            m = st.text_input("Mobile No.", key=f"m_{s['n']}")
            r = st.text_area("Details", key=f"r_{s['n']}")
            if st.button(f"Submit {s['n']}"):
                wa_txt = f"New Inquiry: {s['n']}\nMobile: {m}\nDetails: {r}"
                st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(wa_txt)}" target="_blank">📲 Send to Roshan Mishra</a>', unsafe_allow_html=True)

elif st.session_state.page == "bill":
    st.title("📑 Create Invoice")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        amt = st.number_input("Amount", value=800)
        particulars = st.text_input("Particulars", value="GST Filing Charges")
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        st.markdown(f'<div style="border:2px solid #1e3a8a; padding:20px; border-radius:10px; background:white;"><h3>Shree Services Bill</h3><p><b>Client:</b> {party}</p><hr><p>{particulars}: ₹{amt}</p><div style="text-align:center;"><img src="{qr}" width="120"><br><b>UPI: {FIXED_UPI}</b></div></div>', unsafe_allow_html=True)
        wa_m = f"Namaste 🙏, Shree Services Bill For: {party}\nAmount: ₹{amt}\nPortal: {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(wa_m)}" target="_blank">📲 Send Bill</a>', unsafe_allow_html=True)

elif st.session_state.page == "up":
    st.title("📤 Document Upload")
    st.info("Select your firm and upload Sale/Purchase bills.")
    if not df.empty: st.selectbox("Firm Name", df['Firm Name'].unique())
    st.file_uploader("Upload Files", accept_multiple_files=True)
    if st.button("Submit to Drive"): st.success("Files processing!")

elif st.session_state.page == "rem":
    st.title("🔔 WhatsApp Reminders")
    if not df.empty:
        party = st.selectbox("Client", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        rem_type = st.radio("Type", ["GSTR-1 (Sale)", "GST-3B (Purchase)", "Payment"])
        msg = f"Namaste 🙏, Shree Services Reminder for {party}. Check portal: {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/{row["Mobile Number"]}?text={urllib.parse.quote(msg)}" target="_blank">📲 Send Reminder</a>', unsafe_allow_html=True)

elif st.session_state.page == "led":
    st.title("📊 Ledger Status")
    st.dataframe(df, use_container_width=True)

# 5. Fixed Contact Info at Bottom
st.markdown("""
    <div class="footer-box">
        📞 Contact Roshan Mishra: 7888273972 | 9220393972 | 8668257610
    </div>
""", unsafe_allow_html=True)
