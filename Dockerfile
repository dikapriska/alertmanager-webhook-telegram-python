FROM python:3.11-alpine

LABEL maintainer="Dika Priska Prastika <dikapriska@gmail.com>"

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        libffi-dev \
        openssl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY flaskAlert.py .
COPY run.sh .

RUN chmod +x run.sh

EXPOSE 9119

ENTRYPOINT ["./run.sh"]
