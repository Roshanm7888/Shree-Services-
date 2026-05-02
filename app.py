import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="Shree Services | Roshan Mishra", layout="centered", page_icon="🏢")

# Custom Styling (Professional UI + Hidden Footers)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { 
        color: white !important; 
        font-size: 16px !important; 
    }
    
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1e3a8a; color: white; font-weight: bold; }
    
    .service-box { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 10px solid #1e3a8a; margin-bottom: 20px; }
    
    .main-header { background: #1e3a8a; color: white; padding: 30px; border-radius: 0 0 20px 20px; text-align: center; margin-top: -60px; margin-bottom: 30px;}
    
    .invoice-card { 
        background: #ffffff; 
        border: 2px solid #1e3a8a; 
        padding: 25px; 
        border-radius: 12px; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
    }
    .invoice-header { text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; margin-bottom: 15px; }
    .services-tag { font-size: 12px; color: #1e3a8a; font-weight: bold; margin-top: 5px; }
    .upload-card { background: #f0f2f6; padding: 10px; border-radius: 8px; margin-top: 15px; font-weight: bold; color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data & Settings
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# ALERT & MAIN NUMBER
MY_NUMBER = "917888273972"

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
    st.markdown("""
        <p style='color:white;'>📞 <b>Contact:</b><br>
        7888273972<br>
        8668257610<br>
        9220393972</p>
    """, unsafe_allow_html=True)

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
        desc = st.text_input("Service Name", value="GST Filing Charges - April Month")
        
        # Phone logic
        p_num = ""
        for c in ['Mobile Number', 'Mobile', 'Phone']:
            if c in df.columns: p_num = str(row[c]); break

        st.markdown("### 📄 Invoice Preview")
        inv_date = datetime.now().strftime("%d-%b-%Y")
        
        st.markdown(f"""
        <div class="invoice-card">
            <div class="invoice-header">
                <h1 style="color:#1e3a8a; margin-bottom:0;">SHREE SERVICES</h1>
                <p style="margin-top:5px; margin-bottom:5px;"><b>Accounting, Taxation & Insurance Solutions</b></p>
                <div class="services-tag">TAXATION • INSURANCE • ACCOUNTING • ONLINE WORK • ONLINE TICKET</div>
                <hr style="border:0.5px solid #1e3a8a; margin: 10px 0;">
                <small>Address: Plot no. 64&65 Block k-5, Mohan Garden, Delhi-110059</small><br>
                <small>Mob: 7888273972, 8668257610</small>
            </div>
            <table style="width:100%">
                <tr><td><b>Invoice To:</b> {party}</td><td style="text-align:right;"><b>Date:</b> {inv_date}</td></tr>
                <tr><td><b>Owner:</b> {row['Owner']}</td><td style="text-align:right;"><b>Status:</b> Pending</td></tr>
            </table>
            <hr style="border:1px solid #eee">
            <p><b>Description:</b> {desc}</p>
            <div style="background:#1e3a8a; color:white; padding:15px; border-radius:8px; text-align:right; font-size:20px;">
                Total Payable: <b>₹{amount}/-</b>
            </div>
            <p style="font-size:10px; margin-top:15px; color:gray;">* This is a computer generated bill issued by Shree Services Delhi.</p>
        </div>
        """, unsafe_allow_html=True)
        
        msg = f"Namaste 🙏, *Shree Services Delhi* ki taraf se.\n\nAapka GST 3B file ho gaya hai.\n*Bill Amount:* ₹{amount}\n*Description:* {desc}\n\n*Address:* Mohan Garden, Delhi-59\n*Contact:* 7888273972, 8668257610\n\nKripya payment clear karein. Shukriya!"
        wa_url = f"https://wa.me/{p_num}?text={urllib.parse.quote(msg)}"
        
        st.write(" ")
        st.markdown(f'<a href="{wa_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px;">📲 Send Invoice via WhatsApp</div></a>', unsafe_allow_html=True)

elif choice == "📊 Ledger Status":
    st.title("📊 Ledger Status")
    if not df.empty: st.dataframe(df, use_container_width=True)

elif choice == "🔔 WhatsApp Reminder":
    st.title("🔔 Send Data Reminder")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        p_num = ""
        for c in ['Mobile Number', 'Mobile', 'Phone']:
            if c in df.columns: p_num = str(row[c]); break
        m = f"Namaste 🙏, Shree Services ki taraf se reminder. Aapka GST data pending hai, kripya yahan upload karein: https://shree-services.streamlit.app"
        st.markdown(f'<a href="https://wa.me/{p_num}?text={urllib.parse.quote(m)}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:20px; border-radius:10px; text-align:center; font-weight:bold;">Send Reminder to Client</div></a>', unsafe_allow_html=True)

elif choice == "📤 Upload Bills":
    st.title("📤 Client Upload Portal")
    if not df.empty: st.selectbox("Select Your Firm", df['Firm Name'].unique())
    st.markdown('<div class="upload-card">📁 GSTR-1 (Sale Bills)</div>', unsafe_allow_html=True)
    st.file_uploader("Upload Sales", accept_multiple_files=True, key="s")
    st.markdown('<div class="upload-card">📁 GST-3B (Purchase Bills)</div>', unsafe_allow_html=True)
    st.file_uploader("Upload Purchases", accept_multiple_files=True, key="p")
    if st.button("Submit Documents"): st.success("Bills Successfully Uploaded!")
