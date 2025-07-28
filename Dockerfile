# syntax=docker/dockerfile:1.4
FROM python:3.10-slim

ENV CUDA_VISIBLE_DEVICES=""  

# Only absolutely essential dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install from PyPI only
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY app/ ./app/

CMD ["python", "extractor_runner_1b.py"]