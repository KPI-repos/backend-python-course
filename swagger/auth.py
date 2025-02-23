from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@example.com",
                    "role": "customer"
                }
            }
        }

class BasicResponse(BaseModel):
    success: bool
    message: str

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Registration successful"
            }
        }