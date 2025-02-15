import requests
from app.config import settings
from typing import Tuple
from pathlib import Path
from mistralai import ChatCompletionResponse, Mistral
from dotenv import load_dotenv
import os 
import time
# get prompt messages
root: Path = Path(".").resolve()

load_dotenv()
api_key: str | None = settings.LLM_API_KEY
model = settings.LLM_MISTRAL_MODEL

current_file: Path = Path(__file__).resolve()
# Navigate up three levels to reach the project root
project_root: Path = current_file.parents[3]

COMPREHENSIVE_PROMPT_FILE: Path = project_root / "prompts" / "stage_01" / "stage01_latest.md"
FINAL_SUMMARY_PROMPT_FILE: Path = project_root / "prompts" / "stage_02" / "stage02_latest.md"
MOCK_PATIENT_FILE: Path = project_root / "data" / "patient_001.txt"


def call_llm(prompt: str) -> str:
    """
    Calls the Mistral LLM with the provided prompt and data.
    Returns the generated summary.
    """
    client = Mistral(api_key=settings.LLM_API_KEY)
    chat_response: ChatCompletionResponse = client.chat.complete(
        model=settings.LLM_MISTRAL_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return chat_response.choices[0].message.content
    

def generate_report(patient_id: str) -> Tuple[str, str]:
    """
    Mock function to simulate generating a patient's report.
    Returns a comprehensive report and a final report.
    """
    # get files for patient
    if MOCK_PATIENT_FILE.is_file() is False:
        raise FileNotFoundError(f"File {MOCK_PATIENT_FILE} not found.")
    content: str = MOCK_PATIENT_FILE.read_text(encoding="utf-8")

    # create Comprehensive Medical History Summary
    if COMPREHENSIVE_PROMPT_FILE.is_file() is False:
        raise FileNotFoundError(f"File {COMPREHENSIVE_PROMPT_FILE} not found.")
    
    comprehensive_prompt: str = COMPREHENSIVE_PROMPT_FILE.read_text(encoding="utf-8").format(content=content)
    comprehensive_report: str = call_llm(comprehensive_prompt)
    # save to temp file with timestamp
    save_report("cs", comprehensive_report, patient_id, root)

    # create Final Report
    if FINAL_SUMMARY_PROMPT_FILE.is_file() is False:
        raise FileNotFoundError(f"File {FINAL_SUMMARY_PROMPT_FILE} not found.")
    final_summary_prompt: str = FINAL_SUMMARY_PROMPT_FILE.read_text(encoding="utf-8").format(content=comprehensive_report)

    final_report: str = call_llm(final_summary_prompt)
    # save to temp file with timestamp
    report_file_fs = save_report("fs", final_report, patient_id, root)

    # print(f"Comprehensive Report saved to: {report_file_cs}")
    print(f"Final Report saved to: {report_file_fs}")

    return comprehensive_report, final_report

def save_report(report_type: str, report_content: str, patient_id: str, root: Path) -> None:
    timestamp: str = time.strftime("%Y%m%d_%H%M%S")
    file_path: Path = root / f"../app/reports/{patient_id}_{report_type}_{timestamp}.md"
    file_path.write_text(data=report_content, encoding="utf-8")
    return file_path