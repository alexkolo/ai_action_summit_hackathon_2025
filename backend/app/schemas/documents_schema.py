from pydantic import BaseModel

class DocumentSchema(BaseModel):
    link: str
    patient_social_security_number: str

    class Config:
        orm_mode = True
