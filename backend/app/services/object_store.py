import requests
from app.config import settings

def fetch_document(link: str) -> str:
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
