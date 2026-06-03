from app.database.connection import SessionLocal
from app.models.customer import Customer

db = SessionLocal()

customers = [
    {
        "name": "XYZ Traders",
        "phone": "9876543211",
        "email": "xyz.traders@gmail.com"
    },
    {
        "name": "Tech World Solutions",
        "phone": "9876543212",
        "email": "techworld@gmail.com"
    },
    {
        "name": "Smart Solutions Pvt Ltd",
        "phone": "9876543213",
        "email": "smartsolutions@gmail.com"
    },
    {
        "name": "Elite Systems",
        "phone": "9876543214",
        "email": "elite.systems@gmail.com"
    },
    {
        "name": "Future Electronics",
        "phone": "9876543215",
        "email": "futureelectronics@gmail.com"
    },
    {
        "name": "Nova Technologies",
        "phone": "9876543216",
        "email": "nova.tech@gmail.com"
    },
    {
        "name": "Prime Retail Mart",
        "phone": "9876543217",
        "email": "primeretail@gmail.com"
    },
    {
        "name": "Digital Hub Enterprises",
        "phone": "9876543218",
        "email": "digitalhub@gmail.com"
    },
    {
        "name": "Innovate Business Solutions",
        "phone": "9876543219",
        "email": "innovate@gmail.com"
    },
    {
        "name": "Vertex Trading Company",
        "phone": "9876543220",
        "email": "vertextrading@gmail.com"
    }
]

inserted = 0
skipped = 0

for item in customers:

    existing = (
        db.query(Customer)
        .filter(Customer.email == item["email"])
        .first()
    )

    if existing:
        skipped += 1
        continue

    customer = Customer(**item)

    db.add(customer)

    inserted += 1

db.commit()

print(f"Inserted: {inserted}")
print(f"Skipped: {skipped}")

db.close()