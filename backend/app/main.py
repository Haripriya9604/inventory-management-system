from fastapi import FastAPI
from app.routes.customer import router as customer_router
from app.routes.product import router as product_router
from app.routes.supplier import router as supplier_router
from app.routes.invoice import router as invoice_router
app = FastAPI(
    title="Inventory Management System"
)

app.include_router(product_router)
app.include_router(customer_router)
app.include_router(supplier_router)
app.include_router(invoice_router)
@app.get("/")
def root():
    return {
        "message": "Inventory API Running"
    }