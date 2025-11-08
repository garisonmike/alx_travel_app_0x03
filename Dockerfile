# Multi-stage Dockerfile for Django + Celery
# Stage 1: Build dependencies
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=alx_travel_app.settings

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-traditional \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder and install
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/staticfiles /app/mediafiles && \
    chown -R appuser:appuser /app

# Copy project files
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/admin/login/ || exit 1

# Default command (can be overridden in docker-compose)
CMD ["gunicorn", "alx_travel_app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "--timeout", "60"]
