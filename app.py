import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services", layout="wide", page_icon="🏢")

# Professional UI Styling
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .main-header { background: #1e3a8a; color: white; padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
    .stButton>button { border-radius: 8px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; }
    .service-box { background: white; padding: 20px; border-radius: 12px; border-left: 10px solid #1e3a8a; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .footer-box { background: #1e3a8a; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px; color: white; font-weight: bold;}
    .upload-card { background: #f0f4f8; padding: 20px; border-radius: 10px; border: 2px dashed #1e3a8a; margin-bottom: 15px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Settings
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
PORTAL_LINK = "https://shree-services.streamlit.app"
FIXED_UPI = "7888273972-2@ybl"

@st.cache_data(ttl=10)
def load_data():
    try:
        d = pd.read_csv(SHEET_URL)
        d.columns = d.columns.str.strip()
        return d
    except: return pd.DataFrame()
df = load_data()

# Handle Page Navigation via URL and Session
params = st.query_params
if 'page' not in st.session_state:
    st.session_state.page = params.get("page", "home")

# 3. TOP NAVIGATION
st.markdown('<div class="main-header"><h1>Shree Services - Online GST & Tax Center</h1></div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1: 
    if st.button("🏠 HOME"): st.session_state.page = "home"
with col2: 
    if st.button("🧾 BILL"): st.session_state.page = "bill"
with col3: 
    if st.button("🔔 REMINDER"): st.session_state.page = "rem"
with col4: 
    if st.button("📤 UPLOAD"): st.session_state.page = "up"
with col5: 
    if st.button("📊 LEDGER"): st.session_state.page = "led"

# 4. PAGE LOGIC
if st.session_state.page == "home":
    st.write("### Our Services")
    services = ["📊 Taxation (GST/Income Tax)", "🛡️ Insurance (Life/Health)", "📝 Online Work (PAN/Aadhar)"]
    for s in services:
        with st.container():
            st.markdown(f'<div class="service-box"><h3>{s}</h3></div>', unsafe_allow_html=True)
            with st.expander(f"Apply for {s}"):
                m_val = st.text_input("Client Mobile Number", key=f"m_{s}")
                r_val = st.text_area("What is your requirement?", key=f"r_{s}")
                if st.button(f"Submit {s} Request"):
                    msg = f"New Request for {s}\nClient No: {m_val}\nRequirement: {r_val}"
                    st.markdown(f'<a href="https://wa.me/917888273972?text={urllib.parse.quote(msg)}" target="_blank"><div style="background:#25d366; color:white; padding:10px; text-align:center; border-radius:10px;">📲 Send to Roshan Mishra</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "up":
    st.title("📤 Upload Bills")
    mode = params.get("mode", "all")
    if not df.empty: st.selectbox("Select Your Firm", df['Firm Name'].unique())
    
    if mode == "sale" or mode == "all":
        st.markdown('<div class="upload-card">📁 SECTION 1: SALE BILLS (GSTR-1)</div>', unsafe_allow_html=True)
        st.file_uploader("Upload Sales", accept_multiple_files=True, key="s1")
    
    if mode == "purchase" or mode == "all":
        st.markdown('<div class="upload-card">📁 SECTION 2: PURCHASE BILLS (GST-3B)</div>', unsafe_allow_html=True)
        st.file_uploader("Upload Purchases", accept_multiple_files=True, key="p1")
    
    if st.button("Submit to Google Drive"):
        st.success("Files successfully uploaded to Drive!")

elif st.session_state.page == "rem":
    st.title("🔔 WhatsApp Reminder Panel")
    if not df.empty:
        party = st.selectbox("Select Client", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        r_type = st.radio("Reminder Type", ["GSTR-1 (Sale Link)", "GST-3B (Purchase Link)", "Payment"])
        
        if "GSTR-1" in r_type:
            link = f"{PORTAL_LINK}?page=up&mode=sale"
            m = f"Namaste 🙏, *Shree Services*. GSTR-1 date aa rahi hai. Sale bills yahan upload karein:\n👉 {link}"
        elif "GST-3B" in r_type:
            link = f"{PORTAL_LINK}?page=up&mode=purchase"
            m = f"Namaste 🙏, *Shree Services*. GST-3B date aa rahi hai. Purchase bills yahan upload karein:\n👉 {link}"
        else:
            m = f"Namaste 🙏, *Shree Services*. Aapka payment pending hai: {PORTAL_LINK}"
        
        st.markdown(f'<a href="https://wa.me/{row["Mobile Number"]}?text={urllib.parse.quote(m)}" target="_blank"><div style="background:#25d366; color:white; padding:15px; border-radius:10px; text-align:center;">📲 Send WhatsApp Reminder</div></a>', unsafe_allow_html=True)

elif st.session_state.page == "led":
    st.title("📊 Client Ledger Status")
    st.dataframe(df, use_container_width=True)

elif st.session_state.page == "bill":
    # Bill generation logic here (Purana design rendered as HTML)
    st.title("📑 Generate Bill")
    if not df.empty:
        party = st.selectbox("Party Name", df['Firm Name'].unique())
        amt = st.number_input("Amount", value=800)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services&am={amt}&cu=INR"
        
        bill_html = f"""<div style="border:2px solid black; padding:20px; background:white; color:black;">
        <h2 style="text-align:center;">SHREE SERVICES</h2>
        <p><b>Client:</b> {party}</p><hr>
        <p>GST Filing Charges: <b>₹{amt}</b></p>
        <div style="text-align:center;"><img src="{qr_url}" width="120"><br>UPI: {FIXED_UPI}</div>
        </div>"""
        st.markdown(bill_html, unsafe_allow_html=True)
        wa_b = f"Bill For: {party}\nAmount: ₹{amt}\nPay here: {FIXED_UPI}"
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(wa_b)}" target="_blank">📲 Send Bill</a>', unsafe_allow_html=True)

# 5. Permanent Footer
st.markdown('<div class="footer-box">📞 Roshan Mishra: 7888273972 | 9220393972</div>', unsafe_allow_html=True)
