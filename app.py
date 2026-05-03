import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Master Portal", layout="wide", page_icon="🏢")

# Final Styling Fix
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.main-header { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
.stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; background: #1e3a8a; color: white; }

/* Boxes styling */
.service-box, .reminder-container { 
    background: white !important; 
    padding: 20px; 
    border-radius: 12px; 
    border: 1px solid #ddd;
    border-left: 10px solid #1e3a8a; 
    margin-bottom: 15px; 
    box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
    color: black !important; 
}

/* Professional Bill Layout */
.bill-container { background: white; border: 2px solid #000; padding: 30px; font-family: Arial; color: black; max-width: 800px; margin: auto; }
.bill-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.bill-table th, .bill-table td { border: 1px solid #000; padding: 10px; text-align: left; }
.pay-section { display: flex; align-items: center; justify-content: space-around; border: 1px dashed #333; padding: 10px; margin-top: 15px; }
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
        with st.expander(f"Apply for {title}"):
            m = st.text_input("Mobile Number", key=f"m_{title}")
            if st.button(f"Submit {title}"):
                st.success("Request ready to send!")

elif st.session_state.page == "bill":
    if not df.empty:
        party = st.selectbox("Party Name", df['Firm Name'].unique())
        amt = st.number_input("Amount", value=800)
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        
        st.markdown(f"""
        <div class="bill-container">
            <h2 style="text-align:center; color:#1e3a8a; margin:0;">SHREE SERVICES</h2>
            <p style="text-align:center; margin:5px;">Mohan Garden, New Delhi | 7888273972</p>
            <hr>
            <p><b>Client:</b> {party} <span style="float:right;"><b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}</span></p>
            <table class="bill-table">
                <tr style="background:#eee;"><th>Description</th><th style="text-align:right;">Amount</th></tr>
                <tr><td style="height:80px;">GST Compliance Filing Charges</td><td style="text-align:right;">₹{amt}.00</td></tr>
            </table>
            <div class="pay-section">
                <div style="text-align:center;"><img src="{qr}" width="120"><br><small>Scan to Pay</small></div>
                <div style="text-align:left;">
                    <p><b>Payment Details:</b><br>
                    UPI ID: <b>{FIXED_UPI}</b><br>
                    Name: Roshan Mishra<br>
                    Status: <span style="color:green;">Authorized</span></p>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        wa_b = f"Namaste 🙏, Bill for {party}: ₹{amt}. Pay: {FIXED_UPI}"
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(wa_b)}" target="_blank"><div style="background:#25d366; color:white; padding:12px; text-align:center; border-radius:10px; font-weight:bold;">📲 Send Bill on WhatsApp</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "rem":
    st.title("🔔 Reminder Center")
    if not df.empty:
        st.markdown('<div class="reminder-container"><h3>Select Party & Reminder Type</h3></div>', unsafe_allow_html=True)
        p = st.selectbox("Select Client", df['Firm Name'].unique())
        r_type = st.radio("What to send?", ["GSTR-1 Sale", "GST-3B Purchase", "Payment Reminder"])
        
        link = f"{PORTAL_LINK}?page=upload&mode="
        if "GSTR-1" in r_type: msg = f"GSTR-1 date aa rahi hai. Sale bills upload karein: {link}sale"
        elif "GST-3B" in r_type: msg = f"GST-3B date aa rahi hai. Purchase bills upload karein: {link}purchase"
        else: msg = f"Aapka payment pending hai. Check Ledger: {PORTAL_LINK}?page=ledger"
        
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank"><div style="background:#1e3a8a; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Click to Send WhatsApp</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "ledger":
    if not df.empty:
        firm = st.selectbox("Firm Name", df['Firm Name'].unique())
        f_df = df[df['Firm Name'] == firm]
        c1, c2, c3 = st.columns(3)
        with c1: yr = st.selectbox("Year", f_df['Year'].unique() if 'Year' in f_df.columns else ["2025-26"])
        with c2: qtr = st.selectbox("Quarter", f_df['Quarter'].unique() if 'Quarter' in f_df.columns else ["Apr-Jun"])
        with c3: view = st.selectbox("View", ["GST Status", "Payment Status"])
        
        res = f_df[(f_df['Year'] == yr) & (f_df.iloc[:, 2] == qtr)] # Using position for safety
        
        if view == "GST Status":
            # Auto-searching columns for R1 and 3B
            c_r1 = next((c for c in res.columns if "R1" in c or "GSTR1" in c), res.columns[4])
            c_3b = next((c for c in res.columns if "3B" in c or "GST3B" in c), res.columns[5])
            st.table(res[['Month', c_r1, c_3b]])
        else:
            p_col = next((c for c in res.columns if "Pay" in c), res.columns[-1])
            st.table(res[['Month', p_col]])

elif st.session_state.page == "upload":
    st.title("📤 Upload Bills")
    st.file_uploader("Upload Files", accept_multiple_files=True)
    if st.button("Submit"): st.success("Bills Submitted!")

st.markdown('<div class="main-header" style="margin-top:20px; padding:10px;">📞 Contact: 7888273972</div>', unsafe_allow_html=True)
