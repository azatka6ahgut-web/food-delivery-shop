from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=schemas.OrderOut, status_code=201)
def create_order(
    order_in: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    cart_items = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == current_user.id)
        .all()
    )
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0.0
    order = models.Order(
        user_id=current_user.id,
        delivery_address=order_in.delivery_address,
        status=models.OrderStatus.PENDING,
        total=0.0,
    )
    db.add(order)
    db.flush()  # get order.id before commit

    for cart_item in cart_items:
        if not cart_item.product.in_stock:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Product '{cart_item.product.name}' is no longer in stock",
            )
        line_total = cart_item.product.price * cart_item.quantity
        total += line_total
        db.add(
            models.OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price_at_order=cart_item.product.price,
            )
        )

    order.total = round(total, 2)
    db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).delete()
    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=List[schemas.OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.is_admin:
        return db.query(models.Order).order_by(models.Order.id.desc()).all()
    return (
        db.query(models.Order)
        .filter(models.Order.user_id == current_user.id)
        .order_by(models.Order.id.desc())
        .all()
    )


@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not current_user.is_admin and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to view this order")
    return order


@router.patch("/{order_id}/status", response_model=schemas.OrderOut)
def update_order_status(
    order_id: int,
    status_in: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.get_current_admin),
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status_in.status
    db.commit()
    db.refresh(order)
    return order
