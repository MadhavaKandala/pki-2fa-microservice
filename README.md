# PKI-Based 2FA Microservice with Docker

Secure authentication microservice implementing RSA encryption, TOTP-based 2FA, and persistent storage using Docker.

## Features

- **RSA/OAEP Encryption**: 4096-bit RSA key pair for secure seed transmission
- **TOTP Authentication**: Time-based One-Time Password generation and verification
- **REST API**: Three endpoints for seed decryption, 2FA generation, and verification
- **Persistent Storage**: Docker volumes for data persistence across restarts
- **Cron Integration**: Automated 2FA code logging every minute
- **Multi-Stage Docker Build**: Optimized container image with minimal size

## Setup

1. Clone the repository
2. Generate RSA keys: `python generate_keys.py`
3. Request encrypted seed from instructor API
4. Build and run: `docker-compose up --build`

## API Endpoints

- `POST /decrypt-seed` - Decrypt encrypted seed
- `GET /generate-2fa` - Generate current 2FA code
- `POST /verify-2fa` - Verify 2FA code

## Technologies

- FastAPI (Python Web Framework)
- Cryptography (RSA/OAEP)
- PyOTP (TOTP)
- Docker & Docker Compose
- Cron (scheduled tasks)
