# Newsletter Microservices

## Description

A microservices application for user management and email distribution.
It consists of two main services:
- **user_management_service** — user management service (Django + PostgreSQL)
- **mailer_service** — mailing service (FastAPI)

The services interact via Kafka.

## Project Structure

- `user_management_service/` — user management service (Django)
- `mailer_service/` — mailing service (FastAPI)
- `docker/` — Dockerfiles and docker-compose.yaml for launching all services

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yarickFullbody/newsletter
   cd newsletter
   ```

2. Start all services:
   ```bash
   docker compose -f docker/docker-compose.yaml up --build
   ```

3. The services will be available at:
   - Django (user_management_service): http://localhost:8000
   - FastAPI (mailer_service): http://localhost:8001

## Service Description

### user_management_service

- Framework: Django 4.2
- Database: PostgreSQL
- Dependencies: see `user_management_service/requirements.txt`
- Launch: automatically via Docker

### mailer_service

- Framework: FastAPI
- Launch: automatically via Docker (Uvicorn)
- Dependencies: see `mailer_service/requirements.txt`

### Infrastructure

- **PostgreSQL** — user data storage
- **Kafka + Zookeeper** — message exchange between services

## Environment Variables

Use environment variables to configure the services (see examples in docker-compose.yaml and settings.py).
