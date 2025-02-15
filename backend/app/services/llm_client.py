import requests
from app.config import settings
from typing import Tuple
from pathlib import Path
from mistralai import ChatCompletionResponse, Mistral
import time

# Navigate up three levels to reach the project root
PROJECT_ROOT: Path = Path(__file__).resolve().parents[3]
# prompt file path
COMPREHENSIVE_PROMPT_FILE: Path = PROJECT_ROOT / "prompts" / "stage_01" / "stage01_latest.md"
FINAL_SUMMARY_PROMPT_FILE: Path = PROJECT_ROOT / "prompts" / "stage_02" / "stage02_latest.md"
# code to identify report type
COMPREHENSIVE_SUMMARY_CODE = "cs"
FINAL_SUMMARY_CODE = "fs"

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
    

def generate_report(patient_id: str, patient_data: str) -> Tuple[str, str]:
    """
    function to generating a patient's report.
    Generate a comprehensive report and return a final report.
    """
    # create Comprehensive Medical History Summary
    comprehensive_prompt: str = read_and_format_prompt_file(COMPREHENSIVE_PROMPT_FILE, content=patient_data)
    comprehensive_report: str = call_llm(comprehensive_prompt)
    save_report(COMPREHENSIVE_SUMMARY_CODE, comprehensive_report, patient_id)

    # create Final Report
    final_summary_prompt: str = read_and_format_prompt_file(FINAL_SUMMARY_PROMPT_FILE, content=comprehensive_report)
    final_report: str = call_llm(final_summary_prompt)
    report_file_fs = save_report(FINAL_SUMMARY_CODE, final_report, patient_id)

    print(f"Final Report saved to: {report_file_fs}")

    return comprehensive_report, final_report

def save_report(report_type: str, report_content: str, patient_id: str) -> None:
    timestamp: str = time.strftime("%Y%m%d_%H%M%S")
    file_path: Path = PROJECT_ROOT / f"app/reports/{patient_id}_{report_type}_{timestamp}.md"
    file_path.write_text(data=report_content, encoding="utf-8")
    return file_path

def read_and_format_prompt_file(file_path: Path, content: str) -> str:
    """
    Reads a prompt file, verifies it exists, and returns the formatted content.
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"File {file_path} not found.")
    
    try:
        file_text = file_path.read_text(encoding="utf-8")
        return file_text.format(content=content)
    except Exception as e:
        raise Exception(f"Failed to read and format prompt file {file_path}: {e}")
