from fastapi import FastAPI

from app.database import engine, Base
from app.models import Order
from app.routers.orders import router as orders_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(orders_router)


@app.get("/")
def home():
    return {
        "message": "Order Service is running"
    }