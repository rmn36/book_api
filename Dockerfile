FROM python:3-alpine
MAINTAINER Ryan Nowacoski <ryannowacoski@gmail.com> 

RUN apk update && apk upgrade
RUN apk add --no-cache musl-dev openssl-dev libffi-dev gcc

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir flask cryptography

COPY ./src /usr/src/app

# Expose the Flask port
EXPOSE 5000

CMD [ "python", "./app.py" ]