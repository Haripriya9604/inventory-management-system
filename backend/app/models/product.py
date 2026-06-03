from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    category = Column(String)

    sku = Column(String, unique=True)

    purchase_price = Column(Float)

    selling_price = Column(Float)

    quantity = Column(Integer, default=0)

    reorder_level = Column(Integer, default=10)

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id")
    )