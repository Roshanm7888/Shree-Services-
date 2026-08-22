import streamlit as st
from datetime import datetime, timedelta
import json
import os
import time
import pandas as pd
import random

st.set_page_config(page_title="Professional Invoice Portal - SaaS", page_icon="📄", layout="wide")

FORMAT_OPTIONS = [
    "Corporate Curve Wave (New Professional)", 
    "Emerald Green Wave (Modern)", 
    "Sunset Orange Wave (Vibrant)", 
    "Royal Purple Curve (Creative)", 
    "Minimalist Clean (Simple)", 
    "Classic Blue (Standard)"
]

USERS_FILE = "saas_users_data.json"

def load_saas_data():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f: return json.load(f)
        except: pass
    return {}

def save_saas_data(data):
    with open(USERS_FILE, "w") as f: json.dump(data, f, indent=4)

st.markdown("""
    <style>
    @media (max-width: 600px) {
        .main-title { padding: 15px !important; }
        .main-title h1 { font-size: 18px !important; }
        .a4-page { width: 100% !important; padding: 10px !important; }
        div[data-testid="column"] { width: 100% !important; margin-bottom: 8px; }
        .stButton button { width: 100% !important; }
    }
    .login-container { max-width: 500px; margin: 0 auto; background: #ffffff; padding: 30px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
    .benefit-card { background: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 15px; text-align: center; }
    .benefit-card h3 { color: #1e3a8a !important; font-size: 16px; margin-bottom: 8px; font-weight: 700; }
    .benefit-card p { color: #475569 !important; font-size: 13px; margin: 0; }
    label, p, span, div { color: #1e293b !important; }
    input, textarea { background-color: #ffffff !important; color: #1e293b !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; }
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] div, section[data-testid="stSidebar"] .stRadio label { color: #f8fafc !important; }
    section[data-testid="stSidebar"] { background-color: #0f172a !important; }
    select, option, div[data-baseweb="select"] * { background-color: #ffffff !important; color: #1e293b !important; }
    .stApp { background-color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .main-title { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .main-title h1 { margin: 0; font-size: 26px; font-weight: 700; color: #ffffff !important; }
    .main-title p { margin: 5px 0 0 0; font-size: 14px; opacity: 0.9; color: #ffffff !important; }
    div[data-testid="stForm"] { background: #ffffff; padding: 30px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
    .section-box-1 { background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-left: 5px solid #3b82f6; padding: 12px 15px; border-radius: 8px; color: #1e3a8a; font-weight: 700; font-size: 16px; margin-bottom: 15px; }
    .section-box-2 { background: linear-gradient(135deg, #fdf4ff 0%, #fae8ff 100%); border-left: 5px solid #d946ef; padding: 12px 15px; border-radius: 8px; color: #86198f; font-weight: 700; font-size: 16px; margin-top: 20px; margin-bottom: 15px; }
    .section-box-3 { background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border-left: 5px solid #22c55e; padding: 12px 15px; border-radius: 8px; color: #166534; font-weight: 700; font-size: 16px; margin-top: 20px; margin-bottom: 15px; }
    .stFormSubmitButton button, .stButton button { background: linear-gradient(135deg, #059669 0%, #10b981 100%); color: white !important; font-weight: bold; border-radius: 10px; padding: 12px 20px; width: 100%; border: none; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3); font-size: 16px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = None
if "login_time" not in st.session_state: st.session_state.login_time = None
if "inv_rows" not in st.session_state: st.session_state.inv_rows = [{"desc": "", "hsn": "", "unit": "NOS", "qty": 1.0, "rate": 0.0, "tax_type": "Taxable", "tax_pct": 18.0, "amt": 0.0}]
if "c1" not in st.session_state: st.session_state.c1 = random.randint(1, 9)
if "c2" not in st.session_state: st.session_state.c2 = random.randint(1, 9)

saas_db = load_saas_data()

def get_initials(name):
    words = name.split()
    if len(words) >= 2: return (words[0][0] + words[1][0]).upper()
    elif len(words) == 1 and len(words[0]) >= 2: return words[0][:2].upper()
    return "SS"

def ask_gemini_assistant(query):
    q_lower = query.lower()
    if "invoice" in q_lower or "bill" in q_lower or "bana" in q_lower or "create" in q_lower:
        return """📝 **Invoice Create Karne ka Step-by-Step Process:**\n1. Sidebar menu se **'Create Invoice'** par click karein.\n2. Client details bharein aur items add karein.\n3. **'Finalize & Generate Exact A4 Invoice'** button dabayein."""
    else:
        return f"💡 **AI Assistant:** Aapne pucha: '{query}.' Invoice banane ke liye 'Create Invoice' tab use karein!"

SESSION_TIMEOUT_SECONDS = 900
if st.session_state.logged_in_user and st.session_state.login_time:
    elapsed_time = (datetime.now() - st.session_state.login_time).total_seconds()
    if elapsed_time > SESSION_TIMEOUT_SECONDS:
        st.session_state.logged_in_user = None
        st.session_state.login_time = None
        st.warning("⏱️ Session expired due to inactivity. Please login again.")
        st.rerun()

if not st.session_state.logged_in_user:
    st.markdown("""
        <div class="main-title">
            <h1>Professional SaaS Invoice Management Portal</h1>
            <p>Secure Login & Direct Company Registration System</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        auth_tab1, auth_tab2 = st.tabs(["🔐 Login", "📝 New Registration"])
        
        with auth_tab1:
            st.subheader("Existing User Login")
            login_id = st.text_input("Email ID / Mobile Number", key="login_id", value="")
            login_pass = st.text_input("Password", type="password", key="login_pass", value="")
            
            ans1, ans2 = st.session_state.c1, st.session_state.c2
            captcha_input = st.text_input(f"Security Captcha: Solve {ans1} + {ans2} = ?", key="login_captcha")
            
            if st.button("Login to Portal"):
                if "roshan@shreeservices.com" not in saas_db:
                    saas_db["roshan@shreeservices.com"] = {
                        "password": "admin",
                        "profile": {"name": "Shree Services", "legal": "Roshan Mishra", "address": "Mohan Garden, New Delhi", "contact": "7888273972", "gstin": "07SAMPLEGSTIN", "nature": "Goods / Manufacturing / Trading", "format": "Corporate Curve Wave (New Professional)", "border_style": "Solid Line", "gst_enabled": True, "watermark_enabled": True, "watermark_type": "Company Name"},
                        "history": [], "parties": {"RKMK Enterprises": {"legal": "Rinky", "address": "Delhi", "gstin": "07DEOPA0606H1ZU"}},
                        "subscription": "Paid", "bills_created": 0
                    }
                    save_saas_data(saas_db)

                try: user_ans = int(captcha_input.strip())
                except: user_ans = -999

                if user_ans != (ans1 + ans2):
                    st.error("❌ Invalid Security Captcha Answer!")
                elif login_id == "roshan@shreeservices.com" and login_pass == "admin":
                    st.session_state.logged_in_user = login_id
                    st.session_state.login_time = datetime.now()
                    st.success("Admin Login Successful!")
                    st.rerun()
                elif login_id in saas_db and saas_db[login_id]["password"] == login_pass:
                    st.session_state.logged_in_user = login_id
                    st.session_state.login_time = datetime.now()
                    st.success("Login Successful!")
                    st.rerun()
                else: 
                    st.error("❌ Invalid User ID or Password!")
                    
        with auth_tab2:
            st.subheader("Create Company Account")
            reg_id = st.text_input("Enter User ID (Email/Mobile)", key="reg_id", value="")
            reg_pass1 = st.text_input("Create Password", type="password", key="reg_pass1", value="")
            reg_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2", value="")
            comp_name = st.text_input("Company / Trade Name", key="comp_name", value="")
            comp_legal = st.text_input("Authorized Person Name", key="comp_legal", value="")
            comp_address = st.text_input("Complete Address", key="comp_address", value="")
            comp_contact = st.text_input("Contact Number", key="comp_contact", value="")
            comp_gstin = st.text_input("Company GSTIN (Optional)", key="comp_gstin", value="")
            nature_options = ["Goods / Manufacturing / Trading", "Services", "Transport Company", "Other Business"]
            comp_nature = st.selectbox("Fixed Business Nature (Format)", nature_options, key="comp_nature")
            
            if st.button("Register & Create Company Account"):
                if not reg_id or not reg_pass1: st.warning("Please fill User ID and Password fields.")
                elif reg_pass1 != reg_pass2: st.error("Passwords do not match!")
                elif reg_id in saas_db: st.error("User ID already registered!")
                elif not comp_name: st.warning("Please enter Company Name.")
                else:
                    saas_db[reg_id] = {
                        "password": reg_pass1,
                        "profile": {"name": comp_name, "legal": comp_legal, "address": comp_address, "contact": comp_contact, "gstin": comp_gstin, "nature": comp_nature, "format": "Corporate Curve Wave (New Professional)", "border_style": "Solid Line", "gst_enabled": True, "watermark_enabled": True, "watermark_type": "Company Name"},
                        "history": [], "parties": {"Sample Party": {"legal": "Client Name", "address": "Delhi", "gstin": "07AAAAA0000A1Z5"}},
                        "subscription": "Trial", "bills_created": 0
                    }
                    save_saas_data(saas_db)
                    st.success("Account Created Successfully! Go to Login tab.")

else:
    current_user = st.session_state.logged_in_user
    user_data = saas_db[current_user]
    nature_options = ["Goods / Manufacturing / Trading", "Services", "Transport Company", "Other Business"]
    current_nature = user_data["profile"].get("nature", "Goods / Manufacturing / Trading")
    if current_nature not in nature_options: current_nature = nature_options[0]
    
    if "history" not in st.session_state: st.session_state.history = user_data["history"]
    if "saved_parties" not in st.session_state: st.session_state.saved_parties = user_data["parties"]
    if "subscription" not in user_data: user_data["subscription"] = "Trial"
    if "bills_created" not in user_data: user_data["bills_created"] = len(user_data["history"])

    # --- SIDEBAR WITH TIMER ---
    st.sidebar.markdown(f"👤 **User:** `{current_user}`")
    st.sidebar.markdown(f"🏢 **Company:** `{user_data['profile']['name']}`")
    st.sidebar.markdown(f"🌟 **Plan:** `{user_data['subscription']}`")
    
    st.sidebar.markdown("---")
    if st.session_state.login_time:
        rem_secs = max(0, SESSION_TIMEOUT_SECONDS - int((datetime.now() - st.session_state.login_time).total_seconds()))
        rem_mins, rem_s = rem_secs // 60, rem_secs % 60
        st.sidebar.info(f"⏱️ **Session Remaining:** `{rem_mins:02d}:{rem_s:02d}`")

    st.sidebar.markdown("---")
    menu_options_list = ["Create Invoice", "🤖 AI Business Assistant", "📊 Party-wise History & Edit/Delete (24 Days)", "⚙️ Company Profile & Format Settings", "🚪 Logout"]
    menu_option = st.sidebar.radio("Navigation Menu", menu_options_list)

    if menu_option == "🚪 Logout":
        st.session_state.logged_in_user = None
        st.session_state.login_time = None
        st.rerun()

    elif menu_option == "🤖 AI Business Assistant":
        st.markdown("<div class='main-title'><h1>🤖 AI Business Assistant</h1></div>", unsafe_allow_html=True)
        user_query = st.text_area("Type your question here:")
        if st.button("Ask AI Expert") and user_query.strip():
            st.info(ask_gemini_assistant(user_query))

    elif menu_option == "📊 Party-wise History & Edit/Delete (24 Days)":
        st.markdown("<div class='main-title'><h1>Party-wise History, Excel & Ledger PDF</h1></div>", unsafe_allow_html=True)
        if not st.session_state.history: st.info("No invoice history available.")
        else:
            all_parties = list(set([h['client'] for h in st.session_state.history]))
            sel_party = st.selectbox("Select Party", all_parties)
            party_bills = [h for h in st.session_state.history if h['client'] == sel_party]
            
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                if party_bills:
                    excel_html = f"<h3>Ledger: {sel_party}</h3><table border='1'><tr style='background:#1e3a8a;color:#fff;'><th>Invoice No</th><th>Date</th><th>Total</th><th>Paid</th><th>Balance</th></tr>"
                    for b in party_bills: excel_html += f"<tr><td>{b['invoice_no']}</td><td>{b['date']}</td><td>{b['total']:.2f}</td><td>{b['paid']:.2f}</td><td>{b['balance']:.2f}</td></tr>"
                    excel_html += "</table>"
                    st.download_button(label=f"📥 Download Excel Ledger", data=excel_html, file_name=f"{sel_party}_Ledger.xls", mime="application/vnd.ms-excel")
            with col_ex2:
                if st.button(f"🖨️ Print Ledger PDF"):
                    ledger_html_doc = f"<!DOCTYPE html><html><body><h2>{user_data['profile']['name']}</h2><p>Ledger for: {sel_party}</p><table border='1' style='width:100%;border-collapse:collapse;'><tr><th>Invoice</th><th>Date</th><th>Total</th><th>Paid</th><th>Balance</th></tr>"
                    for b in party_bills: ledger_html_doc += f"<tr><td>{b['invoice_no']}</td><td>{b['date']}</td><td>{b['total']:.2f}</td><td>{b['paid']:.2f}</td><td>{b['balance']:.2f}</td></tr>"
                    ledger_html_doc += "</table></body></html>"
                    st.components.v1.html(ledger_html_doc, height=600, scrolling=True)

    elif menu_option == "⚙️ Company Profile & Format Settings":
        st.markdown("<div class='main-title'><h1>Settings & Format Customizer</h1></div>", unsafe_allow_html=True)
        prof = user_data["profile"]
        up_name = st.text_input("Company Name", value=prof.get("name", ""))
        up_address = st.text_input("Address", value=prof.get("address", ""))
        up_contact = st.text_input("Contact", value=prof.get("contact", ""))
        up_gstin = st.text_input("GSTIN", value=prof.get("gstin", ""))
        up_format = st.selectbox("Select Theme", FORMAT_OPTIONS, index=0)
        if st.button("💾 Save Settings"):
            user_data["profile"]["name"] = up_name
            user_data["profile"]["address"] = up_address
            user_data["profile"]["contact"] = up_contact
            user_data["profile"]["gstin"] = up_gstin
            user_data["profile"]["format"] = up_format
            save_saas_data(saas_db)
            st.success("Settings saved!")
            st.rerun()

    else:
        st.markdown(f"<div class='main-title'><h1>{user_data['profile']['name']}</h1><p>Mode: <b>{current_nature}</b></p></div>", unsafe_allow_html=True)
        party_list = list(user_data["parties"].keys()) + ["+ Add New Party"]
        selected_party = st.selectbox("Select Party", party_list)
        if selected_party == "+ Add New Party":
            with st.form("new_party"):
                n_trade = st.text_input("Trade Name")
                n_addr = st.text_input("Address")
                n_gstin = st.text_input("GSTIN")
                if st.form_submit_button("Save Party") and n_trade.strip():
                    user_data["parties"][n_trade.strip()] = {"address": n_addr, "gstin": n_gstin}
                    save_saas_data(saas_db)
                    st.success("Saved!")
                    st.rerun()

        inv_no = st.text_input("Invoice Number", f"TAX/2026-27/{len(st.session_state.history)+1:03d}")
        inv_date = st.text_input("Date", datetime.now().strftime("%B %d, %Y"))

        if st.button("➕ Add Item Row"): st.session_state.inv_rows.append({"desc": "", "hsn": "", "unit": "NOS", "qty": 1.0, "rate": 0.0, "tax_type": "Taxable", "tax_pct": 18.0, "amt": 0.0})

        subtotal_amt, total_tax_amt = 0.0, 0.0
        for i, row in enumerate(st.session_state.inv_rows):
            c1, c2, c3, c4 = st.columns([4, 2, 2, 2])
            row['desc'] = c1.text_input("Item Description", value=row['desc'], key=f"d_{i}")
            row['qty'] = c2.number_input("Qty", value=row['qty'], key=f"q_{i}")
            row['rate'] = c3.number_input("Rate", value=row['rate'], key=f"r_{i}")
            row['amt'] = row['qty'] * row['rate']
            c4.markdown(f"**Amt:** Rs. {row['amt']:.2f}")
            subtotal_amt += row['amt']
            total_tax_amt += row['amt'] * 0.18

        total_paid = st.number_input("Total Amount Paid (Rs.)", min_value=0.0, value=0.0)

        if st.button("✨ Finalize & Generate Exact A4 Invoice"):
            total_amt = subtotal_amt + total_tax_amt
            balance = total_amt - total_paid
            target_party = selected_party if selected_party != "+ Add New Party" else list(user_data["parties"].keys())[-1]
            
            st.session_state.history.append({"invoice_no": inv_no, "client": target_party, "total": total_amt, "paid": total_paid, "balance": balance, "date": inv_date, "timestamp": datetime.now().isoformat()})
            user_data["history"] = st.session_state.history
            save_saas_data(saas_db)

            html_content = f"""
            <!DOCTYPE html><html><head><meta charset="utf-8"><style>
                * {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
                body {{ font-family: Helvetica; background: #e2e8f0; padding: 20px; }}
                .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 20mm; border: 1px solid #cbd5e1; }}
                .wave-header {{ background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%) !important; color: #fff !important; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
            </style></head><body>
            <div style="text-align: center; margin-bottom: 20px;">
                <button onclick="window.print()" style="background:#059669;color:white;padding:12px 25px;font-weight:bold;border:none;border-radius:8px;cursor:pointer;">🖨️ Print / Save Exact Color PDF</button>
                <a href="https://api.whatsapp.com/send?text=Hello%2C%20Invoice%20No%3A%20{inv_no}%20Total%3A%20Rs.%20{total_amt:.2f}" target="_blank" style="background:#25d366;color:white;padding:12px 25px;font-weight:bold;text-decoration:none;border-radius:8px;display:inline-block;margin-left:10px;">📱 Send via WhatsApp</a>
            </div>
            <div class="a4-page">
                <div class="wave-header">
                    <div><h2>{user_data['profile']['name']}</h2><p>{user_data['profile']['address']}</p></div>
                    <div style="text-align:right;"><h2>TAX INVOICE</h2><p>{inv_no}</p></div>
                </div>
                <h3>Billed To: {target_party}</h3>
                <hr>
                <h3>Total Amount: Rs. {total_amt:.2f} | Balance Due: Rs. {balance:.2f}</h3>
            </div></body></html>
            """
            st.success("Invoice Generated Successfully!")
            st.components.v1.html(html_content, height=800, scrolling=True)

