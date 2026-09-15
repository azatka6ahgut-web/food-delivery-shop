from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field

from .models import OrderStatus, PaymentStatus


# ---------- Auth / Users ----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Products ----------

class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float = Field(gt=0)
    category: str = "other"
    image_url: str = ""
    stock_quantity: int = 100


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = None
    image_url: Optional[str] = None
    in_stock: Optional[bool] = None
    stock_quantity: Optional[int] = None


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    image_url: str
    in_stock: bool
    stock_quantity: int

    class Config:
        from_attributes = True


# ---------- Cart ----------

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)


class CartItemOut(BaseModel):
    id: int
    product: ProductOut
    quantity: int
    line_total: float

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    items: List[CartItemOut]
    total: float


# ---------- Orders ----------

class OrderCreate(BaseModel):
    delivery_address: str = Field(min_length=3)


class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price_at_order: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    status: OrderStatus
    total: float
    delivery_address: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


# ---------- Payment ----------

class PaymentCreate(BaseModel):
    card_number: str = Field(min_length=12, max_length=19)
    card_expiry: str
    card_cvv: str = Field(min_length=3, max_length=4)


class PaymentOut(BaseModel):
    id: int
    order_id: int
    amount: float
    status: PaymentStatus
    card_last4: str

    class Config:
        from_attributes = True
