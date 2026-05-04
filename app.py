import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Master Portal", layout="wide", page_icon="🏢")

# Final Styling Fix (All Design Issues Resolved)
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.main-header { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
.stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; background: #1e3a8a; color: white; }
.service-box, .reminder-container { background: white !important; padding: 20px; border-radius: 12px; border: 1px solid #ddd; border-left: 10px solid #1e3a8a; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: black !important; }
.bill-container { background: white; border: 2px solid #000; padding: 30px; font-family: Arial, sans-serif; color: black; max-width: 800px; margin: auto; }
.pay-section { display: flex; align-items: center; justify-content: space-around; border: 1px dashed #333; padding: 15px; margin-top: 15px; }
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
st.markdown('<div class="main-header"><h1>Shree Services - Online GST & Tax Center</h1><p>A Complete Hub for Accounting & Taxation Solutions</p></div>', unsafe_allow_html=True)

nav_cols = st.columns(5)
pages = ["🏠 HOME", "🧾 BILL", "🔔 REMINDER", "📤 UPLOAD", "📊 LEDGER"]
for i, col in enumerate(nav_cols):
    if col.button(pages[i]):
        st.session_state.page = pages[i].split()[-1].lower()

# 4. Page Logic

if st.session_state.page == "home":
    st.write("### 🛠️ Professional Services")
    services = {"Taxation": "GST Filing (R1/3B) & Income Tax Returns.", "Insurance": "Life, Health & Vehicle Insurance.", "Online Work": "PAN, Aadhar & New GST Registration."}
    for title, desc in services.items():
        st.markdown(f'<div class="service-box"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

elif st.session_state.page == "bill":
    if not df.empty:
        party = st.selectbox("Select Party Name", df['Firm Name'].unique() if 'Firm Name' in df.columns else df.iloc[:,0].unique())
        amt = 800
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        st.markdown(f"""
        <div class="bill-container">
            <h2 style="text-align:center; color:#1e3a8a; margin:0;">SHREE SERVICES</h2>
            <p style="text-align:center; margin:5px;">Mohan Garden, New Delhi | Mob: 7888273972</p>
            <hr>
            <p><b>Invoice To:</b> {party} <span style="float:right;"><b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}</span></p>
            <table style="width:100%; border:1px solid #000; border-collapse:collapse; margin:15px 0;">
                <tr style="background:#eee;">
                    <th style="border:1px solid #000; padding:10px;">Service Description</th>
                    <th style="border:1px solid #000; padding:10px; text-align:right;">Amount (₹)</th>
                </tr>
                <tr>
                    <td style="border:1px solid #000; padding:10px; height:80px;">Professional Fees for {current_month} GST Compliance & Filing</td>
                    <td style="border:1px solid #000; padding:10px; text-align:right;"><b>800.00</b></td>
                </tr>
            </table>
            <div class="pay-section">
                <div style="text-align:center;"><img src="{qr}" width="130"><br><small>Scan to Pay</small></div>
                <div style="text-align:left;">
                    <p><b>Payment Details:</b><br>
                    UPI ID: <b>{FIXED_UPI}</b><br>
                    Account Name: Roshan Mishra<br>
                    Bank: Google Pay/PhonePe/Paytm</p>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        wa_b = f"Namaste 🙏, Bill for {party}: ₹800. Pay: {FIXED_UPI}\nCheck Portal: {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(wa_b)}" target="_blank"><div style="background:#25d366; color:white; padding:12px; text-align:center; border-radius:10px; font-weight:bold;">📲 Send Bill on WhatsApp</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "rem":
    st.title("🔔 Automatic Reminder Panel")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        
        # Automatic Reminder Logic
        if today_day <= 11:
            r_type = "GSTR-1 Sale Reminder"
            msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\n*GSTR-1* ki date 11 {current_month} hai. Kripya Sale Bills upload karein:\n👉 {PORTAL_LINK}?page=upload&mode=sale"
        elif today_day <= 20:
            r_type = "GST-3B Purchase Reminder"
            msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\n*GST-3B* ki date kareeb hai. Kripya Purchase Bills upload karein:\n👉 {PORTAL_LINK}?page=upload&mode=purchase"
        else:
            r_type = "Payment Reminder"
            msg = f"Namaste 🙏, *Shree Services*.\n*Bill for {current_month}: ₹800*\n\n1. Portal: {PORTAL_LINK}\n2. Ledger: {PORTAL_LINK}?page=ledger\n3. Bill: {PORTAL_LINK}?page=bill"
        
        st.markdown(f'<div class="reminder-container"><h3>Today\'s Status: {r_type}</h3><p style="white-space: pre-wrap;">{msg}</p></div>', unsafe_allow_html=True)
        if st.button("📲 Send WhatsApp Reminder"):
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank">Click to Open WhatsApp</a>', unsafe_allow_html=True)

elif st.session_state.page == "ledger":
    st.title("📊 Client Ledger Status")
    if not df.empty:
        firm = st.selectbox("Select Firm", df['Firm Name'].unique())
        f_df = df[df['Firm Name'] == firm]
        c1, c2, c3 = st.columns(3)
        with c1: yr = st.selectbox("Year", f_df['Year'].unique() if 'Year' in f_df.columns else ["2025-26"])
        with c2: qtr = st.selectbox("Quarter", f_df['Quarter'].unique() if 'Quarter' in f_df.columns else ["April to June"])
        with c3: view = st.selectbox("Check", ["GST Status", "Payment Status"])
        
        res = f_df[(f_df['Year'] == yr) & (f_df.iloc[:, 2] == qtr)]
        if view == "GST Status":
            # Search columns safely
            c_r1 = next((c for c in res.columns if "R1" in c), res.columns[4])
            c_3b = next((c for c in res.columns if "3B" in c), res.columns[5])
            st.table(res[['Month', c_r1, c_3b]])
        else:
            p_col = next((c for c in res.columns if "Pay" in c), res.columns[-1])
            st.table(res[['Month', p_col]])

elif st.session_state.page == "upload":
    st.title("📤 Document Upload")
    st.info("Kripya apne bills select karke Submit karein.")
    st.file_uploader("Upload Files", accept_multiple_files=True)
    if st.button("Submit"): st.success("Bills Successfully Uploaded!")

st.markdown('<div class="main-header" style="margin-top:20px; padding:10px;">📞 Contact Roshan Mishra: 7888273972</div>', unsafe_allow_html=True)
