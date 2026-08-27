FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
        && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

WORKDIR /app

# Install Python dependencies – this layer is cached unless
# requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

RUN useradd -m appuser
WORKDIR /app
USER appuser

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "src.dogui.app:app", "--bind", "0.0.0.0:$PORT"]