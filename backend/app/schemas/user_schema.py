from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    email: EmailStr
    social_security_number: str
    name: str
    gender: str

    class Config:
        orm_mode = True
