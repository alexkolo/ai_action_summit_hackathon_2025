from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # URL or key to fetch the document from the object store
    link = Column(String, nullable=False)  

    # Relationship back to the user
    owner = relationship("User", back_populates="documents")
