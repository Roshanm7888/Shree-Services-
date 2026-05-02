import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="Shree Services | Roshan Mishra", layout="centered", page_icon="🏢")

# Custom Styling (Footer hide + Sidebar White Text)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Background & White Text */
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] .st-emotion-cache-17l2puu, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label { 
        color: white !important; 
        font-weight: 500 !important;
        font-size: 17px !important;
    }
    
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1e3a8a; color: white; font-weight: bold; font-size: 18px; }
    .service-box { background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 10px solid #1e3a8a; margin-bottom: 25px; }
    .service-title { color: #1e3a8a; font-size: 26px; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; }
    .service-desc { color: #555; font-size: 18px; line-height: 1.6; }
    .main-header { background: #1e3a8a; color: white; padding: 40px 20px; border-radius: 0 0 30px 30px; text-align: center; margin-bottom: 40px; margin-top: -60px; }
    .upload-card { background: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px dashed #1e3a8a; margin-top: 20px; font-weight: bold; color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data & Settings
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
MY_NUMBER = "917888273972"

@st.cache_data(ttl=30)
def load_data():
    try:
        d = pd.read_csv(URL)
        d.columns = d.columns.str.strip()
        return d
    except: return pd.DataFrame()

df = load_data()

# 3. SIDEBAR MENU (White Text Enabled)
with st.sidebar:
    st.markdown("<h2 style='color:white;'>📋 MENU</h2>", unsafe_allow_html=True)
    choice = st.radio("", ["🏠 Home", "📊 Ledger Status", "🔔 WhatsApp Reminder", "📤 Upload Bills"], index=0)
    st.markdown("---")
    st.markdown("""
        <p style='color:white;'>📞 <b>Contact Us:</b><br>
        1. 7888273972<br>
        2. 8668257610<br>
        3. 9220393972</p>
    """, unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---

if choice == "🏠 Home":
    st.markdown('<div class="main-header"><h1>🏛️ SHREE SERVICES</h1><p style="font-size:20px;">A Complete Hub for Accounting, Taxation & Insurance Solutions</p></div>', unsafe_allow_html=True)
    services = [
        {"title": "📑 Taxation", "desc": "House Tax, Salary Tax, Business Tax & Capital Gain Tax Filing."},
        {"title": "🛡️ Insurance", "desc": "Car & Bike, Life Insurance (LIC), Health & Mediclaim."},
        {"title": "📝 GST Services", "desc": "New Registration, Monthly/Quarterly Filing & Compliances."},
        {"title": "💻 Accounting Software", "desc": "Vyapar Software Setup, Training & License Renewal."},
        {"title": "📅 Daily Accounting", "desc": "Day-to-day Bookkeeping and Cash Flow Management."},
        {"title": "📈 Yearly Accounting", "desc": "Finalization of Accounts, Balance Sheet & Profit & Loss Statements."}
    ]
    for s in services:
        st.markdown(f'<div class="service-box"><div class="service-title">{s["title"]}</div><div class="service-desc">{s["desc"]}</div></div>', unsafe_allow_html=True)
        if st.button(f"Inquiry for {s['title']}", key=s['title']):
            st.session_state.inquiry = s['title']
            st.rerun()

    if 'inquiry' in st.session_state:
        st.write("---")
        with st.form("lead_form"):
            st.subheader(f"Requesting Quote for: {st.session_state.inquiry}")
            name = st.text_input("Full Name")
            phone = st.text_input("Mobile Number")
            if st.form_submit_button("Submit"):
                msg = f"New Inquiry Alert!\nService: {st.session_state.inquiry}\nName: {name}\nPhone: {phone}"
                st.markdown(f'<a href="https://wa.me/{MY_NUMBER}?text={urllib.parse.quote(msg)}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Contact Roshan Ji on WhatsApp</div></a>', unsafe_allow_html=True)

elif choice == "📊 Ledger Status":
    st.title("📊 Client Ledger Status")
    if not df.empty: st.dataframe(df, use_container_width=True)

elif choice == "🔔 WhatsApp Reminder":
    st.title("🔔 Send Reminders")
    if not df.empty:
        party = st.selectbox("Select Party", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        p_num = ""
        for c in ['Mobile Number', 'Mobile', 'Phone']:
            if c in df.columns: p_num = str(row[c]); break
        m = f"Namaste 🙏, Shree Services ki taraf se reminder. Aapka data pending hai, kripya upload karein."
        wa_url = f"https://wa.me/{p_num}?text={urllib.parse.quote(m)}"
        st.markdown(f'<a href="{wa_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:20px; border-radius:10px; text-align:center; font-weight:bold;">Send WhatsApp to {party}</div></a>', unsafe_allow_html=True)

elif choice == "📤 Upload Bills":
    st.title("📤 Document Submission")
    if not df.empty:
        st.selectbox("Select Your Firm Name", df['Firm Name'].unique(), key="firm_select")
    
    st.markdown('<div class="upload-card">📁 GSTR-1 (Sale Bills)</div>', unsafe_allow_html=True)
    st.file_uploader("Upload all Sale bills here", accept_multiple_files=True, key="sale_upload")
    
    st.markdown('<div class="upload-card">📁 GST-3B (Purchase Bills)</div>', unsafe_allow_html=True)
    st.file_uploader("Upload all Purchase bills here", accept_multiple_files=True, key="pur_upload")
    
    if st.button("Final Submission"):
        st.success("Bills Successfully Uploaded! Roshan ji ko notify kar diya gaya hai.")
        st.balloons()
