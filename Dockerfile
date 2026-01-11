# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for audio/signal processing
# libasound2: Required for sounddevice/audio IO
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    libasound2-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create non-root user
ARG UID=10001
RUN adduser --disabled-password --gecos "" --home "/app" --shell "/sbin/nologin" --uid "${UID}" appuser

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .
RUN chown -R appuser:appuser /app

USER appuser

# Pre-download ML models (Silero VAD, etc.)
RUN python agent.py download-files

# Start the agent
# Note: In 1.0, 'dev' or 'start' commands are used via the livekit-agents CLI
CMD ["python", "agent.py", "dev"]