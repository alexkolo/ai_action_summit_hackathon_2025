FROM python:3.11.11-slim@sha256:42420f737ba91d509fc60d5ed65ed0492678a90c561e1fa08786ae8ba8b52eda
LABEL org.opencontainers.image.source=https://github.com/alexkolo/ai_action_summit_hackathon_2025

RUN useradd -ms /bin/sh app
USER app
WORKDIR /home/

COPY ./requirements.txt /home/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /home/app

ENV PYTHONPATH "${PYTHONPATH}:/home/app"

RUN export PYTHONPATH

EXPOSE 8000

CMD ["python", "/home/app/main.py"]
