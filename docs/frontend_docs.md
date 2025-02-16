# App (Frontend) Documentation

## Environment

Built with **Python 3.11.10**.

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

## Start the App

Activate the virtual environment and run:

```bash
source venv/bin/activate
streamlit run app/app.py
```

## Run the Application with Docker

1. Build the Docker image:

    ```bash
    docker image build -t streamFront -f DockerfileApp .
    ```

2. Run the Docker container (replace `your_mistral_token` with your actual token):

    ```bash
    docker container run -p 8501:8501 -e MISTRAL_TOKEN=your_mistral_token streamFront
    ```

Open [http://localhost:8501](http://localhost:8501) in your browser to access the app.

## Code Overview

Below is a high-level summary of the files and their responsibilities:

- **`app.py`**:
  Main Streamlit file containing:
  - **Patient Lookup Form**: Collects a patient ID and checks for consent.
  - **Consent Workflow**: Ensures patient has given proper consent.
  - **Report Generation**: Generates comprehensive and final reports (using either a mock backend or real Mistral model).
  - **Q&A Chat Interface**: Allows users to pose questions about the patient's data and saves the conversation history.

- **`mock_backend.py`**:
  Provides a dummy function `generate_report()` used by `app.py` if running in a mocked environment.

- **`call_backend.py`**:
  Contains a function `generate_report_from_back()` that calls a real [Backend](backend/readme.md) or AI model.
