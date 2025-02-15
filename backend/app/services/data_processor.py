from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User
from app.services.object_store import fetch_document
from app.services.llm_client import call_llm

# Define the prompts for each LLM call
COMPREHENSIVE_PROMPT = "Please provide a comprehensive summary for the following documents:\n"
FINAL_PROMPT = "Refine the above summary to produce a final, polished summary:\n"

def process_user_documents(social_security_number: str) -> str:
    """
    Retrieves user documents, processes them through two LLM calls, and returns the final summary.
    """
    return 'fianl llm summary'
