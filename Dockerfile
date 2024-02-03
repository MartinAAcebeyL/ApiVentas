FROM python:3.10-alpine

# Instala libfreetype6-dev
RUN apk update && \
    apk add --no-cache build-base freetype-dev
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY requirements_prod.txt requirements_dev.txt /app/

RUN pip install -r requirements_prod.txt
RUN pip install -r requirements_dev.txt

COPY . /app
