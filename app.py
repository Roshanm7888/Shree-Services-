import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Online GST & Tax Center", layout="wide", page_icon="🏢")

# Custom Styling (Keval Header aur Bill fix kiya hai)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    .main-header { background: #1e3a8a; color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
    .stButton>button { border-radius: 8px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; background-color: white; color: #1e3a8a; }
    .stButton>button:hover { background-color: #1e3a8a; color: white; }
    
    .service-box { background: white; padding: 20px; border-radius: 12px; border-left: 10px solid #1e3a8a; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .footer-box { background: #1e3a8a; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px; color: white; font-weight: bold;}
    .upload-card { background: #f0f4f8; padding: 20px; border-radius: 10px; border: 2px dashed #1e3a8a; margin-bottom: 15px; font-weight: bold; color: #1e3a8a; }
    
    /* Invoice Professional Style */
    .bill-container { background: white; border: 2px solid #333; padding: 40px; font-family: 'Arial', sans-serif; color: #000; width: 95%; margin: auto; }
    .bill-header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
    .bill-table { width: 100%; border-collapse: collapse; margin: 20px 0; border: 1px solid #333; }
    .bill-table th, .bill-table td { border: 1px solid #333; padding: 12px; text-align: left; }
    .bill-table th { background-color: #f2f2f2; }
    .qr-section { text-align: center; margin-top: 20px; border: 1px dashed #1e3a8a; padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data & Settings
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
PORTAL_LINK = "https://shree-services.streamlit.app"
FIXED_UPI = "7888273972-2@ybl"

@st.cache_data(ttl=10)
def load_data():
    try:
        d = pd.read_csv(SHEET_URL)
        d.columns = d.columns.str.strip()
        return d
    except: return pd.DataFrame()
df = load_data()

params = st.query_params
if 'page' not in st.session_state:
    st.session_state.page = params.get("page", "home")

# 3. TOP HEADER (Wahi Header jo kal dal rahe they)
st.markdown("""
    <div class="main-header">
        <h1>Shree Services - Online GST & Tax Center</h1>
        <p style="font-size:20px; margin-top:10px;">A Complete Hub for Accounting & Taxation Solutions</p>
    </div>
    """, unsafe_allow_html=True)

# TOP NAVIGATION
col1, col2, col3, col4, col5 = st.columns(5)
with col1: 
    if st.button("🏠 HOME"): st.session_state.page = "home"
with col2: 
    if st.button("🧾 BILL"): st.session_state.page = "bill"
with col3: 
    if st.button("🔔 REMINDER"): st.session_state.page = "rem"
with col4: 
    if st.button("📤 UPLOAD"): st.session_state.page = "up"
with col5: 
    if st.button("📊 LEDGER"): st.session_state.page = "led"

st.markdown("---")

# 4. PAGE LOGIC
if st.session_state.page == "home":
    st.write("### Choose a Service")
    services = ["📊 Taxation (GST/Income Tax)", "🛡️ Insurance (Life/Health)", "📝 Online Work (PAN/Aadhar)"]
    for s in services:
        st.markdown(f'<div class="service-box"><h3>{s}</h3></div>', unsafe_allow_html=True)
        with st.expander(f"Apply for {s}"):
            m_val = st.text_input("Mobile Number", key=f"m_{s}")
            r_val = st.text_area("What is your requirement?", key=f"r_{s}")
            if st.button(f"Submit {s} Request"):
                msg = f"New Request for {s}\nMobile: {m_val}\nDetails: {r_val}"
                st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(msg)}" target="_blank"><div style="background:#25d366; color:white; padding:10px; text-align:center; border-radius:10px; font-weight:bold;">📲 Send to Roshan Mishra</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "bill":
    st.title("📑 Generate Professional Bill")
    if not df.empty:
        party = st.selectbox("Select Party Name", df['Firm Name'].unique())
        c_row = df[df['Firm Name'] == party].iloc[0]
        amt = st.number_input("Amount (₹)", value=800)
        p_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {p_month}")
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        
        # Professional Bill Template
        bill_html = f"""
        <div class="bill-container">
            <div class="bill-header">
                <h1 style="margin:0; color:#1e3a8a;">SHREE SERVICES</h1>
                <p style="margin:5px; font-weight:bold;">Accounting, GST & Taxation Services</p>
                <p style="margin:2px; font-size:14px;">Mohan Garden, New Delhi-110059 | Mob: 7888273972, 8668257610</p>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px; font-weight:bold;">
                <div>To: {party}</div>
                <div>Date: {datetime.now().strftime('%d/%m/%Y')}</div>
            </div>
            <table class="bill-table">
                <tr><th>Description / Particulars</th><th style="text-align:right;">Amount (₹)</th></tr>
                <tr><td style="height:100px; vertical-align:top;">{particulars}</td><td style="text-align:right; vertical-align:top;"><b>₹{amt}.00</b></td></tr>
                <tr><td style="text-align:right; font-weight:bold;">Total Amount:</td><td style="text-align:right; font-weight:bold;">₹{amt}.00</td></tr>
            </table>
            <div class="qr-section">
                <p style="margin-top:0;"><b>SCAN & PAY VIA ANY UPI APP</b></p>
                <img src="{qr_url}" width="130"><br><b>UPI ID: {FIXED_UPI}</b>
            </div>
            <div style="margin-top:20px; text-align:right;"><p>For <b>Shree Services</b></p><br><p>(Authorized Signatory)</p></div>
        </div>"""
        st.markdown(bill_html, unsafe_allow_html=True)
        
        wa_b = f"Namaste 🙏, *Shree Services*.\n*Bill For:* {party}\n*Amount:* ₹{amt}\n*Link:* {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/{c_row["Mobile Number"]}?text={urllib.parse.quote(wa_b)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; margin-top:10px;">📲 Send Bill on WhatsApp</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "up":
    st.title("📤 Document Portal")
    mode = params.get("mode", "all")
    if not df.empty: st.selectbox("Select Firm", df['Firm Name'].unique())
    if mode in ["sale", "all"]:
        st.markdown('<div class="upload-card">📁 SALE BILLS (GSTR-1)</div>', unsafe_allow_html=True)
        st.file_uploader("Upload Sale Files", accept_multiple_files=True, key="s_up")
    if mode in ["purchase", "all"]:
        st.markdown('<div class="upload-card">📁 PURCHASE BILLS (GST-3B)</div>', unsafe_allow_html=True)
        st.file_uploader("Upload Purchase Files", accept_multiple_files=True, key="p_up")
    if st.button("Submit Documents"): st.success("Bills Submitted Successfully!")

elif st.session_state.page == "rem":
    st.title("🔔 Reminders")
    if not df.empty:
        party = st.selectbox("Select Client", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        r_type = st.radio("Reminder Type", ["GSTR-1 (Sale)", "GST-3B (Purchase)", "Payment"])
        link = f"{PORTAL_LINK}?page=up&mode={'sale' if 'GSTR-1' in r_type else 'purchase' if 'GST-3B' in r_type else 'all'}"
        m = f"Namaste 🙏, *Shree Services*. Reminder for {r_type}. Click to upload/check: {link}"
        st.markdown(f'<a href="https://wa.me/{row["Mobile Number"]}?text={urllib.parse.quote(m)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center;">📲 Send Reminder</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "led":
    st.title("📊 Client Ledger Status")
    st.dataframe(df, use_container_width=True)

# 5. Permanent Footer
st.markdown('<div class="footer-box">📞 Contact Roshan Mishra: 7888273972 | 9220393972</div>', unsafe_allow_html=True)
