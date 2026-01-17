import stripe
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.redis import get_redis_client
from app.db.session import get_db
from app.db.models import User, Subscription

router = APIRouter(prefix="/webhook", tags=["Webhook"])

stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Stripe webhook secret not set")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    # Idempotency using Redis
    r = None
    try:
        r = get_redis_client()
        r.ping()
    except Exception:
        r = None

    event_id = event.get("id", "")
    if r and event_id:
        key = f"stripe_event:{event_id}"
        if r.get(key):
            return {"status": "duplicate_ignored"}
        r.setex(key, 60 * 60 * 24, "1")  # 24 hours

    # Handle event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session.get("id")
        metadata = session.get("metadata", {})
        user_id = metadata.get("user_id")

        if not user_id:
            return {"status": "no_user_id"}

        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            return {"status": "user_not_found"}

        # Mark paid
        user.is_paid = True

        # Store subscription record (avoid duplicate session_id)
        existing_sub = db.query(Subscription).filter(Subscription.stripe_session_id == session_id).first()
        if not existing_sub:
            sub = Subscription(
                user_id=user.id,
                stripe_session_id=session_id,
                status="active",
            )
            db.add(sub)

        db.commit()
        return {"status": "paid_activated"}

    return {"status": "ignored"}
