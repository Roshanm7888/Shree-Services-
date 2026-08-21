import streamlit as st
import base64
from datetime import datetime

st.set_page_config(page_title="Invoice Generator - Roshan Mishra", layout="centered")

st.title("📄 Professional Invoice Generator & Portal")
st.write("Tally-style Party Master & Preview ke sath professional invoice generate karein.")

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

with st.form("invoice_form"):
    st.subheader("1. Client / Party Details")
    party_names = list(st.session_state.saved_parties.keys())
    selected_party = st.selectbox("Select Existing Party", party_names)

    st.markdown("---")
    st.markdown("### ➕ Nayi Party Add Karein (Agar list mein na ho)")
    new_trade_name = st.text_input("New Party Trade Name", "")
    new_legal_name = st.text_input("New Client Legal Name", "")
    new_address = st.text_input("New Client Address", "")
    new_gstin = st.text_input("New Client GSTIN", "")

    st.subheader("2. Invoice Details")
    current_inv_no = f"TAX/2026-27/{st.session_state.invoice_count:03d}"
    inv_no = st.text_input("Invoice Number (Auto-generated)", current_inv_no)
    inv_date = st.text_input("Invoice Date", datetime.now().strftime("%B %d, %Y"))

    st.subheader("3. Select Services & Add Amount")
    selected_services = st.multiselect("Select Services from Library", st.session_state.saved_services, default=["GST"])
    new_service_input = st.text_input("Add New Service (Agar upar list mein na ho)", "")
    
    st.markdown("💡 *Format: Service Name | Period | Amount (Jaise: GST Filing | July | 700)*")
    default_text = "\n".join([f"{s} | July | 700" for s in selected_services])
    services_text = st.text_area("Services Details", default_text)

    total_paid = st.number_input("Total Amount Paid (Rs.)", min_value=0.0, value=0.0)

    submitted = st.form_submit_button("Generate Invoice Preview & Download")

if submitted:
    if new_trade_name.strip():
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
        "date": inv_date
    })

    st.session_state.invoice_count += 1

    # --- Clean HTML Preview Format ---
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: 'Helvetica', Arial, sans-serif; color: #2c3e50; padding: 20px; background: #fff; }}
        .invoice-container {{ max-width: 700px; margin: auto; border: 1px solid #ddd; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.05); }}
        .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #1a365d; padding-bottom: 15px; margin-bottom: 20px; }}
        .company-title {{ font-size: 20px; font-weight: bold; color: #1a365d; }}
        .invoice-title {{ font-size: 22px; font-weight: bold; text-transform: uppercase; color: #2c3e50; text-align: right; }}
        .billing-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; background: #f8fafc; }}
        .billing-table td {{ padding: 10px; vertical-align: top; width: 50%; font-size: 13px; }}
        .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        .items-table th {{ background-color: #1a365d; color: #fff; text-align: left; padding: 8px; font-size: 12px; }}
        .items-table td {{ border-bottom: 1px solid #e2e8f0; padding: 8px; font-size: 12px; }}
        .right {{ text-align: right; }}
        .totals {{ width: 260px; margin-left: auto; font-size: 13px; margin-bottom: 40px; }}
        .totals td {{ padding: 5px; border-bottom: 1px solid #e2e8f0; }}
        .grand-total {{ font-weight: bold; background: #f1f5f9; font-size: 14px; border-top: 2px solid #1a365d; border-bottom: 2px solid #1a365d; }}
        .sign-area {{ float: right; text-align: right; margin-top: 20px; font-size: 13px; }}
        .sign-line {{ border-top: 1px solid #000; width: 180px; margin-top: 40px; text-align: center; font-weight: bold; }}
    </style>
    </head>
    <body>
    <div class="invoice-container">
        <div class="header">
            <div>
                <div class="company-title">Roshan Mishra</div>
                <div style="font-size: 12px; color: #555; margin-top: 5px;">
                    Plot no 64 & 65, Block K-5<br>
                    Mohan Garden, New Delhi - 110059<br>
                    <strong>Contact:</strong> 7888273972
                </div>
            </div>
            <div>
                <div class="invoice-title">Tax Invoice</div>
                <div style="font-size: 12px; color: #555; text-align: right; margin-top: 5px;">
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
                    <th>S.No.</th>
                    <th>Description of Services</th>
                    <th>Period</th>
                    <th class="right">Amount (Rs.)</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for idx, (desc, period, amt) in enumerate(items, 1):
        html_content += "<tr><td>{}</td><td>{}</td><td>{}</td><td class='right'>{:.2f}</td></tr>".format(idx, desc, period, amt)

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
        <hr style="border:none; border-top:1px solid #ddd; margin-top: 30px;">
        <div style="text-align: center; font-size: 11px; color: #777;">Thank you for your business! This is a computer-generated invoice.</div>
    </div>
    </body>
    </html>
    """.format(total_amt, total_paid, balance)

    st.success("Invoice generated successfully! Preview below:")
    st.components.v1.html(html_content, height=650, scrolling=True)

    b64 = base64.b64encode(html_content.encode('utf-8')).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64,{b64}" download="Invoice_{client_name.replace(" ", "_")}_{inv_no.replace("/", "-")}.html" style="display:inline-block; padding:10px 20px; background-color:#1a365d; color:white; text-decoration:none; border-radius:5px; font-weight:bold; margin-top:20px;">📥 Download Invoice File</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.info("💡 Tip: Downloaded file ko open karke aap browser se seedha Print ya Save as PDF kar sakte hain!")

if st.session_state.history:
    st.markdown("---")
    st.subheader("📊 Recent Generated Invoices History")
    for i, h in enumerate(reversed(st.session_state.history)):
        st.write(f"🔹 **{h['invoice_no']}** | Party: **{h['client']}** | Total: Rs. {h['total']} | Paid: Rs. {h['paid']} | Balance: Rs. {h['balance']}")
