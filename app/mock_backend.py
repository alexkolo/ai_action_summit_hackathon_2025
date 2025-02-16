import os
import time
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv
from mistralai import ChatCompletionResponse, Mistral

load_dotenv()
api_key: str | None = os.getenv(key="MISTRAL_TOKEN")
model = "mistral-large-latest"

root: Path = Path(".").resolve()
cs_prompt_file: Path = root / "prompts/stage_01/stage01_latest.md"
fs_prompt_file: Path = root / "prompts/stage_02/stage02_latest.md"

mock_patient_file: Path = root / "data/patient_001.txt"


# Mock function to generate a patient's report
def generate_report(patient_id: str) -> Tuple[str, str]:
    """
    Mock function to simulate generating a patient's report.
    Returns a comprehensive report and a final report.
    """
    client = Mistral(api_key=api_key)
    # print current path
    # print(f"Current path: {os.getcwd()}")

    # get files for patient
    if mock_patient_file.is_file() is False:
        raise FileNotFoundError(f"File {mock_patient_file} not found.")
    content: str = mock_patient_file.read_text(encoding="utf-8")

    # create Comprehensive Medical History Summary
    if cs_prompt_file.is_file() is False:
        raise FileNotFoundError(f"File {cs_prompt_file} not found.")
    cs_prompt: str = cs_prompt_file.read_text(encoding="utf-8").format(content=content)
    chat_response: ChatCompletionResponse = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": cs_prompt}],
    )
    com_report: str = chat_response.choices[0].message.content
    # save to temp file with timestamp
    timestamp: str = time.strftime("%Y%m%d_%H%M%S")
    report_file_cs: Path = root / f"app/reports/{patient_id}_cs_{timestamp}.md"
    report_file_cs.write_text(data=com_report, encoding="utf-8")

    # create Final Report
    if fs_prompt_file.is_file() is False:
        raise FileNotFoundError(f"File {fs_prompt_file} not found.")
    fs_prompt: str = fs_prompt_file.read_text(encoding="utf-8").format(content=com_report)
    chat_response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": fs_prompt}],
    )
    final_report: str = chat_response.choices[0].message.content
    # save to temp file with timestamp
    timestamp: str = time.strftime("%Y%m%d_%H%M%S")
    report_file_fs: Path = root / f"app/reports/{patient_id}_fs_{timestamp}.md"
    report_file_fs.write_text(data=final_report, encoding="utf-8")

    print(f"Comprehensive Report saved to: {report_file_cs}")
    print(f"Final Report saved to: {report_file_fs}")

    return com_report, final_report


