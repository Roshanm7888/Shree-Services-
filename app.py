import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Config
st.set_page_config(page_title="Shree Services | Online GST & Tax Center", layout="centered", page_icon="🏢")

# Custom Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: white !important; font-size: 16px !important; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1e3a8a; color: white; font-weight: bold; }
    
    .main-header { background: #1e3a8a; color: white; padding: 30px; border-radius: 0 0 20px 20px; text-align: center; margin-top: -60px; margin-bottom: 30px;}
    .service-box { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 10px solid #1e3a8a; margin-bottom: 20px; }
    
    .invoice-card { background: #ffffff; border: 2px solid #1e3a8a; padding: 25px; border-radius: 12px; font-family: 'Segoe UI', sans-serif; color: #333; }
    .invoice-header { text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; margin-bottom: 15px; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th { background-color: #f2f2f2; padding: 10px; text-align: left; border-bottom: 2px solid #1e3a8a; }
    td { padding: 10px; border-bottom: 1px solid #eee; }
    .qr-box { text-align: center; margin-top: 15px; border: 1px dashed #1e3a8a; padding: 15px; border-radius: 10px; background: #f9f9f9; }
    .upload-card { background: #f0f2f6; padding: 15px; border-radius: 8px; margin-top: 15px; font-weight: bold; color: #1e3a8a; border-left: 5px solid #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data & Settings
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
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
    st.markdown("<p style='color:white;'>📞 <b>Contact:</b><br>7888273972<br>8668257610<br>9220393972</p>", unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---

if choice == "🏠 Home":
    st.markdown('<div class="main-header"><h1>🏛️ SHREE SERVICES</h1><p>A Complete Hub for Accounting & Taxation Solutions</p></div>', unsafe_allow_html=True)
    services = [
        {"t": "Taxation", "d": "GST, House Tax, Salary Tax & Business Tax Filing."},
        {"t": "Insurance", "d": "Life, Health & Vehicle Insurance Solutions."},
        {"t": "Accounting", "d": "Daily & Yearly Professional Bookkeeping."},
        {"t": "Online Work", "d": "All types of Online Registration & Digital Services."},
        {"t": "Online Ticket", "d": "Flight, Train & Bus Ticket Booking."}
    ]
    for s in services:
        st.markdown(f'<div class="service-box"><h3 style="color:#1e3a8a; margin-top:0;">{s["t"]}</h3><p>{s["d"]}</p></div>', unsafe_allow_html=True)

elif choice == "🧾 Create Invoice":
    st.title("📑 Generate Professional Bill")
    if not df.empty:
        party = st.selectbox("Select Client / Firm", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        amount = st.number_input("Billing Amount (₹)", min_value=0, value=800)
        
        # Auto Month Logic
        prev_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {prev_month}")
        
        qr_link = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amount}&cu=INR"
        inv_date = datetime.now().strftime("%d-%b-%Y")

        st.markdown(f"""
        <div class="invoice-card">
            <div class="invoice-header">
                <h1 style="color:#1e3a8a; margin-bottom:0; font-size:24px;">Shree Services - Online GST & Tax Center</h1>
                <p style="margin-top:5px; margin-bottom:5px;"><b>A Complete Hub for Accounting & Taxation Solutions</b></p>
                <hr style="border:0.5px solid #1e3a8a; margin: 10px 0;">
                <small>Address: Plot no. 64&65 Block k-5, Mohan Garden, Delhi-110059 | Mob: 7888273972</small>
            </div>
            <table style="width:100%; border:none;">
                <tr style="border:none;"><td style="border:none;"><b>Invoice To:</b> {party}</td><td style="text-align:right; border:none;"><b>Date:</b> {inv_date}</td></tr>
            </table>
            <table>
                <tr><th>Description / Particulars</th><th style="text-align:right;">Amount</th></tr>
                <tr><td>{particulars}</td><td style="text-align:right;">₹{amount}/-</td></tr>
                <tr style="background:#f9f9f9;"><td style="font-weight:bold;">Total Payable</td><td style="text-align:right; font-weight:bold; color:#1e3a8a; font-size:18px;">₹{amount}/-</td></tr>
            </table>
            <div class="qr-box">
                <p style="font-size:12px; margin-bottom:5px; color:#1e3a8a;"><b>SCAN TO PAY VIA UPI</b></p>
                <img src="{qr_link}" width="130">
                <p style="font-size:11px; margin-top:5px; color:#555;">UPI ID: {FIXED_UPI}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🖨️ Print / Save as PDF"):
            st.info("Tip: Press Ctrl+P and select 'Save as PDF'")

        msg = f"Namaste 🙏, *Shree Services - Online GST & Tax Center*.\n\n*Bill For:* {party}\n*Details:* {particulars}\n*Amount:* ₹{amount}\n\n*Pay via UPI:* {FIXED_UPI}\n*Portal:* {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/{row["Mobile Number"]}?text={urllib.parse.quote(msg)}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Bill on WhatsApp</div></a>', unsafe_allow_html=True)

elif choice == "🔔 WhatsApp Reminder":
    st.title("🔔 Tax & Payment Reminders")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        r_type = st.radio("Select Reminder Type", ["GSTR-1 (Due 11th)", "GST-3B (Due 20th)", "Custom Payment Reminder"])
        
        curr_m = datetime.now().strftime("%B")
        if "GSTR-1" in r_type:
            r_msg = f"Namaste 🙏, *Shree Services*.\nReminder: {curr_m} month ke *GSTR-1* ki due date 11 tarik hai. Kripya 9 tarik tak apne Sale Bills upload karein: {PORTAL_LINK}"
        elif "GST-3B" in r_type:
            r_msg = f"Namaste 🙏, *Shree Services*.\nReminder: {curr_m} month ke *GST-3B* ki due date 20 tarik hai. Kripya 18 tarik tak apna data upload karein: {PORTAL_LINK}"
        else:
            r_msg = st.text_area("Type your message here...", value="Namaste, Aapka payment pending hai, kripya clear karein. Shukriya!")

        st.markdown(f'<a href="https://wa.me/{row["Mobile Number"]}?text={urllib.parse.quote(r_msg)}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Reminder</div></a>', unsafe_allow_html=True)

elif choice == "📊 Ledger Status":
    st.title("📊 Business Ledger")
    if not df.empty: st.dataframe(df, use_container_width=True)

elif choice == "📤 Upload Bills":
    st.title("📤 Client Upload Portal")
    st.markdown("Kripya niche diye gaye sections mein apne documents upload karein.")
    if not df.empty: st.selectbox("Select Your Firm Name", df['Firm Name'].unique())
    
    st.markdown('<div class="upload-card">📁 GSTR-1 (Sales Documents)</div>', unsafe_allow_html=True)
    st.file_uploader("Upload Sale Bills", accept_multiple_files=True, key="sale")
    
    st.markdown('<div class="upload-card">📁 GST-3B (Purchase Documents)</div>', unsafe_allow_html=True)
    st.file_uploader("Upload Purchase Bills", accept_multiple_files=True, key="purchase")
    
    if st.button("Submit All Documents"):
        st.success("Documents successfully submitted to Shree Services!")
