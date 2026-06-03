from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.models.product import Product
from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem

from app.schemas.invoice import InvoiceCreate

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.post("/")
def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db)
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == invoice_data.customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    subtotal = 0
    invoice_items = []

    for item in invoice_data.items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

        amount = product.selling_price * item.quantity

        subtotal += amount

        invoice_items.append(
            {
                "product": product,
                "quantity": item.quantity,
                "price": product.selling_price,
                "amount": amount
            }
        )

    gst = subtotal * 0.18
    total = subtotal + gst

    invoice = Invoice(
        invoice_number=1000 + (
            db.query(Invoice).count() + 1
        ),
        customer_id=invoice_data.customer_id,
        subtotal=subtotal,
        gst=gst,
        total=total
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    for item in invoice_items:

        invoice_item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item["product"].id,
            quantity=item["quantity"],
            price=item["price"],
            amount=item["amount"]
        )

        db.add(invoice_item)

        # Reduce stock
        item["product"].quantity -= item["quantity"]

    db.commit()

    return {
        "invoice_id": invoice.id,
        "invoice_number": invoice.invoice_number,
        "customer_id": invoice.customer_id,
        "subtotal": subtotal,
        "gst": gst,
        "total": total
    }