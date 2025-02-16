# AI Action Summit Hackathon 2025

## System Design

[add picture here]

## Frontend

## Environment

- build with Python 3.11.10

```bash
python -m venv venv  # removed via: sudo rm -rf venv
source venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

## Start app

```bash
source venv/bin/activate
streamlit run app/app.py
```

## Run the application with Docker locally

```bash
docker image build -t streamFront -f DockerfileApp  .
docker container run  -p 8501:8501  -e MISTRAL_TOKEN=your_mistral_token streamFront
```

## Backend

TODO
