import streamlit as st
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="Invoice Generator - Roshan Mishra", layout="centered")

st.title("📄 Professional Invoice Generator & Portal")
st.write("Tally-style Party Master & PDF Direct Download ke sath invoice generate karein.")

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

    submitted = st.form_submit_button("Generate Invoice PDF")

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

    # --- Generate Real PDF using FPDF ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(190, 10, "TAX INVOICE", ln=True, align="Right")
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(100, 6, "Roshan Mishra", ln=False)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(90, 6, f"Invoice No: {inv_no}", ln=True, align="Right")
    
    pdf.cell(100, 5, "Plot no 64 & 65, Block K-5, Mohan Garden, New Delhi - 110059", ln=False)
    pdf.cell(90, 5, f"Date: {inv_date}", ln=True, align="Right")
    pdf.cell(100, 5, "Contact: 7888273972", ln=False)
    pdf.cell(90, 5, f"GSTIN: {client_gstin}", ln=True, align="Right")
    
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(95, 6, "Billed To:", ln=False)
    pdf.cell(95, 6, "Service Provider:", ln=True)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(95, 5, f"Trade Name: {client_name}", ln=False)
    pdf.cell(95, 5, "Roshan Mishra (Accountant)", ln=True)
    pdf.cell(95, 5, f"Legal Name: {client_legal}", ln=False)
    pdf.cell(95, 5, "Plot no 64 & 65, Block K-5,", ln=True)
    pdf.cell(95, 5, f"Address: {client_address}", ln=False)
    pdf.cell(95, 5, "Mohan Garden, New Delhi - 110059", ln=True)
    
    pdf.ln(10)
    # Table Header
    pdf.set_fill_color(26, 54, 93)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(15, 8, "S.No.", 1, 0, "C", True)
    pdf.cell(95, 8, "Description of Services", 1, 0, "L", True)
    pdf.cell(40, 8, "Period", 1, 0, "C", True)
    pdf.cell(40, 8, "Amount (Rs.)", 1, 1, "R", True)
    
    # Table Rows
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 10)
    for idx, (desc, period, amt) in enumerate(items, 1):
        pdf.cell(15, 7, str(idx), 1, 0, "C")
        pdf.cell(95, 7, desc, 1, 0, "L")
        pdf.cell(40, 7, period, 1, 0, "C")
        pdf.cell(40, 7, f"{amt:.2f}", 1, 1, "R")
        
    pdf.ln(5)
    pdf.cell(110, 6, "", ln=False)
    pdf.cell(40, 6, "Total Amount:", ln=False)
    pdf.cell(40, 6, f"Rs. {total_amt:.2f}", ln=True, align="R")
    
    pdf.cell(110, 6, "", ln=False)
    pdf.cell(40, 6, "Total Paid:", ln=False)
    pdf.cell(40, 6, f"Rs. {total_paid:.2f}", ln=True, align="R")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(110, 8, "", ln=False)
    pdf.cell(40, 8, "Balance Due:", ln=False)
    pdf.cell(40, 8, f"Rs. {balance:.2f}", ln=True, align="R")
    
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(150, 5, "", ln=False)
    pdf.cell(40, 5, "For Roshan Mishra", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(150, 5, "", ln=False)
    pdf.cell(40, 5, "Authorised Signatory", ln=True, align="C")

    pdf_bytes = pdf.output()

    st.success("Invoice PDF generated successfully!")
    st.download_button(
        label="📥 Download Official PDF Invoice",
        data=pdf_bytes,
        file_name=f"Invoice_{client_name.replace(' ', '_')}_{inv_no.replace('/', '-')}.pdf",
        mime="application/pdf"
    )

if st.session_state.history:
    st.markdown("---")
    st.subheader("📊 Recent Generated Invoices History")
    for i, h in enumerate(reversed(st.session_state.history)):
        st.write(f"🔹 **{h['invoice_no']}** | Party: **{h['client']}** | Total: Rs. {h['total']} | Paid: Rs. {h['paid']} | Balance: Rs. {h['balance']}")
