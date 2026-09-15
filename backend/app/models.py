import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    DateTime,
    Enum,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"           # created, not paid yet
    PAID = "paid"                 # payment succeeded
    PAYMENT_FAILED = "payment_failed"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"


class PaymentStatus(str, enum.Enum):
    SUCCESS = "success"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    price = Column(Float, nullable=False)
    category = Column(String, index=True, default="other")
    image_url = Column(String, default="")
    in_stock = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=100)


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total = Column(Float, nullable=False, default=0.0)
    delivery_address = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_order = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)
    card_last4 = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="payment")
