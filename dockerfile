FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY ynet.py .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1:5000/healthz || exit 1

# 🔧 point gunicorn to the right module:name
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "2", "ynet:app"]
