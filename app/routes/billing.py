from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.routes.auth import get_current_user
from app.schemas.billing import CheckoutResponse, BillingStatusResponse
from app.core.config import settings
from app.services.stripe_service import create_checkout_session

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/create-checkout", response_model=CheckoutResponse)
def create_checkout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe secret key not set")

    
    if current_user.is_paid:
        raise HTTPException(status_code=400, detail="Already subscribed")

    success_url = f"{settings.FRONTEND_URL}/dashboard?success=true"
    cancel_url = f"{settings.FRONTEND_URL}/dashboard?canceled=true"

    session = create_checkout_session(
        user_email=current_user.email,
        user_id=current_user.id,
        success_url=success_url,
        cancel_url=cancel_url,
    )

    return CheckoutResponse(checkout_url=session.url)


@router.get("/status", response_model=BillingStatusResponse)
def billing_status(current_user: User = Depends(get_current_user)):
    return BillingStatusResponse(is_paid=current_user.is_paid)
