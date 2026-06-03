from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.dependencies import get_db

from app.models.product import Product
from app.models.customer import Customer
from app.models.supplier import Supplier
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard_summary(
    db: Session = Depends(get_db)
):
    total_products = db.query(Product).count()

    total_customers = db.query(Customer).count()

    total_suppliers = db.query(Supplier).count()

    total_invoices = db.query(Invoice).count()

    revenue = (
        db.query(func.sum(Invoice.total))
        .scalar()
    )

    total_revenue = revenue if revenue else 0

    return {
        "total_products": total_products,
        "total_customers": total_customers,
        "total_suppliers": total_suppliers,
        "total_invoices": total_invoices,
        "total_revenue": total_revenue
    }


@router.get("/low-stock")
def low_stock_products(
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()

    low_stock = []

    for product in products:
        if product.quantity <= product.reorder_level:
            low_stock.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "quantity": product.quantity,
                    "reorder_level": product.reorder_level
                }
            )

    return low_stock


@router.get("/top-products")
def top_selling_products(
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Product.name,
            func.sum(
                InvoiceItem.quantity
            ).label("units_sold")
        )
        .join(
            InvoiceItem,
            Product.id == InvoiceItem.product_id
        )
        .group_by(Product.name)
        .order_by(
            func.sum(
                InvoiceItem.quantity
            ).desc()
        )
        .limit(5)
        .all()
    )

    return [
        {
            "product_name": row.name,
            "units_sold": row.units_sold
        }
        for row in results
    ]