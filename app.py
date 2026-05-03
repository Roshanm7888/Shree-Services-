import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Master Portal", layout="wide", page_icon="🏢")

# Professional UI Styling
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.main-header { background: #1e3a8a; color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
.stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; }
.service-box { background: white; padding: 20px; border-radius: 12px; border-left: 10px solid #1e3a8a; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.footer-box { background: #1e3a8a; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px; color: white; font-weight: bold;}
.upload-card { background: #f0f4f8; padding: 20px; border-radius: 10px; border: 2px dashed #1e3a8a; margin-bottom: 15px; font-weight: bold; }
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
        d.columns = d.columns.str.strip()
        return d
    except: return pd.DataFrame()

df = load_data()

if 'page' not in st.session_state: st.session_state.page = "home"

# 3. TOP NAVIGATION (Header fixed)
st.markdown("""
<div class="main-header">
    <h1>Shree Services - Online GST & Tax Center</h1>
    <p style="font-size:18px;">A Complete Hub for Accounting & Taxation Solutions</p>
</div>
""", unsafe_allow_html=True)

nav_cols = st.columns(5)
pages = ["🏠 HOME", "🧾 BILL", "🔔 REMINDER", "📤 UPLOAD", "📊 LEDGER"]
for i, col in enumerate(nav_cols):
    if col.button(pages[i]):
        st.session_state.page = pages[i].split()[-1].lower()

# 4. PAGE LOGIC

if st.session_state.page == "home":
    st.write("### Choose a Service")
    services = ["📊 Taxation (GST/Income Tax)", "🛡️ Insurance (Life/Health)", "📝 Online Work (PAN/Aadhar)"]
    for s in services:
        st.markdown(f'<div class="service-box"><h3>{s}</h3></div>', unsafe_allow_html=True)
        with st.expander(f"Apply for {s}"):
            m = st.text_input("Mobile No", key=f"m_{s}")
            r = st.text_area("Requirement", key=f"r_{s}")
            if st.button(f"Submit {s} Request"):
                msg = f"Request for {s}\nMobile: {m}\nDetails: {r}"
                st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(msg)}" target="_blank"><div style="background:#25d366; color:white; padding:10px; text-align:center; border-radius:5px;">📲 Send to Roshan Mishra</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "bill":
    st.title("📑 Generate Bill")
    if not df.empty:
        party = st.selectbox("Select Party Name", df['Firm Name'].unique())
        c_row = df[df['Firm Name'] == party].iloc[0]
        amt = st.number_input("Amount", value=800)
        p_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%B %Y")
        particulars = st.text_input("Particulars", value=f"GST Filing Charges for {p_month}")
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        
        bill_html = f"""
        <div style="border:2px solid #333; padding:30px; background:white; color:black; font-family:Arial;">
            <h2 style="text-align:center; margin-bottom:0;">SHREE SERVICES</h2>
            <p style="text-align:center; margin-top:5px;">Mohan Garden, Delhi | 7888273972</p>
            <hr>
            <p><b>To:</b> {party} <span style="float:right;"><b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}</span></p>
            <table style="width:100%; border-collapse:collapse; margin:20px 0;">
                <tr style="background:#f2f2f2;">
                    <th style="border:1px solid #333; padding:10px;">Description</th>
                    <th style="border:1px solid #333; padding:10px; text-align:right;">Amount</th>
                </tr>
                <tr>
                    <td style="border:1px solid #333; padding:10px; height:100px; vertical-align:top;">{particulars}</td>
                    <td style="border:1px solid #333; padding:10px; text-align:right; vertical-align:top;">₹{amt}.00</td>
                </tr>
            </table>
            <div style="text-align:center;">
                <img src="{qr}" width="130"><br><b>UPI ID: {FIXED_UPI}</b>
            </div>
        </div>"""
        st.markdown(bill_html, unsafe_allow_html=True)
        wa_b = f"Bill For: {party}\nAmount: ₹{amt}\nPay: {FIXED_UPI}"
        st.markdown(f'<a href="https://wa.me/{c_row.get("Mobile Number", "")}?text={urllib.parse.quote(wa_b)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Bill</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "ledger":
    st.title("📊 GST Portal Style Ledger")
    if not df.empty:
        firm = st.selectbox("Select Firm", df['Firm Name'].unique())
        f_df = df[df['Firm Name'] == firm]
        c1, c2, c3 = st.columns(3)
        with c1: yr = st.selectbox("Financial Year", f_df['Year'].unique() if 'Year' in f_df.columns else ["25-26"])
        with c2: qtr = st.selectbox("Select Quarter", ["April to June", "Jul to sep", "Oct to dec", "Jan to Mar"])
        with c3: view = st.selectbox("What to check?", ["GST Status", "Payment Status"])
        
        st.markdown(f"#### Results for {firm} - {qtr}")
        # Ledger filter logic (simulated for your sheet structure)
        res = f_df[f_df['Quarter'] == qtr] if 'Quarter' in f_df.columns else f_df
        if view == "GST Status":
            st.table(res[['Month', 'GSTR-1 Status', 'GST-3B Status']] if 'Month' in res.columns else res)
        else:
            st.table(res[['Month', 'Payment Status']] if 'Month' in res.columns else res)

elif st.session_state.page == "upload":
    st.title("📤 Document Portal")
    mode = st.query_params.get("mode", "all")
    if not df.empty: st.selectbox("Select Firm Name", df['Firm Name'].unique())
    if mode in ["sale", "all"]:
        st.markdown('<div class="upload-card">📁 SALE BILLS (GSTR-1)</div>', unsafe_allow_html=True)
        st.file_uploader("Upload Sales", accept_multiple_files=True, key="s")
    if mode in ["purchase", "all"]:
        st.markdown('<div class="upload-card">📁 PURCHASE BILLS (GST-3B)</div>', unsafe_allow_html=True)
        st.file_uploader("Upload Purchases", accept_multiple_files=True, key="p")
    if st.button("Submit to Drive"): st.success("Bills Submitted Successfully!")

elif st.session_state.page == "rem":
    st.title("🔔 Reminders")
    if not df.empty:
        p = st.selectbox("Select Client", df['Firm Name'].unique())
        row = df[df['Firm Name'] == p].iloc[0]
        r = st.radio("Type", ["GSTR-1 (Sale Link)", "GST-3B (Purchase Link)", "Payment Reminder"])
        l = f"{PORTAL_LINK}?page=upload&mode={'sale' if 'GSTR-1' in r else 'purchase'}"
        msg = f"Namaste 🙏, *Shree Services*. Check Details: {l}"
        st.markdown(f'<a href="https://wa.me/{row.get("Mobile Number", "")}?text={urllib.parse.quote(msg)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center;">📲 Send Reminder</div></a>', unsafe_allow_html=True)

st.markdown(f'<div class="footer-box">📞 Contact Roshan Mishra: 7888273972 | 9220393972</div>', unsafe_allow_html=True)
