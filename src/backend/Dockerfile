
FROM python:3.11-alpine
LABEL authors="ZonDe"

ENV PYTHONUNBUFFERED=1

COPY . /app/

WORKDIR /app

RUN pip install -r requirements.txt


CMD flask run --debug --host 0.0.0.0
