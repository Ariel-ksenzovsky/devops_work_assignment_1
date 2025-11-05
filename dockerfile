FROM python:3.12-slim

# Avoid .pyc and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Add app
COPY ynet.py .

EXPOSE 5000

# Healthcheck (optional)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8081/healthz || exit 1

# Use gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers", "2", "app:app"]
