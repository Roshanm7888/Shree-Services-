import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Shree Services | Admin", layout="wide", page_icon="📑")

# 2. Google Sheet Connection
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=30)
def load_data():
    try:
        data = pd.read_csv(SHEET_URL)
        # Column names ke aage-piche ke space hatane ke liye
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame()

df = load_data()

st.markdown(f"""
    <div style="background-color: #1e3a8a; padding: 25px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
        <h1>📑 SHREE SERVICES - LIVE ADMIN</h1>
        <p>Accountant: Roshan Mishra | GST Services</p>
    </div>
    """, unsafe_allow_html=True)

if not df.empty:
    tab1, tab2 = st.tabs(["📊 Ledger Status", "🔔 WhatsApp Reminders"])

    with tab1:
        st.subheader("Current Month Tracking")
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("Send Quick Reminders")
        sel_party = st.selectbox("Select Client", df['Firm Name'].unique())
        
        row = df[df['Firm Name'] == sel_party].iloc[0]
        
        # --- YE HISSA COLUMN DHONDNE KE LIYE HAI ---
        phone = ""
        possible_cols = ['Mobile Number', 'Mobile', 'Mobile No', 'Phone']
        for col in possible_cols:
            if col in df.columns:
                phone = str(row[col])
                break
        
        if phone:
            def create_wa_link(msg_text):
                return f"https://wa.me/{phone}?text={urllib.parse.quote(msg_text)}"

            m1 = f"Namaste, mein Roshan Mishra bol raha hoon. Aapka GST R1 ka last date 11 hai, kripya bill upload karein."
            
            st.write(f"**Client:** {sel_party} | **Number:** {phone}")
            st.markdown(f'<a href="{create_wa_link(m1)}" target="_blank"><button style="background-color:#25d366; color:white; border-radius:10px; padding:15px; border:none; width:100%; cursor:pointer; font-weight:bold; font-size:18px;">📲 Send WhatsApp Reminder</button></a>', unsafe_allow_html=True)
        else:
            st.error("Google Sheet mein 'Mobile Number' naam ka column nahi mila. Kripya check karein.")
else:
    st.error("Data load nahi ho raha. Google Sheet ko 'Anyone with the link can view' pe set karein.")
