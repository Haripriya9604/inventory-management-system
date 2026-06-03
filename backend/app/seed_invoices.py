from random import randint, sample

from app.database.connection import SessionLocal

from app.models.customer import Customer
from app.models.product import Product
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.supplier import Supplier

db = SessionLocal()

customers = db.query(Customer).all()
products = db.query(Product).all()

if not customers:
    print("No customers found.")
    exit()

if not products:
    print("No products found.")
    exit()

created_invoices = 0

for _ in range(25):

    customer = customers[randint(0, len(customers) - 1)]

    available_products = [
        p for p in products
        if p.quantity > 0
    ]

    if not available_products:
        print("All products out of stock.")
        break

    selected_products = sample(
        available_products,
        min(randint(1, 3), len(available_products))
    )

    subtotal = 0
    invoice_items_data = []

    for product in selected_products:

        max_qty = min(product.quantity, 5)

        if max_qty <= 0:
            continue

        quantity = randint(1, max_qty)

        amount = product.selling_price * quantity

        subtotal += amount

        invoice_items_data.append(
            {
                "product": product,
                "quantity": quantity,
                "price": product.selling_price,
                "amount": amount
            }
        )

    if not invoice_items_data:
        continue

    gst = subtotal * 0.18
    total = subtotal + gst

    invoice = Invoice(
        invoice_number=1000 + (
            db.query(Invoice).count() + 1
        ),
        customer_id=customer.id,
        subtotal=subtotal,
        gst=gst,
        total=total
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    for item in invoice_items_data:

        invoice_item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item["product"].id,
            quantity=item["quantity"],
            price=item["price"],
            amount=item["amount"]
        )

        db.add(invoice_item)

        item["product"].quantity -= item["quantity"]

    db.commit()

    created_invoices += 1

print(f"Created {created_invoices} invoices")

db.close()