import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

PLAN_PRICE_INR = 499

def create_checkout_session(user_email: str, user_id: int, success_url: str, cancel_url: str):
    """
    Creates Stripe Checkout Session (Test mode)
    """
    session = stripe.checkout.Session.create(
    mode="payment",
    payment_method_types=["card"],

    customer_email=user_email,
    customer_creation="always",

    billing_address_collection="required",
    shipping_address_collection={
        "allowed_countries": ["IN"]
    },

    line_items=[
        {
            "price_data": {
                "currency": "inr",
                "product_data": {"name": "Trading Signals Pro (₹499)"},
                "unit_amount": PLAN_PRICE_INR * 100,
            },
            "quantity": 1,
        }
    ],

    metadata={
        "user_id": str(user_id),
        "email": user_email,
    },

    success_url=success_url,
    cancel_url=cancel_url,
)
    return session
