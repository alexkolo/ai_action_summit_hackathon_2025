import requests
from app.config import settings
import os

def fetch_document_from_text_file(link: str) -> str:
    """
    Fetches document content from a local file using the provided file path.
    """
    if not os.path.exists(link):
        raise FileNotFoundError(f"Document not found at path: {link}")
    
    try:
        with open(link, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except Exception as e:
        raise Exception(f"Failed to read document from {link}: {e}")
    

def fetch_document_from_oject_store(link: str) -> str:
    """
    Fetches document content from the object store using the provided link.
    """
    # return text or marckdown
    headers = {
        "Authorization": f"Bearer {settings.OBJECT_STORE_KEY}"
    }
    url = f"{settings.OBJECT_STORE_URL}/{link}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch document from {link}, status code: {response.status_code}")
