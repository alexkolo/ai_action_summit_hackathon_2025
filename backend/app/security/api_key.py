from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from app.config import settings

API_KEY_NAME = settings.BACKEND_API_KEY_NAME
API_KEY = settings.BACKEND_API_KEY

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    return api_key
