import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Master Portal", layout="wide", page_icon="🏢")

# Styling
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.main-header { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
.stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; }
.service-box { background: white; padding: 20px; border-radius: 12px; border-left: 10px solid #1e3a8a; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.footer-box { background: #1e3a8a; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px; color: white; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# 2. Data Loading
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
PORTAL_LINK = "https://shree-services.streamlit.app"
FIXED_UPI = "7888273972-2@ybl"

@st.cache_data(ttl=5)
def load_data():
    try:
        d = pd.read_csv(SHEET_URL)
        d.columns = d.columns.str.strip() # Extra spaces hatane ke liye
        return d
    except: return pd.DataFrame()

df = load_data()

if 'page' not in st.session_state: st.session_state.page = "home"

# 3. Header & Nav
st.markdown('<div class="main-header"><h1>Shree Services - Online GST & Tax Center</h1><p>A Complete Hub for Accounting & Taxation Solutions</p></div>', unsafe_allow_html=True)

nav_cols = st.columns(5)
pages = ["🏠 HOME", "🧾 BILL", "🔔 REMINDER", "📤 UPLOAD", "📊 LEDGER"]
for i, col in enumerate(nav_cols):
    if col.button(pages[i]):
        st.session_state.page = pages[i].split()[-1].lower()

# 4. PAGE LOGIC

if st.session_state.page == "home":
    services = ["📊 Taxation (GST/Income Tax)", "🛡️ Insurance (Life/Health)", "📝 Online Work (PAN/Aadhar)"]
    for s in services:
        st.markdown(f'<div class="service-box"><h3>{s}</h3></div>', unsafe_allow_html=True)
        with st.expander(f"Apply for {s}"):
            m = st.text_input("Mobile No", key=f"m_{s}")
            r = st.text_area("Requirement", key=f"r_{s}")
            if st.button(f"Submit {s} Request"):
                wa_msg = f"Request for {s}\nMobile: {m}\nDetails: {r}"
                st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(wa_msg)}" target="_blank"><div style="background:#25d366; color:white; padding:10px; text-align:center; border-radius:5px;">📲 Send to Roshan Mishra</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "bill":
    st.title("📑 Generate Bill")
    if not df.empty:
        party = st.selectbox("Select Party Name", df['Firm Name'].unique())
        amt = st.number_input("Amount", value=800)
        p_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {p_month}")
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        st.markdown(f'<div style="border:2px solid #000; padding:20px; background:white; color:black; text-align:center;"><h2>SHREE SERVICES</h2><hr><p>Party: {party}</p><h3>Amount: ₹{amt}</h3><img src="{qr}" width="130"><br>UPI: {FIXED_UPI}</div>', unsafe_allow_html=True)

elif st.session_state.page == "ledger":
    st.title("📊 GST Portal Style Ledger")
    if not df.empty:
        selected_firm = st.selectbox("Select Your Firm Name", df['Firm Name'].unique())
        f_df = df[df['Firm Name'] == selected_firm]
        
        c1, c2, c3 = st.columns(3)
        with c1: 
            selected_year = st.selectbox("Select Financial Year", f_df['Year'].unique())
        with c2: 
            selected_qtr = st.selectbox("Select Quarter", f_df['Quter'].unique())
        with c3: 
            view_option = st.selectbox("What to check?", ["GST Status", "Payment Status"])
        
        # Filter Data
        res = f_df[(f_df['Year'] == selected_year) & (f_df['Quter'] == selected_qtr)]
        
        st.markdown(f"#### Results for {selected_firm} ({selected_qtr})")
        if view_option == "GST Status":
            st.table(res[['Month', 'Gst R1 status', 'Gst 3B status']])
        else:
            st.table(res[['Month', 'Payment Status']])

elif st.session_state.page == "rem":
    st.title("🔔 Send Reminders")
    if not df.empty:
        p = st.selectbox("Select Client", df['Firm Name'].unique())
        r_type = st.radio("Reminder Type", ["GSTR-1 Sale", "GST-3B Purchase", "Payment Reminder"])
        msg = f"Namaste 🙏, *Shree Services*. Reminder for {p}. Check status: {PORTAL_LINK}"
        st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(msg)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center;">📲 Send WhatsApp</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "upload":
    st.title("📤 Document Portal")
    st.file_uploader("Upload Files", accept_multiple_files=True)
    if st.button("Submit"): st.success("Bills Submitted Successfully!")

st.markdown('<div class="footer-box">📞 Contact Roshan Mishra: 7888273972 | 9220393972</div>', unsafe_allow_html=True)
