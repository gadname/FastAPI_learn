FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.12

RUN dnf install -y tar gzip git
RUN pip install poetry==1.8.3
COPY . .

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction

CMD ["src.main.handler"]