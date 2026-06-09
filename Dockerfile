# SO-101 Intelligent Control — Cable Sorting with ACT Imitation Learning
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/
COPY results/ ./results/
COPY models/ ./models/

CMD ["python3", "scripts/generar_graficas.py"]
