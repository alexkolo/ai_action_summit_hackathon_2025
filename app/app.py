"""
Start: streamlit run app/app.py
"""

import os
import time
from pathlib import Path
from typing import Tuple

import streamlit as st
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()
api_key: str | None = os.getenv(key="MISTRAL_TOKEN")


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


# Mock function to generate a patient's report
def generate_report(patient_id: str) -> Tuple[str, str]:
    """
    Mock function to simulate generation of a patient medical report.
    Returns a static string with a placeholder medical summary.
    """
    # In a real scenario, some NLP or data processing might occur here
    # We'll just return a short fake report for demonstration
    com_report: str = (
        f"### Comprehensive Medical History Summary for {patient_id}\n\n"
        f"- **Age**: 45\n"
        f"- **Condition**: Hypertension\n"
        f"- **Medications**: Amlodipine, Lisinopril\n"
        f"- **Recent Lab Results**: Cholesterol high, needs dietary changes\n\n"
        f"**Additional Notes**:\n"
        f"Patient should continue medication and follow up in 2 weeks."
    )
    final_report: str = (
        f"### Medical Report for {patient_id}\n\n"
        f"- **Age**: 45\n"
        f"- **Condition**: Hypertension\n"
        f"- **Medications**: Amlodipine, Lisinopril\n"
        f"- **Recent Lab Results**: Cholesterol high, needs dietary changes\n\n"
        f"**Additional Notes**:\n"
        f"Patient should continue medication and follow up in 2 weeks."
    )

    return com_report, final_report


def main() -> None:
    """
    Main function to run the Streamlit app.
    """
    st.title(body="Patient Data Lookup")

    # Initialize session state variables if they don't exist
    if "email_checked" not in st.session_state:
        st.session_state.email_checked = False
    if "patient_found" not in st.session_state:
        st.session_state.patient_found = False
    if "report_created" not in st.session_state:
        st.session_state.report_created = False
    if "final_report" not in st.session_state:
        st.session_state.final_report = ""
    if "com_report" not in st.session_state:
        st.session_state.com_report = ""
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Create a form for patient lookup
    with st.form(key="lookup_form"):
        # If the patient was already found, disable the email field
        email_input_disabled: bool = st.session_state.patient_found

        col_input, col_button = st.columns([4, 1], vertical_alignment="bottom")

        # Text input for the patient's email
        user_email: str = col_input.text_input(
            label="Enter patient's email address",
            value="test_patient@gmail.com",
            disabled=email_input_disabled,
            key="user_email_input",
            placeholder="Enter patient's email address",
        )

        # Use a form_submit_button instead of a regular button
        lookup_submit: bool = col_button.form_submit_button(label="Look up patient", type="primary")

    # Step 2: Button to look up the patient
    if lookup_submit:  # st.button(label="Look up patient", disabled=email_input_disabled):
        # Check if the email exists in the mock database
        exists: bool = patient_in_db(patient_id=user_email)
        st.session_state.email_checked = True
        st.session_state.patient_found = exists

        if not exists:
            # If patient doesn't exist, warn the user
            st.warning(body="No data is available for this patient. Please try another email.", icon="❗")
        else:
            # If patient is found, lock the email field
            st.success(body="Data is available for this patient.", icon="✅")

            # Simulate report creation with a spinner (2 seconds)
            with st.spinner(text="Generating report..."):
                time.sleep(2)
                # Once done, store the generated report in session state
                com_report, final_report = generate_report(patient_id=user_email)
                st.session_state.final_report = final_report
                st.session_state.com_report = com_report
                st.session_state.report_created = True

    # Show the report if it was created
    if st.session_state.report_created:
        with st.container(border=True, height=600):
            st.markdown(body=st.session_state.final_report)

        # Step 3: Show action buttons once the report is displayed
        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            if st.button(label="Ask Questions", use_container_width=True, type="primary"):
                st.session_state.chat_open = True  # Open the chat window

        with col2:
            # Provide a download button for the report in .txt format
            file_name: str = f"patient_report_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            st.download_button(
                label="Download Report",
                data=st.session_state.final_report,
                file_name=file_name,
                mime="text/plain",
                use_container_width=True,
            )

        with col3:
            # Restart the app by resetting session state
            if st.button(label="Restart Lookup", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    # If the chat window is open, show a simple chat interface
    if st.session_state.chat_open:
        client = Mistral(api_key=api_key)
        model = "mistral-large-latest"

        # create system message if chat history is empty
        if st.session_state.chat_history == []:
            system_message: str = (
                Path("app/chat_box/system_latest.md")
                .read_text(encoding="utf-8")
                .format(content=st.session_state.com_report)
            )
            st.session_state.chat_history.append({"role": "system", "content": system_message})

        with st.container(border=True):
            st.subheader(body="Ask questions about the patient's data:")

            # Text input for the user's question
            user_question: str = st.text_input(
                label="Your question:",
                value="Is the patient on any medications?",
                placeholder="Ask a question here",
                max_chars=1000,
            )

            if st.button(label="Send Question"):
                # Add the Q&A to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_question})

                # Mock answer from an internal system
                # mock_answer = "This is a mock response with patient-specific insights."
                # st.session_state.chat_history.append({"role": "assistant", "content": mock_answer})

                #  real answer from Mistral
                with st.spinner(text="Generating response..."):
                    chat_response = client.chat.complete(
                        model=model,
                        messages=st.session_state.chat_history,
                    )
                assistant_answer: str = chat_response.choices[0].message.content
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_answer})

            # Display the chat history
            st.divider()
            for entry in st.session_state.chat_history:
                role: str = entry["role"]
                if role == "system":
                    continue
                text = entry["content"]
                role_name: str = "Question" if role == "user" else "Answer"
                st.write(f"**{role_name}:** {text}")
                if role == "assistant":
                    st.divider()

        if st.button(label="Clear Chat History"):
            st.session_state.chat_history.clear()
            st.rerun()

            # st.success(body="Chat history cleared.")


# Run the Streamlit app
if __name__ == "__main__":
    main()
