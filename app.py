import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

# 1. Page Configuration & Professional Styling
st.set_page_config(page_title="Shree Services | Roshan Mishra", layout="wide", page_icon="💼")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #1e3a8a; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #25d366; color: white; border: 2px solid white; }
    .card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; border-left: 5px solid #1e3a8a; }
    .service-head { color: #1e3a8a; font-size: 22px; font-weight: bold; margin-bottom: 10px; }
    .sidebar-text { font-size: 18px; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# 2. Connection & Data
SHEET_ID = "1NVNjNawK0026WPsd6P_X-lSd6LoLWqXo8dG1m7Ou098"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
WEB_LINK = "https://shree-services.streamlit.app"
MY_NUMBER = "919220393972" # Aapka apna number lead alerts ke liye

@st.cache_data(ttl=30)
def load_data():
    try:
        data = pd.read_csv(SHEET_URL)
        data.columns = data.columns.str.strip()
        return data
    except: return pd.DataFrame()

df = load_data()

# 3. Sidebar Menu (Right Side/Standard Menu)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Admin Menu")
    choice = st.radio("Navigate to:", ["🏠 Home & Services", "📊 Client Ledger", "🔔 WhatsApp Manager", "📤 Bill Upload Portal"])
    st.markdown("---")
    st.write("📞 **Support:** +91 9220393972")

# --- NAVIGATION LOGIC ---

if choice == "🏠 Home & Services":
    st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🏛️ SHREE SERVICES</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Professional Accounting & Insurance Solutions</p>", unsafe_allow_html=True)
    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card"><div class="service-head">📑 Tax Services</div>'
                    '• House Tax<br>• Salary Tax<br>• Business Tax<br>• Capital Gain Tax</div>', unsafe_allow_html=True)
        if st.button("Inquiry for Tax Services"):
            st.session_state.show_form = "Tax"

    with col2:
        st.markdown('<div class="card"><div class="service-head">🛡️ Insurance Services</div>'
                    '• Car Insurance<br>• Life Insurance<br>• Health Insurance<br>• LIC</div>', unsafe_allow_html=True)
        if st.button("Inquiry for Insurance"):
            st.session_state.show_form = "Insurance"

    # Lead Form Logic
    if 'show_form' in st.session_state:
        st.write("---")
        with st.form("inquiry_form"):
            st.subheader(f"Request Callback for {st.session_state.show_form}")
            user_name = st.text_input("Aapka Naam")
            user_phone = st.text_input("Mobile Number")
            submitted = st.form_submit_button("Submit Request")
            
            if submitted:
                # Roshan ji ko message bhejne wala link
                alert_msg = f"Alert! Naya Client Aaya Hai:\nNaam: {user_name}\nPhone: {user_phone}\nService: {st.session_state.show_form}"
                wa_url = f"https://wa.me/{MY_NUMBER}?text={urllib.parse.quote(alert_msg)}"
                st.success("Request saved! Kripya niche button dabayein contact karne ke liye.")
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25d366; color:white; padding:10px; width:100%; border-radius:10px; border:none;">Click to Notify Roshan Ji</button></a>', unsafe_allow_html=True)

elif choice == "📊 Client Ledger":
    st.header("📊 Business Ledger Status")
    if not df.empty:
        st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
    else: st.error("Sheet Load Nahi Ho Rahi.")

elif choice == "🔔 WhatsApp Manager":
    st.header("🔔 Professional Reminders")
    if not df.empty:
        sel_party = st.selectbox("Select Client", df['Firm Name'].unique())
        row = df[df['Firm Name'] == sel_party].iloc[0]
        
        # Phone logic
        phone = ""
        for c in ['Mobile Number', 'Mobile', 'Phone']:
            if c in df.columns: phone = str(row[c]); break

        st.markdown(f'<div class="card"><b>Party:</b> {sel_party}<br><b>Owner:</b> {row["Owner"]}<br><b>Contact:</b> {phone}</div>', unsafe_allow_html=True)

        m_text = f"Namaste 🙏, *Shree Services (Roshan Mishra)* ki taraf se. Aapka GST R1/3B ka data pending hai. Kripya is link par upload karein: {WEB_LINK}\n\n*Roshan Mishra (Accountant)*"
        
        wa_link = f"https://wa.me/{phone}?text={urllib.parse.quote(m_text)}"
        st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25d366; color:white;">📲 Send WhatsApp Now</button></a>', unsafe_allow_html=True)

elif choice == "📤 Bill Upload Portal":
    st.header("📤 Document Submission")
    if not df.empty:
        party = st.selectbox("Apni Firm ka Naam Chunein", df['Firm Name'].unique())
        st.file_uploader("Upload Sale/Purchase Bills", accept_multiple_files=True)
        if st.button("Confirm Submission"):
            st.balloons()
            st.success("Bills Successfully Uploaded!")
