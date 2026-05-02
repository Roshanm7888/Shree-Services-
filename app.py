    import streamlit as st
import pandas as pd
import urllib.parse
import requests
import base64
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Online GST & Tax Center", layout="centered", page_icon="🏢")

# Custom Styling (Professional UI)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: white !important; font-size: 16px !important; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1e3a8a; color: white; font-weight: bold; }
    .main-header { background: #1e3a8a; color: white; padding: 30px; border-radius: 0 0 20px 20px; text-align: center; margin-top: -60px; margin-bottom: 30px;}
    .service-box { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 10px solid #1e3a8a; margin-bottom: 20px; }
    .info-alert { background-color: #e0f2fe; padding: 15px; border-radius: 10px; border-left: 5px solid #0369a1; color: #0369a1; font-weight: bold; margin-bottom: 20px; border: 1px solid #bae6fd; }
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
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
FIXED_UPI = "7888273972-2@ybl"
PORTAL_LINK = "https://shree-services.streamlit.app"
# Google Apps Script Web App Link
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwhzALmZZp2KvshihXxQR0QZzhN38aSTHb7KewLnJTO_pQ5t-C4Er4nJBjnfZI3VGXz/exec"

@st.cache_data(ttl=30)
def load_data():
    try:
        d = pd.read_csv(SHEET_URL)
        d.columns = d.columns.str.strip()
        return d
    except:
        return pd.DataFrame()

df = load_data()

# Handle Direct Upload Page access from WhatsApp Link
query_params = st.query_params
nav_idx = 0
if query_params.get("page") == "upload":
    nav_idx = 4

# 3. Sidebar Menu
with st.sidebar:
    st.markdown("<h2 style='color:white; text-align:center;'>📋 MENU</h2>", unsafe_allow_html=True)
    choice = st.radio("", ["🏠 Home", "📊 Ledger Status", "🧾 Create Invoice", "🔔 WhatsApp Reminder", "📤 Upload Bills"], index=nav_idx)
    st.markdown("---")
    st.markdown("<p style='color:white; text-align:center;'>📞 7888273972 | 9220393972</p>", unsafe_allow_html=True)

# 4. Navigation Logic

if choice == "🏠 Home":
    st.markdown('<div class="main-header"><h1>🏛️ SHREE SERVICES</h1><p>Online GST & Tax Center</p></div>', unsafe_allow_html=True)
    st.write("### Choose a service for more details:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Taxation"):
            st.markdown('<div class="info-alert">GST & Tax Filing Service.<br>📞 Contact: 7888273972 (Roshan Mishra)</div>', unsafe_allow_html=True)
        if st.button("🛡️ Insurance"):
            st.markdown('<div class="info-alert">Life, Health & Vehicle Insurance.<br>📞 Contact: 8668257610</div>', unsafe_allow_html=True)
    with col2:
        if st.button("📝 Accounting"):
            st.markdown('<div class="info-alert">Professional Bookkeeping Services.<br>📞 Contact: 9220393972</div>', unsafe_allow_html=True)
        if st.button("🌐 Online Work"):
            st.markdown('<div class="info-alert">PAN, Aadhar & GST Registration.</div>', unsafe_allow_html=True)
    st.markdown('<div class="service-box"><h3>🚆 Online Tickets</h3><p>Flight, Train & Bus Ticket Booking.</p></div>', unsafe_allow_html=True)

elif choice == "🧾 Create Invoice":
    st.title("📑 Generate Invoice")
    if not df.empty:
        party = st.selectbox("Select Client", df['Firm Name'].unique())
        c_row = df[df['Firm Name'] == party].iloc[0]
        amount = st.number_input("Amount (₹)", min_value=0, value=800)
        
        # Particulars with auto-month
        prev_m = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {prev_m}")
        
        qr_link = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amount}&cu=INR"
        
        st.markdown(f"""
        <div class="invoice-card">
            <div class="invoice-header">
                <h1 style="color:#1e3a8a; margin-bottom:0; font-size:24px;">Shree Services - Online GST & Tax Center</h1>
                <p style="margin-top:5px; margin-bottom:5px;"><b>A Complete Hub for Accounting & Taxation Solutions</b></p>
                <hr style="border:0.5px solid #1e3a8a; margin: 10px 0;">
                <small>Address: Plot no. 64&65 Block k-5, Mohan Garden, Delhi-110059 | Mob: 7888273972</small>
            </div>
            <p><b>To:</b> {party} <span style="float:right;"><b>Date:</b> {datetime.now().strftime('%d-%b-%Y')}</span></p>
            <table>
                <tr><th>Description / Particulars</th><th style="text-align:right;">Amount</th></tr>
                <tr><td>{particulars}</td><td style="text-align:right;">₹{amount}/-</td></tr>
                <tr style="background:#f9f9f9;"><td style="font-weight:bold;">Total Payable</td><td style="text-align:right; font-weight:bold; color:#1e3a8a; font-size:18px;">₹{amount}/-</td></tr>
            </table>
            <div class="qr-box"><img src="{qr_link}" width="130"><br><small>UPI ID: {FIXED_UPI}</small></div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🖨️ Save as PDF"): st.info("Press Ctrl+P and select 'Save as PDF' from browser print menu.")
        msg = f"Namaste 🙏, *Shree Services*.\n*Bill For:* {party}\n*Details:* {particulars}\n*Amount:* ₹{amount}\n*Pay via UPI:* {FIXED_UPI}\n*Portal:* {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/{c_row["Mobile Number"]}?text={urllib.parse.quote(msg)}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Bill</div></a>', unsafe_allow_html=True)

elif choice == "🔔 WhatsApp Reminder":
    st.title("🔔 Tax & Payment Reminders")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        c_row = df[df['Firm Name'] == party].iloc[0]
        # Restored Payment Reminder
        r_type = st.radio("Select Type", ["GSTR-1 (11th Due - Sale Bills)", "GST-3B (20th Due - Data)", "💰 Payment Reminder"])
        
        upload_url = f"{PORTAL_LINK}?page=upload"
        cur_m = datetime.now().strftime("%B")

        if "GSTR-1" in r_type:
            r_msg = f"Namaste 🙏, *Shree Services*.\nReminder: {cur_m} month ke *GSTR-1* ki due date 11 tarik hai. Kripya apne Sale Bills yahan upload karein:\n👉 {upload_url}"
        elif "GST-3B" in r_type:
            r_msg = f"Namaste 🙏, *Shree Services*.\nReminder: {cur_m} month ke *GST-3B* ki due date 20 tarik hai. Kripya apna data yahan upload karein:\n👉 {upload_url}"
        else:
            r_msg = f"Namaste 🙏, *Shree Services*.\nAapka pichli filing ka payment pending hai. Kripya check karein aur payment clear karein. Shukriya!\n👉 {PORTAL_LINK}"

        st.markdown(f'<a href="https://wa.me/{c_row["Mobile Number"]}?text={urllib.parse.quote(r_msg)}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Reminder</div></a>', unsafe_allow_html=True)

elif choice == "📤 Upload Bills":
    st.title("📤 Upload to Google Drive")
    if not df.empty:
        firm_name = st.selectbox("Select Your Firm Name", df['Firm Name'].unique())
        st.markdown('<div class="upload-card">📁 Select Sales or Purchase Documents</div>', unsafe_allow_html=True)
        uploaded_files = st.file_uploader("Upload Bills", accept_multiple_files=True)
        
        if st.button("Submit to Drive"):
            if uploaded_files:
                for f in uploaded_files:
                    f_bytes = f.read()
                    f_b64 = base64.b64encode(f_bytes).decode('utf-8')
                    # This sends the file to your Google Script URL
                    payload = {"filename": f"{firm_name}_{f.name}", "mimetype": f.type, "data": f_b64}
                    try:
                        resp = requests.post(SCRIPT_URL, json=payload)
                        if resp.status_code == 200: st.success(f"{f.name} uploaded successfully!")
                    except: st.error(f"Error in {f.name}")
                st.balloons()
            else: st.warning("Select files first!")

elif choice == "📊 Ledger Status":
    st.title("📊 Business Ledger Status")
    if not df.empty: st.dataframe(df, use_container_width=True)
