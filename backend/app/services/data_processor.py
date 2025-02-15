from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User
from app.services.object_store import fetch_document
from app.services.llm_client import call_llm

# Define the prompts for each LLM call
COMPREHENSIVE_PROMPT = "Please provide a comprehensive summary for the following documents:\n"
FINAL_PROMPT = "Refine the above summary to produce a final, polished summary:\n"

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
        for document in user.documents:
            content = fetch_document(document.link)
            contents.append(content)
        
        contents_string = " ".join(contents)
        # First LLM call: Get the comprehensive summary
        comprehensive_summary = call_llm(prompt=COMPREHENSIVE_PROMPT, data=contents_string)

        # Second LLM call: Refine the comprehensive summary to get the final summary
        final_summary = call_llm(prompt=FINAL_PROMPT, data=comprehensive_summary)

        return final_summary
    finally:
        db.close()
