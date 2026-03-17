# Multi-stage Dockerfile for intuitive-openstack-manager

# 1) Build stage
FROM python:3.14-slim AS builder

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project source for install
COPY pyproject.toml poetry.lock* /app/
COPY src /app/src

# Install runtime dependencies
RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir .

# 2) Runtime stage
FROM python:3.14-slim

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source code (optional; package is already installed but useful for debugging)
COPY src /app/src

# Ensure the user can write logs etc.
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Default command
CMD ["uvicorn", "intuitive_openstack_manager.main:app", "--host", "0.0.0.0", "--port", "8000"]
