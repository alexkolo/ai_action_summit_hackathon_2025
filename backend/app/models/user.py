from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base  

class User(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    num_social_sec = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    gender = Column(String, nullable=True)

    # Relationship to documents
    documents = relationship("Document", back_populates="owner")
