FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    glib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY vision-service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY vision-service/ .

CMD ["python", "src/detector.py"]