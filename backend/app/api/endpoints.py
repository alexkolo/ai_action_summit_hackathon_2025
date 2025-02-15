from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserEmail
from app.services.data_processor import process_user_documents

router = APIRouter()

@router.post("/summarize", summary="Generate a final summary for user documents")
def summarize_documents(user: UserEmail):
    """
    Receives a user email, processes the associated documents, and returns a final summary.
    """
    try:
        final_summary = process_user_documents(user.email)
        return {"final_summary": final_summary}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
