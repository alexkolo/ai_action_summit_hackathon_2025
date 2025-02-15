from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User
from app.services.object_store import fetch_document_from_text_file
from app.services.llm_client import call_llm, generate_report
import os
current_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
# Define the prompts for each LLM call
COMPREHENSIVE_PROMPT_FILE = os.path.join(root_dir, "prompts", "stage_01/stage01_latest.md"),
FINAL_PROMPT_FILE = os.path.join(root_dir, "prompts", "stage_02/stage02_latest.md")

def process_user_documents(num_social_sec: str) -> str:
    """
    Retrieves user documents, processes them through two LLM calls, and returns the final summary.
    """
    db: Session = SessionLocal()
    try:
        # Retrieve the user and their associated documents from the database using num_social_sec
        user = db.query(User).filter(User.num_social_sec == num_social_sec).first()
        if not user:
            raise Exception("User not found")

        # Aggregate all document contents
        contents = []
        # simulate link document
        links_url = {
            "patient_001" : os.path.join(root_dir, "data", "patient_001.txt"),
            "patient_002" : os.path.join(root_dir, "data", "patient_002.txt"),
            "patient_003" : os.path.join(root_dir, "data", "patient_003.txt"),
            "patient_004" : os.path.join(root_dir, "data", "patient_004.txt"),
            "patient_005" : os.path.join(root_dir, "data", "patient_005.txt"),
        }
        for _, file_path in links_url.items():
            content = fetch_document_from_text_file(file_path)
            contents.append(content)
        # calling real db
        # for document in user.documents:
        #     content = fetch_document_from_oject_store(document.link)
        #     contents.append(content)
        contents_string = " ".join(contents)
        # First LLM call: Get the comprehensive summary

        # COMPREHENSIVE_PROMPT: str = COMPREHENSIVE_PROMPT_FILE.read_text(encoding="utf-8").format(content=contents_string)
        # comprehensive_summary = call_llm(prompt=COMPREHENSIVE_PROMPT, data=contents_string)

        # # Second LLM call: Refine the comprehensive summary to get the final summary
        # final_summary = call_llm(prompt=FINAL_PROMPT, data=comprehensive_summary)

        # return final_summary
        return generate_report(num_social_sec)
    finally:
        db.close()
