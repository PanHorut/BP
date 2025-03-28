FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    pkg-config \
    gcc \
    python3-dev \
    libssl-dev \
    portaudio19-dev \
    gstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    libsndfile1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

WORKDIR /code/

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt 

COPY . /code/

EXPOSE 8000
