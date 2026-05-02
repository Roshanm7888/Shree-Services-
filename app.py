import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# 1. Page Config & Professional Theme
st.set_page_config(page_title="Shree Services | Roshan Mishra", layout="wide", page_icon="🏢")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #ffffff; border-radius: 5px; padding: 10px 20px; border: 1px solid #ddd; }
    .stTabs [data-baseweb="tab--active"] { border-bottom: 3px solid #1e3a8a !important; background-color: #e6f0ff; }
    .service-card { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #1e3a8a; height: 100%; transition: 0.3s; }
    .service-card:hover { transform: translateY(-5px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
    .header-style { background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 40px; border-radius: 15px; text-align: center; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Connection
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
MY_NUMBER = "919220393972" 

@st.cache_data(ttl=30)
def load_data():
    try:
        d = pd.read_csv(URL)
        d.columns = d.columns.str.strip()
        return d
    except: return pd.DataFrame()

df = load_data()

# --- HEADER ---
st.markdown('<div class="header-style"><h1>🏛️ SHREE SERVICES</h1><p>A Complete Hub for Accounting, Taxation & Insurance Solutions</p></div>', unsafe_allow_html=True)

# Main Navigation
tab_home, tab_ledger, tab_whatsapp, tab_upload = st.tabs(["🏠 Home & Services", "📊 Ledger", "🔔 WhatsApp Manager", "📤 Upload Bills"])

# --- HOME & SERVICES ---
with tab_home:
    st.subheader("Our Professional Services")
    
    # Row 1: Tax & GST
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="service-card"><h3 style="color:#1e3a8a;">📑 TAXATION</h3>• House Tax / Property Tax<br>• Salary Tax Filing<br>• Business Tax Solutions<br>• Capital Gain Tax</div>', unsafe_allow_html=True)
        if st.button("Inquiry for Tax", key="tax_btn"): st.session_state.serv = "Taxation"
    
    with col2:
        st.markdown('<div class="service-card"><h3 style="color:#1e3a8a;">📝 GST SERVICES</h3>• New GST Registration<br>• Monthly/Quarterly Filing<br>• GST Reconciliation<br>• Notice Reply & Compliance</div>', unsafe_allow_html=True)
        if st.button("Inquiry for GST", key="gst_btn"): st.session_state.serv = "GST"
    
    with col3:
        st.markdown('<div class="service-card"><h3 style="color:#1e3a8a;">🛡️ INSURANCE</h3>• Car & Bike Insurance<br>• Life Insurance (LIC)<br>• Health & Mediclaim<br>• Term Insurance</div>', unsafe_allow_html=True)
        if st.button("Inquiry for Insurance", key="ins_btn"): st.session_state.serv = "Insurance"

    st.write(" ") # Space

    # Row 2: Accounting & Software
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown('<div class="service-card"><h3 style="color:#1e3a8a;">💻 SOFTWARE</h3>• Vyapar Accounting Software<br>• Software Migration<br>• Training & Setup<br>• License Renewal</div>', unsafe_allow_html=True)
        if st.button("Inquiry for Software", key="soft_btn"): st.session_state.serv = "Accounting Software"
    
    with col5:
        st.markdown('<div class="service-card"><h3 style="color:#1e3a8a;">📅 DAILY ACCOUNTS</h3>• Day-to-day Bookkeeping<br>• Cash Flow Management<br>• Expense Tracking<br>• Daily Reporting</div>', unsafe_allow_html=True)
        if st.button("Inquiry for Daily Accounts", key="daily_btn"): st.session_state.serv = "Daily Accounting"

    with col6:
        st.markdown('<div class="service-card"><h3 style="color:#1e3a8a;">📈 YEARLY ACCOUNTS</h3>• Finalization of Accounts<br>• Balance Sheet Prep<br>• Profit & Loss Statements<br>• Yearly Tax Planning</div>', unsafe_allow_html=True)
        if st.button("Inquiry for Yearly Accounts", key="yearly_btn"): st.session_state.serv = "Yearly Accounting"

    # Lead Form
    if 'serv' in st.session_state:
        st.write("---")
        with st.form("lead_form"):
            st.markdown(f"### 📞 Get Quote for **{st.session_state.serv}**")
            n = st.text_input("Aapka Naam")
            p = st.text_input("Mobile Number")
            if st.form_submit_button("Submit & Contact Roshan Ji"):
                msg = f"Inquiry Alert!\nService: {st.session_state.serv}\nClient: {n}\nPhone: {p}"
                wa_url = f"https://wa.me/{MY_NUMBER}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{wa_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 WhatsApp Roshan Ji Now</div></a>', unsafe_allow_html=True)

# --- LEDGER ---
with tab_ledger:
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else: st.warning("Sheet check karein.")

# --- WHATSAPP MANAGER ---
with tab_whatsapp:
    if not df.empty:
        party = st.selectbox("Select Party for Reminder", df['Firm Name'].unique())
        row = df[df['Firm Name'] == party].iloc[0]
        phone = ""
        for c in ['Mobile Number', 'Mobile', 'Phone']:
            if c in df.columns: phone = str(row[c]); break
        
        m_text = f"Namaste 🙏, *Shree Services* ki taraf se.\nReminder: Aapka GST data pending hai.\nKripya link par upload karein: https://shree-services.streamlit.app\n\n*Roshan Mishra*"
        url = f"https://wa.me/{phone}?text={urllib.parse.quote(m_text)}"
        st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 Send Professional WhatsApp</div></a>', unsafe_allow_html=True)

# --- UPLOAD ---
with tab_upload:
    st.subheader("Bill Submission Portal")
    if not df.empty:
        st.selectbox("Apni Firm Chunein", df['Firm Name'].unique(), key="up_p")
        st.file_uploader("Upload Bills (Sale/Purchase)", accept_multiple_files=True)
        if st.button("Confirm Submit"): st.success("Bills received by Roshan Mishra!")

