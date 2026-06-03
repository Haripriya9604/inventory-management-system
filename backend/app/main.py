from fastapi import FastAPI
from app.routes.customer import router as customer_router
from app.routes.product import router as product_router

app = FastAPI(
    title="Inventory Management System"
)

app.include_router(product_router)
app.include_router(customer_router)
@app.get("/")
def root():
    return {
        "message": "Inventory API Running"
    }