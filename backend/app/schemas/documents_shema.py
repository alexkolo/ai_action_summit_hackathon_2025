from pydantic import BaseModel

class DocumentLink(BaseModel):
    link: str

    class Config:
        orm_mode = True
