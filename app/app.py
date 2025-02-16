"""
Start: streamlit run app/app.py
"""

import os
import time
from io import StringIO
from pathlib import Path
from typing import Tuple

import streamlit as st
from dotenv import load_dotenv
from mistralai import ChatCompletionResponse, Mistral
from mock_backend import generate_report as generate_report_mock

load_dotenv()
api_key: str | None = os.getenv(key="MISTRAL_TOKEN")
model = "mistral-large-latest"


# Mock function to check if a patient is in the database
def patient_in_db(patient_id: str) -> bool:
    """
    Mock function to simulate checking whether a patient exists in a database.
    Returns True for demonstration purposes.
    """
    # In a real scenario, this would query an actual database
    if patient_id == "":
        return False
    # Here, we simply return True
    return True


# Generate a patient's report
@st.cache_data(ttl="1d", show_spinner=False)
def generate_report(patient_id: str) -> Tuple[str, str]:
    """
    Generates a comprehensive and final report for a patient.

    Parameters
    ----------
    patient_id : str
        The ID of the patient for whom the report is generated.

    Returns
    -------
    Tuple[str, str]
        A tuple containing the comprehensive report and final report.
    """

    # mock implementation for debugging
    # com_report: str = (
    #     f"### Comprehensive Medical History Summary for {patient_id}\n\n"
    #     f"- **Age**: 45\n"
    #     f"- **Condition**: Hypertension\n"
    #     f"- **Medications**: Amlodipine, Lisinopril\n"
    #     f"- **Recent Lab Results**: Cholesterol high, needs dietary changes\n\n"
    #     f"**Additional Notes**:\n"
    #     f"Patient should continue medication and follow up in 2 weeks."
    # )
    # final_report: str = com_report
    # return com_report, final_report

    return generate_report_mock(patient_id=patient_id)


def convert_history_to_markdown(history: list[dict[str, str]]) -> str:
    """
    Returns a Markdown string of the conversation history.
    """

    # Zip user messages with their corresponding assistant replies
    # history[0] => system message
    # history[1::2] => every "user" message
    # history[2::2] => every "assistant" message
    question_answer_pairs = list(zip(history[1::2], history[2::2]))

    markdown_output: str = ""
    for i, (user_item, assistant_item) in enumerate(question_answer_pairs, start=1):
        question: str = user_item["content"].strip()
        answer: str = assistant_item["content"]
        markdown_output += f"# {i}. Question: '{question}'\n\n{answer}\n\n"

    return markdown_output


def main() -> None:
    """
    Main function to run the Streamlit app.
    """
    APP_TITLE = "Consultation Warm Up 💚"
    APP_ICON = "💚"
    st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON)
    st.title(body=f"{APP_ICON} {APP_TITLE}")

    # Initialize session state variables if they don't exist
    if "patient_found" not in st.session_state:
        st.session_state.patient_found = False
    if "report_created" not in st.session_state:
        st.session_state.report_created = False
    if "final_report" not in st.session_state:
        st.session_state.final_report = ""
    if "com_report" not in st.session_state:
        st.session_state.com_report = ""
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = True
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "consent_for_search" not in st.session_state:
        st.session_state.consent_for_search = False
    if "consent_for_analysis" not in st.session_state:
        st.session_state.consent_for_analysis = False
    if "user_question" not in st.session_state:
        st.session_state.user_question = "Is the patient on any medications?"

    # Create a form for patient lookup
    with st.form(key="lookup_form"):
        # col_input, col_button = st.columns([3, 1], vertical_alignment="bottom")

        # Text input for the patient's email
        user_email: str = st.text_input(
            label="Enter Social Security Number",
            value="0000000000000",
            key="user_email_input",
            placeholder="Enter Social Security Number",
        )

        consent_for_search: bool = st.checkbox(
            label="Patient gave consents to search for medical records in their Doctolib account."
        )
        st.session_state.consent_for_search = consent_for_search

        # st.write(f"Current path: {Path('.').resolve()}")

        # Use a form_submit_button instead of a regular button
        lookup_submit: bool = st.form_submit_button(label="🔎 Look up patient", type="primary")

    if lookup_submit and not st.session_state.consent_for_search:
        st.warning(body="Patient consents to search for medical records must be granted.", icon="❗")

    # Step 2: Button to look up the patient
    elif lookup_submit:  # st.button(label="Look up patient", disabled=email_input_disabled):
        # Check if the email exists in the mock database
        exists: bool = patient_in_db(patient_id=user_email)
        st.session_state.patient_found = exists

        if not exists:
            # If patient doesn't exist, warn the user
            st.warning(body="No medical records are available for this patient at the moment.", icon="❗")

    if st.session_state.patient_found:
        st.success(body="Medical records are available for this patient.", icon="✅")

        # question whether the patient gives consent to analyze their medical records
        st.write("Does the patient gave consents to analyze their medical records?")

        col_yes, col_no = st.columns(spec=2, gap="large")
        no_analysis_consent: bool = col_no.button(label="No", use_container_width=True)
        gave_consent: bool = col_yes.button(label="Yes", type="primary", use_container_width=True)
        if gave_consent:
            st.session_state.consent_for_analysis = True
        if no_analysis_consent:
            st.session_state.consent_for_analysis = False
            st.warning(body="It is not possible to analyze medical records without consent!", icon="❗")

        # Analyzing medical records & generating report
        if st.session_state.consent_for_analysis:
            st.success(body="Consent analyzing medical records granted!", icon="✅")
            with st.spinner(text="Analyzing medical records & generating report..."):
                com_report, final_report = generate_report(patient_id=user_email)
                st.session_state.final_report = final_report
                st.session_state.com_report = com_report
                st.session_state.report_created = True

    # Show the report if it was created
    if st.session_state.report_created:
        st.success(body="Report created!", icon="✅")
        st.divider()
        st.subheader(body="Patient's Medical Report")

        # Step 3: Show action buttons once the report is displayed
        col1, col2 = st.columns(2, gap="large")

        # with col1:
        #     if st.button(label="❓ Ask Questions", use_container_width=True, type="primary"):
        #         st.session_state.chat_open = True  # Open the chat window

        with col1:
            # Provide a download button for the report in .txt format
            file_name: str = f"patient_report_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            st.download_button(
                label="📥 Download Report",
                data=st.session_state.final_report,
                file_name=file_name,
                mime="text/plain",
                use_container_width=True,
            )

        with col2:
            # Restart the app by resetting session state
            if st.button(label="🚮 Reset Lookup", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        # show the final report
        with st.container(border=True, height=600):
            st.markdown(body=st.session_state.final_report)

    # If the chat window is open, show a simple chat interface
    if st.session_state.report_created and st.session_state.chat_open:
        client = Mistral(api_key=api_key)
        st.subheader(body="Ask questions about the patient's medical history:")

        # create system message if chat history is empty
        if st.session_state.chat_history == []:
            system_message: str = (
                Path("app/chat_box/system_latest.md")
                .read_text(encoding="utf-8")
                .format(content=st.session_state.com_report)
            )
            st.session_state.chat_history.append({"role": "system", "content": system_message})

        history: list[dict[str, str]] = st.session_state.chat_history
        if len(history) > 1:
            # Zip user messages with their corresponding assistant replies
            # history[0] => system message
            # history[1::2] => every "user" message
            # history[2::2] => every "assistant" message
            pairs = list(zip(history[1::2], history[2::2]))

            for i, (user_item, assistant_item) in enumerate(pairs):
                # We want only the last expander opened by default
                expanded: bool = i == len(pairs) - 1

                with st.expander(label=f"{i + 1}. Question: **{user_item['content'].strip()}**", expanded=expanded):
                    st.write(assistant_item["content"])

        with st.container(border=False):
            # Text input for the user's question
            with st.form(key="question_form", clear_on_submit=True):
                user_question: str = st.text_input(
                    label="Enter your question here",
                    value=st.session_state.user_question,
                    placeholder="Ask a question here",
                    max_chars=1000,
                )
                submit: bool = st.form_submit_button(label="Submit Question", type="primary")

            if submit:
                # Add the user's question to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_question})
                st.session_state.user_question = user_question

                # Mock answer from an internal system
                # mock_answer = "This is a mock response with patient-specific insights."
                # st.session_state.chat_history.append({"role": "assistant", "content": mock_answer})

                #  real answer from Mistral
                with st.spinner(text="Generating response..."):
                    chat_response: ChatCompletionResponse = client.chat.complete(
                        model=model,
                        messages=st.session_state.chat_history,
                    )
                assistant_answer: str = chat_response.choices[0].message.content
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_answer})

                # with st.expander(label=f" Question: **{user_question.strip()}**", expanded=True):
                #     st.write(assistant_answer)
                st.rerun()

        # Footer with buttons to export and clear chat history
        col_export, col_clear = st.columns(2, gap="large")
        if col_clear.button(label="🧹 Clear Chat History", use_container_width=True):
            st.session_state.chat_history.clear()
            st.session_state.user_question = ""
            st.rerun()

        # Use Streamlit's download_button to download the content
        downloaded: bool = col_export.download_button(
            label="📥 Download Chat History",
            data=StringIO(convert_history_to_markdown(history=history)).getvalue(),
            file_name=f"chat_history_{time.strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

        if downloaded:
            st.success(body="Chat history exported as Markdown.", icon="✅")


# Run the Streamlit app
if __name__ == "__main__":
    main()
