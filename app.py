import streamlit as st
from datetime import datetime, timedelta
import json
import os
import time
import pandas as pd
import random

# ==========================================
# 1. PAGE CONFIGURATION & INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="Professional Invoice Portal - SaaS Enterprise Edition", 
    page_icon="📄", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. GLOBAL CONSTANTS & STORAGE UTILITIES
# ==========================================
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
            with open(USERS_FILE, "r") as database_file: 
                return json.load(database_file)
        except Exception as file_error:
            st.error(f"Error loading storage database: {file_error}")
    return {}

def save_saas_data(database_payload):
    try:
        with open(USERS_FILE, "w") as database_file: 
            json.dump(database_payload, database_file, indent=4)
    except Exception as file_error:
        st.error(f"Error saving storage database: {file_error}")

# ==========================================
# 3. ENTERPRISE STYLING & RESPONSIVE CSS
# ==========================================
st.markdown("""
    <style>
    @media (max-width: 600px) {
        .main-title { padding: 15px !important; }
        .main-title h1 { font-size: 18px !important; }
        .a4-page { width: 100% !important; padding: 10px !important; }
        div[data-testid="column"] { width: 100% !important; margin-bottom: 8px; }
        .stButton button { width: 100% !important; }
    }
    
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        background: #ffffff;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }

    .benefit-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 15px;
        text-align: center;
    }
    
    .benefit-card h3 { color: #1e3a8a !important; font-size: 16px; margin-bottom: 8px; font-weight: 700; }
    .benefit-card p { color: #475569 !important; font-size: 13px; margin: 0; }

    label, p, span, div { color: #1e293b !important; }
    input, textarea { background-color: #ffffff !important; color: #1e293b !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; }
    
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] div, 
    section[data-testid="stSidebar"] .stRadio label { color: #f8fafc !important; }
    
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

# ==========================================
# 4. SESSION STATE INITIALIZATION
# ==========================================
if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = None
if "login_time" not in st.session_state: st.session_state.login_time = None
if "inv_rows" not in st.session_state: 
    st.session_state.inv_rows = [{"desc": "", "hsn": "-", "unit": "NOS", "qty": 1.0, "rate": 0.0, "tax_type": "Taxable", "tax_pct": 18.0, "amt": 0.0}]

if "cap_n1" not in st.session_state: st.session_state.cap_n1 = random.randint(1, 5)
if "cap_n2" not in st.session_state: st.session_state.cap_n2 = random.randint(1, 4)

saas_db = load_saas_data()

if "roshan@shreeservices.com" not in saas_db:
    saas_db["roshan@shreeservices.com"] = {
        "password": "admin",
        "profile": {
            "name": "Shree Services", "legal": "Roshan Mishra", "address": "Mohan Garden, New Delhi", 
            "contact": "7888273972", "gstin": "07SAMPLEGSTIN", "nature": "Goods / Manufacturing / Trading", 
            "format": "Corporate Curve Wave (New Professional)", "border_style": "Solid Line", 
            "custom_logo": "", "watermark_enabled": True, "watermark_type": "Company Name",
            "bank_name": "State Bank of India", "acc_no": "1234567890", "ifsc": "SBIN0016324", "branch": "Nashik Ashok Nagar",
            "terms": "1. Payment shall be made on a quarterly basis (e.g., April, May, June constitutes Q1).\n2. All quarterly invoices are due and payable strictly on or before the 20th of the month following the quarter-end.\n3. Late payments will attract an interest charge of 18% per annum."
        },
        "history": [], "parties": {"RKMK Enterprises": {"address": "Delhi", "gstin": "07DEOPA0606H1ZU"}},
        "subscription": "Paid", "bills_created": 0
    }
    save_saas_data(saas_db)

def get_initials(company_name):
    words = company_name.split()
    if len(words) >= 2: return (words[0][0] + words[1][0]).upper()
    elif len(words) == 1 and len(words[0]) >= 2: return words[0][:2].upper()
    return "SS"

def ask_gemini_assistant(user_query):
    query_lower = user_query.lower()
    if "invoice" in query_lower or "bill" in query_lower:
        return "📝 **Invoice Guide:** Use the 'Create Invoice' tab. Toggle 'Enable GST Tax Invoice Mode' ON for Tax Invoices or OFF for Bills of Supply."
    return f"💡 **AI Assistant:** Regarding '{query_lower}', navigate using the sidebar menu."

SESSION_TIMEOUT_SECONDS = 900
if st.session_state.logged_in_user and st.session_state.login_time:
    if (datetime.now() - st.session_state.login_time).total_seconds() > SESSION_TIMEOUT_SECONDS:
        st.session_state.logged_in_user = None
        st.session_state.login_time = None
        st.warning("⏱️ Session expired. Please login again.")
        st.rerun()

# ==========================================
# 5. AUTHENTICATION & LANDING ROUTING
# ==========================================
if not st.session_state.logged_in_user:
    st.markdown("""
        <div class="main-title">
            <h1>Professional SaaS Invoice Management Portal</h1>
            <p>Secure Enterprise Login & Direct Company Registration System</p>
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
                try: user_ans = int(captcha_ans.strip())
                except: user_ans = -999

                if user_ans != (n1 + n2):
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
            st.subheader("Create Enterprise Account")
            reg_id = st.text_input("Enter User ID (Email/Mobile)", key="reg_id_inp")
            reg_pass1 = st.text_input("Create Password", type="password", key="reg_pass1_inp")
            reg_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2_inp")
            comp_name = st.text_input("Company / Trade Name", key="comp_name_inp")
            comp_address = st.text_input("Complete Address", key="comp_addr_inp")
            comp_contact = st.text_input("Contact Number", key="comp_cont_inp")
            comp_gstin = st.text_input("Company GSTIN (Optional)", key="comp_gst_inp")
            nature_options = ["Goods / Manufacturing / Trading", "Services", "Transport Company", "Other Business"]
            comp_nature = st.selectbox("Fixed Business Nature", nature_options, key="comp_nat_inp")
            
            if st.button("Register & Create Enterprise Account"):
                if not reg_id or not reg_pass1: st.warning("Fill User ID and Password.")
                elif reg_pass1 != reg_pass2: st.error("Passwords do not match!")
                elif reg_id in saas_db: st.error("User ID already registered!")
                elif not comp_name: st.warning("Enter Company Name.")
                else:
                    saas_db[reg_id] = {
                        "password": reg_pass1,
                        "profile": {
                            "name": comp_name, "address": comp_address, "contact": comp_contact, 
                            "gstin": comp_gstin, "nature": comp_nature, "format": "Corporate Curve Wave (New Professional)", 
                            "border_style": "Solid Line", "custom_logo": "", "watermark_enabled": True, "watermark_type": "Company Name",
                            "bank_name": "State Bank of India", "acc_no": "1234567890", "ifsc": "SBIN0016324", "branch": "Nashik Ashok Nagar",
                            "terms": "1. Payment on quarterly basis by 20th of quarter-end month."
                        },
                        "history": [], "parties": {"Sample Party": {"address": "New Delhi", "gstin": "07AAAAA0000A1Z5"}},
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
    menu_options_list = [
        "Create Invoice", 
        "🤖 AI Business Assistant", 
        "📊 Party-wise History, Item Editor & Ledger", 
        "⚙️ Company Profile & Format Settings", 
        "🚪 Logout"
    ]
    menu_option = st.sidebar.radio("Navigation Menu", menu_options_list)

    if menu_option == "🚪 Logout":
        st.session_state.logged_in_user = None
        st.session_state.login_time = None
        st.rerun()

    elif menu_option == "🤖 AI Business Assistant":
        st.markdown("<div class='main-title'><h1>🤖 AI Business & Tax Assistant</h1></div>", unsafe_allow_html=True)
        user_query = st.text_area("Type your question here:")
        if st.button("Ask AI Expert"):
            if user_query.strip():
                st.info(ask_gemini_assistant(user_query))
            else: st.warning("Please enter a question.")

    elif menu_option == "📊 Party-wise History, Item Editor & Ledger":
        st.markdown("<div class='main-title'><h1>Tally-Grade Party Ledger & Item-Level Bill Editor</h1></div>", unsafe_allow_html=True)
        
        if not user_data["parties"]: 
            st.info("No parties registered yet.")
        else:
            all_parties = list(user_data["parties"].keys())
            sel_party = st.selectbox("Select Party (Tally Ledger Search)", all_parties)
            
            if sel_party in user_data["parties"]:
                p_dat = user_data["parties"][sel_party]
                st.info(f"🏢 **Party Master Profile:** `{sel_party}` | **Address:** {p_dat.get('address')} | **GSTIN:** {p_dat.get('gstin')}")

                with st.expander(f"✏️ Edit Party Master Profile ({sel_party}) - Tally Style"):
                    edit_p_addr = st.text_input("Edit Party Address", value=p_dat.get('address', ''), key=f"epa_{sel_party}")
                    edit_p_gst = st.text_input("Edit Party GSTIN", value=p_dat.get('gstin', ''), key=f"epg_{sel_party}")
                    if st.button("💾 Save Party Profile Changes", key=f"svp_{sel_party}"):
                        user_data["parties"][sel_party]["address"] = edit_p_addr
                        user_data["parties"][sel_party]["gstin"] = edit_p_gst
                        save_saas_data(saas_db)
                        st.success("Party Profile Updated Successfully!")
                        st.rerun()

            party_bills = [h for h in user_data["history"] if h['client'] == sel_party]
            
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                if party_bills:
                    excel_html = f"<h3>Statement: {sel_party}</h3><table border='1'><tr style='background:#1e3a8a;color:#fff;'><th>Invoice No</th><th>Date</th><th>Total</th><th>Paid</th><th>Balance</th></tr>"
                    for b in party_bills: excel_html += f"<tr><td>{b['invoice_no']}</td><td>{b['date']}</td><td>{b['total']:.2f}</td><td>{b['paid']:.2f}</td><td>{b['balance']:.2f}</td></tr>"
                    excel_html += "</table>"
                    st.download_button(label=f"📥 Download Excel Ledger", data=excel_html, file_name=f"{sel_party}_Ledger.xls", mime="application/vnd.ms-excel")
            with col_ex2:
                if st.button(f"🖨️ Print Ledger PDF Statement"):
                    ledger_html_doc = f"<!DOCTYPE html><html><body><h2>{user_data['profile']['name']}</h2><p>Ledger for: <b>{sel_party}</b></p><table border='1' style='width:100%;border-collapse:collapse;'><tr><th>Invoice</th><th>Date</th><th>Total</th><th>Paid</th><th>Balance</th></tr>"
                    for b in party_bills: ledger_html_doc += f"<tr><td>{b['invoice_no']}</td><td>{b['date']}</td><td>{b['total']:.2f}</td><td>{b['paid']:.2f}</td><td>{b['balance']:.2f}</td></tr>"
                    ledger_html_doc += "</table></body></html>"
                    st.components.v1.html(ledger_html_doc, height=600, scrolling=True)

            st.markdown("---")
            st.subheader("📝 Edit Bill Items & Reprint")
            for bill in party_bills:
                with st.expander(f"Invoice No: {bill['invoice_no']} | Date: {bill['date']} | Total: Rs. {bill['total']}"):
                    new_inv_no = st.text_input("Edit Invoice No", value=bill['invoice_no'], key=f"ein_{bill['invoice_no']}")
                    new_paid = st.number_input("Edit Paid Amount (Rs.)", value=float(bill.get('paid', 0.0)), key=f"epa_{bill['invoice_no']}")
                    
                    if "parsed_items" not in bill: 
                        bill["parsed_items"] = [{"desc": "Item", "hsn": "-", "unit": "NOS", "qty": 1.0, "rate": float(bill['total']), "tax_type": "Taxable", "tax_pct": 18.0, "amt": float(bill['total'])}]
                    
                    updated_items = []
                    new_subtotal = 0.0
                    new_tax_amt = 0.0
                    
                    for idx, itm in enumerate(bill["parsed_items"]):
                        col_it1, col_it2, col_it3, col_it4, col_del = st.columns([3, 1.5, 1.5, 1.5, 1])
                        i_desc = col_it1.text_input("Description", value=itm.get('desc',''), key=f"id_{bill['invoice_no']}_{idx}")
                        i_qty = col_it2.number_input("Qty", value=float(itm.get('qty', 1.0)), key=f"iq_{bill['invoice_no']}_{idx}")
                        i_rate = col_it3.number_input("Rate", value=float(itm.get('rate', 0.0)), key=f"ir_{bill['invoice_no']}_{idx}")
                        i_amt = i_qty * i_rate
                        col_it4.markdown(f"**Amt:** {i_amt:.2f}")
                        
                        keep_item = col_del.checkbox("Keep", value=True, key=f"k_{bill['invoice_no']}_{idx}")
                        if keep_item:
                            updated_items.append({"desc": i_desc, "hsn": itm.get('hsn', '-'), "unit": itm.get('unit', 'NOS'), "qty": i_qty, "rate": i_rate, "tax_type": itm.get('tax_type', 'Taxable'), "tax_pct": float(itm.get('tax_pct', 18.0)), "amt": i_amt})
                            new_subtotal += i_amt
                            if itm.get('tax_type', 'Taxable') == "Taxable":
                                new_tax_amt += i_amt * (float(itm.get('tax_pct', 18.0)) / 100.0)

                    is_tax_inv = bill.get("is_tax_invoice", True)
                    actual_tax_amt = new_tax_amt if is_tax_inv else 0.0
                    new_total_amt = new_subtotal + actual_tax_amt
                    new_balance = new_total_amt - new_paid
                    
                    col_s, col_d, col_p = st.columns(3)
                    with col_s:
                        if st.button("💾 Save Bill Changes", key=f"sb_{bill['invoice_no']}"):
                            bill['invoice_no'] = new_inv_no
                            bill['parsed_items'] = updated_items
                            bill['total'] = new_total_amt
                            bill['paid'] = new_paid
                            bill['balance'] = new_balance
                            user_data["history"] = st.session_state.history
                            save_saas_data(saas_db)
                            st.success("Bill Updated Successfully!")
                            st.rerun()
                    with col_d:
                        if st.button("❌ Delete Bill", key=f"db_{bill['invoice_no']}"):
                            user_data["history"] = [h for h in user_data["history"] if h['invoice_no'] != bill['invoice_no']]
                            save_saas_data(saas_db)
                            st.warning("Bill Deleted!")
                            st.rerun()
                    with col_p:
                        if st.button("🖨️ Reprint Bill", key=f"rp_{bill['invoice_no']}"):
                            sel_theme = user_data["profile"].get("format", FORMAT_OPTIONS[0])
                            if "Emerald Green" in sel_theme: p_col, wave_gradient = "#065f46", "linear-gradient(135deg, #059669 0%, #10b981 100%)"
                            elif "Sunset Orange" in sel_theme: p_col, wave_gradient = "#c2410c", "linear-gradient(135deg, #ea580c 0%, #fb923c 100%)"
                            elif "Royal Purple" in sel_theme: p_col, wave_gradient = "#581c87", "linear-gradient(135deg, #7e22ce 0%, #a855f7 100%)"
                            elif "Minimalist Clean" in sel_theme: p_col, wave_gradient = "#334155", "linear-gradient(135deg, #475569 0%, #64748b 100%)"
                            elif "Classic Blue" in sel_theme: p_col, wave_gradient = "#1e3a8a", "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)"
                            else: p_col, wave_gradient = "#0f172a", "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)"
                            
                            print_rows = "".join([f"<tr><td>{r['desc']}</td><td>{r['qty']}</td><td>{r['rate']:.2f}</td><td>{r['tax_type']} ({r['tax_pct']}%)</td><td style='text-align:right;'>{r['amt']:.2f}</td></tr>" for r in bill["parsed_items"]])
                            comp_terms = user_data["profile"].get("terms", "Standard terms apply.")
                            inv_title_text = "TAX INVOICE" if is_tax_inv else "BILL OF SUPPLY"
                            
                            reprint_html = f"""
                            <!DOCTYPE html><html><head><meta charset="utf-8"><style>
                                * {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
                                body {{ font-family: Helvetica; background: #e2e8f0; padding: 20px; }}
                                .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 20mm; border: 1px solid #cbd5e1; }}
                                .wave-header {{ background: {wave_gradient} !important; color: #fff !important; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
                                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                                th, td {{ border: 1px solid #cbd5e1; padding: 8px; font-size: 13px; }}
                                th {{ background: {p_col}; color: white; text-align: left; }}
                                @media print {{ body {{ background: none; padding: 0; }} .no-print {{ display: none !important; }} }}
                            </style></head><body>
                            <div class="no-print" style="text-align: center; margin-bottom: 20px;"><button onclick="window.print()" style="background:#059669;color:white;padding:12px 25px;font-weight:bold;border:none;border-radius:8px;cursor:pointer;">🖨️ Print / Save PDF</button></div>
                            <div class="a4-page">
                                <div class="wave-header">
                                    <div><h2>{user_data['profile']['name']}</h2><p>{user_data['profile']['address']}<br>Contact: {user_data['profile']['contact']}<br>GSTIN: {user_data['profile']['gstin']}</p></div>
                                    <div style="text-align:right;"><h2>{inv_title_text}</h2><p>{bill['invoice_no']}</p></div>
                                </div>
                                <table style="width:100%; border-collapse:collapse; margin-bottom:20px;"><tr>
                                <td style="padding:10px; border:1px solid #cbd5e1;"><strong>Service Provider:</strong><br>{user_data['profile']['name']}<br>Address: {user_data['profile']['address']}<br>Contact: {user_data['profile']['contact']}<br>GSTIN: {user_data['profile']['gstin']}</td>
                                <td style="padding:10px; border:1px solid #cbd5e1;"><strong>Billed To:</strong><br>{bill['client']}</td>
                                </tr></table>
                                <table><thead><tr><th>Description</th><th>Qty</th><th>Rate</th><th>Tax Type</th><th style='text-align:right;'>Amount</th></tr></thead><tbody>{print_rows}</tbody></table>
                                <br>
                                <h3>Total Amount: Rs. {bill['total']:.2f} | Paid: Rs. {bill.get('paid',0):.2f} | Balance: Rs. {bill['balance']:.2f}</h3>
                                <br><hr><p style="font-size:11px; white-space: pre-line;"><strong>Terms & Conditions:</strong><br>{comp_terms}</p>
                            </div></body></html>
                            """
                            st.components.v1.html(reprint_html, height=750, scrolling=True)

    # ==========================================
    # 11. COMPANY PROFILE & FORMAT SETTINGS (RESTORED FULL UI)
    # ==========================================
    elif menu_option == "⚙️ Company Profile & Format Settings":
        st.markdown("<div class='main-title'><h1>Settings, Theme & Format Customizer</h1></div>", unsafe_allow_html=True)
        prof = user_data["profile"]
        
        st.subheader("🏢 Company Information")
        up_name = st.text_input("Company Name", value=prof.get("name", ""))
        up_address = st.text_input("Address", value=prof.get("address", ""))
        up_contact = st.text_input("Contact", value=prof.get("contact", ""))
        up_gstin = st.text_input("GSTIN", value=prof.get("gstin", ""))
        
        st.subheader("🎨 Invoice Theme & Visual Branding")
        fmt_val = prof.get("format", FORMAT_OPTIONS[0])
        fmt_idx = FORMAT_OPTIONS.index(fmt_val) if fmt_val in FORMAT_OPTIONS else 0
        up_format = st.selectbox("Select Invoice Designer Theme", FORMAT_OPTIONS, index=fmt_idx)
        
        up_custom_logo = st.text_input("Logo Image URL (Optional)", value=prof.get("custom_logo", ""))
        up_watermark_enabled = st.checkbox("Enable Background Watermark on Invoice", value=prof.get("watermark_enabled", True))
        wm_type_val = prof.get("watermark_type", "Company Name")
        up_watermark_type = st.radio("Watermark Content Type", ["Company Name", "Logo Initials"], index=0 if wm_type_val == "Company Name" else 1)

        st.subheader("🏦 Bank Details for Invoice Footer")
        col_b1, col_b2 = st.columns(2)
        up_bank_name = col_b1.text_input("Bank Name", value=prof.get("bank_name", ""))
        up_acc_no = col_b2.text_input("Account Number", value=prof.get("acc_no", ""))
        col_b3, col_b4 = st.columns(2)
        up_ifsc = col_b3.text_input("IFSC Code", value=prof.get("ifsc", ""))
        up_branch = col_b4.text_input("Branch Name", value=prof.get("branch", ""))
        
        st.subheader("📜 Terms & Conditions")
        up_terms = st.text_area("Invoice Terms & Conditions", value=prof.get("terms", "Standard terms apply."), height=120)
        
        if st.button("💾 Save All Enterprise Settings"):
            user_data["profile"]["name"] = up_name
            user_data["profile"]["address"] = up_address
            user_data["profile"]["contact"] = up_contact
            user_data["profile"]["gstin"] = up_gstin
            user_data["profile"]["format"] = up_format
            user_data["profile"]["custom_logo"] = up_custom_logo
            user_data["profile"]["watermark_enabled"] = up_watermark_enabled
            user_data["profile"]["watermark_type"] = up_watermark_type
            user_data["profile"]["bank_name"] = up_bank_name
            user_data["profile"]["acc_no"] = up_acc_no
            user_data["profile"]["ifsc"] = up_ifsc
            user_data["profile"]["branch"] = up_branch
            user_data["profile"]["terms"] = up_terms
            save_saas_data(saas_db)
            st.success("All Settings, Themes & Terms saved successfully!")
            st.rerun()

        st.markdown("---")
        st.markdown("### 👁️ Instant Full A4 Size Live Preview")
        if "Emerald Green" in up_format: p_col, wave_gradient = "#065f46", "linear-gradient(135deg, #059669 0%, #10b981 100%)"
        elif "Sunset Orange" in up_format: p_col, wave_gradient = "#c2410c", "linear-gradient(135deg, #ea580c 0%, #fb923c 100%)"
        elif "Royal Purple" in up_format: p_col, wave_gradient = "#581c87", "linear-gradient(135deg, #7e22ce 0%, #a855f7 100%)"
        elif "Minimalist Clean" in up_format: p_col, wave_gradient = "#334155", "linear-gradient(135deg, #475569 0%, #64748b 100%)"
        elif "Classic Blue" in up_format: p_col, wave_gradient = "#1e3a8a", "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)"
        else: p_col, wave_gradient = "#0f172a", "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)"

        init = get_initials(up_name)
        logo_html = f"<div style='width: 50px; height: 50px; background: {p_col}; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: bold; border-radius: 8px;'>{init}</div>"
        if up_custom_logo.strip(): logo_html = f"<img src='{up_custom_logo}' style='max-height: 50px; max-width: 50px; object-fit: contain;'>"
        wm_text = up_name if up_watermark_type == "Company Name" else init
        wm_html = f'<div style="position: absolute; top: 40%; left: 20%; transform: rotate(-30deg); font-size: 90px; font-weight: bold; color: rgba(0, 0, 0, 0.04); z-index: 0; pointer-events: none; white-space: nowrap;">{wm_text}</div>' if up_watermark_enabled else ""

        full_a4_preview_html = f"""
        <!DOCTYPE html><html><head><meta charset="utf-8"><style>
            body {{ font-family: Helvetica, Arial; color: #1e293b; background: #e2e8f0; margin: 0; padding: 20px; }}
            .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 15mm 20mm; box-sizing: border-box; border: 1px solid #cbd5e1; position: relative; overflow: hidden; }}
            .wave-header {{ background: {wave_gradient}; color: #fff; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom-left-radius: 30px; border-bottom-right-radius: 30px; }}
            .company-title {{ font-size: 24px; font-weight: bold; color: #ffffff; }}
            .invoice-title {{ font-size: 26px; font-weight: bold; text-transform: uppercase; color: #ffffff; text-align: right; }}
            .billing-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; border: 1px solid #cbd5e1; background: #f8fafc; }}
            .billing-table td {{ padding: 12px; vertical-align: top; width: 50%; font-size: 13px; border: 1px solid #cbd5e1; }}
            .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            .items-table th {{ background-color: {p_col}; color: #fff; text-align: left; padding: 10px; font-size: 12px; border: 1px solid {p_col}; }}
            .items-table td {{ border: 1px solid #cbd5e1; padding: 10px; font-size: 12px; }}
            .right {{ text-align: right; }}
            .totals {{ width: 300px; margin-left: auto; font-size: 13px; border: 1px solid #cbd5e1; border-collapse: collapse; }}
            .totals td {{ padding: 8px; border: 1px solid #cbd5e1; }}
            .grand-total {{ font-weight: bold; background: #eff6ff; font-size: 14px; color: {p_col}; }}
        </style></head><body><div class="a4-page">
            {wm_html}
            <div class="wave-header">
                <div style="display: flex; gap: 15px; align-items:center;">{logo_html}<div><div class="company-title">{up_name}</div><div style="font-size: 12px; color: #e2e8f0;">{up_address}<br>Contact: {up_contact}</div></div></div>
                <div><div class="invoice-title">Tax Invoice</div><div style="font-size: 12px; color: #e2e8f0; text-align: right;">Invoice No: TAX/2026-27/001</div></div>
            </div>
            <table class="billing-table"><tr><td><strong>Service Provider:</strong><br>{up_name}</td><td><strong>Billed To:</strong><br>Sample Client</td></tr></table>
            <table class="items-table"><thead><tr><th>S.No.</th><th>Description</th><th>Mode</th><th class='right'>Amount (Rs.)</th></tr></thead><tbody><tr><td>1</td><td>Sample Item</td><td>{up_nature}</td><td class='right'>700.00</td></tr></tbody></table>
            <table class="totals"><tr><td>Subtotal:</td><td class="right">Rs. 700.00</td></tr><tr><td>GST (18%):</td><td class="right">Rs. 126.00</td></tr><tr class="grand-total"><td>Total Amount:</td><td class="right">Rs. 826.00</td></tr></table>
        </div></body></html>
        """
        st.components.v1.html(full_a4_preview_html, height=800, scrolling=True)

    # ==========================================
    # 12. CREATE INVOICE WORKFLOW TAB (WITH GST TOGGLE)
    # ==========================================
    else:
        st.markdown(f"<div class='main-title'><h1>{user_data['profile']['name']}</h1><p>Invoice Mode: <b>{current_nature}</b></p></div>", unsafe_allow_html=True)

        if user_data["subscription"] == "Trial" and user_data.get("bills_created", 0) >= 1:
            st.error("🚨 **Free Trial Limit Reached!** Subscribe via UPI: **`roshan@shreeservices.upi`**")
            with st.form("subscription_payment_form"):
                tx_id_input = st.text_input("Enter UPI Transaction Reference ID (UTR / Txn ID)")
                if st.form_submit_button("Submit Payment for Activation") and tx_id_input.strip():
                    user_data["subscription"] = "Pending Approval"
                    save_saas_data(saas_db)
                    st.success("Transaction submitted successfully! Admin will review shortly.")
                    st.rerun()
            st.stop()
        elif user_data["subscription"] == "Pending Approval":
            st.info("⏳ **Payment Verification Pending:** Your payment is under review by admin.")
            st.stop()

        next_inv_num = len(user_data["history"]) + 1
        current_inv_no = f"TAX/2026-27/{next_inv_num:03d}"

        # --- TAX INVOICE vs BILL OF SUPPLY TOGGLE ---
        st.markdown('<div class="section-box-1">🎛️ Invoice Type Control (GST Toggle)</div>', unsafe_allow_html=True)
        is_tax_invoice = st.toggle("Enable GST Tax Invoice Mode (ON = Tax Invoice | OFF = Bill of Supply / Non-GST)", value=True)

        st.markdown('<div class="section-box-1">👤 1. Client / Party Details</div>', unsafe_allow_html=True)
        party_list = list(user_data["parties"].keys()) + ["+ Add New Party"]
        selected_party = st.selectbox("Select Party", party_list)

        if selected_party == "+ Add New Party":
            with st.form("new_party_form"):
                n_trade = st.text_input("Trade Name")
                n_legal = st.text_input("Legal Name")
                n_addr = st.text_input("Address")
                n_gstin = st.text_input("GSTIN")
                if st.form_submit_button("Save Party Permanently") and n_trade.strip():
                    user_data["parties"][n_trade.strip()] = {"legal": n_legal, "address": n_addr, "gstin": n_gstin}
                    save_saas_data(saas_db)
                    st.success("Party Saved Successfully!")
                    st.rerun()

        st.markdown('<div class="section-box-2">📋 2. Invoice Meta Details</div>', unsafe_allow_html=True)
        col_i1, col_i2 = st.columns(2)
        inv_no = col_i1.text_input("Invoice Number", current_inv_no)
        inv_date = col_i2.text_input("Invoice Date", datetime.now().strftime("%B %d, %Y"))

        st.markdown(f'<div class="section-box-3">💼 3. Items & Grid Entry ({current_nature})</div>', unsafe_allow_html=True)
        if st.button("➕ Add Row"): 
            st.session_state.inv_rows.append({"desc": "", "hsn": "-", "unit": "NOS", "qty": 1.0, "rate": 0.0, "tax_type": "Taxable", "tax_pct": 18.0, "amt": 0.0})

        subtotal_amt, total_tax_amt = 0.0, 0.0
        for i, row in enumerate(st.session_state.inv_rows):
            st.markdown(f"**Item Row {i+1}**")
            if is_tax_invoice:
                c1, c2, c3, c4, c5, c6 = st.columns([3, 1.5, 1.5, 1.5, 1.5, 1.5])
                row['desc'] = c1.text_input("Description", value=row['desc'], key=f"d_{i}")
                row['qty'] = c2.number_input("Qty", value=row['qty'], key=f"q_{i}")
                row['rate'] = c3.number_input("Rate", value=row['rate'], key=f"r_{i}")
                row['tax_type'] = c4.selectbox("Tax Type", ["Taxable", "Nil Rated / Exempt"], key=f"tt_{i}")
                row['tax_pct'] = c5.selectbox("Tax %", [0.0, 5.0, 12.0, 18.0, 28.0], index=3, key=f"tp_{i}")
                
                base_amt = row['qty'] * row['rate']
                row['amt'] = base_amt
                c6.markdown(f"**Amt:** Rs. {base_amt:.2f}")
                
                subtotal_amt += base_amt
                if row['tax_type'] == "Taxable":
                    total_tax_amt += base_amt * (row['tax_pct'] / 100.0)
            else:
                c1, c2, c3, c4 = st.columns([4, 2, 2, 2])
                row['desc'] = c1.text_input("Description", value=row['desc'], key=f"d_ng_{i}")
                row['qty'] = c2.number_input("Qty", value=row['qty'], key=f"q_ng_{i}")
                row['rate'] = c3.number_input("Rate", value=row['rate'], key=f"r_ng_{i}")
                
                base_amt = row['qty'] * row['rate']
                row['amt'] = base_amt
                row['tax_type'] = "Non-GST"
                row['tax_pct'] = 0.0
                c4.markdown(f"**Amt:** Rs. {base_amt:.2f}")
                subtotal_amt += base_amt

        st.markdown("---")
        disc_type = st.radio("Discount Type", ["None", "Percentage (%)", "Flat Amount (Rs.)"], horizontal=True)
        discount_val = st.number_input("Discount Value", min_value=0.0, value=0.0)

        effective_tax = total_tax_amt if is_tax_invoice else 0.0
        calc_subtotal = subtotal_amt + effective_tax
        discount_amount = (calc_subtotal * (discount_val / 100.0)) if disc_type == "Percentage (%)" else discount_val if disc_type == "Flat Amount (Rs.)" else 0.0
        final_total_amt = max(0.0, calc_subtotal - discount_amount)

        total_paid = st.number_input("Total Amount Paid (Rs.)", min_value=0.0, value=0.0)

        if st.button("✨ Finalize & Generate Exact A4 Invoice"):
            target_party = selected_party if selected_party != "+ Add New Party" else list(user_data["parties"].keys())[-1]
            p_info = user_data["parties"].get(target_party, {"address": "New Delhi", "gstin": "07AAAAA0000A1Z5"})
            
            client_gstin = p_info.get("gstin", "")
            company_gstin = user_data["profile"].get("gstin", "")
            
            tax_breakdown_html = ""
            if is_tax_invoice:
                if client_gstin.startswith("07") or (company_gstin and client_gstin[:2] == company_gstin[:2]):
                    cgst_amt = total_tax_amt / 2.0
                    sgst_amt = total_tax_amt / 2.0
                    tax_breakdown_html = f"""
                    <tr><td>CGST:</td><td style='text-align:right;'>Rs. {cgst_amt:.2f}</td></tr>
                    <tr><td>SGST:</td><td style='text-align:right;'>Rs. {sgst_amt:.2f}</td></tr>
                    """
                else:
                    igst_amt = total_tax_amt
                    tax_breakdown_html = f"""
                    <tr><td>IGST:</td><td style='text-align:right;'>Rs. {igst_amt:.2f}</td></tr>
                    """

            balance = final_total_amt - total_paid

            user_data["bills_created"] = user_data.get("bills_created", 0) + 1
            user_data["history"].append({
                "invoice_no": inv_no, "client": target_party, "total": final_total_amt,
                "paid": total_paid, "balance": balance, "date": inv_date,
                "parsed_items": list(st.session_state.inv_rows), "is_tax_invoice": is_tax_invoice,
                "timestamp": datetime.now().isoformat()
            })
            save_saas_data(saas_db)

            sel_theme = user_data["profile"].get("format", FORMAT_OPTIONS[0])
            if "Emerald Green" in sel_theme: p_col, wave_gradient = "#065f46", "linear-gradient(135deg, #059669 0%, #10b981 100%)"
            elif "Sunset Orange" in sel_theme: p_col, wave_gradient = "#c2410c", "linear-gradient(135deg, #ea580c 0%, #fb923c 100%)"
            elif "Royal Purple" in sel_theme: p_col, wave_gradient = "#581c87", "linear-gradient(135deg, #7e22ce 0%, #a855f7 100%)"
            elif "Minimalist Clean" in sel_theme: p_col, wave_gradient = "#334155", "linear-gradient(135deg, #475569 0%, #64748b 100%)"
            elif "Classic Blue" in sel_theme: p_col, wave_gradient = "#1e3a8a", "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)"
            else: p_col, wave_gradient = "#0f172a", "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)"

            init = get_initials(user_data['profile']['name'])
            logo_html = f"<div style='width:50px;height:50px;background:{p_col};color:#fff;display:flex;align-items:center;justify-content:center;font-weight:bold;border-radius:8px;'>{init}</div>"
            custom_logo_url = user_data["profile"].get("custom_logo", "")
            if custom_logo_url.strip(): logo_html = f"<img src='{custom_logo_url}' style='max-height:50px;max-width:50px;object-fit:contain;'>"

            wm_enabled = user_data["profile"].get("watermark_enabled", True)
            wm_type = user_data["profile"].get("watermark_type", "Company Name")
            wm_text = user_data["profile"]["name"] if wm_type == "Company Name" else init
            wm_html = f'<div style="position:absolute; top:40%; left:20%; transform:rotate(-30deg); font-size:90px; font-weight:bold; color:rgba(0,0,0,0.04); z-index:0; pointer-events:none; white-space:nowrap;">{wm_text}</div>' if wm_enabled else ""

            comp_bank_name = user_data["profile"].get("bank_name", "State Bank of India")
            comp_acc_no = user_data["profile"].get("acc_no", "1234567890")
            comp_ifsc = user_data["profile"].get("ifsc", "SBIN0016324")
            comp_branch = user_data["profile"].get("branch", "Nashik Ashok Nagar")
            comp_terms = user_data["profile"].get("terms", "Standard terms apply.")
            
            invoice_title_text = "TAX INVOICE" if is_tax_invoice else "BILL OF SUPPLY"
            table_headers = "<th>Description</th><th>Qty</th><th>Rate</th>" + ("<th>Tax Type</th>" if is_tax_invoice else "") + "<th style='text-align:right;'>Amount</th>"
            table_rows_new = "".join([f"<tr><td>{r['desc']}</td><td>{r['qty']}</td><td>{r['rate']:.2f}</td>" + (f"<td>{r['tax_type']} ({r['tax_pct']}%)</td>" if is_tax_invoice else "") + f"<td style='text-align:right;'>{r['amt']:.2f}</td></tr>" for r in st.session_state.inv_rows])

            html_content = f"""
            <!DOCTYPE html><html><head><meta charset="utf-8"><style>
                * {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
                body {{ font-family: Helvetica; background: #e2e8f0; padding: 20px; }}
                .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 20mm; border: 1px solid #cbd5e1; position: relative; overflow:hidden; }}
                .wave-header {{ background: {wave_gradient} !important; color: #fff !important; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom-left-radius: 30px; border-bottom-right-radius: 30px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                th, td {{ border: 1px solid #cbd5e1; padding: 8px; font-size: 13px; }}
                th {{ background: {p_col}; color: white; text-align: left; }}
                @media print {{ body {{ background: none; padding: 0; }} .no-print {{ display: none !important; }} }}
            </style></head><body>
            <div class="no-print" style="text-align: center; margin-bottom: 20px;">
                <button onclick="window.print()" style="background:#059669;color:white;padding:12px 25px;font-weight:bold;border:none;border-radius:8px;cursor:pointer;">🖨️ Print / Save Exact Color PDF</button>
                <a href="https://api.whatsapp.com/send?text=Hello%2C%20Invoice%20No%3A%20{inv_no}%20Total%3A%20Rs.%20{final_total_amt:.2f}" target="_blank" style="background:#25d366;color:white;padding:12px 25px;font-weight:bold;text-decoration:none;border-radius:8px;display:inline-block;margin-left:10px;">📱 Send via WhatsApp</a>
            </div>
            <div class="a4-page">
                {wm_html}
                <div class="wave-header">
                    <div style="display: flex; gap: 15px; align-items:center;">{logo_html}<div><h2>{user_data['profile']['name']}</h2><p>{user_data['profile']['address']}<br>Contact: {user_data['profile']['contact']}<br>GSTIN: {user_data['profile']['gstin']}</p></div></div>
                    <div style="text-align:right;"><h2>{invoice_title_text}</h2><p>{inv_no}</p></div>
                </div>
                <table style="width:100%; border-collapse:collapse; margin-bottom:20px;"><tr>
                <td style="padding:10px; border:1px solid #cbd5e1;"><strong>Service Provider:</strong><br>{user_data['profile']['name']}<br>Address: {user_data['profile']['address']}<br>Contact: {user_data['profile']['contact']}<br>GSTIN: {user_data['profile']['gstin']}</td>
                <td style="padding:10px; border:1px solid #cbd5e1;"><strong>Billed To:</strong><br>{target_party}<br>Address: {p_info.get('address')}<br>GSTIN: {p_info.get('gstin')}</td>
                </tr></table>
                <table><thead><tr>{table_headers}</tr></thead><tbody>{table_rows_new}</tbody></table>
                <br>
                <table style="width: 350px; margin-left: auto;">
                    <tr><td>Subtotal:</td><td style='text-align:right;'>Rs. {subtotal_amt:.2f}</td></tr>
                    {tax_breakdown_html}
                    <tr><td>Discount Applied:</td><td style='text-align:right;'>- Rs. {discount_amount:.2f}</td></tr>
                    <tr style="font-weight:bold; background:#f1f5f9;"><td>Final Total Amount:</td><td style='text-align:right;'>Rs. {final_total_amt:.2f}</td></tr>
                    <tr><td>Total Paid:</td><td style='text-align:right;'>Rs. {total_paid:.2f}</td></tr>
                    <tr style="font-weight:bold; background:#e2e8f0;"><td>Balance Due:</td><td style='text-align:right;'>Rs. {balance:.2f}</td></tr>
                </table>
                <br>
                <table style="width:100%; border-collapse:collapse; margin-top:20px; font-size:11px;">
                    <tr>
                        <td style="width:50%; border:1px solid #cbd5e1; padding:10px; vertical-align:top;">
                            <strong>Bank Details:</strong><br>
                            Bank Name: {comp_bank_name}<br>
                            A/C No: {comp_acc_no}<br>
                            IFSC Code: {comp_ifsc}<br>
                            Branch: {comp_branch}
                        </td>
                        <td style="width:50%; border:1px solid #cbd5e1; padding:10px; vertical-align:top;">
                            <strong>Terms & Conditions:</strong><br>
                            {comp_terms}
                        </td>
                    </tr>
                </table>
            </div></body></html>
            """
            st.success("Invoice Generated Successfully with GST Toggle & Bank Details!")
            st.components.v1.html(html_content, height=850, scrolling=True)

