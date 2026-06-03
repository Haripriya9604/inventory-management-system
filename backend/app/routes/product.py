from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.database.dependencies import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(
        name=product.name,
        category=product.category,
        sku=product.sku,
        purchase_price=product.purchase_price,
        selling_price=product.selling_price,
        quantity=product.quantity,
        reorder_level=product.reorder_level
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get("/", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db)
):
    return db.query(Product).all()

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    existing_product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not existing_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing_product.name = product.name
    existing_product.category = product.category
    existing_product.sku = product.sku
    existing_product.purchase_price = product.purchase_price
    existing_product.selling_price = product.selling_price
    existing_product.quantity = product.quantity
    existing_product.reorder_level = product.reorder_level

    db.commit()
    db.refresh(existing_product)

    return existing_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@router.get("/alerts/low-stock")
def low_stock_alert(
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()

    alerts = []

    for product in products:
        if product.quantity <= product.reorder_level:
            alerts.append({
                "id": product.id,
                "name": product.name,
                "quantity": product.quantity,
                "reorder_level": product.reorder_level
            })

    return alerts
