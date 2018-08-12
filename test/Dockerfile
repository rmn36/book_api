FROM python:3-alpine
MAINTAINER Ryan Nowacoski <ryannowacoski@gmail.com> 

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir flask requests

COPY ./src /usr/src/app

# Expose the Flask port
EXPOSE 5000

CMD [ "python", "./test.py" ]