import requests
from app.config import settings

def call_llm(prompt: str, data: str) -> str:
    """
    Calls the Mistral LLM with the provided prompt and data.
    Returns the generated summary.
    """
    payload = {
            "prompt": prompt,
            "data": data
        }
    headers = {
        "Authorization": f"Bearer {settings.LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(settings.LLM_ENDPOINT, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result.get("output", "")
    else:
        raise Exception(f"LLM request failed with status code {response.status_code}")
