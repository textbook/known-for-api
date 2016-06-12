FROM python:alpine

MAINTAINER Jonathan Sharpe <mail@jonrshar.pe>

RUN apk update
RUN apk add ca-certificates
RUN update-ca-certificates

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY ./server.py /usr/src/app
COPY ./mock.json /usr/src/app

EXPOSE 8080

CMD [ "python3", "server.py" ]
