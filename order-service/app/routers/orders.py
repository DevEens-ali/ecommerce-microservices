import httpx
import os
import jwt

from dotenv import load_dotenv

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Order

from app.schemas import (
    OrderCreate,
    OrderUpdate,
    OrderResponse
)
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not configured")

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")

ALGORITHM = "HS256"

security = HTTPBearer()


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
    
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return user_id

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )



@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        response = httpx.get(
            f"{PRODUCT_SERVICE_URL}/products/{order.product_id}"
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Product Service is unavailable"
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch product"
        )

    product = response.json()

    if product["quantity"] < order.quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough product stock"
        )

    total_price = product["price"] * order.quantity

    new_order = Order(
    user_id=current_user_id,
    product_id=order.product_id,
    quantity=order.quantity,
    total_price=total_price,
    status="pending"
)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

@router.get("/", response_model=list[OrderResponse])
def get_orders(
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(
        Order.user_id == current_user_id
    ).all()

    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = order_data.status

    db.commit()
    db.refresh(order)

    return order

@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted successfully"
    }