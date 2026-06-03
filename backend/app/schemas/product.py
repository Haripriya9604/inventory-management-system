from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    category: str
    sku: str
    purchase_price: float
    selling_price: float
    quantity: int
    reorder_level: int
    supplier_id: int


class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True