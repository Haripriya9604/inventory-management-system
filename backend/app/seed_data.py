from app.database.connection import SessionLocal
from app.models.product import Product
from app.models.supplier import Supplier
db = SessionLocal()

products = [
    {
        "name": "Thermal Receipt Printer",
        "category": "Retail Equipment",
        "sku": "TRP001",
        "purchase_price": 4200,
        "selling_price": 6500,
        "quantity": 8,
        "reorder_level": 2,
        "supplier_id": 4
    },
    {
        "name": "Fingerprint Scanner",
        "category": "Security",
        "sku": "FPS001",
        "purchase_price": 1800,
        "selling_price": 3200,
        "quantity": 15,
        "reorder_level": 4,
        "supplier_id": 2
    },
    {
        "name": "Document Scanner",
        "category": "Office Equipment",
        "sku": "DOC001",
        "purchase_price": 5500,
        "selling_price": 7900,
        "quantity": 10,
        "reorder_level": 3,
        "supplier_id": 3
    },
    {
        "name": "Label Printer",
        "category": "Retail Equipment",
        "sku": "LBL001",
        "purchase_price": 3000,
        "selling_price": 4800,
        "quantity": 12,
        "reorder_level": 3,
        "supplier_id": 4
    },
    {
        "name": "HDMI Capture Card",
        "category": "Video Equipment",
        "sku": "CAP001",
        "purchase_price": 2400,
        "selling_price": 3900,
        "quantity": 14,
        "reorder_level": 4,
        "supplier_id": 2
    },
    {
        "name": "Mini UPS Router Backup",
        "category": "Power Solutions",
        "sku": "UPS001",
        "purchase_price": 1100,
        "selling_price": 1900,
        "quantity": 25,
        "reorder_level": 5,
        "supplier_id": 4
    },
    {
        "name": "Conference Speakerphone",
        "category": "Audio",
        "sku": "CONF001",
        "purchase_price": 3500,
        "selling_price": 5600,
        "quantity": 9,
        "reorder_level": 2,
        "supplier_id": 1
    },
    {
        "name": "Smart Power Strip",
        "category": "Power Solutions",
        "sku": "PWR001",
        "purchase_price": 700,
        "selling_price": 1300,
        "quantity": 40,
        "reorder_level": 10,
        "supplier_id": 1
    },
    {
        "name": "USB Docking Station",
        "category": "Accessories",
        "sku": "DOCK001",
        "purchase_price": 2600,
        "selling_price": 4300,
        "quantity": 18,
        "reorder_level": 4,
        "supplier_id": 3
    },
    {
        "name": "Portable Projector",
        "category": "Presentation Equipment",
        "sku": "PROJ001",
        "purchase_price": 12000,
        "selling_price": 16500,
        "quantity": 6,
        "reorder_level": 2,
        "supplier_id": 3
    }
]

inserted = 0
skipped = 0

for item in products:

    existing = (
        db.query(Product)
        .filter(Product.sku == item["sku"])
        .first()
    )

    if existing:
        skipped += 1
        continue

    product = Product(**item)

    db.add(product)

    inserted += 1

db.commit()

print(f"Inserted: {inserted}")
print(f"Skipped: {skipped}")

db.close()