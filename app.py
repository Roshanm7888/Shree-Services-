import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="Shree Services | Online GST & Tax Center", layout="centered", page_icon="🏢")

# Custom Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: white !important; font-size: 16px !important; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1e3a8a; color: white; font-weight: bold; }
    .service-box { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 10px solid #1e3a8a; margin-bottom: 20px; }
    .main-header { background: #1e3a8a; color: white; padding: 30px; border-radius: 0 0 20px 20px; text-align: center; margin-top: -60px; margin-bottom: 30px;}
    .invoice-card { background: #ffffff; border: 2px solid #1e3a8a; padding: 25px; border-radius: 12px; font-family: 'Segoe UI', sans-serif; color: #333; }
    .invoice-header { text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; margin-bottom: 15px; }
    .qr-box { text-align: center; margin-top: 15px; border: 1px dashed #1e3a8a; padding: 15px; border-radius: 10px; background: #f9f9f9; }
    @media print { .no-print { display: none !important; } .invoice-card { border: none !important; } }
    </style>
    """, unsafe_allow_html=True)

# 2. Data & Settings
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
MY_NUMBER = "917888273972"
FIXED_UPI = "7888273972-2@ybl"
PORTAL_LINK = "https://shree-services.streamlit.app"

@st.cache_data(ttl=30)
def load_data():
    try:
        d = pd.read_csv(URL)
        d.columns = d.columns.str.strip()
        return d
    except: return pd.DataFrame()

df = load_data()

# 3. SIDEBAR MENU
with st.sidebar:
    st.markdown("<h2 style='color:white;'>📋 MENU</h2>", unsafe_allow_html=True)
    choice = st.radio("", ["🏠 Home", "📊 Ledger Status", "🧾 Create Invoice", "🔔 WhatsApp Reminder", "📤 Upload Bills"], index=0)
    st.markdown("---")
    st.markdown(f"<p style='color:white;'>📞 7888273972<br>8668257610<br>9220393972</p>", unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---

if choice == "🏠 Home":
    st.markdown('<div class="main-header"><h1>🏛️ SHREE SERVICES</h1><p>A Complete Hub for Accounting & Taxation Solutions</p></div>', unsafe_allow_html=True)
    services = [{"t": "Taxation", "d": "GST & Income Tax Filing."}, {"t": "Insurance", "d": "Life & Health Insurance."}, {"t": "Accounting", "d": "Professional Bookkeeping."}]
    for s in services:
        st.markdown(f'<div class="service-box"><h3>{s["t"]}</h3><p>{s["d"]}</p></div>', unsafe_allow_html=True)

elif choice == "🧾 Create Invoice":
    st.title("📑 Generate Professional Bill")
    if not df.empty:
        party = st.selectbox("Select Client", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        amount = st.number_input("Amount (₹)", min_value=0, value=800)
        desc = st.text_input("Service Name", value="GST Filing Charges - April Month")
        qr_link = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amount}&cu=INR"

        st.markdown("### 📄 Invoice Preview")
        inv_date = datetime.now().strftime("%d-%b-%Y")
        
        invoice_html = f"""
        <div class="invoice-card">
            <div class="invoice-header">
                <h2 style="color:#1e3a8a; margin-bottom:0;">Shree Services - Online GST & Tax Center</h2>
                <p><b>Accounting, Taxation & Insurance Solutions</b></p>
                <hr style="border:0.5px solid #1e3a8a;">
                <small>Address: Plot no. 64&65 Block k-5, Mohan Garden, Delhi-110059 | Mob: 7888273972</small>
            </div>
            <table style="width:100%">
                <tr><td><b>Invoice To:</b> {party}</td><td style="text-align:right;"><b>Date:</b> {inv_date}</td></tr>
            </table>
            <p style="margin-top:20px;"><b>Description:</b> {desc}</p>
            <div style="background:#1e3a8a; color:white; padding:15px; border-radius:8px; text-align:right; font-size:20px;">Total: ₹{amount}/-</div>
            <div class="qr-box">
                <p style="font-size:12px; margin-bottom:5px;"><b>SCAN TO PAY</b></p>
                <img src="{qr_link}" width="120">
                <p style="font-size:10px; margin-top:5px;">UPI ID: {FIXED_UPI}</p>
            </div>
        </div>
        """
        st.markdown(invoice_html, unsafe_allow_html=True)
        
        # WhatsApp Message
        msg = f"Namaste 🙏, *Shree Services - Online GST & Tax Center*.\nAapka GST 3B file ho gaya hai.\n*Bill Amount:* ₹{amount}\n*Description:* {desc}\n\n*Pay via UPI:* {FIXED_UPI}\n*Portal Link:* {PORTAL_LINK}"
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<a href="https://wa.me/{row["Mobile Number"]}?text={urllib.parse.quote(msg)}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send on WhatsApp</div></a>', unsafe_allow_html=True)
        with col2:
            if st.button("🖨️ Print / Download Bill"):
                st.write("Tip: Press Ctrl+P (or Share -> Print) and select 'Save as PDF'")

elif choice == "📊 Ledger Status":
    st.title("📊 Ledger Status")
    if not df.empty: st.dataframe(df, use_container_width=True)

elif choice == "🔔 WhatsApp Reminder":
    st.title("🔔 Send Reminder")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        m = f"Namaste 🙏, Shree Services reminder. Aapka GST data pending hai: {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/{row["Mobile Number"]}?text={urllib.parse.quote(m)}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">Send Reminder</div></a>', unsafe_allow_html=True)

elif choice == "📤 Upload Bills":
    st.title("📤 Client Upload Portal")
    if not df.empty: st.selectbox("Select Your Firm", df['Firm Name'].unique())
    st.file_uploader("Upload Sales", accept_multiple_files=True, key="s")
    st.file_uploader("Upload Purchases", accept_multiple_files=True, key="p")
    if st.button("Submit"): st.success("Bills Uploaded!")
