FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git
RUN pip install poetry==1.8.3

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]