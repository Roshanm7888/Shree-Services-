import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Master Portal", layout="wide", page_icon="🏢")

# Professional UI Styling (Purana Design Preserved)
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.main-header { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
.stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; }
.service-box { background: white; padding: 20px; border-radius: 12px; border-left: 10px solid #1e3a8a; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.bill-container { background: white; border: 2px solid #333; padding: 30px; font-family: Arial; color: #000; width: 100%; margin: auto; }
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

# 3. Header
st.markdown('<div class="main-header"><h1>Shree Services - Online GST & Tax Center</h1><p>A Complete Hub for Accounting & Taxation Solutions</p></div>', unsafe_allow_html=True)

# Navigation
nav_cols = st.columns(5)
pages = ["🏠 HOME", "🧾 BILL", "🔔 REMINDER", "📤 UPLOAD", "📊 LEDGER"]
for i, col in enumerate(nav_cols):
    if col.button(pages[i]):
        st.session_state.page = pages[i].split()[-1].lower()

# 4. Page Logic

if st.session_state.page == "home":
    services = ["📊 Taxation (GST/Income Tax)", "🛡️ Insurance (Life/Health)", "📝 Online Work (PAN/Aadhar)"]
    for s in services:
        st.markdown(f'<div class="service-box"><h3>{s}</h3></div>', unsafe_allow_html=True)
        with st.expander(f"Apply for {s}"):
            m = st.text_input("Mobile No", key=f"m_{s}")
            r = st.text_area("Requirement", key=f"r_{s}")
            if st.button(f"Submit Request for {s}"):
                wa_msg = f"Request for {s}\nMobile: {m}\nDetails: {r}"
                st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(wa_msg)}" target="_blank"><div style="background:#25d366; color:white; padding:10px; text-align:center; border-radius:5px;">📲 Send to Roshan Mishra</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "bill":
    st.title("📑 Generate Professional Bill")
    if not df.empty:
        party = st.selectbox("Select Party Name", df['Firm Name'].unique())
        amt = st.number_input("Amount", value=800)
        p_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {p_month}")
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        
        st.markdown(f"""
        <div class="bill-container">
            <h2 style="text-align:center;">SHREE SERVICES</h2>
            <p style="text-align:center;">Mohan Garden, Delhi | Mob: 7888273972</p><hr>
            <p><b>To:</b> {party} <span style="float:right;"><b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}</span></p>
            <table style="width:100%; border:1px solid #000; border-collapse:collapse; margin:15px 0;">
                <tr style="background:#eee;"><th>Particulars</th><th style="text-align:right;">Amount</th></tr>
                <tr><td style="border:1px solid #000; padding:10px; height:80px;">{particulars}</td>
                <td style="border:1px solid #000; padding:10px; text-align:right;">₹{amt}.00</td></tr>
            </table>
            <div style="text-align:center;"><img src="{qr}" width="120"><br><b>UPI ID: {FIXED_UPI}</b></div>
        </div>""", unsafe_allow_html=True)
        
        # Two Links as requested
        col_b1, col_b2 = st.columns(2)
        wa_text = f"Bill for {party}: ₹{amt}. Pay via UPI: {FIXED_UPI}"
        with col_b1:
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(wa_text)}" target="_blank"><div style="background:#1e3a8a; color:white; padding:10px; text-align:center; border-radius:5px;">🔗 Send Portal Link</div></a>', unsafe_allow_html=True)
        with col_b2:
            st.markdown(f'<div style="background:#000; color:white; padding:10px; text-align:center; border-radius:5px; cursor:pointer;">📥 Download Bill (Screenshot)</div>', unsafe_allow_html=True)

elif st.session_state.page == "rem":
    st.title("🔔 Reminder Panel")
    if not df.empty:
        p = st.selectbox("Select Client", df['Firm Name'].unique())
        r_type = st.radio("Reminder Type", ["GSTR-1 (Sale)", "GST-3B (Purchase)", "Payment Pending"])
        
        # Upload links logic
        up_link = f"{PORTAL_LINK}?page=upload&mode="
        if "GSTR-1" in r_type:
            msg = f"Namaste 🙏, GSTR-1 date aa rahi hai. Sale bills yahan upload karein: {up_link}sale"
        elif "GST-3B" in r_type:
            msg = f"Namaste 🙏, GST-3B date aa rahi hai. Purchase bills yahan upload karein: {up_link}purchase"
        else:
            msg = f"Namaste 🙏, Aapka payment pending hai. Check Ledger: {PORTAL_LINK}?page=ledger"
            
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send WhatsApp Reminder</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "ledger":
    st.title("📊 Client Ledger Status")
    if not df.empty:
        firm = st.selectbox("Firm Name", df['Firm Name'].unique())
        f_df = df[df['Firm Name'] == firm]
        
        c1, c2, c3 = st.columns(3)
        with c1: yr = st.selectbox("Year", f_df['Year'].unique() if 'Year' in f_df.columns else ["25-26"])
        with c2: qtr = st.selectbox("Quarter", f_df['Quarter'].unique() if 'Quarter' in f_df.columns else ["April to June"])
        with c3: view = st.selectbox("View", ["GST Status", "Payment Status"])
        
        # Filtering with safety
        res = f_df[(f_df['Year'] == yr) & (f_df['Quarter'] == qtr)] if 'Quarter' in f_df.columns else f_df
        
        if view == "GST Status":
            # Match sheet column names from your photo
            cols = [c for c in ['Month', 'GSTR1 Status', 'GST3B Status'] if c in res.columns]
            st.table(res[cols] if cols else res)
        else:
            cols = [c for c in ['Month', 'Payment Status'] if c in res.columns]
            st.table(res[cols] if cols else res)

elif st.session_state.page == "upload":
    st.title("📤 Document Upload")
    mode = st.query_params.get("mode", "all")
    if mode in ["sale", "all"]:
        st.info("📁 Uploading SALE Bills for GSTR-1")
        st.file_uploader("Upload Sales", accept_multiple_files=True, key="s")
    if mode in ["purchase", "all"]:
        st.info("📁 Uploading PURCHASE Bills for GST-3B")
        st.file_uploader("Upload Purchases", accept_multiple_files=True, key="p")
    if st.button("Submit"): st.success("Uploaded!")

st.markdown('<div style="background:#1e3a8a; padding:15px; border-radius:10px; text-align:center; color:white; margin-top:20px;">📞 Contact Roshan Mishra: 7888273972</div>', unsafe_allow_html=True)
