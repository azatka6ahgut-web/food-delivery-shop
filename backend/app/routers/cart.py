from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/cart", tags=["cart"])


def _cart_to_schema(cart_items):
    items_out = []
    total = 0.0
    for item in cart_items:
        line_total = item.product.price * item.quantity
        total += line_total
        items_out.append(
            schemas.CartItemOut(
                id=item.id,
                product=schemas.ProductOut.model_validate(item.product),
                quantity=item.quantity,
                line_total=line_total,
            )
        )
    return schemas.CartOut(items=items_out, total=round(total, 2))


@router.get("", response_model=schemas.CartOut)
def get_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    cart_items = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == current_user.id)
        .all()
    )
    return _cart_to_schema(cart_items)


@router.post("/items", response_model=schemas.CartOut, status_code=201)
def add_item(
    item_in: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    product = db.query(models.Product).filter(models.Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not product.in_stock:
        raise HTTPException(status_code=400, detail="Product is out of stock")

    existing = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.user_id == current_user.id,
            models.CartItem.product_id == item_in.product_id,
        )
        .first()
    )
    if existing:
        existing.quantity += item_in.quantity
    else:
        existing = models.CartItem(
            user_id=current_user.id,
            product_id=item_in.product_id,
            quantity=item_in.quantity,
        )
        db.add(existing)
    db.commit()

    cart_items = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == current_user.id)
        .all()
    )
    return _cart_to_schema(cart_items)


@router.put("/items/{item_id}", response_model=schemas.CartOut)
def update_item(
    item_id: int,
    item_in: schemas.CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    item = (
        db.query(models.CartItem)
        .filter(models.CartItem.id == item_id, models.CartItem.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    item.quantity = item_in.quantity
    db.commit()

    cart_items = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == current_user.id)
        .all()
    )
    return _cart_to_schema(cart_items)


@router.delete("/items/{item_id}", response_model=schemas.CartOut)
def remove_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    item = (
        db.query(models.CartItem)
        .filter(models.CartItem.id == item_id, models.CartItem.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()

    cart_items = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == current_user.id)
        .all()
    )
    return _cart_to_schema(cart_items)


@router.delete("", response_model=schemas.CartOut)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).delete()
    db.commit()
    return schemas.CartOut(items=[], total=0.0)
