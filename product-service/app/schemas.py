from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=500)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class ProductUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=500)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int