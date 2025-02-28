FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    pkg-config \
    gcc \
    python3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000
