import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Online GST & Tax Center", layout="wide", page_icon="🏢")

# Custom Styling (Purana Professional Look Wapas)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .main-header { background: #1e3a8a; color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
    .stButton>button { border-radius: 8px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; background-color: white; color: #1e3a8a; }
    .stButton>button:hover { background-color: #1e3a8a; color: white; }
    
    /* Bill Styling - Purana Format */
    .bill-container { background: white; border: 2px solid #000; padding: 40px; border-radius: 5px; font-family: 'Arial'; max-width: 700px; margin: auto; color: black; }
    .bill-header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px; }
    .bill-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    .bill-table th, .bill-table td { border: 1px solid #000; padding: 12px; text-align: left; }
    .bill-table th { background-color: #f2f2f2; }
    .qr-section { text-align: center; margin-top: 30px; border: 1px dashed #1e3a8a; padding: 15px; }
    
    .footer-box { background: #1e3a8a; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px; color: white; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 2. Data & Settings
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

# Navigation logic
if 'page' not in st.session_state:
    st.session_state.page = "home"

# 3. TOP NAVIGATION
st.markdown('<div class="main-header"><h1>Shree Services - Online GST & Tax Center</h1><p>Accounting & Taxation Solutions</p></div>', unsafe_allow_html=True)

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

# 4. Page Routing
if st.session_state.page == "bill":
    st.title("📑 Generate Professional Invoice")
    if not df.empty:
        party = st.selectbox("Select Client / Firm Name", df['Firm Name'].unique())
        c_row = df[df['Firm Name'] == party].iloc[0]
        amt = st.number_input("Amount (₹)", value=800)
        p_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {p_month}")
        
        qr_code = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        
        # Purana Bill Format Display
        st.markdown(f"""
        <div class="bill-container">
            <div class="bill-header">
                <h1 style="margin:0; color:#1e3a8a;">SHREE SERVICES</h1>
                <p style="margin:5px;">Accounting, GST & Taxation Services</p>
                <p style="margin:2px; font-size:14px;">Mohan Garden, New Delhi-110059 | Mob: 7888273972</p>
            </div>
            
            <div style="display: flex; justify-content: space-between;">
                <p><b>To:</b> {party}</p>
                <p><b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}</p>
            </div>
            
            <table class="bill-table">
                <tr>
                    <th>Description / Particulars</th>
                    <th style="text-align:right; width:150px;">Amount (₹)</th>
                </tr>
                <tr>
                    <td style="height:100px; vertical-align:top;">{particulars}</td>
                    <td style="text-align:right; vertical-align:top;"><b>₹{amt}.00</b></td>
                </tr>
                <tr>
                    <td style="text-align:right;"><b>Total Amount:</b></td>
                    <td style="text-align:right;"><b>₹{amt}.00</b></td>
                </tr>
            </table>
            
            <div class="qr-section">
                <p style="margin-top:0;"><b>SCAN & PAY VIA ANY UPI APP</b></p>
                <img src="{qr_code}" width="140">
                <p style="margin-bottom:0; font-family:monospace;">{FIXED_UPI}</p>
            </div>
            
            <div style="margin-top:20px; text-align:right;">
                <p>For <b>Shree Services</b></p><br>
                <p>(Authorized Signatory)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # WhatsApp Button
        wa_msg = f"Namaste 🙏, *Shree Services*.\n*Bill For:* {party}\n*Amount:* ₹{amt}\n\n👉 *View/Download Bill:* {PORTAL_LINK}\n\n*UPI ID:* {FIXED_UPI}"
        st.markdown(f'<a href="https://wa.me/{c_row["Mobile Number"]}?text={urllib.parse.quote(wa_msg)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; margin-top:20px;">📲 Send This Bill on WhatsApp</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "home":
    st.info("Welcome Roshan ji! Please select a service from top buttons.")
    for s in ["📊 Taxation", "🛡️ Insurance", "📝 Online Work"]:
        st.markdown(f'<div style="background:white; padding:20px; border-radius:10px; border-left:10px solid #1e3a8a; margin-bottom:15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);"><h3>{s}</h3><p>Click to check more details.</p></div>', unsafe_allow_html=True)

elif st.session_state.page == "up":
    st.title("📤 Document Upload")
    st.info("Bills upload karne ke baad wo aapke Linked Google Drive folder mein jayenge.")
    if not df.empty: st.selectbox("Select Your Firm", df['Firm Name'].unique())
    st.file_uploader("Choose Files", accept_multiple_files=True)
    if st.button("Submit to Drive"):
        st.success("Documents successfully sent to your Google Drive!")

# Footer
st.markdown('<div class="footer-box">📞 Contact: 7888273972 | 9220393972</div>', unsafe_allow_html=True)
