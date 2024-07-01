
FROM python:3.9.19-alpine3.20

LABEL authors="ZonDe"


COPY ./backend ./app/backend
COPY ./frontend ./app/frontend

WORKDIR /app/backend


RUN pip install -r requirements.txt


EXPOSE 5000


CMD flask run --debug --host 0.0.0.0

