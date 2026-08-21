import streamlit as st
from datetime import datetime, timedelta
import json
import os
import time
from google import genai

st.set_page_config(page_title="Professional Invoice Portal - SaaS", page_icon="📄", layout="wide")

# --- GEMINI API CONFIG (Replace with your actual API key) ---
API_KEY = "YOUR_GOOGLE_GEMINI_API_KEY"
client = genai.Client(api_key=API_KEY) if API_KEY and API_KEY != "YOUR_GOOGLE_GEMINI_API_KEY" else None

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
if "login_time" not in st.session_state: st.session_state.login_time = None
if "inv_rows" not in st.session_state: st.session_state.inv_rows = [{"desc": "", "hsn": "", "unit": "NOS", "qty": 1.0, "rate": 0.0, "tax_type": "Taxable", "tax_pct": 18.0, "amt": 0.0}]

saas_db = load_saas_data()

def get_initials(name):
    words = name.split()
    if len(words) >= 2: return (words[0][0] + words[1][0]).upper()
    elif len(words) == 1 and len(words[0]) >= 2: return words[0][:2].upper()
    return "SS"

# --- UPDATED AI BUSINESS ASSISTANT FUNCTION (google-genai standard) ---
def ask_gemini_assistant(query):
    if not client:
        return "API Key is missing or not configured properly."
    try:
        instructions = """You are an expert, polite AI Business Assistant for 'Shree Services Invoice Portal'. 
        Knowledge base to guide users:
        1. Business Natures supported: Goods/Manufacturing/Trading, Services, Transport Company, Other Business.
        2. Settings & Customization: Users can configure company details, choose from 6 Designer Wave Themes, toggle GST, and set watermarks in the 'Settings' tab.
        3. Subscription & Plans: Free trial allows 1 invoice generation. Paid subscription is Rs. 5 via UPI (roshan@shreeservices.upi). Users can submit UTR/Txn ID, and Admin reviews it.
        4. History & Management: Users can view and edit/delete past invoices up to 24 days.
        Provide step-by-step, accurate, and professional answers."""
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{instructions} User Query: {query}"
        )
        return response.text
    except Exception as e:
        return f"AI Assistant error: {str(e)}"

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
            if st.button("Login to Portal"):
                if login_id == "roshan@shreeservices.com" and login_pass == "admin":
                    if login_id not in saas_db:
                        saas_db[login_id] = {
                            "password": "admin",
                            "profile": {"name": "Shree Services", "legal": "Roshan Mishra", "address": "Mohan Garden, New Delhi", "contact": "7888273972", "gstin": "07SAMPLEGSTIN", "nature": "Goods / Manufacturing / Trading", "format": "Corporate Curve Wave (New Professional)", "border_style": "Solid Line", "gst_enabled": True, "watermark_enabled": True, "watermark_type": "Company Name"},
                            "history": [], "parties": {"RKMK Enterprises": {"legal": "Rinky", "address": "Delhi", "gstin": "07DEOPA0606H1ZU"}},
                            "subscription": "Paid", "bills_created": 0
                        }
                        save_saas_data(saas_db)
                    st.session_state.logged_in_user = login_id
                    st.session_state.login_time = datetime.now()
                    st.success("Admin Login Successful!")
                    st.rerun()
                elif login_id in saas_db and saas_db[login_id]["password"] == login_pass:
                    st.session_state.logged_in_user = login_id
                    st.session_state.login_time = datetime.now()
                    st.success("Login Successful!")
                    st.rerun()
                else: st.error("Invalid User ID or Password!")
                    
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

    # --- WEBSITE KEY BENEFITS & FEATURES SECTION ---
    st.markdown("<br><hr><h2 style='text-align: center; color: #1e3a8a;'>🌟 Why Businesses Choose Our Portal</h2><p style='text-align: center; color: #64748b;'>Built specifically for Indian MSMEs, Accountants, and Service Providers with Tally-grade accuracy.</p><br>", unsafe_allow_html=True)
    
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    with b_col1:
        st.markdown("""
            <div class="benefit-card">
                <h3>⚡ Smart Multi-Nature Billing</h3>
                <p>Supports Goods (Manufacturing/Trading), Services, Transport (LR No/Vehicle), and General businesses with auto-adjusted columns.</p>
            </div>
        """, unsafe_allow_html=True)
    with b_col2:
        st.markdown("""
            <div class="benefit-card">
                <h3>📊 Tally-Grade Grid Entry</h3>
                <p>Smooth item creation with unit selectors (NOS, Box, Pcs, Kgs), HSN codes, Nil Rated vs Taxable selection, and auto-calculations.</p>
            </div>
        """, unsafe_allow_html=True)
    with b_col3:
        st.markdown("""
            <div class="benefit-card">
                <h3>🎨 Designer Wave Themes & Watermarks</h3>
                <p>Choose from corporate curved wave designs (Navy, Emerald, Sunset Orange, Royal Blue) with custom watermarks.</p>
            </div>
        """, unsafe_allow_html=True)
    with b_col4:
        st.markdown("""
            <div class="benefit-card">
                <h3>🤖 24/7 AI Business Assistant</h3>
                <p>Instant expert support for tax rules, settings navigation, and step-by-step portal assistance powered by Gemini.</p>
            </div>
        """, unsafe_allow_html=True)

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

    # --- ADMIN DASHBOARD IN SIDEBAR ---
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

    # --- Sidebar Menu & Session Info ---
    st.sidebar.markdown(f"👤 **User:** `{current_user}`")
    st.sidebar.markdown(f"🏢 **Company:** `{user_data['profile']['name']}`")
    st.sidebar.markdown(f"🌟 **Plan:** `{user_data['subscription']}`")
    
    st.sidebar.markdown("---")
    if st.session_state.login_time:
        rem_secs = max(0, SESSION_TIMEOUT_SECONDS - int((datetime.now() - st.session_state.login_time).total_seconds()))
        rem_mins = rem_secs // 60
        rem_s = rem_secs % 60
        st.sidebar.info(f"⏱️ **Session Remaining:** `{rem_mins:02d}:{rem_s:02d}`")

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
        st.markdown("<div class='main-title'><h1>🤖 AI Business & Tax Assistant</h1><p>Ask anything about taxes, invoice settings, or how to use the portal!</p></div>", unsafe_allow_html=True)
        
        user_query = st.text_area("Type your question here (e.g., 'How do I change my invoice theme?' or 'What is the GST calculation rule?'):")
        if st.button("Ask AI Expert"):
            if user_query.strip():
                with st.spinner("Thinking..."):
                    ai_answer = ask_gemini_assistant(user_query)
                    st.markdown("### 💡 AI Expert Response:")
                    st.info(ai_answer)
            else:
                st.warning("Please enter a valid question.")

    elif menu_option == "⚙️ Company Profile & Format Settings":
        st.markdown("""
            <div class="main-title">
                <h1>Settings & Format Customizer</h1>
                <p>Configure fixed business nature, Designer Wave Themes, watermark options, and live preview</p>
            </div>
        """, unsafe_allow_html=True)
        
        prof = user_data["profile"]
        format_options = [
            "Corporate Curve Wave (New Professional)", 
            "Emerald Green Wave (Modern)", 
            "Sunset Orange Wave (Vibrant)", 
            "Royal Purple Curve (Creative)", 
            "Minimalist Clean (Simple)", 
            "Classic Blue (Standard)"
        ]
        border_options = ["Solid Line", "Dotted Border (Stylish)", "Double Line (Accounting)", "Dashed Border (Modern)"]

        st.markdown("### 🏢 Business Information")
        up_name = st.text_input("Company / Trade Name", value=prof.get("name", ""))
        up_legal = st.text_input("Authorized Person / Owner Name", value=prof.get("legal", ""))
        up_address = st.text_input("Company Complete Address", value=prof.get("address", ""))
        up_contact = st.text_input("Contact Number", value=prof.get("contact", ""))
        up_gstin = st.text_input("Company GSTIN", value=prof.get("gstin", ""))
        
        nat_idx = nature_options.index(current_nature) if current_nature in nature_options else 0
        up_nature = st.selectbox("Fixed Business Nature (Format)", nature_options, index=nat_idx)
        
        st.markdown("### 🎨 Invoice Theme & Designer Wave Layout")
        fmt_val = prof.get("format", format_options[0])
        fmt_idx = format_options.index(fmt_val) if fmt_val in format_options else 0
        up_format = st.selectbox("Select Invoice Designer Theme", format_options, index=fmt_idx)

        b_val = prof.get("border_style", "Solid Line")
        b_idx = border_options.index(b_val) if b_val in border_options else 0
        up_border = st.selectbox("Select Invoice Border Style", border_options, index=b_idx)

        up_custom_logo = st.text_input("Logo Image URL (Optional - leave blank for automatic Initials badge)", value=prof.get("custom_logo", ""))
        up_watermark_enabled = st.checkbox("Enable Background Watermark on Invoice", value=prof.get("watermark_enabled", True))
        
        wm_type_val = prof.get("watermark_type", "Company Name")
        up_watermark_type = st.radio("Watermark Content Type (2 Options)", ["Company Name", "Logo Initials"], index=0 if wm_type_val == "Company Name" else 1)

        st.markdown("### 💰 Tax & GST Configuration")
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

        # --- INSTANT FULL A4 SIZE LIVE PREVIEW WITH DESIGNER WAVE STYLING ---
        st.markdown("---")
        st.markdown("### 👁️ Instant Full A4 Size Live Preview (Real-Time)")
        
        if "Emerald Green" in up_format:
            p_col = "#065f46"
            wave_gradient = "linear-gradient(135deg, #059669 0%, #10b981 100%)"
        elif "Sunset Orange" in up_format:
            p_col = "#c2410c"
            wave_gradient = "linear-gradient(135deg, #ea580c 0%, #fb923c 100%)"
        elif "Royal Purple" in up_format:
            p_col = "#581c87"
            wave_gradient = "linear-gradient(135deg, #7e22ce 0%, #a855f7 100%)"
        elif "Minimalist Clean" in up_format:
            p_col = "#334155"
            wave_gradient = "linear-gradient(135deg, #475569 0%, #64748b 100%)"
        elif "Classic Blue" in up_format:
            p_col = "#1e3a8a"
            wave_gradient = "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)"
        else: # Corporate Curve Wave (Default Professional)
            p_col = "#0f172a"
            wave_gradient = "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)"

        if "Dotted" in up_border: b_css = "2px dotted #1e293b"
        elif "Dashed" in up_border: b_css = "2px dashed #1e293b"
        elif "Double" in up_border: b_css = "4px double #1e293b"
        else: b_css = "1px solid #cbd5e1"

        init = get_initials(up_name)
        logo_html = f"<div style='width: 50px; height: 50px; background: {p_col}; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: bold; border-radius: 8px; font-size: 18px;'>{init}</div>"
        if up_custom_logo.strip():
            logo_html = f"<img src='{up_custom_logo}' style='max-height: 50px; max-width: 50px; object-fit: contain;' onerror=\"this.onerror=null; this.parentNode.innerHTML='<div style=\\'width: 50px; height: 50px; background: {p_col}; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: bold; border-radius: 8px; font-size: 18px;\\'>{init}</div>';\">"

        wm_text = up_name if up_watermark_type == "Company Name" else init
        wm_html = f'<div style="position: absolute; top: 40%; left: 20%; transform: rotate(-30deg); font-size: 90px; font-weight: bold; color: rgba(0, 0, 0, 0.04); z-index: 0; pointer-events: none; white-space: nowrap;">{wm_text}</div>' if up_watermark_enabled else ""

        full_a4_preview_html = f"""
        <!DOCTYPE html><html><head><meta charset="utf-8"><style>
            body {{ font-family: 'Helvetica', Arial, sans-serif; color: #1e293b; background: #e2e8f0; margin: 0; padding: 20px; }}
            .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 15mm 20mm; box-sizing: border-box; box-shadow: 0 0 20px rgba(0,0,0,0.15); border: {b_css}; position: relative; overflow: hidden; }}
            .wave-header {{ background: {wave_gradient}; color: #fff; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; position: relative; z-index: 1; border-bottom-left-radius: 30px; border-bottom-right-radius: 30px; }}
            .company-title {{ font-size: 24px; font-weight: bold; color: #ffffff; }}
            .invoice-title {{ font-size: 26px; font-weight: bold; text-transform: uppercase; color: #ffffff; text-align: right; }}
            .billing-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; border: 1px solid #cbd5e1; background: #f8fafc; position: relative; z-index: 1; }}
            .billing-table td {{ padding: 12px; vertical-align: top; width: 50%; font-size: 13px; border: 1px solid #cbd5e1; line-height: 1.5; }}
            .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; position: relative; z-index: 1; }}
            .items-table th {{ background-color: {p_col}; color: #fff; text-align: left; padding: 10px; font-size: 12px; border: 1px solid {p_col}; }}
            .items-table td {{ border: 1px solid #cbd5e1; padding: 10px; font-size: 12px; }}
            .right {{ text-align: right; }}
            .totals {{ width: 300px; margin-left: auto; font-size: 13px; margin-bottom: 40px; border: 1px solid #cbd5e1; border-collapse: collapse; position: relative; z-index: 1; }}
            .totals td {{ padding: 8px; border: 1px solid #cbd5e1; }}
            .grand-total {{ font-weight: bold; background: #eff6ff; font-size: 14px; color: {p_col}; }}
        </style></head><body><div class="a4-page">
            {wm_html}
            <div class="wave-header">
                <div style="display: flex; align-items: flex-start; gap: 15px;">
                    {logo_html}
                    <div>
                        <div class="company-title">{up_name}</div>
                        <div style="font-size: 12px; color: #e2e8f0; margin-top: 5px; line-height: 1.4;">{up_address}<br><strong>Contact:</strong> {up_contact}<br><strong>GSTIN:</strong> {up_gstin}</div>
                    </div>
                </div>
                <div><div class="invoice-title">Tax Invoice</div><div style="font-size: 12px; color: #e2e8f0; text-align: right; margin-top: 5px; line-height: 1.4;"><strong>Invoice No:</strong> TAX/2026-27/001<br><strong>Date:</strong> July 15, 2026</div></div>
            </div>
            <table class="billing-table"><tr><td><strong>Service Provider:</strong><br>{up_name}</td><td><strong>Billed To:</strong><br><strong>Sample Client Enterprises</strong><br>New Delhi</td></tr></table>
            <table class="items-table"><thead><tr><th style="width: 10%;">S.No.</th><th style="width: 55%;">Description</th><th style="width: 15%;">Mode</th><th class='right' style="width: 20%;">Amount (Rs.)</th></tr></thead><tbody><tr><td class='right'>1</td><td>Sample Item / Service</td><td>{up_nature}</td><td class='right'>700.00</td></tr></tbody></table>
            <table class="totals"><tr><td>Subtotal:</td><td class="right">Rs. 700.00</td></tr><tr><td>GST (18%):</td><td class="right">Rs. 126.00</td></tr><tr class="grand-total"><td>Total Amount:</td><td class="right">Rs. 826.00</td></tr></table>
            <div style="text-align: center; font-size: 11px; color: #64748b; position: relative; z-index: 1;">Thank you for your business! Theme: {up_format}</div>
        </div></body></html>
        """
        st.components.v1.html(full_a4_preview_html, height=800, scrolling=True)

    elif menu_option == "📊 Party-wise History & Edit/Delete (24 Days)":
        st.markdown("<div class='main-title'><h1>Party-wise Invoice Management & Editing</h1></div>", unsafe_allow_html=True)
        if not st.session_state.history: st.info("No invoice history available for the last 24 days.")
        else:
            all_parties = list(set([h['client'] for h in st.session_state.history]))
            sel_party = st.selectbox("Select Party to Manage History", all_parties)
            for bill in [h for h in st.session_state.history if h['client'] == sel_party]:
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

    else:
        # --- CREATE INVOICE TAB ---
        st.markdown(f"<div class='main-title'><h1>{user_data['profile']['name']}</h1><p>Invoice Mode: <b>{current_nature}</b> | Plan: <b>{user_data['subscription']}</b></p></div>", unsafe_allow_html=True)

        if user_data["subscription"] == "Trial" and user_data.get("bills_created", 0) >= 1:
            st.error("🚨 **Free Trial Limit Reached!** You have already generated 1 free invoice on your trial account.")
            st.warning("💳 **Subscribe to Pro Plan (Rs. 5/- only)**")
            st.markdown("Please scan / pay via UPI to: **`roshan@shreeservices.upi`**")
            
            with st.form("subscription_payment_form"):
                tx_id_input = st.text_input("Enter UPI Transaction Reference ID (UTR / Txn ID)")
                submit_tx = st.form_submit_button("Submit Payment for Activation")
                if submit_tx:
                    if tx_id_input.strip():
                        user_data["subscription"] = "Pending Approval"
                        save_saas_data(saas_db)
                        st.success("Transaction submitted successfully! Admin will review and activate your account shortly.")
                        st.rerun()
                    else:
                        st.warning("Please enter a valid Transaction ID.")
            st.stop()
        
        elif user_data["subscription"] == "Pending Approval":
            st.info("⏳ **Payment Verification Pending:** Your subscription payment is currently under review by the admin. Once verified, unlimited invoice creation will be unlocked.")
            st.stop()

        next_inv_num = len(st.session_state.history) + 1
        current_inv_no = f"TAX/2026-27/{next_inv_num:03d}"

        # 1. Party Management
        st.markdown('<div class="section-box-1">👤 1. Client / Party Details</div>', unsafe_allow_html=True)
        party_list = list(user_data["parties"].keys()) + ["+ Add New Party"]
        selected_party = st.selectbox("Select Party", party_list)

        if selected_party == "+ Add New Party":
            with st.form("new_party_form"):
                n_trade = st.text_input("Trade Name")
                n_legal = st.text_input("Legal Name")
                n_addr = st.text_input("Address")
                n_gstin = st.text_input("GSTIN")
                if st.form_submit_button("Save Party Permanently"):
                    if n_trade.strip():
                        user_data["parties"][n_trade.strip()] = {"legal": n_legal, "address": n_addr, "gstin": n_gstin}
                        save_saas_data(saas_db)
                        st.success("Party Saved Successfully!")
                        st.rerun()
                    else: st.warning("Please enter Trade Name.")

        st.markdown('<div class="section-box-2">📋 2. Invoice Meta Details</div>', unsafe_allow_html=True)
        col_i1, col_i2 = st.columns(2)
        inv_no = col_i1.text_input("Invoice Number", current_inv_no)
        inv_date = col_i2.text_input("Invoice Date", datetime.now().strftime("%B %d, %Y"))

        # 2. Dynamic Tally-Style Grid Entry based on 4 Natures
        st.markdown(f'<div class="section-box-3">💼 3. Items & Grid Entry ({current_nature})</div>', unsafe_allow_html=True)
        if st.button("➕ Add Row"): 
            st.session_state.inv_rows.append({"desc": "", "hsn": "", "unit": "NOS", "qty": 1.0, "rate": 0.0, "tax_type": "Taxable", "tax_pct": 18.0, "amt": 0.0, "lr_no": "", "vehicle": "", "route": ""})

        subtotal_amt = 0.0
        total_tax_amt = 0.0
        cgst_amt = 0.0
        sgst_amt = 0.0
        igst_amt = 0.0

        for i, row in enumerate(st.session_state.inv_rows):
            st.markdown(f"**Row {i+1}**")
            if current_nature == "Goods / Manufacturing / Trading":
                c1, c2, c3, c4, c5, c6, c7 = st.columns([3, 2, 1.5, 1.5, 2, 2, 2])
                row['desc'] = c1.text_input("Item Name", value=row['desc'], key=f"d_{i}")
                row['hsn'] = c2.text_input("HSN", value=row['hsn'], key=f"h_{i}")
                row['unit'] = c3.selectbox("Unit", ["NOS", "Box", "Pcs", "Kgs", "Units"], key=f"u_{i}")
                row['qty'] = c4.number_input("Qty", value=row['qty'], key=f"q_{i}")
                row['rate'] = c5.number_input("Rate", value=row['rate'], key=f"r_{i}")
                row['tax_type'] = c6.selectbox("Tax Type", ["Taxable", "Nil Rated"], key=f"tt_{i}")
                row['tax_pct'] = c7.selectbox("Tax %", [0.0, 5.0, 12.0, 18.0, 28.0], index=3, key=f"tp_{i}")
                
                base_amt = row['qty'] * row['rate']
                row['amt'] = base_amt
                subtotal_amt += base_amt
                if row['tax_type'] == "Taxable":
                    total_tax_amt += base_amt * (row['tax_pct'] / 100.0)

            elif current_nature == "Services":
                c1, c2, c3, c4 = st.columns([4, 2, 2, 2])
                row['desc'] = c1.text_input("Service Description", value=row['desc'], key=f"sd_{i}")
                row['tax_type'] = c2.selectbox("Tax Type", ["Taxable", "Nil Rated"], key=f"stt_{i}")
                row['tax_pct'] = c3.selectbox("Tax %", [0.0, 5.0, 12.0, 18.0, 28.0], index=3, key=f"stp_{i}")
                row['amt'] = c4.number_input("Amount", value=row['amt'], key=f"sa_{i}")
                
                subtotal_amt += row['amt']
                if row['tax_type'] == "Taxable":
                    total_tax_amt += row['amt'] * (row['tax_pct'] / 100.0)

            elif current_nature == "Transport Company":
                c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 2])
                row['lr_no'] = c1.text_input("LR No", value=row['lr_no'], key=f"lr_{i}")
                row['vehicle'] = c2.text_input("Vehicle No", value=row['vehicle'], key=f"vh_{i}")
                row['route'] = c3.text_input("From -> To", value=row['route'], key=f"rt_{i}")
                row['desc'] = c4.text_input("Goods Desc", value=row['desc'], key=f"td_{i}")
                row['amt'] = c5.number_input("Freight Amt", value=row['amt'], key=f"ta_{i}")
                subtotal_amt += row['amt']

            else: # Other Business
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
                cgst_amt = total_tax_amt / 2.0
                sgst_amt = total_tax_amt / 2.0
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

            sel_theme = user_data["profile"].get("format", format_options[0])
            if "Emerald Green" in sel_theme:
                p_col = "#065f46"
                wave_gradient = "linear-gradient(135deg, #059669 0%, #10b981 100%)"
            elif "Sunset Orange" in sel_theme:
                p_col = "#c2410c"
                wave_gradient = "linear-gradient(135deg, #ea580c 0%, #fb923c 100%)"
            elif "Royal Purple" in sel_theme:
                p_col = "#581c87"
                wave_gradient = "linear-gradient(135deg, #7e22ce 0%, #a855f7 100%)"
            elif "Minimalist Clean" in sel_theme:
                p_col = "#334155"
                wave_gradient = "linear-gradient(135deg, #475569 0%, #64748b 100%)"
            elif "Classic Blue" in sel_theme:
                p_col = "#1e3a8a"
                wave_gradient = "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)"
            else:
                p_col = "#0f172a"
                wave_gradient = "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)"

            sel_border = user_data["profile"].get("border_style", "Solid Line")
            if "Dotted" in sel_border: b_css = "2px dotted #1e293b"
            elif "Dashed" in sel_border: b_css = "2px dashed #1e293b"
            elif "Double" in sel_border: b_css = "4px double #1e293b"
            else: b_css = "1px solid #cbd5e1"

            comp_name_val = user_data["profile"].get("name", "Company")
            custom_logo_val = user_data["profile"].get("custom_logo", "")
            init = get_initials(comp_name_val)
            
            l_html = f"<div style='width:50px;height:50px;background:{p_col};color:#fff;display:flex;align-items:center;justify-content:center;font-weight:bold;border-radius:8px;'>{init}</div>"
            if custom_logo_val.strip():
                l_html = f"<img src='{custom_logo_val}' style='max-height:50px;max-width:50px; object-fit:contain;' onerror=\"this.onerror=null; this.parentNode.innerHTML='<div style=\\'width: 50px; height: 50px; background: {p_col}; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: bold; border-radius: 8px; font-size: 18px;\\'>{init}</div>';\">"

            wm_en = user_data["profile"].get("watermark_enabled", True)
            wm_tp = user_data["profile"].get("watermark_type", "Company Name")
            wm_text = comp_name_val if wm_tp == "Company Name" else init
            wm_html = f'<div style="position: absolute; top: 40%; left: 20%; transform: rotate(-30deg); font-size: 90px; font-weight: bold; color: rgba(0, 0, 0, 0.04); z-index: 0; pointer-events: none; white-space: nowrap;">{wm_text}</div>' if wm_en else ""

            table_headers = ""
            table_rows = ""
            if current_nature == "Goods / Manufacturing / Trading":
                table_headers = "<th>S.No.</th><th>Item Description</th><th>HSN</th><th>Unit</th><th>Qty</th><th>Rate</th><th>Tax Type</th><th class='right'>Amount (Rs.)</th>"
                for i, row in enumerate(st.session_state.inv_rows, 1):
                    table_rows += f"<tr><td class='right'>{i}</td><td>{row['desc']}</td><td>{row['hsn']}</td><td>{row['unit']}</td><td>{row['qty']}</td><td>{row['rate']:.2f}</td><td>{row['tax_type']} ({row['tax_pct']}%)</td><td class='right'>{row['amt']:.2f}</td></tr>"
            elif current_nature == "Services":
                table_headers = "<th>S.No.</th><th>Service Description</th><th>Tax Type</th><th class='right'>Amount (Rs.)</th>"
                for i, row in enumerate(st.session_state.inv_rows, 1):
                    table_rows += f"<tr><td class='right'>{i}</td><td>{row['desc']}</td><td>{row['tax_type']} ({row['tax_pct']}%)</td><td class='right'>{row['amt']:.2f}</td></tr>"
            elif current_nature == "Transport Company":
                table_headers = "<th>S.No.</th><th>LR No</th><th>Vehicle No</th><th>Route (From -> To)</th><th>Goods Desc</th><th class='right'>Freight (Rs.)</th>"
                for i, row in enumerate(st.session_state.inv_rows, 1):
                    table_rows += f"<tr><td class='right'>{i}</td><td>{row['lr_no']}</td><td>{row['vehicle']}</td><td>{row['route']}</td><td>{row['desc']}</td><td class='right'>{row['amt']:.2f}</td></tr>"
            else:
                table_headers = "<th>S.No.</th><th>Description</th><th>Tax %</th><th class='right'>Amount (Rs.)</th>"
                for i, row in enumerate(st.session_state.inv_rows, 1):
                    table_rows += f"<tr><td class='right'>{i}</td><td>{row['desc']}</td><td>{row['tax_pct']}%</td><td class='right'>{row['amt']:.2f}</td></tr>"

            html_content = f"""
            <!DOCTYPE html><html><head><meta charset="utf-8"><style>
                body {{ font-family: Helvetica, Arial; color: #1e293b; background: #e2e8f0; padding: 20px; }}
                .a4-page {{ width: 210mm; min-height: 297mm; margin: auto; background: #fff; padding: 15mm 20mm; box-sizing: border-box; border: {b_css}; position: relative; overflow: hidden; }}
                .wave-header {{ background: {wave_gradient}; color: #fff; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; position: relative; z-index: 1; border-bottom-left-radius: 30px; border-bottom-right-radius: 30px; }}
                .company-title {{ font-size: 24px; font-weight: bold; color: #ffffff; }}
                .invoice-title {{ font-size: 26px; font-weight: bold; text-transform: uppercase; color: #ffffff; text-align: right; }}
                .billing-table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; border: 1px solid #cbd5e1; background: #f8fafc; position: relative; z-index: 1; }}
                .billing-table td {{ padding: 12px; vertical-align: top; width: 50%; font-size: 13px; border: 1px solid #cbd5e1; line-height: 1.5; }}
                .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; position: relative; z-index: 1; }}
                .items-table th {{ background-color: {p_col}; color: #fff; padding: 10px; font-size: 12px; text-align: left; border: 1px solid {p_col}; }}
                .items-table td {{ border: 1px solid #cbd5e1; padding: 10px; font-size: 12px; }}
                .right {{ text-align: right; }}
                .totals {{ width: 340px; margin-left: auto; font-size: 13px; border-collapse: collapse; position: relative; z-index: 1; }}
                .totals td {{ padding: 8px; border: 1px solid #cbd5e1; }}
                .grand-total {{ font-weight: bold; background: #eff6ff; color: {p_col}; }}
                @media print {{ body {{ background: none; padding: 0; }} .no-print {{ display: none !important; }} }}
            </style></head><body>
            <div class="no-print" style="text-align: center; margin-bottom: 20px;"><button onclick="window.print()" style="background:#059669;color:white;padding:12px 25px;font-weight:bold;border:none;border-radius:8px;cursor:pointer;">🖨️ Print / Save PDF Directly</button></div>
            <div class="a4-page">
                {wm_html}
                <div class="wave-header">
                    <div style="display:flex;gap:15px; align-items:flex-start;">{l_html}<div><h2 style="margin:0;color:#ffffff;">{user_data['profile']['name']}</h2><p style="margin:3px 0;font-size:12px;color:#e2e8f0;">{user_data['profile']['address']}<br>Contact: {user_data['profile']['contact']}<br>GSTIN: {user_data['profile']['gstin']}</p></div></div>
                    <div style="text-align:right;"><h2 style="margin:0;color:#ffffff;">Tax Invoice</h2><p style="margin:3px 0;font-size:12px;color:#e2e8f0;">Invoice No: {inv_no}<br>Date: {inv_date}<br>Mode: {current_nature}</p></div>
                </div>
                <table style="width:100%;border-collapse:collapse;margin-bottom:20px;font-size:13px;position:relative;z-index:1;"><tr><td style="border:1px solid #cbd5e1;padding:10px;"><strong>Service Provider:</strong><br>{user_data['profile']['name']}</td><td style="border:1px solid #cbd5e1;padding:10px;"><strong>Billed To:</strong><br><strong>{target_party}</strong><br>Address: {p_info.get('address')}<br>GSTIN: {p_info.get('gstin')}</td></tr></table>
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

