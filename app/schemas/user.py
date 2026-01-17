from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_paid: bool

    class Config:
        from_attributes = True
