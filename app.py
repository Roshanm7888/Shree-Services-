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

if "cap_n1" not in st.session_state: st.session_state.cap_n1 = random.randint(1, 5)
if "cap_n2" not in st.session_state: st.session_state.cap_n2 = random.randint(1, 4)

saas_db = load_saas_data()

if "roshan@shreeservices.com" not in saas_db:
    saas_db["roshan@shreeservices.com"] = {
        "password": "admin",
        "profile": {"name": "Shree Services", "legal": "Roshan Mishra", "address": "Mohan Garden, New Delhi", "contact": "7888273972", "gstin": "07SAMPLEGSTIN", "nature": "Goods / Manufacturing / Trading", "format": "Corporate Curve Wave (New Professional)", "border_style": "Solid Line", "gst_enabled": True, "watermark_enabled": True, "watermark_type": "Company Name"},
        "history": [], "parties": {"RKMK Enterprises": {"address": "Delhi", "gstin": "07DEOPA0606H1ZU"}},
        "subscription": "Paid", "bills_created": 0
    }
    save_saas_data(saas_db)

def get_initials(name):
    words = name.split()
    if len(words) >= 2: return (words[0][0] + words[1][0]).upper()
    elif len(words) == 1 and len(words[0]) >= 2: return words[0][:2].upper()
    return "SS"

SESSION_TIMEOUT_SECONDS = 900
if st.session_state.logged_in_user and st.session_state.login_time:
    if (datetime.now() - st.session_state.login_time).total_seconds() > SESSION_TIMEOUT_SECONDS:
        st.session_state.logged_in_user = None
        st.session_state.login_time = None
        st.warning("⏱️ Session expired. Please login again.")
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
            login_id = st.text_input("Email ID / Mobile Number", key="login_id_inp")
            login_pass = st.text_input("Password", type="password", key="login_pass_inp")
            
            n1 = st.session_state.cap_n1
            n2 = st.session_state.cap_n2
            captcha_ans = st.text_input(f"Security Verification: Solve {n1} + {n2} = ?", key="captcha_inp")
            
            if st.button("Login to Portal"):
                try: u_ans = int(captcha_ans.strip())
                except: u_ans = -999

                if u_ans != (n1 + n2):
                    st.error("❌ Incorrect Captcha Answer!")
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
            reg_id = st.text_input("Enter User ID (Email/Mobile)", key="reg_id_inp")
            reg_pass1 = st.text_input("Create Password", type="password", key="reg_pass1_inp")
            reg_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2_inp")
            comp_name = st.text_input("Company / Trade Name", key="comp_name_inp")
            comp_address = st.text_input("Complete Address", key="comp_addr_inp")
            comp_contact = st.text_input("Contact Number", key="comp_cont_inp")
            comp_gstin = st.text_input("Company GSTIN (Optional)", key="comp_gst_inp")
            nature_options = ["Goods / Manufacturing / Trading", "Services", "Transport Company", "Other Business"]
            comp_nature = st.selectbox("Fixed Business Nature", nature_options, key="comp_nat_inp")
            
            if st.button("Register & Create Company Account"):
                if not reg_id or not reg_pass1: st.warning("Fill User ID and Password.")
                elif reg_pass1 != reg_pass2: st.error("Passwords do not match!")
                elif reg_id in saas_db: st.error("User ID already registered!")
                elif not comp_name: st.warning("Enter Company Name.")
                else:
                    saas_db[reg_id] = {
                        "password": reg_pass1,
                        "profile": {"name": comp_name, "address": comp_address, "contact": comp_contact, "gstin": comp_gstin, "nature": comp_nature, "format": "Corporate Curve Wave (New Professional)", "border_style": "Solid Line", "gst_enabled": True, "watermark_enabled": True, "watermark_type": "Company Name"},
                        "history": [], "parties": {"Sample Party": {"address": "Delhi", "gstin": "07AAAAA0000A1Z5"}},
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

    st.sidebar.markdown(f"👤 **User:** `{current_user}`")
    st.sidebar.markdown(f"🏢 **Company:** `{user_data['profile']['name']}`")
    st.sidebar.markdown(f"🌟 **Plan:** `{user_data['subscription']}`")
    
    st.sidebar.markdown("---")
    if st.session_state.login_time:
        rem_secs = max(0, SESSION_TIMEOUT_SECONDS - int((datetime.now() - st.session_state.login_time).total_seconds()))
        st.sidebar.info(f"⏱️ **Session Remaining:** `{rem_secs // 60:02d}:{rem_secs % 60:02d}`")

    st.sidebar.markdown("---")
    menu_options_list = ["Create Invoice", "📊 Party-wise History, Edit & Ledger", "⚙️ Company Profile & Format Settings", "🚪 Logout"]
    menu_option = st.sidebar.radio("Navigation Menu", menu_options_list)

    if menu_option == "🚪 Logout":
        st.session_state.logged_in_user = None
        st.session_state.login_time = None
        st.rerun()

    elif menu_option == "📊 Party-wise History, Edit & Ledger":
        st.markdown("<div class='main-title'><h1>Party Ledger, Profile & Bill Editor</h1></div>", unsafe_allow_html=True)
        if not st.session_state.history: 
            st.info("No invoice history available.")
        else:
            all_parties = list(user_data["parties"].keys())
            sel_party = st.selectbox("Select Party (Tally Ledger Search)", all_parties)
            
            if sel_party in user_data["parties"]:
                p_dat = user_data["parties"][sel_party]
                st.info(f"🏢 **Party Profile:** `{sel_party}` | **Address:** {p_dat.get('address')} | **GSTIN:** {p_dat.get('gstin')}")

            party_bills = [h for h in st.session_state.history if h['client'] == sel_party]
            
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                if party_bills:
                    excel_html = f"<h3>Ledger Statement: {sel_party}</h3><table border='1'><tr style='background:#1e3a8a;color:#fff;'><th>Invoice No</th><th>Date</th><th>Total</th><th>Paid</th><th>Balance</th></tr>"
                    for b in party_bills: excel_html += f"<tr><td>{b['invoice_no']}</td><td>{b['date']}</td><td>{b['total']:.2f}</td><td>{b['paid']:.2f}</td><td>{b['balance']:.2f}</td></tr>"
                    excel_html += "</table>"
                    st.download_button(label=f"📥 Download Excel Ledger", data=excel_html, file_name=f"{sel_party}_Ledger.xls", mime="application/vnd.ms-excel")
            with col_ex2:
                if st.button(f"🖨️ Print Ledger PDF Statement"):
                    ledger_html_doc = f"<!DOCTYPE html><html><body><h2>{user_data['profile']['name']}</h2><p>Ledger Statement for: <b>{sel_party}</b></p><table border='1' style='width:100%;border-collapse:collapse;'><tr><th>Invoice</th><th>Date</th><th>Total</th><th>Paid</th><th>Balance</th></tr>"
                    for b in party_bills: ledger_html_doc += f"<tr><td>{b['invoice_no']}</td><td>{b['date']}</td><td>{b['total']:.2f}</td><td>{b['paid']:.2f}</td><td>{b['balance']:.2f}</td></tr>"
                    ledger_html_doc += "</table></body></html>"
                    st.components.v1.html(ledger_html_doc, height=600, scrolling=True)

            st.markdown("---")
            st.subheader("📝 Edit Generated Bills / Reprint Invoice")
            for bill in party_bills:
                with st.expander(f"Invoice No: {bill['invoice_no']} | Date: {bill['date']} | Total: Rs. {bill['total']}"):
                    new_inv_no = st.text_input("Edit Invoice No", value=bill['invoice_no'], key=f"ein_{bill['invoice_no']}")
                    new_total = st.number_input("Edit Total Amount (Rs.)", value=float(bill['total']), key=f"eto_{bill['invoice_no']}")
                    new_paid = st.number_input("Edit Paid Amount (Rs.)", value=float(bill.get('paid', 0.0)), key=f"epa_{bill['invoice_no']}")
                    
                    col_s, col_d, col_p = st.columns(3)
                    with col_s:
                        if st.button("💾 Save Bill Changes", key=f"sb_{bill['invoice_no']}"):
                            bill['invoice_no'] = new_inv_no
                            bill['total'] = new_total
                            bill['paid'] = new_paid
                            bill['balance'] = new_total - new_paid
                            user_data["history"] = st.session_state.history
                            save_saas_data(saas_db)
                            st.success("Bill Updated Successfully!")
                            st.rerun()
                    with col_d:
                        if st.button("❌ Delete Bill", key=f"db_{bill['invoice_no']}"):
                            st.session_state.history = [h for h in st.session_state.history if h['invoice_no'] != bill['invoice_no']]
                            user_data["history"] = st.session_state.history
                            save_saas_data(saas_db)
                            st.warning("Bill Deleted!")
                            st.rerun()
                    with col_p:
                        if st.button("🖨️ Reprint Edited Bill", key=f"rp_{bill['invoice_no']}"):
                            sel_theme = user_data["profile"].get("format", FORMAT_OPTIONS[0])
                            p_col, wave_gradient = ("#065f46", "linear-gradient(135deg, #059669 0%, #10b981 100%)") if "Emerald Green" in sel_theme else ("#1e3a8a", "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)")
                            reprint_html = f"""
                            <!DOCTYPE html><html><head><meta charset="utf-8"><style>
                                * {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
                                body {{ font-family: Helvetica; background: #e2e8f0; padding: 20px; }}
                                .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 20mm; border: 1px solid #cbd5e1; }}
                                .wave-header {{ background: {wave_gradient} !important; color: #fff !important; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
                                @media print {{ body {{ background: none; padding: 0; }} .no-print {{ display: none !important; }} }}
                            </style></head><body>
                            <div class="no-print" style="text-align: center; margin-bottom: 20px;"><button onclick="window.print()" style="background:#059669;color:white;padding:12px 25px;font-weight:bold;border:none;border-radius:8px;cursor:pointer;">🖨️ Print / Save PDF</button></div>
                            <div class="a4-page">
                                <div class="wave-header"><div><h2>{user_data['profile']['name']}</h2><p>{user_data['profile']['address']}</p></div><div style="text-align:right;"><h2>TAX INVOICE</h2><p>{bill['invoice_no']}</p></div></div>
                                <h3>Billed To: {bill['client']}</h3><hr>
                                <h3>Total Amount: Rs. {bill['total']:.2f} | Paid: Rs. {bill.get('paid',0):.2f} | Balance: Rs. {bill['balance']:.2f}</h3>
                            </div></body></html>
                            """
                            st.components.v1.html(reprint_html, height=750, scrolling=True)

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
        # --- CREATE INVOICE TAB ---
        st.markdown(f"<div class='main-title'><h1>{user_data['profile']['name']}</h1><p>Invoice Mode: <b>{current_nature}</b></p></div>", unsafe_allow_html=True)

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

        # --- DISCOUNT FIELD ADDED ---
        st.markdown("---")
        disc_type = st.radio("Discount Type", ["None", "Percentage (%)", "Flat Amount (Rs.)"], horizontal=True)
        discount_val = st.number_input("Discount Value", min_value=0.0, value=0.0)

        calc_subtotal = subtotal_amt + total_tax_amt
        discount_amount = (calc_subtotal * (discount_val / 100.0)) if disc_type == "Percentage (%)" else discount_val if disc_type == "Flat Amount (Rs.)" else 0.0
        final_total_amt = max(0.0, calc_subtotal - discount_amount)

        total_paid = st.number_input("Total Amount Paid (Rs.)", min_value=0.0, value=0.0)

        if st.button("✨ Finalize & Generate Exact A4 Invoice"):
            balance = final_total_amt - total_paid
            target_party = selected_party if selected_party != "+ Add New Party" else list(user_data["parties"].keys())[-1]
            
            user_data["bills_created"] = user_data.get("bills_created", 0) + 1
            st.session_state.history.append({"invoice_no": inv_no, "client": target_party, "total": final_total_amt, "paid": total_paid, "balance": balance, "date": inv_date, "timestamp": datetime.now().isoformat()})
            user_data["history"] = st.session_state.history
            save_saas_data(saas_db)

            sel_theme = user_data["profile"].get("format", FORMAT_OPTIONS[0])
            p_col, wave_gradient = ("#065f46", "linear-gradient(135deg, #059669 0%, #10b981 100%)") if "Emerald Green" in sel_theme else ("#1e3a8a", "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)")
            
            html_content = f"""
            <!DOCTYPE html><html><head><meta charset="utf-8"><style>
                * {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
                body {{ font-family: Helvetica; background: #e2e8f0; padding: 20px; }}
                .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 20mm; border: 1px solid #cbd5e1; position: relative; }}
                .wave-header {{ background: {wave_gradient} !important; color: #fff !important; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
                @media print {{ body {{ background: none; padding: 0; }} .no-print {{ display: none !important; }} }}
            </style></head><body>
            <div class="no-print" style="text-align: center; margin-bottom: 20px;">
                <button onclick="window.print()" style="background:#059669;color:white;padding:12px 25px;font-weight:bold;border:none;border-radius:8px;cursor:pointer;">🖨️ Print / Save Exact Color PDF</button>
                <a href="https://api.whatsapp.com/send?text=Hello%2C%20Invoice%20No%3A%20{inv_no}%20Total%3A%20Rs.%20{final_total_amt:.2f}" target="_blank" style="background:#25d366;color:white;padding:12px 25px;font-weight:bold;text-decoration:none;border-radius:8px;display:inline-block;margin-left:10px;">📱 Send via WhatsApp</a>
            </div>
            <div class="a4-page">
                <div class="wave-header">
                    <div><h2>{user_data['profile']['name']}</h2><p>{user_data['profile']['address']}</p></div>
                    <div style="text-align:right;"><h2>TAX INVOICE</h2><p>{inv_no}</p></div>
                </div>
                <h3>Billed To: {target_party}</h3>
                <hr>
                <p>Subtotal + Tax: Rs. {calc_subtotal:.2f}</p>
                <p>Discount Applied: - Rs. {discount_amount:.2f}</p>
                <h3>Final Total Amount: Rs. {final_total_amt:.2f} | Balance Due: Rs. {balance:.2f}</h3>
            </div></body></html>
            """
            st.success("Invoice Generated Successfully with Discount!")
            st.components.v1.html(html_content, height=800, scrolling=True)

