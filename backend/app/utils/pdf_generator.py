from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_invoice_pdf(
    filename,
    invoice,
    customer,
    items
):
    c = canvas.Canvas(
        filename,
        pagesize=letter
    )

    y = 750

    c.setFont("Helvetica-Bold", 18)
    c.drawString(
        50,
        y,
        "Inventory Management System"
    )

    y -= 40

    c.setFont("Helvetica", 12)

    c.drawString(
        50,
        y,
        f"Invoice No: {invoice.invoice_number}"
    )

    y -= 20

    c.drawString(
        50,
        y,
        f"Customer: {customer.name}"
    )

    y -= 40

    c.drawString(
        50,
        y,
        "Product"
    )

    c.drawString(
        250,
        y,
        "Qty"
    )

    c.drawString(
        350,
        y,
        "Price"
    )

    y -= 20

    for item in items:

        c.drawString(
            50,
            y,
            item["product_name"]
        )

        c.drawString(
            250,
            y,
            str(item["quantity"])
        )

        c.drawString(
            350,
            y,
            str(item["price"])
        )

        y -= 20

    y -= 30

    c.drawString(
        50,
        y,
        f"Subtotal: ₹{invoice.subtotal}"
    )

    y -= 20

    c.drawString(
        50,
        y,
        f"GST: ₹{invoice.gst}"
    )

    y -= 20

    c.drawString(
        50,
        y,
        f"Total: ₹{invoice.total}"
    )

    c.save()