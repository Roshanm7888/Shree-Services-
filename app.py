import streamlit as st
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="Professional Invoice Portal - SaaS", page_icon="📄", layout="centered")

# --- Colorful & Responsive Modern UI CSS ---
st.markdown("""
    <style>
    label, p, span, div { color: #1e293b !important; }
    input, textarea, select { background-color: #ffffff !important; color: #1e293b !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; }
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

USERS_FILE = "saas_users_data.json"

def load_saas_data():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f: return json.load(f)
        except: pass
    return {}

def save_saas_data(data):
    with open(USERS_FILE, "w") as f: json.dump(data, f, indent=4)

if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = None
saas_db = load_saas_data()

def get_initials(name):
    words = name.split()
    if len(words) >= 2: return (words[0][0] + words[1][0]).upper()
    elif len(words) == 1 and len(words[0]) >= 2: return words[0][:2].upper()
    return "SS"

# --- Authentication & Registration Flow (No OTP) ---
if not st.session_state.logged_in_user:
    st.markdown("""
        <div class="main-title">
            <h1>SaaS Invoice Management Portal</h1>
            <p>Secure Login & Direct Company Registration System</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("⚡ Quick Admin Test Login"):
        master_id = "roshan@shreeservices.com"
        if master_id not in saas_db:
            saas_db[master_id] = {
                "password": "admin",
                "profile": {
                    "name": "Shree Services", "legal": "Roshan Mishra",
                    "address": "Plot no 64 & 65, Block K-5, Mohan Garden, New Delhi - 110059",
                    "contact": "7888273972", "gstin": "07SAMPLEGSTIN",
                    "nature": "Tax Consultancy & Accounting Services",
                    "format": "Classic Blue (Professional)", "border_style": "Solid Line",
                    "gst_enabled": True, "tax_rate": 18.0, "watermark_enabled": True,
                    "watermark_type": "Company Name", "logo_choice": "Modern Shield (Auto)"
                },
                "history": [],
                "parties": {
                    "RKMK Enterprises": {"legal": "Rinky Acharya", "address": "Mohan Garden, New Delhi", "gstin": "07DEOPA0606H1ZU"},
                    "Chandra Enterprises": {"legal": "Manoj Kumar", "address": "Mohan Garden, New Delhi", "gstin": "07AMSPK3043R1ZC"}
                },
                "services": ["ITR", "GST", "GST REGISTRATION", "UDYAM", "SHOP ACT"],
                "stock_items": [{"name": "GST Monthly Filing", "rate": 700.0}, {"name": "ITR Filing", "rate": 1000.0}]
            }
            save_saas_data(saas_db)
        st.session_state.logged_in_user = master_id
        st.rerun()

    auth_tab1, auth_tab2 = st.tabs(["🔐 Login", "📝 New User & Company Registration"])
    
    with auth_tab1:
        st.subheader("Existing User Login")
        login_id = st.text_input("Email ID / Mobile Number", key="login_id", placeholder="e.g. user@gmail.com or 9876543210")
        login_pass = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
        if st.button("Login to Portal"):
            if login_id in saas_db and saas_db[login_id]["password"] == login_pass:
                st.session_state.logged_in_user = login_id
                st.success("Login Successful!")
                st.rerun()
            else: st.error("Invalid User ID or Password!")
                
    with auth_tab2:
        st.subheader("Create Account & Company Profile")
        reg_id = st.text_input("Enter Email ID or Mobile Number (User ID)", key="reg_id", placeholder="e.g. client@gmail.com")
        reg_pass1 = st.text_input("Create Password", type="password", key="reg_pass1")
        reg_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2")
        
        st.markdown("---")
        st.markdown("#### 🏢 Company / Business Profile Setup")
        comp_name = st.text_input("Company / Trade Name", key="comp_name", placeholder="e.g. Shree Services")
        comp_legal = st.text_input("Authorized Person / Owner Name", key="comp_legal", placeholder="e.g. Roshan Mishra")
        comp_address = st.text_input("Company Complete Address", key="comp_address", placeholder="e.g. Mohan Garden, New Delhi")
        comp_contact = st.text_input("Contact Number", key="comp_contact", placeholder="e.g. +91 7888273972")
        comp_gstin = st.text_input("Company GSTIN (Optional)", key="comp_gstin", placeholder="e.g. 07XXXXX0000X1Z5")
        comp_nature = st.text_input("Nature of Business / Dealings", key="comp_nature", placeholder="e.g. Tax Consultancy")
        
        if st.button("Register & Create Company Account"):
            if not reg_id or not reg_pass1: st.warning("Please fill User ID and Password fields.")
            elif reg_pass1 != reg_pass2: st.error("Passwords do not match!")
            elif reg_id in saas_db: st.error("User ID already registered! Please login.")
            elif not comp_name: st.warning("Please enter Company Name.")
            else:
                saas_db[reg_id] = {
                    "password": reg_pass1,
                    "profile": {
                        "name": comp_name, "legal": comp_legal, "address": comp_address,
                        "contact": comp_contact, "gstin": comp_gstin, "nature": comp_nature,
                        "format": "Classic Blue (Professional)", "border_style": "Solid Line",
                        "gst_enabled": True, "tax_rate": 18.0, "watermark_enabled": True,
                        "watermark_type": "Company Name", "logo_choice": "Modern Shield (Auto)"
                    },
                    "history": [], "parties": {"Sample Party": {"legal": "Client Name", "address": "Delhi", "gstin": "07AAAAA0000A1Z5"}},
                    "services": ["ITR", "GST"], "stock_items": [{"name": "General Service", "rate": 500.0}]
                }
                save_saas_data(saas_db)
                st.success("Account Created Successfully! Now you can go to the Login tab.")

else:
    # --- Logged-In User Portal ---
    current_user = st.session_state.logged_in_user
    user_data = saas_db[current_user]
    
    if "history" not in st.session_state: st.session_state.history = user_data["history"]
    if "saved_parties" not in st.session_state: st.session_state.saved_parties = user_data["parties"]
    if "saved_services" not in st.session_state: st.session_state.saved_services = user_data["services"]
    if "stock_items" not in user_data: user_data["stock_items"] = [{"name": "Default Service", "rate": 500.0}]

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

    # --- Integrated AI Gemini Design Studio Widget ---
    st.sidebar.markdown("---")
    with st.sidebar.expander("🤖 AI Design & Logo Studio"):
        task = st.selectbox("I need help with:", ["Logo Creation", "Invoice Layout"])
        req = st.text_area("Describe your requirement (e.g. 'Shree Hindi me circle mein')")
        if st.button("✨ Generate AI Prompt"):
            if req:
                st.info(f"💡 **AI Suggestion:** Create a {task} based on: '{req}'. Focus on professional typography and minimalist aesthetics.")
            else: st.warning("Type your idea first!")

    if menu_option == "🚪 Logout":
        st.session_state.logged_in_user = None
        st.rerun()

    elif menu_option == "⚙️ Company Profile & Format Settings":
        st.markdown("""
            <div class="main-title">
                <h1>Settings & Format Customizer</h1>
                <p>Configure company branding, themes, borders, watermarks, and instant live preview</p>
            </div>
        """, unsafe_allow_html=True)
        
        prof = user_data["profile"]
        format_options = ["Classic Blue (Professional)", "Modern Dark (Executive)", "Emerald Green (Corporate)", "Royal Purple (Creative)", "Minimalist Clean (Simple)", "Crimson Red (Bold)"]
        border_options = ["Solid Line", "Dotted Border (Stylish)", "Double Line (Accounting)", "Dashed Border (Modern)"]
        logo_choices = ["Modern Shield (Auto)", "Circular Monogram (Auto)", "Geometric Badge (Auto)", "Minimalist Crest (Auto)", "Classic Starburst (Auto)", "Sleek Diamond (Auto)"]

        st.markdown("### 🏢 Business Information")
        up_name = st.text_input("Company / Trade Name", value=prof.get("name", ""))
        up_legal = st.text_input("Authorized Person / Owner Name", value=prof.get("legal", ""))
        up_address = st.text_input("Company Complete Address", value=prof.get("address", ""))
        up_contact = st.text_input("Contact Number", value=prof.get("contact", ""))
        up_gstin = st.text_input("Company GSTIN", value=prof.get("gstin", ""))
        up_nature = st.text_input("Nature of Business / Dealings", value=prof.get("nature", ""))
        
        st.markdown("### 🎨 Invoice Theme & Border Design")
        up_format = st.selectbox("Select Invoice Color Theme", format_options, index=format_options.index(prof.get("format", "Classic Blue (Professional)")))
        up_border = st.selectbox("Select Invoice Border Style", border_options, index=border_options.index(prof.get("border_style", "Solid Line")))

        st.markdown("### 🖼️ Logo & Watermark Settings")
        up_logo = st.selectbox("Select Auto-Generated Logo Design", logo_choices, index=logo_choices.index(prof.get("logo_choice", "Modern Shield (Auto)")))
        up_custom_logo = st.text_input("Upload / Image URL for Custom Logo (Optional)", value=prof.get("custom_logo", ""))
        up_watermark_enabled = st.checkbox("Enable Background Watermark on Invoice", value=prof.get("watermark_enabled", True))
        up_watermark_type = st.radio("Watermark Content Type", ["Company Name", "Logo Watermark"], index=0 if prof.get("watermark_type", "Company Name") == "Company Name" else 1)

        st.markdown("### 💰 Tax & GST Configuration")
        up_gst_enabled = st.checkbox("Enable GST / Tax Calculation on Invoices", value=prof.get("gst_enabled", True))
        up_tax_rate = st.number_input("Default Tax / GST Rate (%)", min_value=0.0, max_value=28.0, value=float(prof.get("tax_rate", 18.0)))
        
        if st.button("💾 Save All Settings Permanently"):
            user_data["profile"] = {
                "name": up_name, "legal": up_legal, "address": up_address, "contact": up_contact,
                "gstin": up_gstin, "nature": up_nature, "format": up_format, "border_style": up_border,
                "logo_choice": up_logo, "custom_logo": up_custom_logo, "watermark_enabled": up_watermark_enabled,
                "watermark_type": up_watermark_type, "gst_enabled": up_gst_enabled, "tax_rate": up_tax_rate
            }
            save_saas_data(saas_db)
            st.success("Settings saved successfully!")

        # --- Instant Full A4 Size Live Preview Box ---
        st.markdown("---")
        st.markdown("### 👁️ Instant Full A4 Size Live Preview (Real-Time)")
        
        p_color = "#0f172a" if "Modern Dark" in up_format else "#065f46" if "Emerald Green" in up_format else "#581c87" if "Royal Purple" in up_format else "#334155" if "Minimalist Clean" in up_format else "#991b1b" if "Crimson Red" in up_format else "#1e3a8a"
        border_css = "2px dotted #1e293b" if "Dotted" in up_border else "2px dashed #1e293b" if "Dashed" in up_border else "4px double #1e293b" if "Double" in up_border else "1px solid #cbd5e1"

        initials = get_initials(up_name)
        logo_html = f"<div style='width: 50px; height: 50px; background: {p_color}; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: bold; border-radius: 8px; font-size: 18px;'>{initials}</div>"
        if up_custom_logo.strip(): logo_html = f"<img src='{up_custom_logo}' style='max-height: 50px; max-width: 50px; object-fit: contain;'>"

        wm_html = f'<div style="position: absolute; top: 40%; left: 20%; transform: rotate(-30deg); font-size: 90px; font-weight: bold; color: rgba(0, 0, 0, 0.04); z-index: 0; pointer-events: none; white-space: nowrap;">{up_name if up_watermark_type == "Company Name" else initials}</div>' if up_watermark_enabled else ""

        full_a4_preview_html = f"""
        <!DOCTYPE html><html><head><meta charset="utf-8"><style>
            body {{ font-family: 'Helvetica', Arial, sans-serif; color: #1e293b; background: #e2e8f0; margin: 0; padding: 20px; }}
            .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 15mm 20mm; box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.15); border: {border_css}; position: relative; overflow: hidden; }}
            .header {{ display: flex; justify-content: space-between; border-bottom: 3px solid {p_color}; padding-bottom: 12px; margin-bottom: 20px; position: relative; z-index: 1; }}
            .company-title {{ font-size: 24px; font-weight: bold; color: {p_color}; }}
            .invoice-title {{ font-size: 26px; font-weight: bold; text-transform: uppercase; color: #1e293b; text-align: right; }}
            .billing-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; border: 1px solid #cbd5e1; background: #f8fafc; position: relative; z-index: 1; }}
            .billing-table td {{ padding: 12px; vertical-align: top; width: 50%; font-size: 13px; border: 1px solid #cbd5e1; line-height: 1.5; }}
            .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; position: relative; z-index: 1; }}
            .items-table th {{ background-color: {p_color}; color: #fff; text-align: left; padding: 10px; font-size: 12px; border: 1px solid {p_color}; }}
            .items-table td {{ border: 1px solid #cbd5e1; padding: 10px; font-size: 12px; }}
            .right {{ text-align: right; }}
            .totals {{ width: 300px; margin-left: auto; font-size: 13px; margin-bottom: 40px; border: 1px solid #cbd5e1; border-collapse: collapse; position: relative; z-index: 1; }}
            .totals td {{ padding: 8px; border: 1px solid #cbd5e1; }}
            .grand-total {{ font-weight: bold; background: #eff6ff; font-size: 14px; color: {p_color}; }}
        </style></head><body><div class="a4-page">
            {wm_html}
            <div class="header">
                <div style="display: flex; align-items: flex-start; gap: 15px;">
                    {logo_html}
                    <div>
                        <div class="company-title">{up_name}</div>
                        <div style="font-size: 12px; color: #475569; margin-top: 5px; line-height: 1.4;">{up_address}<br><strong>Contact:</strong> {up_contact}<br><strong>GSTIN:</strong> {up_gstin}</div>
                    </div>
                </div>
                <div><div class="invoice-title">Tax Invoice</div><div style="font-size: 12px; color: #475569; text-align: right; margin-top: 5px; line-height: 1.4;"><strong>Invoice No:</strong> TAX/2026-27/001<br><strong>Date:</strong> July 15, 2026</div></div>
            </div>
            <table class="billing-table"><tr><td><strong>Service Provider:</strong><br>{up_name}</td><td><strong>Billed To:</strong><br><strong>Sample Client Enterprises</strong><br>New Delhi</td></tr></table>
            <table class="items-table"><thead><tr><th style="width: 10%;">S.No.</th><th style="width: 55%;">Description of Services</th><th style="width: 15%;">Period</th><th class="right" style="width: 20%;">Amount (Rs.)</th></tr></thead><tbody><tr><td class='right'>1</td><td>Sample GST Monthly Filing Service</td><td>July 2026</td><td class='right'>700.00</td></tr></tbody></table>
            <table class="totals"><tr><td>Subtotal:</td><td class="right">Rs. 700.00</td></tr><tr><td>GST (18%):</td><td class="right">Rs. 126.00</td></tr><tr class="grand-total"><td>Total Amount:</td><td class="right">Rs. 826.00</td></tr></table>
            <div style="text-align: center; font-size: 11px; color: #64748b; position: relative; z-index: 1;">Thank you for your business! Theme: {up_format}</div>
        </div></body></html>
        """
        st.components.v1.html(full_a4_preview_html, height=800, scrolling=True)

    elif menu_option == "📦 Stock & Items Manager":
        st.markdown("<div class='main-title'><h1>Stock & Service Items Manager</h1></div>", unsafe_allow_html=True)
        with st.form("add_stock_form"):
            st_item_name = st.text_input("Item / Service Name", placeholder="e.g. GST Annual Return Filing")
            st_item_rate = st.number_input("Standard Rate (Rs.)", min_value=0.0, value=500.0)
            if st.form_submit_button("Add Item to Master"):
                if st_item_name.strip():
                    user_data["stock_items"].append({"name": st_item_name.strip(), "rate": st_item_rate})
                    save_saas_data(saas_db)
                    st.success(f"Item '{st_item_name}' added!")
                else: st.warning("Enter item name.")
        for idx, item in enumerate(user_data["stock_items"]):
            col1, col2 = st.columns([3, 1])
            with col1: st.write(f"🔹 **{item['name']}** — Rs. {item['rate']}")
            with col2:
                if st.button("🗑️ Delete", key=f"del_stock_{idx}"):
                    user_data["stock_items"].pop(idx)
                    save_saas_data(saas_db)
                    st.rerun()

    elif menu_option == "📊 Party-wise History & Edit/Delete (24 Days)":
        st.markdown("<div class='main-title'><h1>Party-wise Invoice Management</h1></div>", unsafe_allow_html=True)
        if not st.session_state.history: st.info("No invoice history available.")
        else:
            all_parties = list(set([h['client'] for h in st.session_state.history]))
            sel_party = st.selectbox("Select Party", all_parties)
            for bill in [h for h in st.session_state.history if h['client'] == sel_party]:
                with st.expander(f"Invoice No: {bill['invoice_no']} | Total: Rs. {bill['total']}"):
                    new_serv = st.text_area("Edit Services", value=bill.get('services', ''), key=f"serv_{bill['invoice_no']}")
                    new_pd = st.number_input("Paid Amount", value=float(bill.get('paid', 0.0)), key=f"pd_{bill['invoice_no']}")
                    if st.button("💾 Save Changes", key=f"sv_{bill['invoice_no']}"):
                        tot = sum([float(l.split('|')[-1].strip()) for l in new_serv.split('\n') if l.strip()])
                        bill.update({'services': new_serv, 'total': tot, 'paid': new_pd, 'balance': tot - new_pd})
                        user_data["history"] = st.session_state.history
                        save_saas_data(saas_db)
                        st.success("Updated!")
                        st.rerun()
                    if st.button("❌ Delete Invoice", key=f"dl_{bill['invoice_no']}"):
                        st.session_state.history = [h for h in st.session_state.history if h['invoice_no'] != bill['invoice_no']]
                        user_data["history"] = st.session_state.history
                        save_saas_data(saas_db)
                        st.warning("Deleted!")
                        st.rerun()

    else:
        # --- Create Invoice Tab ---
        comp_profile = user_data["profile"]
        st.markdown(f"<div class='main-title'><h1>{comp_profile.get('name', 'Invoice Portal')}</h1><p>{comp_profile.get('nature', 'Billing System')}</p></div>", unsafe_allow_html=True)

        next_inv_num = len(st.session_state.history) + 1
        current_inv_no = f"TAX/2026-27/{next_inv_num:03d}"

        with st.form("invoice_form"):
            st.markdown('<div class="section-box-1">👤 1. Client Details</div>', unsafe_allow_html=True)
            party_names = list(st.session_state.saved_parties.keys())
            selected_party = st.selectbox("Select Existing Party", party_names)

            with st.expander("➕ Add New Party"):
                new_trade_name = st.text_input("Trade Name")
                new_legal_name = st.text_input("Legal Name")
                new_address = st.text_input("Address")
                new_gstin = st.text_input("GSTIN")

            st.markdown('<div class="section-box-2">📋 2. Invoice Details</div>', unsafe_allow_html=True)
            inv_no = st.text_input("Invoice Number", current_inv_no)
            inv_date = st.text_input("Invoice Date", datetime.now().strftime("%B %d, %Y"))

            st.markdown('<div class="section-box-3">💼 3. Services & Amount</div>', unsafe_allow_html=True)
            quick_selected = st.multiselect("Quick Add from Stock", [s['name'] for s in user_data.get("stock_items", [])])
            default_text = "\n".join([f"{s} | Current | {next((i['rate'] for i in user_data['stock_items'] if i['name'] == s), 500.0)}" for s in quick_selected])
            services_text = st.text_area("Services Details (Service | Period | Amount)", value=default_text)
            total_paid = st.number_input("Total Amount Paid (Rs.)", min_value=0.0, value=0.0)

            submitted = st.form_submit_button("✨ Generate Exact A4 Invoice Preview")

        if submitted:
            client_name = new_trade_name.strip() if 'new_trade_name' in locals() and new_trade_name.strip() else selected_party
            if client_name == new_trade_name.strip() and new_trade_name.strip():
                st.session_state.saved_parties[client_name] = {"legal": new_legal_name, "address": new_address, "gstin": new_gstin}
            p_info = st.session_state.saved_parties.get(client_name, {"legal": "-", "address": "-", "gstin": "-"})
            
            subtotal_amt = sum([float(l.split('|')[-1].strip()) for l in services_text.split('\n') if l.strip() and '|' in l])
            tax_rate = float(comp_profile.get("tax_rate", 18.0)) if comp_profile.get("gst_enabled", True) else 0.0
            tax_amount = (subtotal_amt * tax_rate) / 100.0
            total_amt = subtotal_amt + tax_amount
            balance = total_amt - total_paid

            st.session_state.history.append({
                "invoice_no": inv_no, "client": client_name, "total": total_amt,
                "paid": total_paid, "balance": balance, "date": inv_date,
                "services": services_text, "timestamp": datetime.now().isoformat()
            })
            user_data["history"] = st.session_state.history
            user_data["parties"] = st.session_state.saved_parties
            save_saas_data(saas_db)

            p_col = "#0f172a" if "Modern Dark" in comp_profile.get("format") else "#1e3a8a"
            b_css = "2px dotted #1e293b" if "Dotted" in comp_profile.get("border_style") else "1px solid #cbd5e1"
            init = get_initials(comp_profile.get("name"))
            l_html = f"<div style='width:50px;height:50px;background:{p_col};color:#fff;display:flex;align-items:center;justify-content:center;font-weight:bold;border-radius:8px;'>{init}</div>"
            
            items_html = "".join([f"<tr><td class='right'>{i}</td><td>{l.split('|')[0]}</td><td>{l.split('|')[1]}</td><td class='right'>{l.split('|')[2]}</td></tr>" for i, l in enumerate(services_text.split('\n'), 1) if l.strip() and '|' in l])

            html_content = f"""
            <!DOCTYPE html><html><head><meta charset="utf-8"><style>
                body {{ font-family: Helvetica, Arial; color: #1e293b; background: #e2e8f0; padding: 20px; }}
                .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 15mm 20mm; box-sizing: border-box; border: {b_css}; position: relative; }}
                .header {{ display: flex; justify-content: space-between; border-bottom: 3px solid {p_col}; padding-bottom: 12px; margin-bottom: 20px; }}
                .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                .items-table th {{ background-color: {p_col}; color: #fff; padding: 10px; font-size: 12px; text-align: left; }}
                .items-table td {{ border: 1px solid #cbd5e1; padding: 10px; font-size: 12px; }}
                .right {{ text-align: right; }}
                .totals {{ width: 300px; margin-left: auto; font-size: 13px; border-collapse: collapse; }}
                .totals td {{ padding: 8px; border: 1px solid #cbd5e1; }}
                .grand-total {{ font-weight: bold; background: #eff6ff; color: {p_col}; }}
                @media print {{ body {{ background: none; padding: 0; }} .no-print {{ display: none !important; }} }}
            </style></head><body>
            <div class="no-print" style="text-align: center; margin-bottom: 20px;"><button onclick="window.print()" style="background:#059669;color:white;padding:12px 25px;font-weight:bold;border:none;border-radius:8px;cursor:pointer;">🖨️ Print / Save PDF</button></div>
            <div class="a4-page">
                <div class="header"><div style="display:flex;gap:15px;">{l_html}<div><h2 style="margin:0;color:{p_col};">{comp_profile.get('name')}</h2><p style="margin:3px 0;font-size:12px;">{comp_profile.get('address')}</p></div></div><div style="text-align:right;"><h2 style="margin:0;">Tax Invoice</h2><p style="margin:3px 0;font-size:12px;">No: {inv_no}<br>Date: {inv_date}</p></div></div>
                <table style="width:100%;border-collapse:collapse;margin-bottom:20px;font-size:13px;"><tr><td style="border:1px solid #cbd5e1;padding:10px;"><strong>From:</strong> {comp_profile.get('name')}</td><td style="border:1px solid #cbd5e1;padding:10px;"><strong>Billed To:</strong> {client_name}<br>GSTIN: {p_info.get('gstin')}</td></tr></table>
                <table class="items-table"><thead><tr><th>S.No.</th><th>Description</th><th>Period</th><th class="right">Amount</th></tr></thead><tbody>{items_html}</tbody></table>
                <table class="totals"><tr><td>Subtotal:</td><td class="right">Rs. {subtotal_amt:.2f}</td></tr><tr><td>GST ({tax_rate}%):</td><td class="right">Rs. {tax_amount:.2f}</td></tr><tr class="grand-total"><td>Total Amount:</td><td class="right">Rs. {total_amt:.2f}</td></tr><tr><td>Paid:</td><td class="right">Rs. {total_paid:.2f}</td></tr><tr class="grand-total"><td>Balance Due:</td><td class="right">Rs. {balance:.2f}</td></tr></table>
            </div></body></html>
            """
            st.success("✨ Invoice Generated Successfully!")
            st.components.v1.html(html_content, height=800, scrolling=True)
