from app.database.connection import engine
from app.database.base import Base
from app.models.customer import Customer
from app.models.product import Product
from app.models.supplier import Supplier
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.user import User
Base.metadata.create_all(bind=engine)

print("Tables created successfully")