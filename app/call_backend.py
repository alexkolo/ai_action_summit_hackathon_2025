import requests
import os

def generate_report_from_back(patient_id):
    endpoint_api = "/v1/summarize"
    api_url = os.getenv("API_URL") + endpoint_api
    api_key = os.getenv("USER_API_KEY")
    headers = {"api_key": api_key} 
    print(api_url)
    try:
        response = requests.post(api_url, json={"num_social_sec": patient_id}, headers=headers)
        response.raise_for_status()  # Lève une erreur pour les codes d'état HTTP 4xx/5xx
        response_data = response.json()
        print(response_data)
        cm_summary = response_data["final_summary"][0]
        final_summary = response_data["final_summary"][1]
        return cm_summary, final_summary  # Retourne la réponse au format JSON
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel à l'API : {e}")
        return None