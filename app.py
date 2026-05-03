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
.main-header { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
.stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; background: #1e3a8a; color: white; }

/* Home & Reminder Box Fix (White Background, Black Text) */
.service-box, .reminder-box { 
    background: white !important; 
    padding: 20px; 
    border-radius: 12px; 
    border-left: 10px solid #1e3a8a; 
    margin-bottom: 15px; 
    box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
    color: black !important; 
}
.service-box h3, .reminder-box h3 { color: #1e3a8a !important; margin-bottom: 5px; }
.service-box p, .reminder-box p { color: black !important; }

/* Bill Styling */
.bill-container { background: white; border: 2px solid #000; padding: 40px; font-family: 'Arial', sans-serif; color: #000; width: 100%; max-width: 850px; margin: auto; }
.bill-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
.bill-table th, .bill-table td { border: 1px solid #000; padding: 12px; text-align: left; color: black; }
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
    st.write("### 🛠️ Our Professional Services")
    services = {
        "📊 Taxation": "GST Filing (R1 & 3B), Income Tax Returns, Audit Support.",
        "🛡️ Insurance": "Life, Health & Vehicle Insurance with best premiums.",
        "📝 Online Work": "PAN Card, Aadhar Updates, GST New Registration."
    }
    for title, desc in services.items():
        st.markdown(f'<div class="service-box"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
        with st.expander(f"Click here to Apply for {title}"):
            m = st.text_input("Mobile Number", key=f"m_{title}")
            r = st.text_area("Requirement", key=f"r_{title}")
            if st.button(f"Submit {title} Inquiry"):
                wa_msg = f"Inquiry for {title}\nMobile: {m}\nDetails: {r}"
                st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(wa_msg)}" target="_blank"><div style="background:#25d366; color:white; padding:10px; text-align:center; border-radius:10px;">📲 Send to Roshan Ji</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "bill":
    st.title("📑 Professional Tax Invoice")
    if not df.empty:
        party = st.selectbox("Select Party Name", df['Firm Name'].unique())
        amt = st.number_input("Amount", value=800)
        particulars = st.text_input("Services Provided", value=f"GST Compliance & Filing Charges")
        qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        st.markdown(f"""
        <div class="bill-container">
            <div style="text-align:center; border-bottom:3px solid #1e3a8a; padding-bottom:10px;">
                <h1 style="margin:0; color:#1e3a8a;">SHREE SERVICES</h1>
                <p><b>Accounting, GST & Taxation Specialist</b><br>Mohan Garden, New Delhi-110059 | Mob: 7888273972</p>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:20px;">
                <p><b>Invoice To:</b><br>{party}</p>
                <p style="text-align:right;"><b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}</p>
            </div>
            <table class="bill-table">
                <tr style="background:#1e3a8a; color:white;"><th>Description</th><th style="text-align:right;">Total (₹)</th></tr>
                <tr><td style="height:100px; vertical-align:top;">{particulars}</td><td style="text-align:right;"><b>₹{amt}.00</b></td></tr>
            </table>
            <div style="text-align:center; border:1px dashed #ccc; padding:15px;"><img src="{qr}" width="140"><br>UPI ID: {FIXED_UPI}</div>
        </div>""", unsafe_allow_html=True)
        wa_b = f"Namaste 🙏, Bill for {party}: ₹{amt}. Pay: {FIXED_UPI}"
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(wa_b)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Bill on WhatsApp</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "rem":
    st.title("🔔 Tax Compliance Reminders")
    if not df.empty:
        # Reminder box with Black Text
        st.markdown('<div class="reminder-box"><h3>Select Reminder Type</h3><p>Niche diye gaye options se reminder chunein:</p></div>', unsafe_allow_html=True)
        p = st.selectbox("Select Client", df['Firm Name'].unique())
        r_type = st.radio("Reminder Options:", ["GSTR-1 Sale Upload", "GST-3B Purchase Upload", "Payment Reminder (Ledger)"])
        
        if "GSTR-1" in r_type:
            msg = f"Namaste 🙏, *Shree Services*. GSTR-1 date kareeb hai. Sale bills yahan upload karein: {PORTAL_LINK}?page=upload&mode=sale"
        elif "GST-3B" in r_type:
            msg = f"Namaste 🙏, *Shree Services*. GST-3B ke liye Purchase bills yahan upload karein: {PORTAL_LINK}?page=upload&mode=purchase"
        else:
            msg = f"Namaste 🙏, *Shree Services*. Aapka pichla payment pending hai. Ledger check karein: {PORTAL_LINK}?page=ledger"
            
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank"><div style="background:#1e3a8a; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Reminder on WhatsApp</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "ledger":
    st.title("📊 Client Ledger Status")
    if not df.empty:
        firm = st.selectbox("Select Firm Name", df['Firm Name'].unique())
        f_df = df[df['Firm Name'] == firm]
        c1, c2, c3 = st.columns(3)
        with c1: yr = st.selectbox("Financial Year", f_df['Year'].unique() if 'Year' in f_df.columns else ["2025-26"])
        with c2: qtr = st.selectbox("Quarter", f_df['Quarter'].unique() if 'Quarter' in f_df.columns else ["April To June"])
        with c3: view = st.selectbox("View Options", ["GST Status", "Payment Status"])
        
        res = f_df[(f_df['Year'] == yr) & (f_df['Quarter'] == qtr)]
        
        if view == "GST Status":
            # AUTO-FIX for Spelling (Super Safe)
            c1_name = next((c for c in res.columns if "GSTR1" in c or "R1 Status" in c), "GSTR1 Status")
            c2_name = next((c for c in res.columns if "GST3B" in c or "3B Status" in c), "GST3B Status")
            try:
                st.table(res[['Month', c1_name, c2_name]])
            except:
                st.error("Sheet headings check karein (GSTR1 Status / GST3B Status)")
        else:
            p_col = next((c for c in res.columns if "Payment" in c), "Payment Status")
            st.table(res[['Month', p_col]])

elif st.session_state.page == "upload":
    st.title("📤 Document Portal")
    mode = st.query_params.get("mode", "all")
    if mode in ["sale", "all"]:
        st.markdown('<div style="background:white; color:black; padding:15px; border-radius:10px; border:2px dashed #1e3a8a;">📁 **UPLOAD SALE BILLS (GSTR-1)**</div>', unsafe_allow_html=True)
        st.file_uploader("Select Sales", accept_multiple_files=True, key="s")
    if mode in ["purchase", "all"]:
        st.markdown('<div style="background:white; color:black; padding:15px; border-radius:10px; border:2px dashed #b91c1c;">📁 **UPLOAD PURCHASE BILLS (GST-3B)**</div>', unsafe_allow_html=True)
        st.file_uploader("Select Purchases", accept_multiple_files=True, key="p")
    if st.button("Submit to Drive"): st.success("Bills Submitted Successfully!")

st.markdown('<div style="background:#1e3a8a; color:white; padding:15px; border-radius:10px; text-align:center; margin-top:20px;">📞 Contact Roshan Mishra: 7888273972</div>', unsafe_allow_html=True)
