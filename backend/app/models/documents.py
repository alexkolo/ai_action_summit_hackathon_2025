from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, nullable=False)
    patient_social_security_number = Column(
        String,
        ForeignKey("users.social_security_number"),
        nullable=False
    )

    # Relationship to the User model. This allows accessing the user (owner) that this document belongs to.
    owner = relationship("User", back_populates="documents")
