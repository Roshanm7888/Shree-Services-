import streamlit as st
from datetime import datetime, timedelta
import json
import os
import random

st.set_page_config(page_title="Professional Invoice Portal - SaaS", page_icon="📄", layout="centered")

# --- Colorful & Responsive Modern UI CSS ---
st.markdown("""
    <style>
    label, p, span, div {
        color: #1e293b !important;
    }
    input, textarea, select {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    .stApp {
        background-color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    @media (max-width: 600px) {
        .main-title { padding: 15px !important; }
        .main-title h1 { font-size: 20px !important; }
        div[data-testid="stForm"] { padding: 15px !important; }
    }
    .main-title {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .main-title h1 { margin: 0; font-size: 26px; font-weight: 700; color: #ffffff !important; }
    .main-title p { margin: 5px 0 0 0; font-size: 14px; opacity: 0.9; color: #ffffff !important; }
    div[data-testid="stForm"] {
        background: #ffffff;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    .section-box-1 {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 5px solid #3b82f6;
        padding: 12px 15px;
        border-radius: 8px;
        color: #1e3a8a;
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 15px;
    }
    .section-box-2 {
        background: linear-gradient(135deg, #fdf4ff 0%, #fae8ff 100%);
        border-left: 5px solid #d946ef;
        padding: 12px 15px;
        border-radius: 8px;
        color: #86198f;
        font-weight: 700;
        font-size: 16px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .section-box-3 {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 5px solid #22c55e;
        padding: 12px 15px;
        border-radius: 8px;
        color: #166534;
        font-weight: 700;
        font-size: 16px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .stFormSubmitButton button, .stButton button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 20px;
        width: 100%;
        border: none;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
        font-size: 16px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

USERS_FILE = "saas_users_data.json"

def load_saas_data():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

def save_saas_data(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "reg_step" not in st.session_state:
    st.session_state.reg_step = 1
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None
if "temp_reg_data" not in st.session_state:
    st.session_state.temp_reg_data = {}

saas_db = load_saas_data()

# --- Authentication & Registration Flow with OTP Verification ---
if not st.session_state.logged_in_user:
    st.markdown("""
        <div class="main-title">
            <h1>SaaS Invoice Management Portal</h1>
            <p>Secure Login & OTP Verified Registration System</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Admin Bypass with Default History for Testing
    if st.sidebar.button("⚡ Quick Admin Test Login"):
        master_id = "roshan@shreeservices.com"
        if master_id not in saas_db:
            saas_db[master_id] = {
                "password": "admin",
                "profile": {
                    "name": "Shree Services",
                    "legal": "Roshan Mishra",
                    "address": "Plot no 64 & 65, Block K-5, Mohan Garden, New Delhi - 110059",
                    "contact": "7888273972",
                    "gstin": "07SAMPLEGSTIN",
                    "nature": "Tax Consultancy & Accounting Services",
                    "format": "Classic Blue (Professional)",
                    "gst_enabled": True,
                    "tax_rate": 18.0
                },
                "history": [
                    {
                        "invoice_no": "TAX/2026-27/001",
                        "client": "RKMK Enterprises",
                        "total": 1400.0,
                        "paid": 1000.0,
                        "balance": 400.0,
                        "date": "July 15, 2026",
                        "services": "GST Filing | July | 700\nITR Filing | 2025-26 | 700",
                        "timestamp": datetime.now().isoformat()
                    }
                ],
                "parties": {
                    "RKMK Enterprises": {
                        "legal": "Rinky Acharya",
                        "address": "Flat No. 34, Ground Floor, Block P Extn, Mohan Garden, New Delhi - 110059",
                        "gstin": "07DEOPA0606H1ZU"
                    },
                    "Chandra Enterprises": {
                        "legal": "Manoj Kumar",
                        "address": "2nd Floor Front Side, N Block Extn, Plot No.1 Mohan Garden, New Delhi",
                        "gstin": "07AMSPK3043R1ZC"
                    }
                },
                "services": ["ITR", "GST", "GST REGISTRATION", "UDYAM", "SHOP ACT"],
                "stock_items": [
                    {"name": "GST Monthly Filing", "rate": 700.0},
                    {"name": "ITR Filing", "rate": 1000.0},
                    {"name": "Udyam Registration", "rate": 500.0}
                ]
            }
            save_saas_data(saas_db)
        st.session_state.logged_in_user = master_id
        st.rerun()

    auth_tab1, auth_tab2 = st.tabs(["🔐 Login", "📝 New User Registration (OTP Secured)"])
    
    with auth_tab1:
        st.subheader("Existing User Login")
        login_id = st.text_input("Email ID / Mobile Number", key="login_id", placeholder="e.g. user@gmail.com")
        login_pass = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
        
        if st.button("Login to Portal"):
            if login_id in saas_db and saas_db[login_id]["password"] == login_pass:
                st.session_state.logged_in_user = login_id
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid User ID or Password!")
                
    with auth_tab2:
        if st.session_state.reg_step == 1:
            st.subheader("Step 1: Enter Account & Company Details")
            reg_id = st.text_input("Enter Email ID / Mobile Number (User ID)", key="reg_id", placeholder="e.g. client@gmail.com")
            reg_pass1 = st.text_input("Create Password", type="password", key="reg_pass1", placeholder="Create secure password")
            reg_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2", placeholder="Re-enter password")
            
            st.markdown("---")
            st.markdown("#### 🏢 Company / Business Profile Setup")
            comp_name = st.text_input("Company / Trade Name", key="comp_name", placeholder="e.g. Acme Services")
            comp_legal = st.text_input("Authorized Person / Owner Name", key="comp_legal", placeholder="e.g. Amit Sharma")
            comp_address = st.text_input("Company Complete Address", key="comp_address", placeholder="e.g. Connaught Place, New Delhi")
            comp_contact = st.text_input("Contact Number", key="comp_contact", placeholder="e.g. +91 9876543210")
            comp_gstin = st.text_input("Company GSTIN (Optional)", key="comp_gstin", placeholder="e.g. 07XXXXX0000X1Z5")
            comp_nature = st.text_input("Nature of Business / Dealings", key="comp_nature", placeholder="e.g. Accounting & Billing")
            
            if st.button("Send Verification OTP"):
                if not reg_id or not reg_pass1:
                    st.warning("Please fill User ID and Password fields.")
                elif reg_pass1 != reg_pass2:
                    st.error("Passwords do not match! Please verify confirmation.")
                elif reg_id in saas_db:
                    st.error("User ID already registered! Please login.")
                elif not comp_name:
                    st.warning("Please enter Company Name.")
                else:
                    otp = str(random.randint(100000, 999999))
                    st.session_state.generated_otp = otp
                    st.session_state.temp_reg_data = {
                        "id": reg_id,
                        "password": reg_pass1,
                        "profile": {
                            "name": comp_name,
                            "legal": comp_legal,
                            "address": comp_address,
                            "contact": comp_contact,
                            "gstin": comp_gstin,
                            "nature": comp_nature,
                            "format": "Classic Blue (Professional)",
                            "gst_enabled": True,
                            "tax_rate": 18.0
                        }
                    }
                    st.session_state.reg_step = 2
                    st.success(f"OTP Sent Successfully! (Demo OTP for testing: {otp})")
                    st.rerun()
                    
        elif st.session_state.reg_step == 2:
            st.subheader("Step 2: Enter Verification OTP")
            st.info(f"We have sent a 6-digit verification code to **{st.session_state.temp_reg_data.get('id')}**")
            
            entered_otp = st.text_input("Enter 6-Digit OTP", max_chars=6, placeholder="e.g. 123456")
            
            col_ver, col_back = st.columns(2)
            with col_ver:
                if st.button("Verify & Complete Registration"):
                    if entered_otp == st.session_state.generated_otp:
                        reg_data = st.session_state.temp_reg_data
                        saas_db[reg_data["id"]] = {
                            "password": reg_data["password"],
                            "profile": reg_data["profile"],
                            "history": [],
                            "parties": {
                                "Sample Party": {
                                    "legal": "Client Name",
                                    "address": "Sample Address, Delhi",
                                    "gstin": "07AAAAA0000A1Z5"
                                }
                            },
                            "services": ["ITR", "GST", "GST REGISTRATION", "UDYAM"],
                            "stock_items": [
                                {"name": "General Service", "rate": 500.0}
                            ]
                        }
                        save_saas_data(saas_db)
                        st.success("Account Verified & Registered Successfully! Please go to Login tab.")
                        st.session_state.reg_step = 1
                        st.session_state.generated_otp = None
                        st.session_state.temp_reg_data = {}
                        st.rerun()
                    else:
                        st.error("Invalid OTP! Please check and try again.")
            with col_back:
                if st.button("Back / Resend"):
                    st.session_state.reg_step = 1
                    st.rerun()

else:
    # --- Logged-In User Portal ---
    current_user = st.session_state.logged_in_user
    user_data = saas_db[current_user]
    
    if "history" not in st.session_state:
        st.session_state.history = user_data["history"]
    if "saved_parties" not in st.session_state:
        st.session_state.saved_parties = user_data["parties"]
    if "saved_services" not in st.session_state:
        st.session_state.saved_services = user_data["services"]
    if "stock_items" not in user_data:
        user_data["stock_items"] = [{"name": "Default Service", "rate": 500.0}]

    # Auto-clean History (24 Days retention)
    current_time = datetime.now()
    cleaned_history = [
        h for h in st.session_state.history 
        if current_time - datetime.fromisoformat(h.get('timestamp', current_time.isoformat())) <= timedelta(days=24)
    ]
    if len(cleaned_history) != len(st.session_state.history):
        st.session_state.history = cleaned_history
        user_data["history"] = st.session_state.history
        save_saas_data(saas_db)

    # --- Sidebar Menu ---
    st.sidebar.markdown(f"👤 **Logged in as:** `{current_user}`")
    st.sidebar.markdown(f"🏢 **Company:** `{user_data['profile']['name']}`")
    st.sidebar.markdown("---")
    
    menu_option = st.sidebar.radio("Navigation Menu", [
        "Create Invoice", 
        "📊 Party-wise History & Edit/Delete (24 Days)", 
        "📦 Stock & Items Manager", 
        "⚙️ Company Profile & Format Settings", 
        "🚪 Logout"
    ])

    if menu_option == "🚪 Logout":
        st.session_state.logged_in_user = None
        st.rerun()

    elif menu_option == "⚙️ Company Profile & Format Settings":
        st.markdown("""
            <div class="main-title">
                <h1>Settings & Format Customizer</h1>
                <p>Configure company branding, 6 invoice formats/themes, and tax options with Instant Live Preview</p>
            </div>
        """, unsafe_allow_html=True)
        
        prof = user_data["profile"]
        
        format_options = [
            "Classic Blue (Professional)", 
            "Modern Dark (Executive)", 
            "Emerald Green (Corporate)", 
            "Royal Purple (Creative)", 
            "Minimalist Clean (Simple)", 
            "Crimson Red (Bold)"
        ]
        
        with st.form("profile_form"):
            st.markdown("### 🏢 Business Information")
            up_name = st.text_input("Company / Trade Name", value=prof.get("name", ""), placeholder="e.g. Shree Services")
            up_legal = st.text_input("Authorized Person / Owner Name", value=prof.get("legal", ""), placeholder="e.g. Roshan Mishra")
            up_address = st.text_input("Company Complete Address", value=prof.get("address", ""), placeholder="e.g. Plot No 64, Mohan Garden, New Delhi")
            up_contact = st.text_input("Contact Number", value=prof.get("contact", ""), placeholder="e.g. +91 7888273972")
            up_gstin = st.text_input("Company GSTIN", value=prof.get("gstin", ""), placeholder="e.g. 07XXXXX0000X1Z5")
            up_nature = st.text_input("Nature of Business / Dealings", value=prof.get("nature", ""), placeholder="e.g. Tax Consultancy & Document Services")
            
            st.markdown("### 🎨 Invoice Format & Themes (6 Types)")
            current_format = prof.get("format", "Classic Blue (Professional)")
            fmt_idx = format_options.index(current_format) if current_format in format_options else 0
            up_format = st.selectbox("Select Invoice Design Format & Color Theme", format_options, index=fmt_idx)
            
            st.markdown("### 💰 Tax & GST Configuration")
            up_gst_enabled = st.checkbox("Enable GST / Tax Calculation on Invoices", value=prof.get("gst_enabled", True))
            up_tax_rate = st.number_input("Default Tax / GST Rate (%)", min_value=0.0, max_value=28.0, value=float(prof.get("tax_rate", 18.0)))
            
            up_submit = st.form_submit_button("💾 Save All Settings")
            if up_submit:
                user_data["profile"] = {
                    "name": up_name,
                    "legal": up_legal,
                    "address": up_address,
                    "contact": up_contact,
                    "gstin": up_gstin,
                    "nature": up_nature,
                    "format": up_format,
                    "gst_enabled": up_gst_enabled,
                    "tax_rate": up_tax_rate
                }
                save_saas_data(saas_db)
                st.success("Settings and Invoice Format updated successfully!")
                st.rerun()

        # --- Instant Live Format Preview Box on Settings Page ---
        st.markdown("---")
        st.markdown("### 👁️ Instant Live Preview of Selected Theme")
        
        # Determine theme color based on current selection in form or profile
        live_theme = up_format if 'up_format' in locals() else prof.get("format", "Classic Blue")
        if "Modern Dark" in live_theme:
            prev_color = "#0f172a"
        elif "Emerald Green" in live_theme:
            prev_color = "#065f46"
        elif "Royal Purple" in live_theme:
            prev_color = "#581c87"
        elif "Minimalist Clean" in live_theme:
            prev_color = "#334155"
        elif "Crimson Red" in live_theme:
            prev_color = "#991b1b"
        else:
            prev_color = "#1e3a8a"

        sample_preview_html = f"""
        <div style="background: #fff; border: 2px dashed {prev_color}; padding: 20px; border-radius: 12px; font-family: sans-serif;">
            <div style="display: flex; justify-content: space-between; border-bottom: 2px solid {prev_color}; padding-bottom: 8px; margin-bottom: 15px;">
                <div>
                    <h3 style="margin: 0; color: {prev_color};">{up_name if 'up_name' in locals() else prof.get('name')}</h3>
                    <p style="margin: 3px 0 0 0; font-size: 11px; color: #64748b;">{up_address if 'up_address' in locals() else prof.get('address')}</p>
                </div>
                <div style="text-align: right;">
                    <h4 style="margin: 0; color: #1e293b;">TAX INVOICE</h4>
                    <p style="margin: 3px 0 0 0; font-size: 11px; color: #64748b;">Theme: {live_theme}</p>
                </div>
            </div>
            <table style="width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 10px;">
                <tr style="background: {prev_color}; color: #fff;">
                    <th style="padding: 6px; text-align: left;">Service Description</th>
                    <th style="padding: 6px; text-align: right;">Amount</th>
                </tr>
                <tr>
                    <td style="padding: 6px; border-bottom: 1px solid #cbd5e1;">Sample GST Filing (July)</td>
                    <td style="padding: 6px; border-bottom: 1px solid #cbd5e1; text-align: right;">Rs. 700.00</td>
                </tr>
            </table>
            <div style="text-align: right; font-size: 13px; font-weight: bold; color: {prev_color};">
                Total Amount: Rs. 826.00 (Incl. Tax)
            </div>
        </div>
        """
        st.components.v1.html(sample_preview_html, height=220, scrolling=False)

    elif menu_option == "📦 Stock & Items Manager":
        st.markdown("""
            <div class="main-title">
                <h1>Stock & Service Items Manager</h1>
                <p>Manage your standard items and rates for quick billing</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("add_stock_form"):
            st.markdown("### ➕ Add New Item / Service Rate")
            st_item_name = st.text_input("Item / Service Name", placeholder="e.g. GST Annual Return Filing")
            st_item_rate = st.number_input("Standard Rate (Rs.)", min_value=0.0, value=500.0)
            st_add_btn = st.form_submit_button("Add Item to Master")
            
            if st_add_btn:
                if st_item_name.strip():
                    user_data["stock_items"].append({"name": st_item_name.strip(), "rate": st_item_rate})
                    save_saas_data(saas_db)
                    st.success(f"Item '{st_item_name}' added successfully!")
                else:
                    st.warning("Please enter item name.")
                    
        st.markdown("### 📋 Current Active Items List")
        for idx, item in enumerate(user_data["stock_items"]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"🔹 **{item['name']}** — Rs. {item['rate']}")
            with col2:
                if st.button("🗑️ Delete", key=f"del_stock_{idx}"):
                    user_data["stock_items"].pop(idx)
                    save_saas_data(saas_db)
                    st.rerun()

    elif menu_option == "📊 Party-wise History & Edit/Delete (24 Days)":
        st.markdown("""
            <div class="main-title">
                <h1>Party-wise Invoice Management</h1>
                <p>View, Edit, or Delete bills created in the last 24 days</p>
            </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.history:
            st.info("No invoice history available for the last 24 days.")
        else:
            all_parties_in_history = list(set([h['client'] for h in st.session_state.history]))
            selected_history_party = st.selectbox("Select Party to View History", all_parties_in_history)
            
            party_bills = [h for h in st.session_state.history if h['client'] == selected_history_party]
            
            st.markdown(f"### Bills for: {selected_history_party}")
            
            for idx, bill in enumerate(party_bills):
                with st.expander(f"Invoice No: {bill['invoice_no']} | Date: {bill['date']} | Total: Rs. {bill['total']}"):
                    edit_key_services = f"edit_serv_{bill['invoice_no']}"
                    edit_key_paid = f"edit_paid_{bill['invoice_no']}"
                    
                    new_serv = st.text_area("Edit Services Details", value=bill.get('services', ''), key=edit_key_services, placeholder="Service Name | Period | Amount")
                    new_pd = st.number_input("Edit Total Amount Paid (Rs.)", value=float(bill.get('paid', 0.0)), key=edit_key_paid)
                    
                    col_save, col_del = st.columns(2)
                    with col_save:
                        if st.button("💾 Save Changes", key=f"save_{bill['invoice_no']}"):
                            lines = new_serv.split('\n')
                            tot_amt = 0.0
                            for line in lines:
                                if line.strip():
                                    if '|' in line:
                                        parts = [p.strip() for p in line.split('|')]
                                        try:
                                            amt = float(parts[2]) if len(parts) > 2 else float(parts[1])
                                        except:
                                            amt = 0.0
                                    else:
                                        parts = line.strip().rsplit(' ', 1)
                                        try:
                                            amt = float(parts[1])
                                        except:
                                            amt = 0.0
                                    tot_amt += amt
                            
                            for item in st.session_state.history:
                                if item['invoice_no'] == bill['invoice_no']:
                                    item['services'] = new_serv
                                    item['total'] = tot_amt
                                    item['paid'] = new_pd
                                    item['balance'] = tot_amt - new_pd
                            
                            user_data["history"] = st.session_state.history
                            save_saas_data(saas_db)
                            st.success(f"Invoice {bill['invoice_no']} updated successfully!")
                            st.rerun()
                            
                    with col_del:
                        if st.button("❌ Delete Invoice", key=f"del_{bill['invoice_no']}"):
                            st.session_state.history = [item for item in st.session_state.history if item['invoice_no'] != bill['invoice_no']]
                            user_data["history"] = st.session_state.history
                            save_saas_data(saas_db)
                            st.warning(f"Invoice {bill['invoice_no']} deleted! Sequence adjusted.")
                            st.rerun()

    else:
        # --- Create Invoice Tab ---
        comp_profile = user_data["profile"]
        
        st.markdown(f"""
            <div class="main-title">
                <h1>{comp_profile.get('name', 'Invoice Portal')}</h1>
                <p>{comp_profile.get('nature', 'Professional Billing System')} | Theme: {comp_profile.get('format', 'Classic Blue')}</p>
            </div>
        """, unsafe_allow_html=True)

        next_inv_num = len(st.session_state.history) + 1
        current_inv_no = f"TAX/2026-27/{next_inv_num:03d}"

        with st.form("invoice_form"):
            st.markdown('<div class="section-box-1">👤 1. Client / Party Details</div>', unsafe_allow_html=True)
            party_names = list(st.session_state.saved_parties.keys())
            selected_party = st.selectbox("Select Existing Party", party_names)

            with st.expander("➕ Click Here to Add New Party"):
                new_trade_name = st.text_input("New Party Trade Name", placeholder="e.g. Chandra Enterprises")
                new_legal_name = st.text_input("New Client Legal Name", placeholder="e.g. Manoj Kumar")
                new_address = st.text_input("New Client Address", placeholder="e.g. 2nd Floor, N Block, Mohan Garden")
                new_gstin = st.text_input("New Client GSTIN", placeholder="e.g. 07AAAAA0000A1Z5")

            st.markdown('<div class="section-box-2">📋 2. Invoice Details</div>', unsafe_allow_html=True)
            inv_no = st.text_input("Invoice Number (Auto-generated)", current_inv_no)
            inv_date = st.text_input("Invoice Date", datetime.now().strftime("%B %d, %Y"))

            st.markdown('<div class="section-box-3">💼 3. Select Services & Add Amount</div>', unsafe_allow_html=True)
            
            stock_names = [s['name'] for s in user_data.get("stock_items", [])]
            quick_selected = st.multiselect("Quick Add from Stock Items", stock_names)
            
            default_text = "\n".join([f"{s} | Current | {next((item['rate'] for item in user_data['stock_items'] if item['name'] == s), 500.0)}" for s in quick_selected])
            
            services_text = st.text_area("Services Details (Format: Service | Period | Amount)", value=default_text, placeholder="GST Filing | July | 700")

            total_paid = st.number_input("Total Amount Paid (Rs.)", min_value=0.0, value=0.0)

            submitted = st.form_submit_button("✨ Generate Exact A4 Invoice Preview")

        if submitted:
            if 'new_trade_name' in locals() and new_trade_name.strip():
                client_name = new_trade_name.strip()
                client_legal = new_legal_name.strip()
                client_address = new_address.strip()
                client_gstin = new_gstin.strip()
                st.session_state.saved_parties[client_name] = {
                    "legal": client_legal,
                    "address": client_address,
                    "gstin": client_gstin
                }
            else:
                client_name = selected_party
                p_info = st.session_state.saved_parties[selected_party]
                client_legal = p_info["legal"]
                client_address = p_info["address"]
                client_gstin = p_info["gstin"]

            lines = services_text.split('\n')
            items = []
            subtotal_amt = 0.0
            for line in lines:
                if line.strip():
                    if '|' in line:
                        parts = [p.strip() for p in line.split('|')]
                        desc = parts[0]
                        period = parts[1] if len(parts) > 1 else "-"
                        try:
                            amt = float(parts[2]) if len(parts) > 2 else float(parts[1])
                        except:
                            amt = 0.0
                    else:
                        parts = line.strip().rsplit(' ', 1)
                        desc = parts[0]
                        period = "General"
                        try:
                            amt = float(parts[1])
                        except:
                            amt = 0.0
                    
                    items.append((desc, period, amt))
                    subtotal_amt += amt

            gst_enabled = comp_profile.get("gst_enabled", True)
            tax_rate = float(comp_profile.get("tax_rate", 18.0)) if gst_enabled else 0.0
            tax_amount = (subtotal_amt * tax_rate) / 100.0 if gst_enabled else 0.0
            total_amt = subtotal_amt + tax_amount
            balance = total_amt - total_paid

            new_invoice_record = {
                "invoice_no": inv_no,
                "client": client_name,
                "total": total_amt,
                "paid": total_paid,
                "balance": balance,
                "date": inv_date,
                "services": services_text,
                "timestamp": datetime.now().isoformat()
            }

            st.session_state.history.append(new_invoice_record)
            
            user_data["history"] = st.session_state.history
            user_data["parties"] = st.session_state.saved_parties
            user_data["services"] = st.session_state.saved_services
            save_saas_data(saas_db)

            # --- Theme Color Selection based on Settings ---
            selected_theme_fmt = comp_profile.get("format", "Classic Blue (Professional)")
            if "Modern Dark" in selected_theme_fmt:
                primary_color = "#0f172a"
            elif "Emerald Green" in selected_theme_fmt:
                primary_color = "#065f46"
            elif "Royal Purple" in selected_theme_fmt:
                primary_color = "#581c87"
            elif "Minimalist Clean" in selected_theme_fmt:
                primary_color = "#334155"
            elif "Crimson Red" in selected_theme_fmt:
                primary_color = "#991b1b"
            else:
                primary_color = "#1e3a8a"

            # --- Dynamic Company Branded A4 HTML Layout with Theme ---
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Helvetica', Arial, sans-serif; color: #1e293b; background: #e2e8f0; margin: 0; padding: 20px; }}
                .a4-page {{ 
                    width: 210mm; 
                    min-height: 297mm; 
                    margin: auto; 
                    background: #fff; 
                    padding: 15mm 20mm; 
                    box-sizing: border-box; 
                    box-shadow: 0 0 20px rgba(0,0,0,0.15); 
                }}
                .header {{ display: flex; justify-content: space-between; border-bottom: 3px solid {primary_color}; padding-bottom: 12px; margin-bottom: 20px; }}
                .company-title {{ font-size: 24px; font-weight: bold; color: {primary_color}; }}
                .invoice-title {{ font-size: 26px; font-weight: bold; text-transform: uppercase; color: #1e293b; text-align: right; }}
                .billing-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; border: 1px solid #cbd5e1; background: #f8fafc; }}
                .billing-table td {{ padding: 12px; vertical-align: top; width: 50%; font-size: 13px; border: 1px solid #cbd5e1; line-height: 1.5; }}
                .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                .items-table th {{ background-color: {primary_color}; color: #fff; text-align: left; padding: 10px; font-size: 12px; border: 1px solid {primary_color}; }}
                .items-table td {{ border: 1px solid #cbd5e1; padding: 10px; font-size: 12px; }}
                .right {{ text-align: right; }}
                .totals {{ width: 300px; margin-left: auto; font-size: 13px; margin-bottom: 40px; border: 1px solid #cbd5e1; border-collapse: collapse; }}
                .totals td {{ padding: 8px; border: 1px solid #cbd5e1; }}
                .grand-total {{ font-weight: bold; background: #eff6ff; font-size: 14px; color: {primary_color}; }}
                .sign-area {{ float: right; text-align: right; margin-top: 30px; font-size: 13px; }}
                .sign-line {{ border-top: 1px solid #000; width: 180px; margin-top: 50px; text-align: center; font-weight: bold; }}
                .print-btn-container {{ text-align: center; margin-bottom: 20px; }}
                .print-btn {{
                    background-color: #059669;
                    color: white;
                    padding: 12px 25px;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .print-btn:hover {{ background-color: #047857; }}
                @media print {{
                    body {{ background: none; padding: 0; }}
                    .a4-page {{ box-shadow: none; margin: 0; width: 100%; padding: 10mm; }}
                    .no-print {{ display: none !important; }}
                }}
            </style>
            </head>
            <body>
            
            <div class="print-btn-container no-print">
                <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF Directly</button>
            </div>

            <div class="a4-page">
                <div class="header">
                    <div>
                        <div class="company-title">{comp_profile.get('name', 'Company Name')}</div>
                        <div style="font-size: 12px; color: #475569; margin-top: 5px; line-height: 1.4;">
                            {comp_profile.get('address', '')}<br>
                            <strong>Contact:</strong> {comp_profile.get('contact', '')}<br>
                            <strong>GSTIN:</strong> {comp_profile.get('gstin', 'N/A')}
                        </div>
                    </div>
                    <div>
                        <div class="invoice-title">Tax Invoice</div>
                        <div style="font-size: 12px; color: #475569; text-align: right; margin-top: 5px; line-height: 1.4;">
                            <strong>Invoice No:</strong> {inv_no}<br>
                            <strong>Date:</strong> {inv_date}<br>
                            <strong>Client GSTIN:</strong> {client_gstin}
                        </div>
                    </div>
                </div>

                <table class="billing-table">
                    <tr>
                        <td>
                            <strong>Service Provider:</strong><br>
                            {comp_profile.get('name', '')} ({comp_profile.get('legal', '')})<br>
                            {comp_profile.get('address', '')}
                        </td>
                        <td>
                            <strong>Billed To:</strong><br>
                            <strong>{client_name}</strong><br>
                            Legal Name: {client_legal}<br>
                            Address: {client_address}
                        </td>
                    </tr>
                </table>

                <table class="items-table">
                    <thead>
                        <tr>
                            <th style="width: 10%;">S.No.</th>
                            <th style="width: 55%;">Description of Services</th>
                            <th style="width: 15%;">Period</th>
                            <th class="right" style="width: 20%;">Amount (Rs.)</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for idx, (desc, period, amt) in enumerate(items, 1):
                html_content += "<tr><td class='right'>{}</td><td>{}</td><td>{}</td><td class='right'>{:.2f}</td></tr>".format(idx, desc, period, amt)

            gst_html_row = ""
            if gst_enabled:
                gst_html_row = f"<tr><td>GST / Tax ({tax_rate}%):</td><td class='right'>Rs. {tax_amount:.2f}</td></tr>"

            html_content += f"""
                    </tbody>
                </table>

                <table class="totals">
                    <tr><td>Subtotal:</td><td class="right">Rs. {subtotal_amt:.2f}</td></tr>
                    {gst_html_row}
                    <tr><td>Total Amount:</td><td class="right">Rs. {total_amt:.2f}</td></tr>
                    <tr><td>Total Paid:</td><td class="right">Rs. {total_paid:.2f}</td></tr>
                    <tr class="grand-total"><td>Balance Due:</td><td class="right">Rs. {balance:.2f}</td></tr>
                </table>

                <div style="clear: both;"></div>
                <div class="sign-align" style="float: right; text-align: right; margin-top: 30px; font-size: 13px;">
                    For <strong>{comp_profile.get('name', '')}</strong>
                    <div style="border-top: 1px solid #000; width: 180px; margin-top: 50px; text-align: center; font-weight: bold;">Authorised Signatory</div>
                </div>
                <div style="clear: both;"></div>
                <hr style="border:none; border-top:1px solid #cbd5e1; margin-top: 40px;">
                <div style="text-align: center; font-size: 11px; color: #64748b;">Thank you for your business! This is a computer-generated invoice. Format: {selected_theme_fmt}</div>
            </div>
            </body>
            </html>
            """

            st.success("✨ Invoice Generated Successfully! Preview below:")
            st.components.v1.html(html_content, height=800, scrolling=True)

