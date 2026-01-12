FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy ALL application code
COPY . .

# Ensure keys are present (if they weren't caught by COPY . .)
# It's better to rely on COPY . . but verify they exist in build
# We should not strictly fail here if we are local dev, but for prod/submission they must be there.
# Since we are generating them in the same dir, COPY . . covers them.

# Fix cron permissions and install
RUN chmod 644 cron/2fa-cron && crontab cron/2fa-cron
RUN mkdir -p /data /cron && chmod 777 /data /cron

EXPOSE 8080

# Start cron and FastAPI
CMD ["sh", "-c", "service cron start && python -m uvicorn app.main:app --host 0.0.0.0 --port 8080"]
