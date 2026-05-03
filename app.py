import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Master Portal", layout="wide", page_icon="🏢")

# Custom CSS for Professional Look
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.main-header { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
.stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; }
.service-box { background: white; padding: 20px; border-radius: 12px; border-left: 10px solid #1e3a8a; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# 2. Data Loading with Auto-Fix for Column Names
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
PORTAL_LINK = "https://shree-services.streamlit.app"
FIXED_UPI = "7888273972-2@ybl"

@st.cache_data(ttl=2)
def load_data():
    try:
        d = pd.read_csv(SHEET_URL)
        d.columns = d.columns.str.strip() # Spaces hatane ke liye
        return d
    except: return pd.DataFrame()

df = load_data()

# Page Routing
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
    services = ["📊 Taxation", "🛡️ Insurance", "📝 Online Work"]
    for s in services:
        st.markdown(f'<div class="service-box"><h3>{s}</h3></div>', unsafe_allow_html=True)
        with st.expander(f"Apply for {s}"):
            m = st.text_input("Client Mobile Number", key=f"m_{s}")
            r = st.text_area("Requirement Details", key=f"r_{s}")
            if st.button(f"Submit {s} Request"):
                wa_msg = f"Request for {s}\nMobile: {m}\nDetails: {r}"
                st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(wa_msg)}" target="_blank"><div style="background:#25d366; color:white; padding:10px; text-align:center; border-radius:5px;">📲 Send to Roshan Mishra</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "bill":
    st.title("📑 Generate Bill")
    if not df.empty:
        party = st.selectbox("Select Party Name", df.iloc[:, 0].unique())
        amt = st.number_input("Amount", value=800)
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        st.markdown(f'<div style="border:2px solid #000; padding:20px; background:white; color:black; text-align:center;"><h2>SHREE SERVICES</h2><hr><p>Party: {party}</p><h3>Amount: ₹{amt}</h3><img src="{qr}" width="130"><br>UPI ID: {FIXED_UPI}</div>', unsafe_allow_html=True)

elif st.session_state.page == "ledger":
    st.title("📊 GST Portal Style Ledger")
    if not df.empty:
        # Auto-detecting columns from your photo
        firm_col = 'Firm Name' if 'Firm Name' in df.columns else df.columns[0]
        year_col = 'Year' if 'Year' in df.columns else df.columns[1]
        qtr_col = 'Quarter' if 'Quarter' in df.columns else 'Quter' if 'Quter' in df.columns else df.columns[2]
        month_col = 'Month' if 'Month' in df.columns else df.columns[3]
        
        firm = st.selectbox("Select Firm", df[firm_col].unique())
        f_df = df[df[firm_col] == firm]
        
        c1, c2, c3 = st.columns(3)
        with c1: yr = st.selectbox("Financial Year", f_df[year_col].unique())
        with c2: qtr = st.selectbox("Select Quarter", f_df[qtr_col].unique())
        with c3: view = st.selectbox("What to check?", ["GST Status", "Payment Status"])
        
        # Filtering
        res = f_df[(f_df[year_col] == yr) & (f_df[qtr_col] == qtr)]
        
        st.markdown(f"#### Results for {firm} - {qtr}")
        
        if view == "GST Status":
            # Matching your photo's column names exactly: GSTR1 Status, GST3B Status
            c1_name = 'GSTR1 Status' if 'GSTR1 Status' in res.columns else 'GSTR-1 Status'
            c2_name = 'GST3B Status' if 'GST3B Status' in res.columns else 'GST-3B Status'
            st.table(res[[month_col, c1_name, c2_name]] if month_col in res.columns else res)
        else:
            p_col = 'Payment Status' if 'Payment Status' in res.columns else res.columns[-1]
            st.table(res[[month_col, p_col]] if month_col in res.columns else res)

elif st.session_state.page == "rem":
    st.title("🔔 Send Reminders")
    if not df.empty:
        firm_col = 'Firm Name' if 'Firm Name' in df.columns else df.columns[0]
        p = st.selectbox("Select Party", df[firm_col].unique())
        r = st.radio("Reminder Type", ["GSTR-1 Sale", "GST-3B Purchase", "Payment Reminder"])
        msg = f"Namaste 🙏, *Shree Services*. Reminder for {p}. Status: {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(msg)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center;">📲 Send WhatsApp Reminder</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "upload":
    st.title("📤 Document Portal")
    st.file_uploader("Upload Files", accept_multiple_files=True)
    if st.button("Submit"): st.success("Bills Submitted Successfully!")

st.markdown('<div style="background:#1e3a8a; padding:15px; border-radius:10px; text-align:center; color:white; margin-top:20px;">📞 Contact Roshan Mishra: 7888273972 | 9220393972</div>', unsafe_allow_html=True)
