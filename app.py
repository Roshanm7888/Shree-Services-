import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Master Portal", layout="wide", page_icon="🏢")

# Master Styling
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.main-header { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
.stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; background: #1e3a8a; color: white; }
.service-box, .reminder-box { background: white !important; padding: 20px; border-radius: 12px; border: 1px solid #ddd; border-left: 10px solid #1e3a8a; margin-bottom: 15px; color: black !important; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.bill-container { background: white; border: 2px solid #000; padding: 35px; color: black; max-width: 800px; margin: auto; font-family: Arial; }
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
if 'page' not in st.session_state:
    # URL params check for deep linking (Ledger/Upload)
    params = st.query_params
    st.session_state.page = params.get("page", "home")

# 3. Header & Navigation
st.markdown('<div class="main-header"><h1>Shree Services - Master Portal</h1><p>Accounting, GST & Taxation Solutions</p></div>', unsafe_allow_html=True)

nav_cols = st.columns(5)
pages = ["🏠 HOME", "🧾 BILL", "🔔 REMINDER", "📤 UPLOAD", "📊 LEDGER"]
for i, col in enumerate(nav_cols):
    if col.button(pages[i]):
        st.session_state.page = pages[i].split()[-1].lower()
        st.query_params.clear() # Clear params on manual nav

# 4. Page Logic

# --- HOME PAGE ---
if st.session_state.page == "home":
    st.write("### 🛠️ Our Professional Services")
    services = {
        "📊 Taxation": "GST Filing (R1 & 3B), Income Tax Returns, Audit Support.",
        "🛡️ Insurance": "Life, Health & Vehicle Insurance with best premiums.",
        "📝 Online Work": "PAN Card, Aadhar Updates, GST New Registration."
    }
    for title, desc in services.items():
        st.markdown(f'<div class="service-box"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
        with st.expander(f"Apply for {title}"):
            m = st.text_input("Mobile Number", key=f"m_{title}")
            r = st.text_area("Details", key=f"r_{title}")
            if st.button(f"Submit {title} Inquiry"):
                wa_msg = f"Inquiry for {title}\nMobile: {m}\nDetails: {r}"
                st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(wa_msg)}" target="_blank"><div style="background:#25d366; color:white; padding:10px; text-align:center; border-radius:10px;">📲 Send to Roshan Mishra</div></a>', unsafe_allow_html=True)

# --- BILL PAGE ---
elif st.session_state.page == "bill":
    st.title("📑 Generate Bill")
    if not df.empty:
        party = st.selectbox("Select Party Name", df.iloc[:,0].unique())
        amt = st.number_input("Amount (₹)", value=800)
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        st.markdown(f"""
        <div class="bill-container">
            <h2 style="text-align:center; color:#1e3a8a; margin:0;">SHREE SERVICES</h2>
            <p style="text-align:center; margin:5px;">Mohan Garden, New Delhi | Mob: 7888273972</p><hr>
            <p><b>Client:</b> {party} <span style="float:right;"><b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}</span></p>
            <table style="width:100%; border:1px solid #000; border-collapse:collapse; margin:15px 0;">
                <tr style="background:#eee;"><th>Description</th><th style="text-align:right;">Amount</th></tr>
                <tr><td style="padding:10px; height:80px;">Professional GST Filing Fees</td><td style="text-align:right; padding:10px;">₹{amt}.00</td></tr>
            </table>
            <div class="pay-section">
                <div style="text-align:center;"><img src="{qr}" width="130"><br><small>Scan & Pay</small></div>
                <div style="text-align:left;"><p><b>Payment Info:</b><br>UPI ID: {FIXED_UPI}<br>Name: Roshan Mishra</p></div>
            </div>
        </div>""", unsafe_allow_html=True)
        wa_b = f"Namaste 🙏, Bill for {party}: ₹{amt}. Pay via UPI: {FIXED_UPI}"
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(wa_b)}" target="_blank"><div style="background:#25d366; color:white; padding:12px; text-align:center; border-radius:10px; font-weight:bold;">📲 Send Bill on WhatsApp</div></a>', unsafe_allow_html=True)

# --- REMINDER PAGE ---
elif st.session_state.page == "reminder" or st.session_state.page == "rem":
    st.title("🔔 Reminder System")
    if not df.empty:
        party = st.selectbox("Choose Client", df.iloc[:,0].unique())
        mode = st.radio("Select Type", ["GSTR-1 (Sale)", "GST-3B (Purchase)", "Payment Pending"])
        
        final_msg = ""
        if mode == "GSTR-1 (Sale)":
            final_msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\n*GSTR-1* ki date kareeb hai. Sale bills yahan upload karein:\n👉 {PORTAL_LINK}?page=upload&mode=sale"
        elif mode == "GST-3B (Purchase)":
            final_msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\n*GST-3B* ki date kareeb hai. Purchase bills yahan upload karein:\n👉 {PORTAL_LINK}?page=upload&mode=purchase"
        else:
            sel_months = st.multiselect("Mahine chunein:", ["April", "May", "June", "July", "August", "September", "October", "November", "December", "January", "February", "March"])
            if sel_months:
                breakdown = "\n".join([f"• {m}: ₹800" for m in sel_months])
                final_msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\nAapka Payment pending hai:\n{breakdown}\n*Total Amount: ₹{len(sel_months)*800}*\n\n*Pay UPI:* {FIXED_UPI}\n*Ledger:* {PORTAL_LINK}?page=ledger"
        
        if final_msg:
            st.markdown(f'<div class="reminder-box"><h3>Generated Message:</h3><p style="white-space: pre-wrap;">{final_msg}</p></div>', unsafe_allow_html=True)
            if st.button("📲 Send WhatsApp"):
                st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(final_msg)}" target="_blank">✅ Click to Confirm Send</a>', unsafe_allow_html=True)

# --- UPLOAD PAGE ---
elif st.session_state.page == "upload":
    st.title("📤 Document Portal")
    mode = st.query_params.get("mode", "all")
    st.info(f"Uploading for: {mode.upper()}")
    st.file_uploader("Select Files", accept_multiple_files=True)
    if st.button("Submit"): st.success("Files Submitted!")

# --- LEDGER PAGE ---
elif st.session_state.page == "ledger":
    st.title("📊 Client Ledger Status")
    if not df.empty:
        firm = st.selectbox("Select Firm", df.iloc[:,0].unique())
        f_df = df[df.iloc[:,0] == firm]
        c1, c2, c3 = st.columns(3)
        with c1: yr = st.selectbox("Year", f_df['Year'].unique() if 'Year' in f_df.columns else ["2025-26"])
        with c2: qtr = st.selectbox("Quarter", f_df['Quarter'].unique() if 'Quarter' in f_df.columns else ["Apr-Jun"])
        with c3: view = st.selectbox("Check", ["GST Status", "Payment Status"])
        
        res = f_df[(f_df['Year'] == yr)] # Simplified filter for safety
        if view == "GST Status":
            c_r1 = next((c for c in res.columns if "R1" in c or "GSTR1" in c), res.columns[4])
            c_3b = next((c for c in res.columns if "3B" in c or "GST3B" in c), res.columns[5])
            st.table(res[['Month', c_r1, c_3b]])
        else:
            p_col = next((c for c in res.columns if "Pay" in c), res.columns[-1])
            st.table(res[['Month', p_col]])

st.markdown('<div class="main-header" style="margin-top:20px; padding:10px;">📞 Roshan Mishra: 7888273972</div>', unsafe_allow_html=True)
