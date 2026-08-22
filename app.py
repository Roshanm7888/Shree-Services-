import streamlit as st
from datetime import datetime, timedelta
import json
import os
import time
import pandas as pd
import random

st.set_page_config(page_title="Professional Invoice Portal - SaaS", page_icon="📄", layout="wide")

# --- GLOBAL SETTINGS ---
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

# --- FIXED CSS FOR COMPACT LOGIN, DESIGNER WAVE THEMES & ANDROID/DESKTOP ---
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

# --- SMART INTERACTIVE AI ASSISTANT FUNCTION ---
def ask_gemini_assistant(query):
    q_lower = query.lower()
    if "invoice" in q_lower or "bill" in q_lower or "bana" in q_lower or "create" in q_lower:
        return """📝 **Invoice Create Karne ka Step-by-Step Process:**
1. Sidebar navigation menu se **'Create Invoice'** tab par click karein.
2. **Section 1 (Client / Party Details):** Apne client ko select karein ya '+ Add New Party' par click karke naye client ki details (Trade Name, Address, GSTIN) save karein.
3. **Section 2 (Invoice Meta Details):** Invoice Number aur Date check karein.
4. **Section 3 (Items & Grid Entry):** Apne business nature ke mutabik items ki description, HSN code, quantity, rate aur tax % enter karein.
5. Niche diye gaye **'✨ Finalize & Generate Exact A4 Invoice'** button par click karein."""
    elif "history" in q_lower or "client" in q_lower or "excel" in q_lower or "ledger" in q_lower:
        return """📊 **Client Ledger & Professional Excel/PDF Export:**
Aap kisi bhi client ki history ya ledger dekhne ke liye sidebar se **'📊 Party-wise History & Edit/Delete (24 Days)'** tab par click karein. Wahan se aap professional formatted Excel sheet ya Ledger PDF download kar sakte hain!"""
    else:
        return f"💡 **AI Assistant Guide:** Aapne pucha: '{query}'. Invoice banane ke liye 'Create Invoice' tab par jayein aur Ledger ke liye 'Party-wise History' tab check karein."

SESSION_TIMEOUT_SECONDS = 900
if st.session_state.logged_in_user and st.session_state.login_time:
    elapsed_time = (datetime.now() - st.session_state.login_time).total_seconds()
    if elapsed_time > SESSION_TIMEOUT_SECONDS:
        st.session_state.logged_in_user = None
        st.session_state.login_time = None
        st.warning("⏱️ Session expired due to inactivity. Please login again.")
        st.rerun()

# --- AUTHENTICATION & LANDING PAGE ---
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
            login_id = st.text_input("Email ID / Mobile Number", key="login_id", value="", placeholder="Enter email or mobile")
            login_pass = st.text_input("Password", type="password", key="login_pass", value="", placeholder="Enter password")
            
            ans1 = st.session_state.c1
            ans2 = st.session_state.c2
            captcha_input = st.text_input(f"Security Captcha: Solve {ans1} + {ans2} = ?", key="login_captcha", placeholder="Enter sum")
            
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
                    st.error("❌ Invalid Security Captcha Answer! Please try again.")
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
                    st.error("❌ Invalid User ID or Password! Please check your credentials.")
                    
        with auth_tab2:
            st.subheader("Create Company Account")
            reg_id = st.text_input("Enter User ID (Email/Mobile)", key="reg_id", value="", placeholder="e.g. name@company.com")
            reg_pass1 = st.text_input("Create Password", type="password", key="reg_pass1", value="", placeholder="Create password")
            reg_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2", value="", placeholder="Confirm password")
            
            comp_name = st.text_input("Company / Trade Name", key="comp_name", value="", placeholder="e.g. My Business")
            comp_legal = st.text_input("Authorized Person Name", key="comp_legal", value="", placeholder="e.g. John Doe")
            comp_address = st.text_input("Complete Address", key="comp_address", value="", placeholder="Enter full address")
            comp_contact = st.text_input("Contact Number", key="comp_contact", value="", placeholder="10-digit mobile")
            comp_gstin = st.text_input("Company GSTIN (Optional)", key="comp_gstin", value="", placeholder="07AAAAA0000A1Z5")
            
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
                        "profile": {
                            "name": comp_name, "legal": comp_legal, "address": comp_address,
                            "contact": comp_contact, "gstin": comp_gstin, "nature": comp_nature,
                            "format": "Corporate Curve Wave (New Professional)", "border_style": "Solid Line",
                            "gst_enabled": True, "watermark_enabled": True, "watermark_type": "Company Name"
                        },
                        "history": [], "parties": {"Sample Party": {"legal": "Client Name", "address": "Delhi", "gstin": "07AAAAA0000A1Z5"}},
                        "subscription": "Trial", "bills_created": 0
                    }
                    save_saas_data(saas_db)
                    st.success("Account Created Successfully! Free Trial Activated. Go to Login tab.")

    st.markdown("<br><hr><h2 style='text-align: center; color: #1e3a8a;'>🌟 Why Businesses Choose Our Portal</h2><br>", unsafe_allow_html=True)

else:
    # --- LOGGED-IN USER PORTAL ---
    current_user = st.session_state.logged_in_user
    user_data = saas_db[current_user]
    nature_options = ["Goods / Manufacturing / Trading", "Services", "Transport Company", "Other Business"]
    
    current_nature = user_data["profile"].get("nature", "Goods / Manufacturing / Trading")
    if current_nature not in nature_options: current_nature = nature_options[0]
    
    if "history" not in st.session_state: st.session_state.history = user_data["history"]
    if "saved_parties" not in st.session_state: st.session_state.saved_parties = user_data["parties"]
    if "subscription" not in user_data: user_data["subscription"] = "Trial"
    if "bills_created" not in user_data: user_data["bills_created"] = len(user_data["history"])

    current_time = datetime.now()
    cleaned_history = [
        h for h in st.session_state.history 
        if current_time - datetime.fromisoformat(h.get('timestamp', current_time.isoformat())) <= timedelta(days=24)
    ]
    if len(cleaned_history) != len(st.session_state.history):
        st.session_state.history = cleaned_history
        user_data["history"] = st.session_state.history
        save_saas_data(saas_db)

    if current_user == "roshan@shreeservices.com":
        st.sidebar.markdown("🛠️ **Admin Subscription Manager**")
        for u_id, u_info in saas_db.items():
            if u_id != "roshan@shreeservices.com":
                current_sub = u_info.get("subscription", "Trial")
                new_sub = st.sidebar.selectbox(f"Plan for `{u_id}`", ["Trial", "Paid"], index=["Trial", "Paid"].index(current_sub if current_sub in ["Trial", "Paid"] else 0), key=f"sub_{u_id}")
                if new_sub != current_sub:
                    u_info["subscription"] = new_sub
                    save_saas_data(saas_db)
                    st.sidebar.success(f"Updated {u_id} to {new_sub}!")
        st.sidebar.markdown("---")

    st.sidebar.markdown(f"👤 **User:** `{current_user}`")
    st.sidebar.markdown(f"🏢 **Company:** `{user_data['profile']['name']}`")
    st.sidebar.markdown(f"🌟 **Plan:** `{user_data['subscription']}`")
    
    st.sidebar.markdown("---")
    menu_options_list = [
        "Create Invoice", 
        "🤖 AI Business Assistant", 
        "📊 Party-wise History & Edit/Delete (24 Days)", 
        "⚙️ Company Profile & Format Settings", 
        "🚪 Logout"
    ]
    menu_option = st.sidebar.radio("Navigation Menu", menu_options_list)

    if menu_option == "🚪 Logout":
        st.session_state.logged_in_user = None
        st.session_state.login_time = None
        st.rerun()

    elif menu_option == "🤖 AI Business Assistant":
        st.markdown("<div class='main-title'><h1>🤖 AI Business & Tax Assistant</h1><p>Ask anything about taxes, invoice settings, or client history!</p></div>", unsafe_allow_html=True)
        user_query = st.text_area("Type your question here:")
        if st.button("Ask AI Expert"):
            if user_query.strip():
                with st.spinner("Thinking..."):
                    time.sleep(0.3)
                    ai_answer = ask_gemini_assistant(user_query)
                    st.markdown("### 💡 AI Expert Response:")
                    st.info(ai_answer)
            else: st.warning("Please enter a valid question.")

    elif menu_option == "📊 Party-wise History & Edit/Delete (24 Days)":
        st.markdown("<div class='main-title'><h1>Party-wise History, Professional Excel & Ledger PDF</h1></div>", unsafe_allow_html=True)
        
        if not st.session_state.history: 
            st.info("No invoice history available for the last 24 days.")
        else:
            all_parties = list(set([h['client'] for h in st.session_state.history]))
            sel_party = st.selectbox("Select Party for History, Excel & Ledger", all_parties)
            
            party_bills = [h for h in st.session_state.history if h['client'] == sel_party]
            
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                if party_bills:
                    excel_html = f"""
                    <h3>Statement of Accounts / Ledger: {sel_party}</h3>
                    <table border="1">
                        <tr style="background:#1e3a8a; color:#ffffff;">
                            <th>Invoice No</th><th>Date</th><th>Client Name</th><th>Total (Rs.)</th><th>Paid (Rs.)</th><th>Balance (Rs.)</th>
                        </tr>
                    """
                    tot_t, tot_p, tot_b = 0, 0, 0
                    for b in party_bills:
                        tot_t += b['total']
                        tot_p += b['paid']
                        tot_b += b['balance']
                        excel_html += f"<tr><td>{b['invoice_no']}</td><td>{b['date']}</td><td>{b['client']}</td><td>{b['total']:.2f}</td><td>{b['paid']:.2f}</td><td>{b['balance']:.2f}</td></tr>"
                    excel_html += f"<tr style='font-weight:bold; background:#f1f5f9;'><td colspan='3'>Total</td><td>{tot_t:.2f}</td><td>{tot_p:.2f}</td><td>{tot_b:.2f}</td></tr></table>"
                    
                    st.download_button(
                        label=f"📥 Download Formatted Excel Ledger ({sel_party})",
                        data=excel_html,
                        file_name=f"{sel_party}_Ledger_Statement.xls",
                        mime="application/vnd.ms-excel"
                    )

            with col_ex2:
                if st.button(f"🖨️ Print / Save Ledger PDF ({sel_party})"):
                    ledger_rows_html = ""
                    for b in party_bills:
                        ledger_rows_html += f"<tr><td>{b['invoice_no']}</td><td>{b['date']}</td><td>Rs. {b['total']:.2f}</td><td>Rs. {b['paid']:.2f}</td><td>Rs. {b['balance']:.2f}</td></tr>"
                    
                    ledger_html_doc = f"""
                    <!DOCTYPE html><html><head><meta charset="utf-8"><style>
                        body {{ font-family: Helvetica, Arial; color: #1e293b; padding: 20px; }}
                        .ledger-box {{ width: 210mm; margin: auto; background: #fff; padding: 20mm; border: 1px solid #cbd5e1; }}
                        h2 {{ color: #1e3a8a; margin-bottom: 5px; }}
                        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                        th {{ background: #1e3a8a; color: white; padding: 10px; font-size: 13px; text-align: left; border: 1px solid #1e3a8a; }}
                        td {{ border: 1px solid #cbd5e1; padding: 10px; font-size: 13px; }}
                        .right {{ text-align: right; }}
                        @media print {{ body {{ background: none; padding: 0; }} .no-print {{ display: none !important; }} }}
                    </style></head><body>
                    <div class="no-print" style="text-align: center; margin-bottom: 20px;"><button onclick="window.print()" style="background:#059669;color:white;padding:12px 25px;font-weight:bold;border:none;border-radius:8px;cursor:pointer;">🖨️ Print / Save Ledger PDF</button></div>
                    <div class="ledger-box">
                        <h2>{user_data['profile']['name']}</h2>
                        <p style="font-size:12px; color:#64748b;">Statement of Account / Ledger for: <strong>{sel_party}</strong><br>Generated on: {datetime.now().strftime('%B %d, %Y')}</p>
                        <hr style="border: 1px solid #cbd5e1; margin: 15px 0;">
                        <table>
                            <thead><tr><th>Invoice No</th><th>Date</th><th>Total Amount</th><th>Paid Amount</th><th>Balance Due</th></tr></thead>
                            <tbody>{ledger_rows_html}</tbody>
                        </table>
                        <br>
                        <div style="text-align: right; font-size: 14px; font-weight: bold;">Total Outstanding Balance: Rs. {sum([b['balance'] for b in party_bills]):.2f}</div>
                    </div></body></html>
                    """
                    st.components.v1.html(ledger_html_doc, height=700, scrolling=True)

            st.markdown("---")
            for bill in party_bills:
                with st.expander(f"Invoice No: {bill['invoice_no']} | Client: {bill['client']} | Total: Rs. {bill['total']}"):
                    edit_paid = st.number_input("Edit Paid Amount (Rs.)", value=float(bill.get('paid', 0.0)), key=f"ep_{bill['invoice_no']}")
                    col_s, col_d = st.columns(2)
                    with col_s:
                        if st.button("💾 Save Changes", key=f"sv_{bill['invoice_no']}"):
                            bill['paid'] = edit_paid
                            bill['balance'] = bill['total'] - edit_paid
                            user_data["history"] = st.session_state.history
                            save_saas_data(saas_db)
                            st.success("Invoice Updated Successfully!")
                            st.rerun()
                    with col_d:
                        if st.button("❌ Delete Invoice", key=f"dl_{bill['invoice_no']}"):
                            st.session_state.history = [h for h in st.session_state.history if h['invoice_no'] != bill['invoice_no']]
                            user_data["history"] = st.session_state.history
                            save_saas_data(saas_db)
                            st.warning("Invoice Deleted!")
                            st.rerun()

    elif menu_option == "⚙️ Company Profile & Format Settings":
        st.markdown("<div class='main-title'><h1>Settings & Format Customizer</h1></div>", unsafe_allow_html=True)
        prof = user_data["profile"]
        border_options = ["Solid Line", "Dotted Border (Stylish)", "Double Line (Accounting)", "Dashed Border (Modern)"]

        up_name = st.text_input("Company / Trade Name", value=prof.get("name", ""))
        up_legal = st.text_input("Authorized Person Name", value=prof.get("legal", ""))
        up_address = st.text_input("Company Complete Address", value=prof.get("address", ""))
        up_contact = st.text_input("Contact Number", value=prof.get("contact", ""))
        up_gstin = st.text_input("Company GSTIN", value=prof.get("gstin", ""))
        
        nat_idx = nature_options.index(current_nature) if current_nature in nature_options else 0
        up_nature = st.selectbox("Fixed Business Nature (Format)", nature_options, index=nat_idx)
        
        fmt_val = prof.get("format", FORMAT_OPTIONS[0])
        fmt_idx = FORMAT_OPTIONS.index(fmt_val) if fmt_val in FORMAT_OPTIONS else 0
        up_format = st.selectbox("Select Invoice Designer Theme", FORMAT_OPTIONS, index=fmt_idx)

        b_val = prof.get("border_style", "Solid Line")
        b_idx = border_options.index(b_val) if b_val in border_options else 0
        up_border = st.selectbox("Select Invoice Border Style", border_options, index=b_idx)

        up_custom_logo = st.text_input("Logo Image URL (Optional)", value=prof.get("custom_logo", ""))
        up_watermark_enabled = st.checkbox("Enable Background Watermark on Invoice", value=prof.get("watermark_enabled", True))
        
        wm_type_val = prof.get("watermark_type", "Company Name")
        up_watermark_type = st.radio("Watermark Content Type", ["Company Name", "Logo Initials"], index=0 if wm_type_val == "Company Name" else 1)
        up_gst_enabled = st.checkbox("Enable GST / Tax Calculation on Invoices", value=prof.get("gst_enabled", True))
        
        if st.button("💾 Save All Settings Permanently"):
            user_data["profile"] = {
                "name": up_name, "legal": up_legal, "address": up_address, "contact": up_contact,
                "gstin": up_gstin, "nature": up_nature, "format": up_format, "border_style": up_border,
                "custom_logo": up_custom_logo, "watermark_enabled": up_watermark_enabled,
                "watermark_type": up_watermark_type, "gst_enabled": up_gst_enabled
            }
            save_saas_data(saas_db)
            st.success("Settings saved successfully!")
            st.rerun()

        st.markdown("---")
        st.markdown("### 👁️ Instant Full A4 Size Live Preview")
        if "Emerald Green" in up_format: p_col, wave_gradient = "#065f46", "linear-gradient(135deg, #059669 0%, #10b981 100%)"
        elif "Sunset Orange" in up_format: p_col, wave_gradient = "#c2410c", "linear-gradient(135deg, #ea580c 0%, #fb923c 100%)"
        elif "Royal Purple" in up_format: p_col, wave_gradient = "#581c87", "linear-gradient(135deg, #7e22ce 0%, #a855f7 100%)"
        elif "Minimalist Clean" in up_format: p_col, wave_gradient = "#334155", "linear-gradient(135deg, #475569 0%, #64748b 100%)"
        elif "Classic Blue" in up_format: p_col, wave_gradient = "#1e3a8a", "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)"
        else: p_col, wave_gradient = "#0f172a", "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)"

        b_css = "2px dotted #1e293b" if "Dotted" in up_border else "2px dashed #1e293b" if "Dashed" in up_border else "4px double #1e293b" if "Double" in up_border else "1px solid #cbd5e1"
        init = get_initials(up_name)
        logo_html = f"<div style='width: 50px; height: 50px; background: {p_col}; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: bold; border-radius: 8px;'>{init}</div>"
        if up_custom_logo.strip(): logo_html = f"<img src='{up_custom_logo}' style='max-height: 50px; max-width: 50px; object-fit: contain;'>"
        wm_text = up_name if wm_watermark_type == "Company Name" else init
        wm_html = f'<div style="position: absolute; top: 40%; left: 20%; transform: rotate(-30deg); font-size: 90px; font-weight: bold; color: rgba(0, 0, 0, 0.04); z-index: 0; pointer-events: none; white-space: nowrap;">{wm_text}</div>' if up_watermark_enabled else ""

        full_a4_preview_html = f"""
        <!DOCTYPE html><html><head><meta charset="utf-8"><style>
            body {{ font-family: Helvetica, Arial; color: #1e293b; background: #e2e8f0; margin: 0; padding: 20px; }}
            .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 15mm 20mm; box-sizing: border-box; border: {b_css}; position: relative; overflow: hidden; }}
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

    else:
        # --- CREATE INVOICE TAB ---
        st.markdown(f"<div class='main-title'><h1>{user_data['profile']['name']}</h1><p>Invoice Mode: <b>{current_nature}</b></p></div>", unsafe_allow_html=True)

        if user_data["subscription"] == "Trial" and user_data.get("bills_created", 0) >= 1:
            st.error("🚨 **Free Trial Limit Reached!** Subscribe to Pro Plan (Rs. 5/- only) via UPI: **`roshan@shreeservices.upi`**")
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

        next_inv_num = len(st.session_state.history) + 1
        current_inv_no = f"TAX/2026-27/{next_inv_num:03d}"

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
            st.session_state.inv_rows.append({"desc": "", "hsn": "", "unit": "NOS", "qty": 1.0, "rate": 0.0, "tax_type": "Taxable", "tax_pct": 18.0, "amt": 0.0, "lr_no": "", "vehicle": "", "route": ""})

        subtotal_amt, total_tax_amt = 0.0, 0.0
        for i, row in enumerate(st.session_state.inv_rows):
            st.markdown(f"**Row {i+1}**")
            if current_nature == "Goods / Manufacturing / Trading":
                c1, c2, c3, c4, c5, c6, c7 = st.columns([3, 2, 1.5, 1.5, 2, 2, 2])
                row['desc'] = c1.text_input("Item Name", value=row['desc'], key=f"d_{i}")
                row['hsn'] = c2.text_input("HSN", value=row['hsn'], key=f"h_{i}")
                row['unit'] = c3.selectbox("Unit", ["NOS", "Box", "Pcs", "Kgs"], key=f"u_{i}")
                row['qty'] = c4.number_input("Qty", value=row['qty'], key=f"q_{i}")
                row['rate'] = c5.number_input("Rate", value=row['rate'], key=f"r_{i}")
                row['tax_type'] = c6.selectbox("Tax Type", ["Taxable", "Nil Rated"], key=f"tt_{i}")
                row['tax_pct'] = c7.selectbox("Tax %", [0.0, 5.0, 12.0, 18.0, 28.0], index=3, key=f"tp_{i}")
                base_amt = row['qty'] * row['rate']
                row['amt'] = base_amt
                subtotal_amt += base_amt
                if row['tax_type'] == "Taxable": total_tax_amt += base_amt * (row['tax_pct'] / 100.0)
            elif current_nature == "Services":
                c1, c2, c3, c4 = st.columns([4, 2, 2, 2])
                row['desc'] = c1.text_input("Service Description", value=row['desc'], key=f"sd_{i}")
                row['tax_type'] = c2.selectbox("Tax Type", ["Taxable", "Nil Rated"], key=f"stt_{i}")
                row['tax_pct'] = c3.selectbox("Tax %", [0.0, 5.0, 12.0, 18.0, 28.0], index=3, key=f"stp_{i}")
                row['amt'] = c4.number_input("Amount", value=row['amt'], key=f"sa_{i}")
                subtotal_amt += row['amt']
                if row['tax_type'] == "Taxable": total_tax_amt += row['amt'] * (row['tax_pct'] / 100.0)
            elif current_nature == "Transport Company":
                c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 2])
                row['lr_no'] = c1.text_input("LR No", value=row['lr_no'], key=f"lr_{i}")
                row['vehicle'] = c2.text_input("Vehicle No", value=row['vehicle'], key=f"vh_{i}")
                row['route'] = c3.text_input("From -> To", value=row['route'], key=f"rt_{i}")
                row['desc'] = c4.text_input("Goods Desc", value=row['desc'], key=f"td_{i}")
                row['amt'] = c5.number_input("Freight Amt", value=row['amt'], key=f"ta_{i}")
                subtotal_amt += row['amt']
            else:
                c1, c2, c3 = st.columns([4, 2, 2])
                row['desc'] = c1.text_input("Description", value=row['desc'], key=f"od_{i}")
                row['tax_pct'] = c2.selectbox("Tax %", [0.0, 5.0, 12.0, 18.0, 28.0], index=3, key=f"otp_{i}")
                row['amt'] = c3.number_input("Amount", value=row['amt'], key=f"oa_{i}")
                subtotal_amt += row['amt']
                total_tax_amt += row['amt'] * (row['tax_pct'] / 100.0)

        total_paid = st.number_input("Total Amount Paid (Rs.)", min_value=0.0, value=0.0)

        if st.button("✨ Finalize & Generate Exact A4 Invoice"):
            target_party = selected_party if selected_party != "+ Add New Party" else list(user_data["parties"].keys())[-1]
            p_info = user_data["parties"].get(target_party, {"legal": "-", "address": "New Delhi", "gstin": "07AAAAA0000A1Z5"})
            
            client_gstin_val = p_info.get("gstin", "")
            if client_gstin_val.startswith("07"):
                cgst_amt, sgst_amt = total_tax_amt / 2.0, total_tax_amt / 2.0
                tax_rows_html = f"<tr><td>CGST:</td><td class='right'>Rs. {cgst_amt:.2f}</td></tr><tr><td>SGST:</td><td class='right'>Rs. {sgst_amt:.2f}</td></tr>"
            else:
                igst_amt = total_tax_amt
                tax_rows_html = f"<tr><td>IGST:</td><td class='right'>Rs. {igst_amt:.2f}</td></tr>"

            total_amt = subtotal_amt + total_tax_amt
            balance = total_amt - total_paid

            user_data["bills_created"] = user_data.get("bills_created", 0) + 1
            st.session_state.history.append({
                "invoice_no": inv_no, "client": target_party, "total": total_amt,
                "paid": total_paid, "balance": balance, "date": inv_date,
                "parsed_items": st.session_state.inv_rows, "timestamp": datetime.now().isoformat()
            })
            user_data["history"] = st.session_state.history
            save_saas_data(saas_db)

            sel_theme = user_data["profile"].get("format", FORMAT_OPTIONS[0])
            p_col, wave_gradient = ("#065f46", "linear-gradient(135deg, #059669 0%, #10b981 100%)") if "Emerald Green" in sel_theme else ("#c2410c", "linear-gradient(135deg, #ea580c 0%, #fb923c 100%)") if "Sunset Orange" in sel_theme else ("#581c87", "linear-gradient(135deg, #7e22ce 0%, #a855f7 100%)") if "Royal Purple" in sel_theme else ("#334155", "linear-gradient(135deg, #475569 0%, #64748b 100%)") if "Minimalist Clean" in sel_theme else ("#1e3a8a", "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)") if "Classic Blue" in sel_theme else ("#0f172a", "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)")
            b_css = "2px dotted #1e293b" if "Dotted" in user_data["profile"].get("border_style", "Solid") else "1px solid #cbd5e1"
            init = get_initials(user_data['profile']['name'])
            l_html = f"<div style='width:50px;height:50px;background:{p_col};color:#fff;display:flex;align-items:center;justify-content:center;font-weight:bold;border-radius:8px;'>{init}</div>"
            
            table_headers = "<th>S.No.</th><th>Item Description</th><th>HSN</th><th>Unit</th><th>Qty</th><th>Rate</th><th>Tax Type</th><th class='right'>Amount (Rs.)</th>"
            table_rows = "".join([f"<tr><td class='right'>{i}</td><td>{r['desc']}</td><td>{r['hsn']}</td><td>{r['unit']}</td><td>{r['qty']}</td><td>{r['rate']:.2f}</td><td>{r['tax_type']} ({r['tax_pct']}%)</td><td class='right'>{r['amt']:.2f}</td></tr>" for i, r in enumerate(st.session_state.inv_rows, 1)])

            html_content = f"""
            <!DOCTYPE html><html><head><meta charset="utf-8"><style>
                * {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; color-adjust: exact !important; }}
                body {{ font-family: Helvetica, Arial; color: #1e293b; background: #e2e8f0; padding: 20px; }}
                .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 15mm 20mm; box-sizing: border-box; border: {b_css}; position: relative; }}
                .wave-header {{ background: {wave_gradient} !important; color: #fff !important; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom-left-radius: 30px; border-bottom-right-radius: 30px; }}
                .company-title {{ font-size: 24px; font-weight: bold; color: #ffffff !important; }}
                .invoice-title {{ font-size: 26px; font-weight: bold; text-transform: uppercase; color: #ffffff !important; text-align: right; }}
                .billing-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; border: 1px solid #cbd5e1; background: #f8fafc; }}
                .billing-table td {{ padding: 12px; vertical-align: top; width: 50%; font-size: 13px; border: 1px solid #cbd5e1; }}
                .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                .items-table th {{ background-color: {p_col} !important; color: #fff !important; padding: 10px; font-size: 12px; text-align: left; border: 1px solid {p_col}; }}
                .items-table td {{ border: 1px solid #cbd5e1; padding: 10px; font-size: 12px; }}
                .right {{ text-align: right; }}
                .totals {{ width: 340px; margin-left: auto; font-size: 13px; border-collapse: collapse; }}
                .totals td {{ padding: 8px; border: 1px solid #cbd5e1; }}
                .grand-total {{ font-weight: bold; background: #eff6ff !important; color: {p_col}; }}
                @media print {{ body {{ background: none; padding: 0; }} .no-print {{ display: none !important; }} }}
            </style></head><body>
            <div class="no-print" style="text-align: center; margin-bottom: 20px; display: flex; gap: 10px; justify-content: center;">
                <button onclick="window.print()" style="background:#059669;color:white;padding:12px 25px;font-weight:bold;border:none;border-radius:8px;cursor:pointer;">🖨️ Print / Save Exact Color PDF</button>
                <a href="https://api.whatsapp.com/send?text=Hello%2C%20here%20is%20your%20Tax%20Invoice%20No%3A%20{inv_no}%20Total%3A%20Rs.%20{total_amt:.2f}.%20Thank%20you!" target="_blank" style="background:#25d366;color:white;padding:12px 25px;font-weight:bold;text-decoration:none;border-radius:8px;display:inline-block;">📱 Send via WhatsApp</a>
            </div>
            <div class="a4-page">
                <div class="wave-header">
                    <div style="display: flex; gap: 15px; align-items:center;">{l_html}<div><div class="company-title">{user_data['profile']['name']}</div><div style="font-size: 12px; color: #e2e8f0;">{user_data['profile']['address']}<br>Contact: {user_data['profile']['contact']}<br>GSTIN: {user_data['profile']['gstin']}</div></div></div>
                    <div><div class="invoice-title">Tax Invoice</div><div style="font-size: 12px; color: #e2e8f0; text-align: right;">Invoice No: {inv_no}<br>Date: {inv_date}</div></div>
                </div>
                <table class="billing-table"><tr><td><strong>Service Provider:</strong><br>{user_data['profile']['name']}</td><td><strong>Billed To:</strong><br><strong>{target_party}</strong><br>Address: {p_info.get('address')}<br>GSTIN: {p_info.get('gstin')}</td></tr></table>
                <table class="items-table"><thead><tr>{table_headers}</tr></thead><tbody>{table_rows}</tbody></table>
                <table class="totals">
                    <tr><td>Subtotal:</td><td class="right">Rs. {subtotal_amt:.2f}</td></tr>
                    {tax_rows_html}
                    <tr class="grand-total"><td>Total Amount:</td><td class="right">Rs. {total_amt:.2f}</td></tr>
                    <tr><td>Total Paid:</td><td class="right">Rs. {total_paid:.2f}</td></tr>
                    <tr class="grand-total"><td>Balance Due:</td><td class="right">Rs. {balance:.2f}</td></tr>
                </table>
            </div></body></html>
            """
            st.success("✨ Professional Invoice Generated Successfully!")
            st.components.v1.html(html_content, height=850, scrolling=True)

