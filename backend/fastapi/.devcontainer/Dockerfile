FROM python:3.12.7-slim

WORKDIR workspace
RUN apt update
RUN apt install -y git
RUN pip install poetry==1.8.3
COPY ../pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction


