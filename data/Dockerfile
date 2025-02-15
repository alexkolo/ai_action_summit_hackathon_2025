FROM python:3.11.11-slim@sha256:42420f737ba91d509fc60d5ed65ed0492678a90c561e1fa08786ae8ba8b52eda
LABEL org.opencontainers.image.source=https://github.com/alexkolo/ai_action_summit_hackathon_2025

RUN useradd -ms /bin/sh api
USER api
WORKDIR /home/api

COPY ./requirements.txt /home/api/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/api/aihack

ENV PYTHONPATH "${PYTHONPATH}:/home/api/aihack"

RUN export PYTHONPATH

EXPOSE 9000

CMD ["python", "/home/api/aihack/main.py"]