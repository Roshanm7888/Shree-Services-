import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Shree Services - Master Portal", layout="wide", page_icon="🏢")

# UI Styling
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.main-header { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
.stButton>button { border-radius: 10px; height: 3.5em; font-weight: bold; border: 2px solid #1e3a8a; width: 100%; background: #1e3a8a; color: white; }
.reminder-box { background: white !important; padding: 20px; border-radius: 12px; border: 1px solid #ddd; border-left: 10px solid #1e3a8a; margin-bottom: 15px; color: black !important; }
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
current_month_name = datetime.now().strftime("%B")

if 'page' not in st.session_state: st.session_state.page = "home"

# 3. Header & Navigation
st.markdown('<div class="main-header"><h1>Shree Services - Master Portal</h1></div>', unsafe_allow_html=True)

nav_cols = st.columns(5)
pages = ["🏠 HOME", "🧾 BILL", "🔔 REMINDER", "📤 UPLOAD", "📊 LEDGER"]
for i, col in enumerate(nav_cols):
    if col.button(pages[i]):
        st.session_state.page = pages[i].split()[-1].lower()

# 4. Page Logic
if st.session_state.page == "reminder":
    st.title("🔔 Advanced Reminder System")
    if not df.empty:
        party = st.selectbox("Client Name", df.iloc[:,0].unique())
        rem_mode = st.radio("Reminder Type select karein:", ["GSTR-1 (Sale)", "GST-3B (Purchase)", "Payment Pending"])

        final_msg = ""
        
        if rem_mode == "GSTR-1 (Sale)":
            final_msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\n*GSTR-1* ki date kareeb hai. Kripya Sale Bills upload karein:\n👉 {PORTAL_LINK}?page=upload&mode=sale"
        
        elif rem_mode == "GST-3B (Purchase)":
            final_msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\n*GST-3B* ki date kareeb hai. Kripya Purchase Bills upload karein:\n👉 {PORTAL_LINK}?page=upload&mode=purchase"
        
        elif rem_mode == "Payment Pending":
            st.subheader("Select Pending Months")
            selected_months = st.multiselect("Mahine chunein jinka payment baaki hai:", 
                                            ["January", "February", "March", "April", "May", "June", 
                                             "July", "August", "September", "October", "November", "December"])
            
            if selected_months:
                total_amt = len(selected_months) * 800
                breakdown = ""
                for m in selected_months:
                    breakdown += f"• {m} Fees: ₹800\n"
                
                final_msg = f"Namaste 🙏, *Shree Services*.\nReminder for *{party}*.\n\nAapka Payment pending hai, kripya jald karein.\n\n*Pending Months:*\n{breakdown}\n*Total Amount: ₹{total_amt}*\n\n*Pay via UPI:* {FIXED_UPI}\nCheck Ledger: {PORTAL_LINK}?page=ledger"
            else:
                st.warning("Kripya kam se kam ek mahina select karein.")

        # Display Message and QR
        if final_msg:
            st.markdown(f"""<div class="reminder-box"><h3>Generated Message:</h3><p style="white-space: pre-wrap;">{final_msg}</p></div>""", unsafe_allow_html=True)
            
            if rem_mode == "Payment Pending":
                st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa={FIXED_UPI}&pn=Shree%20Services", caption="Aapka Payment QR Code")

            if st.button("📲 SEND WHATSAPP"):
                st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(final_msg)}" target="_blank">✅ Click to Open WhatsApp</a>', unsafe_allow_html=True)

# (Baki pages ka code waisa hi rahega)
elif st.session_state.page == "home":
    st.write("### Services Overview")
    st.info("Taxation, Insurance and Online Services are active.")
elif st.session_state.page == "bill":
    st.write("Bill page active.")
elif st.session_state.page == "ledger":
    st.write("Ledger page active.")
elif st.session_state.page == "upload":
    st.write("Upload page active.")

st.markdown('<div class="main-header" style="margin-top:20px; padding:10px;">📞 Contact: 7888273972</div>', unsafe_allow_html=True)
