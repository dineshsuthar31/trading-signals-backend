from pydantic import BaseModel

class CheckoutResponse(BaseModel):
    checkout_url: str

class BillingStatusResponse(BaseModel):
    is_paid: bool
