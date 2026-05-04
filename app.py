import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Master Portal", layout="wide", page_icon="🏢")

# UI Styling
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.main-header { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
.stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; background: #1e3a8a; color: white; }
.reminder-box { background: white !important; padding: 20px; border-radius: 12px; border: 1px solid #ddd; border-left: 10px solid #1e3a8a; margin-bottom: 15px; color: black !important; }
.bill-container { background: white; border: 2px solid #000; padding: 30px; color: black; max-width: 800px; margin: auto; }
</style>
""", unsafe_allow_html=True)

# 2. Data Loading
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
PORTAL_LINK = "https://shree-services.streamlit.app"
FIXED_UPI = "7888273972-2@ybl"

@st.cache_data(ttl=2)
def load_data():
    try:
        d = pd.read_csv(SHEET_URL)
        d.columns = d.columns.str.strip()
        return d
    except: return pd.DataFrame()

df = load_data()
today_day = datetime.now().day
current_month = datetime.now().strftime("%B")

if 'page' not in st.session_state: st.session_state.page = "home"

# 3. Header & Navigation
st.markdown('<div class="main-header"><h1>Shree Services - Online GST & Tax Center</h1></div>', unsafe_allow_html=True)

nav_cols = st.columns(5)
pages = ["🏠 HOME", "🧾 BILL", "🔔 REMINDER", "📤 UPLOAD", "📊 LEDGER"]
for i, col in enumerate(nav_cols):
    if col.button(pages[i]):
        st.session_state.page = pages[i].split()[-1].lower()

# 4. Page Logic

if st.session_state.page == "home":
    st.write("### 🛠️ Professional Services")
    services = {"Taxation": "GST Filing (R1/3B) & ITR.", "Insurance": "Life & Health.", "Online Work": "PAN & Aadhar."}
    for title, desc in services.items():
        st.markdown(f'<div class="reminder-box"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

elif st.session_state.page == "bill":
    if not df.empty:
        party = st.selectbox("Select Party", df.iloc[:,0].unique())
        amt = 800
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        st.markdown(f"""
        <div class="bill-container">
            <h2 style="text-align:center; color:#1e3a8a;">SHREE SERVICES</h2><hr>
            <p><b>Party:</b> {party} <span style="float:right;"><b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}</span></p>
            <table style="width:100%; border:1px solid #000; border-collapse:collapse; margin:15px 0;">
                <tr style="background:#eee;"><th>Service</th><th style="text-align:right;">Amount</th></tr>
                <tr><td style="padding:10px;">{current_month} GST Filing Fees</td><td style="text-align:right;">₹{amt}.00</td></tr>
            </table>
            <div style="display:flex; justify-content:space-around; align-items:center; border:1px dashed #333; padding:10px;">
                <img src="{qr}" width="130">
                <p><b>Payment Details:</b><br>UPI ID: {FIXED_UPI}<br>Name: Roshan Mishra</p>
            </div>
        </div>""", unsafe_allow_html=True)

elif st.session_state.page == "reminder":
    st.title("🔔 Reminder System")
    if not df.empty:
        # Step 1: Select Party
        party = st.selectbox("Choose Client Name", df.iloc[:,0].unique())
        
        # Step 2: Auto-Detection (Logic hamesha chalega)
        if today_day <= 11:
            auto_type = "GSTR-1 Sale Upload"
            auto_msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\n*GSTR-1* ki date 11 {current_month} hai. Kripya Sale Bills upload karein:\n👉 {PORTAL_LINK}?page=upload&mode=sale"
        elif today_day <= 20:
            auto_type = "GST-3B Purchase Upload"
            auto_msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\n*GST-3B* ki date kareeb hai. Kripya Purchase Bills upload karein:\n👉 {PORTAL_LINK}?page=upload&mode=purchase"
        else:
            auto_type = "Payment Reminder"
            auto_msg = f"Namaste 🙏, *Shree Services*.\n*Bill for {current_month}: ₹800*\n\n1. Portal: {PORTAL_LINK}\n2. Ledger: {PORTAL_LINK}?page=ledger\n3. Bill: {PORTAL_LINK}?page=bill"

        # Step 3: Show the Box
        st.markdown(f"""
        <div class="reminder-box">
            <h3>📢 Today's Recommended Reminder: {auto_type}</h3>
            <p style="white-space: pre-wrap; font-size: 16px;">{auto_msg}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 4: WhatsApp Button (Ekdam visible)
        if st.button("📲 SEND VIA WHATSAPP NOW"):
            wa_link = f"https://wa.me/?text={urllib.parse.quote(auto_msg)}"
            st.markdown(f'<a href="{wa_link}" target="_blank">✅ Click here to confirm and send</a>', unsafe_allow_html=True)

elif st.session_state.page == "ledger":
    st.title("📊 Client Ledger Status")
    if not df.empty:
        firm = st.selectbox("Firm Name", df.iloc[:,0].unique())
        st.table(df[df.iloc[:,0] == firm].tail(5))

elif st.session_state.page == "upload":
    st.title("📤 Document Upload")
    st.file_uploader("Upload Files", accept_multiple_files=True)
    if st.button("Submit"): st.success("Uploaded!")

st.markdown('<div class="main-header" style="margin-top:20px; padding:10px;">📞 Contact: 7888273972</div>', unsafe_allow_html=True)
