from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime

from app.database.base import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(Integer, unique=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    subtotal = Column(Float)

    gst = Column(Float)

    total = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )