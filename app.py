import streamlit as st
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="Professional Invoice Portal - SaaS", page_icon="📄", layout="centered")

# --- Colorful & Responsive Modern UI CSS (Fixed Black Input Lines on Mobile) ---
st.markdown("""
    <style>
    /* Force inputs and textareas to be bright and readable on all devices */
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

    /* Responsive adjustments for phones */
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
    .main-title h1 { margin: 0; font-size: 26px; font-weight: 700; }
    .main-title p { margin: 5px 0 0 0; font-size: 14px; opacity: 0.9; }

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

    .stFormSubmitButton button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 20px;
        width: 100%;
        border: none;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
        font-size: 16px;
        margin-top: 20px;
    }
    .stFormSubmitButton button:hover {
        background: linear-gradient(135deg, #047857 0%, #059669 100%);
    }
    </style>
""", unsafe_allow_html=True)

# --- Multi-User & SaaS Database Storage Functions ---
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

saas_db = load_saas_data()

# --- Authentication & Registration Flow ---
if not st.session_state.logged_in_user:
    st.markdown("""
        <div class="main-title">
            <h1>SaaS Invoice Management Portal</h1>
            <p>Secure Login & Multi-Company Registration System</p>
        </div>
    """, unsafe_allow_html=True)
    
    auth_tab1, auth_tab2 = st.tabs(["🔐 Login", "📝 New User Registration"])
    
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
        st.subheader("Create New Account & Company")
        reg_id = st.text_input("Enter Email ID / Mobile Number (User ID)", key="reg_id", placeholder="e.g. shreeservices@gmail.com")
        reg_pass1 = st.text_input("Create Password", type="password", key="reg_pass1", placeholder="Create secure password")
        reg_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2", placeholder="Re-enter password")
        
        st.markdown("---")
        st.markdown("#### 🏢 Company / Business Profile Setup")
        comp_name = st.text_input("Company / Trade Name", key="comp_name", placeholder="e.g. Shree Services")
        comp_legal = st.text_input("Authorized Person / Owner Name", key="comp_legal", placeholder="e.g. Roshan Mishra")
        comp_address = st.text_input("Company Complete Address", key="comp_address", placeholder="e.g. Plot No 64, Mohan Garden, New Delhi")
        comp_contact = st.text_input("Contact Number", key="comp_contact", placeholder="e.g. +91 7888273972")
        comp_gstin = st.text_input("Company GSTIN (Optional)", key="comp_gstin", placeholder="e.g. 07XXXXX0000X1Z5")
        comp_nature = st.text_input("Nature of Business / Dealings", key="comp_nature", placeholder="e.g. Tax Consultancy & Document Services")
        
        if st.button("Register & Create Account"):
            if not reg_id or not reg_pass1:
                st.warning("Please fill User ID and Password fields.")
            elif reg_pass1 != reg_pass2:
                st.error("Passwords do not match! Please verify confirmation.")
            elif reg_id in saas_db:
                st.error("User ID already registered! Please login.")
            elif not comp_name:
                st.warning("Please enter Company Name.")
            else:
                saas_db[reg_id] = {
                    "password": reg_pass1,
                    "profile": {
                        "name": comp_name,
                        "legal": comp_legal,
                        "address": comp_address,
                        "contact": comp_contact,
                        "gstin": comp_gstin,
                        "nature": comp_nature
                    },
                    "history": [],
                    "parties": {
                        "RKMK Enterprises": {
                            "legal": "Rinky Acharya",
                            "address": "Flat No. 34, Ground Floor, Block P Extn, Mohan Garden, New Delhi - 110059",
                            "gstin": "07DEOPA0606H1ZU"
                        }
                    },
                    "services": ["ITR", "GST", "GST REGISTRATION", "UDYAM", "SHOP ACT"]
                }
                save_saas_data(saas_db)
                st.success("Registration Successful! Now you can go to the Login tab and sign in.")

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
    
    menu_option = st.sidebar.radio("Navigation Menu", ["Create Invoice", "📊 Party-wise History & Edit/Delete (24 Days)", "⚙️ Company Profile Settings", "🚪 Logout"])

    if menu_option == "🚪 Logout":
        st.session_state.logged_in_user = None
        st.rerun()

    elif menu_option == "⚙️ Company Profile Settings":
        st.markdown("""
            <div class="main-title">
                <h1>Company Profile Settings</h1>
                <p>Update your business and invoice branding details</p>
            </div>
        """, unsafe_allow_html=True)
        
        prof = user_data["profile"]
        with st.form("profile_form"):
            up_name = st.text_input("Company / Trade Name", value=prof.get("name", ""), placeholder="e.g. Shree Services")
            up_legal = st.text_input("Authorized Person / Owner Name", value=prof.get("legal", ""), placeholder="e.g. Roshan Mishra")
            up_address = st.text_input("Company Complete Address", value=prof.get("address", ""), placeholder="e.g. Plot No 64, Mohan Garden, New Delhi")
            up_contact = st.text_input("Contact Number", value=prof.get("contact", ""), placeholder="e.g. +91 7888273972")
            up_gstin = st.text_input("Company GSTIN", value=prof.get("gstin", ""), placeholder="e.g. 07XXXXX0000X1Z5")
            up_nature = st.text_input("Nature of Business / Dealings", value=prof.get("nature", ""), placeholder="e.g. Tax Consultancy & Document Services")
            
            up_submit = st.form_submit_button("💾 Save Profile Changes")
            if up_submit:
                user_data["profile"] = {
                    "name": up_name,
                    "legal": up_legal,
                    "address": up_address,
                    "contact": up_contact,
                    "gstin": up_gstin,
                    "nature": up_nature
                }
                save_saas_data(saas_db)
                st.success("Company profile updated successfully!")

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
                <p>{comp_profile.get('nature', 'Professional Billing System')}</p>
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
            selected_services = st.multiselect("Select Services from Library", st.session_state.saved_services, default=["GST"])
            new_service_input = st.text_input("Add New Service (Agar upar list mein na ho)", placeholder="e.g. Income Tax Return")
            
            st.markdown("💡 *Format: Service Name | Period | Amount (Jaise: GST Filing | July | 700)*")
            default_text = "\n".join([f"{s} | July | 700" for s in selected_services])
            services_text = st.text_area("Services Details", value=default_text, placeholder="GST Filing | July | 700")

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

            if new_service_input and new_service_input.upper() not in [s.upper() for s in st.session_state.saved_services]:
                st.session_state.saved_services.append(new_service_input.upper())

            lines = services_text.split('\n')
            items = []
            total_amt = 0.0
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
                    total_amt += amt

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

            # --- Dynamic Company Branded A4 HTML Layout ---
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
                .header {{ display: flex; justify-content: space-between; border-bottom: 3px solid #1e3a8a; padding-bottom: 12px; margin-bottom: 20px; }}
                .company-title {{ font-size: 24px; font-weight: bold; color: #1e3a8a; }}
                .invoice-title {{ font-size: 26px; font-weight: bold; text-transform: uppercase; color: #1e293b; text-align: right; }}
                .billing-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; border: 1px solid #cbd5e1; background: #f8fafc; }}
                .billing-table td {{ padding: 12px; vertical-align: top; width: 50%; font-size: 13px; border: 1px solid #cbd5e1; line-height: 1.5; }}
                .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                .items-table th {{ background-color: #1e3a8a; color: #fff; text-align: left; padding: 10px; font-size: 12px; border: 1px solid #1e3a8a; }}
                .items-table td {{ border: 1px solid #cbd5e1; padding: 10px; font-size: 12px; }}
                .right {{ text-align: right; }}
                .totals {{ width: 300px; margin-left: auto; font-size: 13px; margin-bottom: 40px; border: 1px solid #cbd5e1; border-collapse: collapse; }}
                .totals td {{ padding: 8px; border: 1px solid #cbd5e1; }}
                .grand-total {{ font-weight: bold; background: #eff6ff; font-size: 14px; color: #1e3a8a; }}
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

            html_content += f"""
                    </tbody>
                </table>

                <table class="totals">
                    <tr><td>Total Amount:</td><td class="right">Rs. {total_amt:.2f}</td></tr>
                    <tr><td>Total Paid:</td><td class="right">Rs. {total_paid:.2f}</td></tr>
                    <tr class="grand-total"><td>Balance Due:</td><td class="right">Rs. {balance:.2f}</td></tr>
                </table>

                <div style="clear: both;"></div>
                <div class="sign-area">
                    For <strong>{comp_profile.get('name', '')}</strong>
                    <div class="sign-line">Authorised Signatory</div>
                </div>
                <div style="clear: both;"></div>
                <hr style="border:none; border-top:1px solid #cbd5e1; margin-top: 40px;">
                <div style="text-align: center; font-size: 11px; color: #64748b;">Thank you for your business! This is a computer-generated invoice.</div>
            </div>
            </body>
            </html>
            """

            st.success("✨ Invoice Generated Successfully! Preview below:")
            st.components.v1.html(html_content, height=800, scrolling=True)
