FROM python:3.9-alpine3.16

COPY requirements.txt /temp/req.txt
RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r /temp/req.txt
RUN adduser --disabled-password service-user

WORKDIR /service
EXPOSE 8000

COPY service /service

USER service-user
