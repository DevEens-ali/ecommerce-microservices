from fastapi import FastAPI

from app.database import engine, Base
from app.models import User
from app.routers.auth import router as auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Auth Service is running"
    }