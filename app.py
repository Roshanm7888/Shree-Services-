import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Master Portal", layout="wide", page_icon="🏢")

# Purana Styling (Wahi Professional Look)
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.main-header { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
.stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; background: #1e3a8a; color: white; }
.service-box, .reminder-container { background: white !important; padding: 20px; border-radius: 12px; border: 1px solid #ddd; border-left: 10px solid #1e3a8a; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: black !important; }
.bill-container { background: white; border: 2px solid #000; padding: 30px; font-family: Arial; color: black; max-width: 800px; margin: auto; }
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
    st.write("### 🛠️ Services")
    services = {"Taxation": "GST Filing & ITR", "Insurance": "Life & Health", "Online Work": "PAN & Aadhar"}
    for title, desc in services.items():
        st.markdown(f'<div class="service-box"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

elif st.session_state.page == "bill":
    if not df.empty:
        party = st.selectbox("Select Client", df['Firm Name'].unique())
        amt = 800
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        st.markdown(f"""
        <div class="bill-container" id="bill-print">
            <h2 style="text-align:center; color:#1e3a8a;">SHREE SERVICES</h2>
            <hr>
            <p><b>Party:</b> {party} <span style="float:right;"><b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}</span></p>
            <p><b>Description:</b> Professional Fees for {current_month} Compliance</p>
            <h3 style="text-align:center;">Amount Due: ₹{amt}.00</h3>
            <div style="text-align:center; border: 1px dashed #333; padding: 10px;">
                <img src="{qr}" width="120"><br><p>UPI: {FIXED_UPI}</p>
            </div>
        </div>""", unsafe_allow_html=True)
        st.info("Download ke liye mobile par Screenshot lein ya Laptop par Ctrl+P dabayein.")

elif st.session_state.page == "rem":
    st.title("🔔 Smart Reminder System")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        
        # Automatic Message Logic
        if today_day <= 11:
            r_type = "GSTR-1 Sale Reminder"
            msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\n*GSTR-1* ki last date 11 {current_month} hai.\nKripya apne Sale Bills yahan upload karein:\n👉 {PORTAL_LINK}?page=upload&mode=sale"
        elif today_day <= 20:
            r_type = "GST-3B Purchase Reminder"
            msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\n*GST-3B* ki date kareeb hai. Kripya apne Purchase Bills yahan upload karein:\n👉 {PORTAL_LINK}?page=upload&mode=purchase"
        else:
            r_type = "Payment Reminder"
            msg = f"Namaste 🙏, *Shree Services*.\n*Bill for {current_month}: ₹800*\n\n1. Portal: {PORTAL_LINK}\n2. Ledger: {PORTAL_LINK}?page=ledger\n3. Bill Download: {PORTAL_LINK}?page=bill"
        
        st.markdown(f'<div class="reminder-container"><h3>Today\'s Auto-Reminder: {r_type}</h3><p>{msg}</p></div>', unsafe_allow_html=True)
        
        if st.button("📲 Send to Client via WhatsApp"):
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank">Click here to open WhatsApp</a>', unsafe_allow_html=True)

elif st.session_state.page == "ledger":
    if not df.empty:
        firm = st.selectbox("Firm Name", df['Firm Name'].unique())
        f_df = df[df['Firm Name'] == firm]
        # Ledger table logic (Purana wala)
        st.table(f_df.tail(5))

elif st.session_state.page == "upload":
    st.title("📤 Document Upload")
    mode = st.query_params.get("mode", "all")
    st.file_uploader(f"Upload {mode.upper()} Bills", accept_multiple_files=True)
    if st.button("Submit"): st.success("Uploaded!")

st.markdown('<div class="main-header" style="margin-top:20px; padding:10px;">📞 Contact: 7888273972</div>', unsafe_allow_html=True)
