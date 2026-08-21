import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Shree Services - Invoice Portal", page_icon="📄", layout="centered")

# --- Colorful & Modern UI CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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

    /* Form Card Container Styling */
    div[data-testid="stForm"] {
        background: #ffffff;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }

    /* Colorful Section Headings / Banners inside form */
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

    /* Main Submit Button */
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

st.markdown("""
    <div class="main-title">
        <h1>Shree Services & Tax Portal</h1>
        <p>Professional Tally-Style Invoice & Billing System</p>
    </div>
""", unsafe_allow_html=True)

# --- Session States Initialization ---
if "invoice_count" not in st.session_state:
    st.session_state.invoice_count = 1
if "history" not in st.session_state:
    st.session_state.history = []

if "saved_parties" not in st.session_state:
    st.session_state.saved_parties = {
        "RKMK Enterprises": {
            "legal": "Rinky Acharya",
            "address": "Flat No. 34, Ground Floor, Block P Extn, Mohan Garden, New Delhi - 110059",
            "gstin": "07DEOPA0606H1ZU"
        },
        "Chandra Enterprises": {
            "legal": "Manoj Kumar",
            "address": "2nd Floor Front Side, Left Side L Type, N Block Extn, Plot No.1 Mohan Garden, DK Road, New Delhi",
            "gstin": "07AMSPK3043R1ZC"
        }
    }

if "saved_services" not in st.session_state:
    st.session_state.saved_services = [
        "ITR",
        "GST",
        "GST REGISTRATION",
        "UDYAM",
        "SHOP ACT"
    ]

# Edit Mode State Handlers
if "edit_party" not in st.session_state:
    st.session_state.edit_party = ""
if "edit_services" not in st.session_state:
    st.session_state.edit_services = "GST | July | 700"
if "edit_paid" not in st.session_state:
    st.session_state.edit_paid = 0.0

with st.form("invoice_form"):
    # Section 1: Client Details
    st.markdown('<div class="section-box-1">👤 1. Client / Party Details</div>', unsafe_allow_html=True)
    party_names = list(st.session_state.saved_parties.keys())
    
    default_party_idx = 0
    if st.session_state.edit_party in party_names:
        default_party_idx = party_names.index(st.session_state.edit_party)

    selected_party = st.selectbox("Select Existing Party", party_names, index=default_party_idx)

    # Collapsible Expander inside Form for Adding New Party
    with st.expander("➕ Click Here to Add New Party"):
        new_trade_name = st.text_input("New Party Trade Name", "")
        new_legal_name = st.text_input("New Client Legal Name", "")
        new_address = st.text_input("New Client Address", "")
        new_gstin = st.text_input("New Client GSTIN", "")

    # Section 2: Invoice Details
    st.markdown('<div class="section-box-2">📋 2. Invoice Details</div>', unsafe_allow_html=True)
    current_inv_no = f"TAX/2026-27/{st.session_state.invoice_count:03d}"
    inv_no = st.text_input("Invoice Number (Auto-generated)", current_inv_no)
    inv_date = st.text_input("Invoice Date", datetime.now().strftime("%B %d, %Y"))

    # Section 3: Services & Pricing
    st.markdown('<div class="section-box-3">💼 3. Select Services & Add Amount</div>', unsafe_allow_html=True)
    selected_services = st.multiselect("Select Services from Library", st.session_state.saved_services, default=["GST"])
    new_service_input = st.text_input("Add New Service (Agar upar list mein na ho)", "")
    
    st.markdown("💡 *Format: Service Name | Period | Amount (Jaise: GST Filing | July | 700)*")
    services_text = st.text_area("Services Details", value=st.session_state.edit_services)

    total_paid = st.number_input("Total Amount Paid (Rs.)", min_value=0.0, value=st.session_state.edit_paid)

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

    st.session_state.history.append({
        "invoice_no": inv_no,
        "client": client_name,
        "total": total_amt,
        "paid": total_paid,
        "balance": balance,
        "date": inv_date,
        "services": services_text
    })

    st.session_state.invoice_count += 1
    st.session_state.edit_party = ""
    st.session_state.edit_services = "GST | July | 700"
    st.session_state.edit_paid = 0.0

    # --- Perfect A4 Layout HTML & CSS with Built-in Print Button ---
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
                <div class="company-title">Roshan Mishra</div>
                <div style="font-size: 12px; color: #475569; margin-top: 5px; line-height: 1.4;">
                    Plot no 64 & 65, Block K-5<br>
                    Mohan Garden, New Delhi - 110059<br>
                    <strong>Contact:</strong> 7888273972
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
                    Roshan Mishra (Accountant)<br>
                    Plot no 64 & 65, Block K-5, Mohan Garden, New Delhi - 110059
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

    html_content += """
            </tbody>
        </table>

        <table class="totals">
            <tr><td>Total Amount:</td><td class="right">Rs. {:.2f}</td></tr>
            <tr><td>Total Paid:</td><td class="right">Rs. {:.2f}</td></tr>
            <tr class="grand-total"><td>Balance Due:</td><td class="right">Rs. {:.2f}</td></tr>
        </table>

        <div style="clear: both;"></div>
        <div class="sign-area">
            For <strong>Roshan Mishra</strong>
            <div class="sign-line">Authorised Signatory</div>
        </div>
        <div style="clear: both;"></div>
        <hr style="border:none; border-top:1px solid #cbd5e1; margin-top: 40px;">
        <div style="text-align: center; font-size: 11px; color: #64748b;">Thank you for your business! This is a computer-generated invoice.</div>
    </div>
    </body>
    </html>
    """.format(total_amt, total_paid, balance)

    st.success("✨ Invoice Generated Successfully! Preview below:")
    st.components.v1.html(html_content, height=800, scrolling=True)

# --- Recent History with Edit Option ---
if st.session_state.history:
    st.markdown("---")
    st.markdown("### 📊 Recent Generated Invoices History & Edit")
    for i, h in enumerate(reversed(st.session_state.history)):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.info(f"🔹 **{h['invoice_no']}** | Party: **{h['client']}** | Total: Rs. {h['total']} | Paid: Rs. {h['paid']} | Balance: Rs. {h['balance']}")
        with col2:
            if st.button("✏️ Edit", key=f"edit_{i}"):
                st.session_state.edit_party = h['client']
                st.session_state.edit_services = h.get('services', 'GST | July | 700')
                st.session_state.edit_paid = h['paid']
                st.rerun()
