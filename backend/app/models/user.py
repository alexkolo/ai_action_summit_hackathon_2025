from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base  

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    social_security_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    gender = Column(String, nullable=True)

    # Relationship to documents
    documents = relationship("Document", back_populates="owner")
