from pydantic import BaseModel

class DocumentSchema(BaseModel):
    link: str
    patient_id: str

    class Config:
        orm_mode = True
