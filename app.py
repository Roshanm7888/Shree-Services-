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
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: white !important; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #1e3a8a; color: white; font-weight: bold; }
    .invoice-card { background: #ffffff; border: 2px solid #1e3a8a; padding: 25px; border-radius: 12px; font-family: 'Segoe UI', sans-serif; }
    .invoice-header { text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th { background-color: #f2f2f2; border-bottom: 2px solid #1e3a8a; padding: 10px; text-align: left; }
    td { padding: 10px; border-bottom: 1px solid #eee; }
    .qr-box { text-align: center; margin-top: 15px; border: 1px dashed #1e3a8a; padding: 10px; }
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

# 3. SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='color:white;'>📋 MENU</h2>", unsafe_allow_html=True)
    choice = st.radio("", ["🏠 Home", "📊 Ledger Status", "🧾 Create Invoice", "🔔 WhatsApp Reminder", "📤 Upload Bills"])

# --- LOGIC ---

if choice == "🏠 Home":
    st.markdown("<h1 style='text-align:center; color:#1e3a8a;'>SHREE SERVICES</h1><p style='text-align:center;'>A Complete Hub for Accounting & Taxation Solutions</p>", unsafe_allow_html=True)

elif choice == "🧾 Create Invoice":
    st.title("📑 Create Invoice")
    if not df.empty:
        party = st.selectbox("Select Client", df['Firm Name'].unique())
        amount = st.number_input("Amount (₹)", min_value=0, value=800)
        
        # Automatic Month Logic
        current_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {current_month}")
        
        qr_link = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amount}&cu=INR"
        inv_date = datetime.now().strftime("%d-%b-%Y")

        st.markdown(f"""
        <div class="invoice-card">
            <div class="invoice-header">
                <h2 style="color:#1e3a8a;">Shree Services - Online GST & Tax Center</h2>
                <small>Mohan Garden, Delhi-110059 | Mob: 7888273972</small>
            </div>
            <p style="margin-top:10px;"><b>To:</b> {party} <span style="float:right;"><b>Date:</b> {inv_date}</span></p>
            <table>
                <tr><th>Particulars</th><th style="text-align:right;">Amount</th></tr>
                <tr><td>{particulars}</td><td style="text-align:right;">₹{amount}/-</td></tr>
                <tr><td style="font-weight:bold;">Total Payable</td><td style="text-align:right; font-weight:bold; color:#1e3a8a; font-size:18px;">₹{amount}/-</td></tr>
            </table>
            <div class="qr-box">
                <p style="font-size:12px;"><b>SCAN TO PAY VIA UPI</b></p>
                <img src="{qr_link}" width="120">
                <p style="font-size:10px;">UPI ID: {FIXED_UPI}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🖨️ Save as PDF / Print"):
            st.info("Press Ctrl+P and select 'Save as PDF'")

        # WhatsApp
        msg = f"Namaste 🙏, *Shree Services - Online GST & Tax Center*.\n\n*Bill For:* {party}\n*Description:* {particulars}\n*Amount:* ₹{amount}\n\n*Pay via UPI:* {FIXED_UPI}\n*Portal:* {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Invoice on WhatsApp</div></a>', unsafe_allow_html=True)

elif choice == "🔔 WhatsApp Reminder":
    st.title("🔔 Tax Reminders")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        p_num = str(row['Mobile Number'])
        
        # Reminder Types
        r_type = st.radio("Reminder Type", ["GSTR-1 Reminder (Due 11th)", "GST-3B Reminder (Due 20th)", "Payment Reminder"])
        
        current_month = datetime.now().strftime("%B")
        
        if r_type == "GSTR-1 Reminder (Due 11th)":
            r_msg = f"Namaste 🙏, *Shree Services*.\nReminder: {current_month} month ke *GSTR-1* ki due date 11 tarik hai. Kripya 9 tarik tak apne Sale Bills yahan upload karein: {PORTAL_LINK}"
        elif r_type == "GST-3B Reminder (Due 20th)":
            r_msg = f"Namaste 🙏, *Shree Services*.\nReminder: {current_month} month ke *GST-3B* ki due date 20 tarik hai. Kripya 18 tarik tak apna data clear karein aur bills yahan upload karein: {PORTAL_LINK}"
        else:
            r_msg = f"Namaste 🙏, Aapka payment pending hai, kripya check karein. Shukriya!"

        st.markdown(f'<a href="https://wa.me/{p_num}?text={urllib.parse.quote(r_msg)}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send {r_type}</div></a>', unsafe_allow_html=True)

elif choice == "📊 Ledger Status":
    st.title("📊 Ledger Status")
    st.dataframe(df, use_container_width=True)

elif choice == "📤 Upload Bills":
    st.title("📤 Upload Bills")
    st.file_uploader("Upload Sales/Purchase Bills")
    if st.button("Submit"): st.success("Uploaded!")
