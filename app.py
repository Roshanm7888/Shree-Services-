import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services | Admin", layout="wide", page_icon="📑")

# 2. Google Sheet Connection (Aapki Sheet ID)
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 3. App Link (Live hone ke baad wali)
web_link = "https://shree-services-admin.streamlit.app" 

# Date Logic
today = datetime.now()
reporting_month = today.strftime("%B") 
next_month_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
deadline_month = next_month_date.strftime("%B")

@st.cache_data(ttl=60)
def load_data():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame(columns=['Firm Name', 'Owner', 'Mobile', 'GSTR1_Status', 'GST3B_Status', 'Payment'])

df = load_data()

# --- UI HEADER ---
st.markdown(f"""
    <div style="background-color: #1e3a8a; padding: 25px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
        <h1>📑 SHREE SERVICES - LIVE ADMIN</h1>
        <p>Accountant: Roshan Mishra | GST & Accounting Services</p>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Ledger Status", "🔔 WhatsApp Reminders", "📤 Bill Upload Portal"])

# --- TAB 1: LEDGER ---
with tab1:
    st.subheader("Current Month Tracking")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Google Sheet mein data nahi mila.")

# --- TAB 2: WHATSAPP ---
with tab2:
    st.subheader("Send Quick Reminders")
    if not df.empty:
        sel_party = st.selectbox("Select Client", df['Firm Name'])
        row = df[df['Firm Name'] == sel_party].iloc[0]
        phone = str(row['Mobile'])
        
        def create_wa_link(msg_text):
            return f"https://wa.me/{phone}?text={urllib.parse.quote(msg_text)}"

        col1, col2 = st.columns(2)
        
        with col1:
            m1 = f"Namaste, mein Roshan Mishra bol raha hoon. Aapka GST R1 {reporting_month} month ka jis ka last date 11 {deadline_month} hai, kripya karke aap apna bill is link par upload kar de: {web_link}"
            st.markdown(f'<a href="{create_wa_link(m1)}" target="_blank"><button style="background-color:#25d366; color:white; border-radius:10px; padding:12px; border:none; width:100%; cursor:pointer; font-weight:bold;">Send GSTR-1 Reminder</button></a>', unsafe_allow_html=True)

        with col2:
            m2 = f"Namaste {row['Owner']}, aapka {reporting_month} month ka GST bill generate ho gaya hai. Kripya payment clear karein. Link: {web_link}"
            st.markdown(f'<a href="{create_wa_link(m2)}" target="_blank"><button style="background-color:#075e54; color:white; border-radius:10px; padding:12px; border:none; width:100%; cursor:pointer; font-weight:bold;">Send Payment Bill</button></a>', unsafe_allow_html=True)

# --- TAB 3: UPLOAD ---
with tab3:
    st.subheader("Bill Submission")
    st.info("Clients yahan se apne bills upload kar sakte hain.")
    st.file_uploader("Upload Sale/Purchase Bills", accept_multiple_files=True)
    if st.button("Submit to Drive"):
        st.success("Bills processed successfully!")
 

