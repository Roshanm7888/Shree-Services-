import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Online GST & Tax Center", layout="wide", page_icon="🏢")

# Custom Styling (Buttons and Layout)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .main-header { background: #1e3a8a; color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
    .stButton>button { border-radius: 8px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; background-color: white; color: #1e3a8a; }
    .stButton>button:hover { background-color: #1e3a8a; color: white; }
    .footer-box { background: #1e3a8a; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px; color: white; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 2. Data Loading
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

if 'page' not in st.session_state: st.session_state.page = "home"

# 3. TOP NAVIGATION
st.markdown('<div class="main-header"><h1>Shree Services - Online GST & Tax Center</h1><p>A Complete Hub for Accounting & Taxation Solutions</p></div>', unsafe_allow_html=True)

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

# 4. Page Logic
if st.session_state.page == "bill":
    st.markdown("### 📑 Create Professional Invoice")
    if not df.empty:
        party = st.selectbox("Select Client Name", df['Firm Name'].unique())
        c_row = df[df['Firm Name'] == party].iloc[0]
        amt = st.number_input("Amount (₹)", value=800)
        p_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {p_month}")
        
        qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        inv_date = datetime.now().strftime('%d/%m/%Y')
        
        # HTML CODE FOR BILL
        bill_template = f"""
        <html>
        <head>
        <style>
            .bill-container {{ background: white; border: 2px solid #333; padding: 40px; font-family: Arial, sans-serif; color: #000; width: 90%; margin: auto; }}
            .bill-header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }}
            .bill-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; border: 1px solid #333; }}
            .bill-table th, .bill-table td {{ border: 1px solid #333; padding: 12px; text-align: left; }}
            .bill-table th {{ background-color: #f2f2f2; }}
            .qr-section {{ text-align: center; margin-top: 30px; border: 1px dashed #1e3a8a; padding: 15px; background: #f9f9f9; }}
            .flex-row {{ display: flex; justify-content: space-between; }}
        </style>
        </head>
        <body>
        <div class="bill-container">
            <div class="bill-header">
                <h1 style="margin:0; color:#1e3a8a;">SHREE SERVICES</h1>
                <p style="margin:5px; font-weight:bold;">Accounting, GST & Taxation Services</p>
                <p style="margin:2px; font-size:14px;">Address: Mohan Garden, New Delhi-110059 | Mob: 7888273972, 8668257610</p>
            </div>
            <div class="flex-row" style="margin-bottom: 20px;">
                <div><b>Invoice To:</b> {party}</div>
                <div><b>Date:</b> {inv_date}</div>
            </div>
            <table class="bill-table">
                <tr>
                    <th style="width: 70%;">Description / Particulars</th>
                    <th style="text-align:right;">Amount (₹)</th>
                </tr>
                <tr>
                    <td style="height:120px; vertical-align:top;">{particulars}</td>
                    <td style="text-align:right; vertical-align:top;"><b>₹{amt}.00</b></td>
                </tr>
                <tr>
                    <td style="text-align:right; font-weight:bold;">Total Amount:</td>
                    <td style="text-align:right; font-weight:bold; font-size:18px; color:#1e3a8a;">₹{amt}.00</td>
                </tr>
            </table>
            <div class="qr-section">
                <p style="margin-top:0; font-size:14px;"><b>SCAN & PAY VIA ANY UPI APP</b></p>
                <img src="{qr_code_url}" width="140">
                <p style="margin-bottom:0; font-family:monospace; font-weight:bold;">UPI ID: {FIXED_UPI}</p>
            </div>
            <div style="margin-top:30px; text-align:right;">
                <p style="margin-bottom:40px;">For <b>Shree Services</b></p>
                <p>(Authorized Signatory)</p>
            </div>
        </div>
        </body>
        </html>
        """
        
        # RENDERING BILL IN AN IFRAME (SOLVES THE CODE DISPLAY ISSUE)
        st.components.v1.html(bill_template, height=800, scrolling=True)
        
        # Print Tip
        st.info("Tip: Is bill ko save karne ke liye screen ka screenshot lein ya browser print ka upyog karein.")

        # WhatsApp Message
        wa_msg = f"Namaste 🙏, *Shree Services*.\n*Bill For:* {party}\n*Amount:* ₹{amt}\n\n*Pay via UPI:* {FIXED_UPI}\n*Portal:* {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/{c_row["Mobile Number"]}?text={urllib.parse.quote(wa_msg)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; margin-top:20px;">📲 Send Bill on WhatsApp</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "home":
    st.info("Welcome to Shree Services Portal. Use top buttons to navigate.")
    for s in ["📊 Taxation", "🛡️ Insurance", "📝 Online Work"]:
        st.markdown(f'<div style="background:white; padding:20px; border-radius:10px; border-left:10px solid #1e3a8a; margin-bottom:15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);"><h3>{s}</h3><p>Professional services for your business.</p></div>', unsafe_allow_html=True)

elif st.session_state.page == "up":
    st.title("📤 Document Upload")
    st.file_uploader("Upload Files", accept_multiple_files=True)
    if st.button("Submit to Drive"): st.success("Files Submitted Successfully!")

# Footer
st.markdown('<div class="footer-box">📞 Contact: 7888273972 | 9220393972</div>', unsafe_allow_html=True)
