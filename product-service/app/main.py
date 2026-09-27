from fastapi import FastAPI

from app.database import engine, Base
from app.models import Product
from app.routers.products import router as products_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(products_router)


@app.get("/")
def home():
    return {
        "message": "Product Service is running"
    }