FROM python:3.5

MAINTAINER Jonathan Sharpe <mail@jonrshar.pe>

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

COPY ./server.py /usr/src/app

EXPOSE 8080

CMD [ "python3", "server.py" ]
