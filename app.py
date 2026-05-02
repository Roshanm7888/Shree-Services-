import streamlit as st
import pandas as pd
import urllib.parse
import requests
import base64
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Online GST & Tax Center", layout="centered", page_icon="🏢")

# Custom Styling (Original Style Restored)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: white !important; font-size: 16px !important; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1e3a8a; color: white; font-weight: bold; }
    .main-header { background: #1e3a8a; color: white; padding: 30px; border-radius: 0 0 20px 20px; text-align: center; margin-top: -60px; margin-bottom: 30px;}
    .service-box { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 10px solid #1e3a8a; margin-bottom: 20px; text-align: left; }
    .invoice-card { background: #ffffff; border: 2px solid #1e3a8a; padding: 25px; border-radius: 12px; font-family: 'Segoe UI', sans-serif; color: #333; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th { background-color: #f2f2f2; padding: 10px; text-align: left; border-bottom: 2px solid #1e3a8a; }
    td { padding: 10px; border-bottom: 1px solid #eee; }
    .qr-box { text-align: center; margin-top: 15px; border: 1px dashed #1e3a8a; padding: 15px; border-radius: 10px; background: #f9f9f9; }
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

# Handle Direct Upload Page
query_params = st.query_params
nav_idx = 0
if query_params.get("page") == "upload": nav_idx = 4

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 style='color:white; text-align:center;'>📋 MENU</h2>", unsafe_allow_html=True)
    choice = st.radio("", ["🏠 Home", "📊 Ledger Status", "🧾 Create Invoice", "🔔 WhatsApp Reminder", "📤 Upload Bills"], index=nav_idx)

# 4. Navigation

if choice == "🏠 Home":
    st.markdown('<div class="main-header"><h1>🏛️ SHREE SERVICES</h1><p>Online GST & Tax Center</p></div>', unsafe_allow_html=True)
    
    # 1. Taxation Box
    with st.container():
        st.markdown('<div class="service-box"><h3>📊 Taxation</h3><p>GST, House Tax, Salary & Business Tax Filing.</p></div>', unsafe_allow_html=True)
        if st.checkbox("Apply for Taxation", key="tax"):
            st.text_input("Enter your Mobile Number", placeholder="99xxxxxx")
            st.button("Submit Request")

    # 2. Insurance Box
    with st.container():
        st.markdown('<div class="service-box"><h3>🛡️ Insurance</h3><p>Life, Health & Vehicle Insurance Solutions.</p></div>', unsafe_allow_html=True)
        if st.checkbox("Apply for Insurance", key="ins"):
            st.text_input("Enter Mobile Number", key="ins_mob")
            st.button("Request Callback")

    # 3. Online Work Box
    with st.container():
        st.markdown('<div class="service-box"><h3>📝 Online Work</h3><p>PAN, Aadhar & GST Registration Services.</p></div>', unsafe_allow_html=True)
        if st.checkbox("Apply for Online Work", key="online"):
            st.text_input("Enter Mobile Number", key="on_mob")
            st.button("Get Started")

elif choice == "🧾 Create Invoice":
    st.title("📑 Generate Invoice")
    if not df.empty:
        party = st.selectbox("Select Client", df['Firm Name'].unique())
        c_row = df[df['Firm Name'] == party].iloc[0]
        amount = st.number_input("Amount (₹)", min_value=0, value=800)
        prev_m = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {prev_m}")
        qr_link = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amount}&cu=INR"
        
        st.markdown(f"""<div class="invoice-card"><div style="text-align:center;"><h2>Shree Services</h2><small>Mohan Garden, Delhi | 7888273972</small></div><hr><p><b>To:</b> {party}</p><table><tr><th>Description</th><th style="text-align:right;">Amount</th></tr><tr><td>{particulars}</td><td style="text-align:right;">₹{amount}/-</td></tr></table><div class="qr-box"><img src="{qr_link}" width="120"><br><small>UPI: {FIXED_UPI}</small></div></div>""", unsafe_allow_html=True)
        
        # WhatsApp with 2 links
        inv_link = f"{PORTAL_LINK}?party={urllib.parse.quote(party)}&amt={amount}" # Download link placeholder
        wa_msg = f"Namaste 🙏, *Shree Services*.\n*Bill For:* {party}\n*Amount:* ₹{amount}\n\n1️⃣ *Download Invoice:* {inv_link}\n2️⃣ *Visit Portal:* {PORTAL_LINK}\n\n*UPI:* {FIXED_UPI}"
        st.markdown(f'<a href="https://wa.me/{c_row["Mobile Number"]}?text={urllib.parse.quote(wa_msg)}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Invoice (2 Links)</div></a>', unsafe_allow_html=True)

elif choice == "📤 Upload Bills":
    st.title("📤 Client Upload Portal")
    if not df.empty:
        firm_name = st.selectbox("Select Your Firm Name", df['Firm Name'].unique())
        uploaded_files = st.file_uploader("Upload Bills (PDF/Image)", accept_multiple_files=True)
        if st.button("Submit to Drive"):
            if uploaded_files:
                for f in uploaded_files:
                    f_b64 = base64.b64encode(f.read()).decode('utf-8')
                    payload = {"filename": f"{firm_name}_{f.name}", "mimetype": f.type, "data": f_b64}
                    try:
                        r = requests.post(SCRIPT_URL, json=payload, timeout=30)
                        if r.status_code == 200: st.success(f"{f.name} uploaded!")
                    except: st.error(f"Error uploading {f.name}")
                st.balloons()
            else: st.warning("Please select files!")

elif choice == "🔔 WhatsApp Reminder":
    st.title("🔔 Reminders")
    if not df.empty:
        party = st.selectbox("Select Client", df['Firm Name'].unique())
        c_row = df[df['Firm Name'] == party].iloc[0]
        r_type = st.radio("Type", ["GSTR-1", "GST-3B", "💰 Payment"])
        link = f"{PORTAL_LINK}?page=upload"
        if "Payment" in r_type: msg = f"Namaste 🙏, Aapka payment pending hai: {PORTAL_LINK}"
        else: msg = f"Namaste 🙏, GST date aa rahi hai, bills upload karein: {link}"
        st.markdown(f'<a href="https://wa.me/{c_row["Mobile Number"]}?text={urllib.parse.quote(msg)}" target="_blank">📲 Send</a>', unsafe_allow_html=True)

elif choice == "📊 Ledger Status":
    st.title("📊 Ledger Status")
    if not df.empty: st.dataframe(df)
        
