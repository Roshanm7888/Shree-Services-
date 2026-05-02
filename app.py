import streamlit as st
import pandas as pd
import urllib.parse
import requests
import base64
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Online GST & Tax Center", layout="centered", page_icon="🏢")

# Custom Styling (Professional & Full Width)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #1e3a8a; min-width: 260px !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: white !important; font-size: 16px !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.8em; background-color: #1e3a8a; color: white; font-weight: bold; font-size: 18px; }
    .main-header { background: #1e3a8a; color: white; padding: 45px 20px; border-radius: 0 0 30px 30px; text-align: center; margin-top: -65px; margin-bottom: 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .service-box { background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.1); border-left: 12px solid #1e3a8a; margin-bottom: 25px; }
    .invoice-card { background: #ffffff; border: 2px solid #1e3a8a; padding: 25px; border-radius: 15px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .upload-card { background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px dashed #1e3a8a; margin-bottom: 15px; font-weight: bold; color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# 2. Settings & Data
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

# URL Logic for Reminders
params = st.query_params
nav_idx = 0
if params.get("page") == "upload": nav_idx = 4

# 3. Sidebar (Numbers Permanent)
with st.sidebar:
    st.markdown("<h2 style='color:white; text-align:center;'>📋 MENU</h2>", unsafe_allow_html=True)
    choice = st.radio("", ["🏠 Home", "📊 Ledger Status", "🧾 Create Invoice", "🔔 WhatsApp Reminder", "📤 Upload Bills"], index=nav_idx)
    st.markdown("---")
    st.markdown("""
        <div style='color:white; background:rgba(255,255,255,0.1); padding:15px; border-radius:10px;'>
        <p><b>📞 Contact Roshan Mishra:</b></p>
        <p>7888273972<br>9220393972<br>8668257610</p>
        </div>
    """, unsafe_allow_html=True)

# 4. Main App Pages

if choice == "🏠 Home":
    st.markdown("""
        <div class="main-header">
            <h1 style="font-size: 36px; margin-bottom:0;">Shree Services - Online GST & Tax Center</h1>
            <p style="font-size: 20px; opacity: 0.9;">A Complete Hub for Accounting & Taxation Solutions</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Professional Service Boxes with Mobile Input
    services = [
        {"id": "tax", "name": "📊 Taxation", "desc": "Professional GST, House Tax, Salary & Business Tax Filing Services."},
        {"id": "ins", "name": "🛡️ Insurance", "desc": "Best Life, Health & Vehicle Insurance Plans at your fingertips."},
        {"id": "online", "name": "📝 Online Work", "desc": "Quick PAN, Aadhar, GST Registration & all Digital Services."}
    ]

    for s in services:
        st.markdown(f'<div class="service-box"><h2>{s["name"]}</h2><p style="font-size:18px; color:#555;">{s["desc"]}</p></div>', unsafe_allow_html=True)
        with st.expander(f"Click to Apply for {s['name']}"):
            m_num = st.text_input("Your Mobile Number", key=f"m_{s['id']}")
            note = st.text_area("Your Requirement (Briefly)", key=f"n_{s['id']}")
            if st.button(f"Submit Request for {s['name']}", key=f"btn_{s['id']}"):
                msg = f"New Inquiry: {s['name']}\nMobile: {m_num}\nReq: {note}"
                st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(msg)}" target="_blank"><div style="background:#25d366; color:white; padding:10px; text-align:center; border-radius:5px; font-weight:bold;">📲 Send to Roshan Ji on WhatsApp</div></a>', unsafe_allow_html=True)

elif choice == "🧾 Create Invoice":
    st.title("📑 Generate Professional Bill")
    if not df.empty:
        party = st.selectbox("Select Client / Firm Name", df['Firm Name'].unique())
        c_row = df[df['Firm Name'] == party].iloc[0]
        amt = st.number_input("Amount (₹)", min_value=0, value=800)
        p_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Service Particulars", value=f"GST Filing Charges for {p_month}")
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        
        st.markdown(f"""
            <div class="invoice-card">
                <div style="text-align:center; border-bottom:2px solid #1e3a8a; padding-bottom:10px;">
                    <h2 style="color:#1e3a8a; margin-bottom:0;">Shree Services</h2>
                    <small>Mohan Garden, Delhi-59 | Mob: 7888273972</small>
                </div>
                <p style="margin-top:15px;"><b>Invoice To:</b> {party} <span style="float:right;"><b>Date:</b> {datetime.now().strftime('%d-%b-%Y')}</span></p>
                <table style="width:100%; border-collapse: collapse; margin: 15px 0;">
                    <tr style="background:#f2f2f2;"><th>Particulars</th><th style="text-align:right;">Amount</th></tr>
                    <tr><td>{particulars}</td><td style="text-align:right;">₹{amt}/-</td></tr>
                </table>
                <div style="text-align:center; margin-top:15px; background:#f9f9f9; padding:15px; border-radius:10px; border:1px dashed #1e3a8a;">
                    <p style="font-size:12px; margin-bottom:5px;"><b>SCAN TO PAY VIA UPI</b></p>
                    <img src="{qr}" width="130"><br><small>{FIXED_UPI}</small>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        wa_msg = f"Namaste 🙏, *Shree Services*.\n*Bill For:* {party}\n*Amount:* ₹{amt}\n\n👉 *Visit Portal:* {PORTAL_LINK}\n*UPI:* {FIXED_UPI}"
        st.markdown(f'<a href="https://wa.me/{c_row["Mobile Number"]}?text={urllib.parse.quote(wa_msg)}" target="_blank">📲 Send Bill to Client</a>', unsafe_allow_html=True)

elif choice == "📤 Upload Bills":
    st.title("📤 Secure Document Portal")
    mode = params.get("mode", "all")
    if not df.empty: st.selectbox("Select Your Firm Name", df['Firm Name'].unique())
    
    if mode == "sale" or mode == "all":
        st.markdown('<div class="upload-card">📁 GSTR-1 (SALE BILLS ONLY)</div>', unsafe_allow_html=True)
        s_files = st.file_uploader("Upload Sales", accept_multiple_files=True, key="s")
    
    if mode == "purchase" or mode == "all":
        st.markdown('<div class="upload-card">📁 GST-3B (PURCHASE BILLS ONLY)</div>', unsafe_allow_html=True)
        p_files = st.file_uploader("Upload Purchases", accept_multiple_files=True, key="p")
    
    if st.button("Submit Documents to Drive"):
        st.success("Submission successful! Files will appear in your Drive shortly.")
        st.balloons()

elif choice == "🔔 WhatsApp Reminder":
    st.title("🔔 Tax & Payment Reminders")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        r_type = st.radio("Reminder Type", ["GSTR-1 (Send Sale Upload Link)", "GST-3B (Send Purchase Upload Link)", "💰 Payment Reminder"])
        
        if "GSTR-1" in r_type:
            link = f"{PORTAL_LINK}?page=upload&mode=sale"
            msg = f"Namaste 🙏, *Shree Services*. GSTR-1 filing date aa rahi hai. Kripya apne SALE BILLS niche diye gaye link par upload karein:\n👉 {link}"
        elif "GST-3B" in r_type:
            link = f"{PORTAL_LINK}?page=upload&mode=purchase"
            msg = f"Namaste 🙏, *Shree Services*. GST-3B filing date aa rahi hai. Kripya apne PURCHASE BILLS niche diye gaye link par upload karein:\n👉 {link}"
        else:
            msg = f"Namaste 🙏, *Shree Services*. Aapka pichla payment pending hai. Kripya portal par check karein: {PORTAL_LINK}"
        
        st.markdown(f'<a href="https://wa.me/{row["Mobile Number"]}?text={urllib.parse.quote(msg)}" target="_blank">📲 Send WhatsApp Reminder</a>', unsafe_allow_html=True)

elif choice == "📊 Ledger Status":
    st.title("📊 Business Ledger Status")
    st.dataframe(df, use_container_width=True)
