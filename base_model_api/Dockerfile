FROM python:3.10-alpine

RUN apk update && apk upgrade
RUN apk add --no-cache bash gcc python3-dev musl-dev linux-headers build-base libc-dev librdkafka-dev && rm -rf /var/cache/apk/*

RUN ls -la /usr/bin/
RUN which gcc

ARG APPDIR=/home/app

RUN python --version

WORKDIR $APPDIR
COPY requirements.txt .

RUN python -m venv venv
RUN source venv/bin/activate

RUN cat requirements.txt | grep confluent-kafka

RUN pip install -r requirements.txt