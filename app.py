import streamlit as st
from weasyprint import HTML
import tempfile
import os

st.set_page_config(page_title="Invoice Generator - Roshan Mishra", layout="centered")

st.title("📄 Professional Invoice Generator")
st.write("Apni party ki details aur services bhar kar instant PDF invoice download karein.")

with st.form("invoice_form"):
    st.subheader("1. Client (Party) Details")
    client_trade_name = st.text_input("Client Trade Name (e.g., RKMK Enterprises)", "RKMK Enterprises")
    client_legal_name = st.text_input("Client Legal Name", "Rinky Acharya")
    client_address = st.text_input("Client Address", "Flat No. 34, Ground Floor, Block P Extn, Mohan Garden, New Delhi - 110059")
    client_gstin = st.text_input("Client GSTIN", "07DEOPA0606H1ZU")

    st.subheader("2. Invoice Meta Details")
    invoice_no = st.text_input("Invoice Number", "TAX/2026-27/001")
    invoice_date = st.text_input("Invoice Date", "August 21, 2026")

    st.subheader("3. Billing Items (Services & Amounts)")
    st.write("Yahan aap items add kar sakte hain (Comma separated ya basic rows ke roop mein)")
    
    # Simple dynamic rows representation via text area for ease, or standard items
    # For quick entry: Item Name, Period, Amount
    item_desc_1 = st.text_input("Item 1 Description", "GST Filing Charges")
    item_period_1 = st.text_input("Item 1 Period/Details", "November")
    item_amount_1 = st.number_format_val = st.number_input("Item 1 Amount (₹)", value=700.0)

    item_desc_2 = st.text_input("Item 2 Description", "Udyam Registration")
    item_period_2 = st.text_input("Item 2 Period/Details", "One-time")
    item_amount_2 = st.number_input("Item 2 Amount (₹)", value=200.0)

    item_desc_3 = st.text_input("Item 3 Description", "GST Filing Charges")
    item_period_3 = st.text_input("Item 3 Period/Details", "December")
    item_amount_3 = st.number_input("Item 3 Amount (₹)", value=700.0)

    st.subheader("4. Payment Summary")
    total_paid = st.number_input("Total Amount Paid (₹)", value=2000.0)

    submitted = st.form_submit_button("Generate & Download PDF Invoice")

if submitted:
    # Calculations
    items = [
        (item_desc_1, item_period_1, item_amount_1),
        (item_desc_2, item_period_2, item_amount_2),
        (item_desc_3, item_period_3, item_amount_3),
    ]
    total_amount = sum([amt for _, _, amt in items])
    balance_pending = total_amount - total_paid

    # HTML Template generation
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @page {{ size: A4; margin: 10mm; }}
        body {{ font-family: 'Helvetica', Arial, sans-serif; color: #2c3e50; line-height: 1.2; margin: 0; padding: 0; font-size: 11px; }}
        .invoice-container {{ max-width: 800px; margin: auto; }}
        .header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
        .company-title {{ font-size: 18px; font-weight: bold; color: #1a365d; }}
        .invoice-title {{ font-size: 20px; font-weight: bold; color: #2c3e50; text-align: right; text-transform: uppercase; }}
        .billing-section {{ width: 100%; border-collapse: collapse; margin: 10px 0; background: #f8fafc; border: 1px solid #e2e8f0; }}
        .billing-section td {{ padding: 8px; vertical-align: top; width: 50%; }}
        .section-title {{ font-weight: bold; color: #1a365d; margin-bottom: 2px; font-size: 11px; text-transform: uppercase; border-bottom: 1px solid #cbd5e1; }}
        .items-table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        .items-table th {{ background-color: #1a365d; color: #ffffff; text-align: left; padding: 6px; font-size: 11px; }}
        .items-table td {{ border-bottom: 1px solid #e2e8f0; padding: 6px; font-size: 11px; }}
        .totals-table {{ width: 250px; margin-left: auto; border-collapse: collapse; margin-top: 5px; }}
        .totals-table td {{ padding: 4px; font-size: 11px; }}
        .grand-total {{ font-weight: bold; background: #f1f5f9; border-top: 1px solid #1a365d; border-bottom: 1px solid #1a365d; }}
        .signature-line {{ border-top: 1px solid #000; width: 200px; margin-top: 40px; text-align: center; font-weight: bold; float: right; }}
        .footer {{ margin-top: 20px; text-align: center; font-size: 10px; color: #718096; border-top: 1px solid #e2e8f0; padding-top: 5px; }}
    </style>
    </head>
    <body>
    <div class="invoice-container">
        <table class="header-table">
            <tr>
                <td>
                    <div class="company-title">Roshan Mishra</div>
                    <div style="font-size: 10px;">Plot no 64 & 65, Block K-5, Near Star Shine Public School, Mohan Garden, New Delhi - 110059<br><strong>Contact:</strong> 7888273972</div>
                </td>
                <td>
                    <div class="invoice-title">Tax Invoice</div>
                    <div style="text-align: right; font-size: 10px;"><strong>Invoice No:</strong> {invoice_no}<br><strong>Date:</strong> {invoice_date}<br><strong>GSTIN:</strong> {client_gstin}</div>
                </td>
            </tr>
        </table>
        <table class="billing-section">
            <tr>
                <td>
                    <div class="section-title">Service Provider</div>
                    <strong>Accountant:</strong> Roshan Mishra<br>Plot no 64 & 65, Block K-5, Mohan Garden, New Delhi - 110059
                </td>
                <td>
                    <div class="section-title">Billed To</div>
                    <strong>{client_trade_name}</strong><br><strong>Legal Name:</strong> {client_legal_name}<br><strong>Address:</strong> {client_address}
                </td>
            </tr>
        </table>
        <table class="items-table">
            <thead><tr><th>S.No.</th><th>Description</th><th>Period</th><th>Amount (₹)</th></tr></thead>
            <tbody>
    """
    
    for idx, (desc, period, amt) in enumerate(items, 1):
        html_content += f"<tr><td>{idx}</td><td>{desc}</td><td>{period}</td><td>{amt:.2f}</td></tr>"

    html_content += f"""
            </tbody>
        </table>
        <table class="totals-table">
            <tr><td>Total:</td><td style="text-align:right;">₹{total_amount:.2f}</td></tr>
            <tr><td>Paid:</td><td style="text-align:right;">₹{total_paid:.2f}</td></tr>
            <tr class="grand-total"><td>Balance:</td><td style="text-align:right;">₹{balance_pending:.2f}</td></tr>
        </table>
        <div class="signature-line">Authorised Signatory</div>
        <div style="clear:both;"></div>
        <div class="footer">Thank you for your business! This is a computer-generated tax invoice.</div>
    </div>
    </body>
    </html>
    """

    # Create temporary PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        HTML(string=html_content).write_pdf(tmp.name)
        pdf_path = tmp.name

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    st.success("Invoice successfully generated!")
    st.download_button(
        label="📥 Download Invoice PDF",
        data=pdf_bytes,
        file_name=f"Invoice_{client_trade_name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
