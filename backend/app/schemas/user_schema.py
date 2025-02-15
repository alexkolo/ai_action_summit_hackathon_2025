from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    num_social_sec: str         
    email: Optional[EmailStr] = None      
    name: Optional[str] = None             
    gender: Optional[str] = None  

    class Config:
        orm_mode = True
