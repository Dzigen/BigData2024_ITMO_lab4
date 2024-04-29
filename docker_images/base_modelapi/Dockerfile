FROM python:3.10-alpine

RUN apk update && apk add gcc python3-dev musl-dev linux-headers build-base libc-dev

ARG APPDIR=/home/app

RUN python --version

WORKDIR $APPDIR
RUN python -m venv venv
RUN source venv/bin/activate

COPY requirements.txt .
RUN python -m pip install -r requirements.txt