FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    pip install --upgrade pip

# Installa i pacchetti di sistema richiesti da WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential libffi-dev libpango1.0-0 \
    libpangocairo-1.0-0 libcairo2 libjpeg-dev \
    zlib1g-dev libxml2 libxslt1.1 libgdk-pixbuf2.0-0

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /code/entrypoint.sh

