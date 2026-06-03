from app.database.connection import engine
from app.database.base import Base
from app.models.customer import Customer
from app.models.product import Product

Base.metadata.create_all(bind=engine)

print("Tables created successfully")