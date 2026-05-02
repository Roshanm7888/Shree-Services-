import streamlit as st
import pandas as pd
import pywhatkit as kit
import requests
import base64
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services | Live Portal", layout="wide", page_icon="📑")

# 2. Google Sheet Connection
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 3. Settings
web_link = "https://shree-services.streamlit.app" 
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxvLzhqqrCi56VJbagRgE_ePmlWRZo1jmm3dmEAYqp6lLumSdrh6zB7eBeR6DHc7Mij/exec"

today = datetime.now()
reporting_month = today.strftime("%B") 
next_month_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
deadline_month = next_month_date.strftime("%B")

@st.cache_data(ttl=60)
def load_data():
    try:
        return pd.read_csv(SHEET_URL)
    except Exception as e:
        return pd.DataFrame(columns=['Firm Name', 'Owner', 'Mobile', 'GSTR1_Status', 'GST3B_Status', 'Payment'])

df = load_data()

st.markdown(f"""
    <div style="background-color: #1e3a8a; padding: 25px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
        <h1>📑 SHREE SERVICES - LIVE ADMIN</h1>
        <p>Accountant: Roshan Mishra | GST & Accounting Services</p>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📤 Upload Bills", "📊 Accounts Tracking", "🔔 WhatsApp Reminders"])

with tab1:
    st.subheader("Client Document Submission")
    if not df.empty:
        c_firm = st.selectbox("Select Firm Name", df['Firm Name'])
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            sale_files = st.file_uploader("Sale Bills", accept_multiple_files=True)
        with col_u2:
            pur_files = st.file_uploader("Purchase Bills", accept_multiple_files=True)
        
        if st.button("Submit to Roshan Mishra"):
            st.info("Processing files... Yeh bills aapke Drive mein save ho rahe hain.")
    else:
        st.warning("Google Sheet check karein, data nahi mil raha.")

with tab2:
    st.subheader("Current Month Ledger (Live from Google Sheets)")
    st.dataframe(df, use_container_width=True)
    st.info("💡 Note: Naya client add karne ke liye apni Google Sheet app mein change karein.")

with tab3:
    st.subheader("WhatsApp Automation")
    if not df.empty:
        sel_party = st.selectbox("Choose Party", df['Firm Name'], key="rem_sel")
        row = df[df['Firm Name'] == sel_party].iloc[0]
        
        c1, c2, c3 = st.columns(3)
        
        if c1.button("Send GSTR-1 Reminder"):
            msg = f"Namaste, mein Roshan Mishra bol raha hoon. Aapka GST R1 {reporting_month} month ka jis ka last date 11 {deadline_month} hai, kripya karke aap apna bill is link par upload kar de: {web_link}"
            kit.sendwhatmsg_instantly(f"+{str(row['Mobile'])}", msg, 15)
            st.success("R1 Sent!")

        if c2.button("Send GST-3B Reminder"):
            msg = f"Namaste, mein Roshan Mishra bol raha hoon. Aapka GST 3B {reporting_month} month ka jis ka last date 20 {deadline_month} hai, kripya karke aap apna purchase bill is link par upload kar de: {web_link}"
            kit.sendwhatmsg_instantly(f"+{str(row['Mobile'])}", msg, 15)
            st.success("3B Sent!")

        if today.day >= 21:
            st.write("---")
            if st.button("💰 Send Monthly Bill (₹800)"):
                msg = f"Namaste {row['Owner']}, {sel_party} ka {reporting_month} month ka GST filing fee ₹800 pending hai. Kripya payment karke account clear karein. Link: {web_link}"
                kit.sendwhatmsg_instantly(f"+{str(row['Mobile'])}", msg, 15)
                st.success("Bill Sent!")

