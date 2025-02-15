from pydantic import BaseModel, EmailStr

class UserEmail(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True
