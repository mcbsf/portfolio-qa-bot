FROM python:3.11-slim

# Prevent Python from buffering stdout / stderr
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps for building Python packages (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better layer caching)
COPY requirements.txt .

# Install Python deps
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose API port
EXPOSE 8000

# Default command: run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--workers", "4", "--host", "0.0.0.0", "--port", "8000"]
