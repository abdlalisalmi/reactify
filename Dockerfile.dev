# Backend Dockerfile for development

FROM python:3.10.13-alpine

WORKDIR /app

RUN apk update && \
	apk add --virtual python-dev && \
	apk add --virtual build-deps gcc musl-dev && \
	apk add postgresql-dev && \
	apk add tzdata

RUN pip install psycopg2 psycopg2-binary
RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000