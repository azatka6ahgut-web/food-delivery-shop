import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/payment", tags=["payment"])

# Mock payment gateway rules (handy for negative-testing autotests later):
#   - card number ending in "0002" -> always declined
#   - any other valid-looking card number -> always succeeds
# This mirrors how real sandboxes (e.g. Stripe test cards) work, so it's a
# realistic pattern to practice both positive and negative test cases against.
DECLINED_CARD_SUFFIX = "0002"


@router.post("/{order_id}", response_model=schemas.PaymentOut)
def pay_for_order(
    order_id: int,
    payment_in: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to pay for this order")
    if order.status == models.OrderStatus.PAID:
        raise HTTPException(status_code=400, detail="Order is already paid")

    card_digits = re.sub(r"\D", "", payment_in.card_number)
    if len(card_digits) < 12:
        raise HTTPException(status_code=422, detail="Invalid card number")

    existing_payment = (
        db.query(models.Payment).filter(models.Payment.order_id == order.id).first()
    )

    if card_digits.endswith(DECLINED_CARD_SUFFIX):
        status_ = models.PaymentStatus.FAILED
        order.status = models.OrderStatus.PAYMENT_FAILED
    else:
        status_ = models.PaymentStatus.SUCCESS
        order.status = models.OrderStatus.PAID

    if existing_payment:
        existing_payment.status = status_
        existing_payment.card_last4 = card_digits[-4:]
        existing_payment.amount = order.total
        payment = existing_payment
    else:
        payment = models.Payment(
            order_id=order.id,
            amount=order.total,
            status=status_,
            card_last4=card_digits[-4:],
        )
        db.add(payment)

    db.commit()
    db.refresh(payment)

    if status_ == models.PaymentStatus.FAILED:
        raise HTTPException(
            status_code=402,
            detail={
                "message": "Payment declined",
                "payment": schemas.PaymentOut.model_validate(payment).model_dump(),
            },
        )

    return payment
