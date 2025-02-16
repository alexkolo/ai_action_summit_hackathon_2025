from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User
from app.services.object_store import fetch_document_from_text_file
from app.services.llm_client import generate_report
import os
import asyncio

CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))

async def process_user_documents(num_social_sec: str) -> str:
    """
    Retrieves user documents, processes them through two LLM calls, and returns the final summary.
    """
    db: Session = SessionLocal()
    try:
        # Retrieve the user and their associated documents from the database using num_social_sec
        # user = db.query(User).filter(User.num_social_sec == num_social_sec).first()
        # if not user:
        #     raise Exception("User not found")

        # calling real blob stor database to get patient_data
        # for document in user.documents:
        #     content = fetch_document_from_oject_store(document.link)
        #     patient_data.append(content)
        # simulate patient_data
        links_url = {
            "patient_001" : os.path.join(ROOT_DIR, "data/mock_data", "patient_001.txt"),
        }
        # aggregate all document contents
        patient_data = []
        for _, file_path in links_url.items():
            content = fetch_document_from_text_file(file_path)
            patient_data.append(content)
        patient_data_string = " ".join(patient_data)

        # return report
        return await generate_report(num_social_sec, patient_data_string)
    finally:
        db.close()
