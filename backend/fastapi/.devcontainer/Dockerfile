FROM python:3.12.7-slim

WORKDIR /workspace
RUN apt-get update && apt-get install -y git
RUN pip install poetry==1.8.3

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root

ENV PYTHONPATH=/workspace