from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserSchema
from app.services.data_processor import process_user_documents
import asyncio
from app.security.api_key import get_api_key

router = APIRouter()

@router.post("/summarize", summary="Generate a final summary for user documents")
async def summarize_documents(user: UserSchema, api_key: str = Depends(get_api_key)):
    """
    Receives a user num_social_sec, processes the associated documents, and returns a final summary.
    """
    try:
        final_summary = await process_user_documents(user.num_social_sec)
        return {"final_summary": final_summary}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
