from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    social_security_number: str         
    email: Optional[EmailStr] = None      
    name: Optional[str] = None             
    gender: Optional[str] = None  

    class Config:
        orm_mode = True
