# Buildable Chatbot

A FastAPI chatbot using LangGraph, Groq, Redis caching, Redis-backed rate limiting, and PostgreSQL.

## Requirements

- Docker Desktop with Docker Compose
- A Groq API key
- A LangSmith API key only if tracing is enabled

## Run with Docker

1. Copy `.env.example` to `.env`.
2. Add your real API keys to `.env`.
3. Start the application:

```bash
docker compose up --build
```

The API is available at `http://localhost:8123`.

- Swagger UI: `http://localhost:8123/docs`
- Health check: `http://localhost:8123/health`
- Chat endpoint: `POST http://localhost:8123/chat`

PostgreSQL is available to the app at the Compose hostname `postgres`. From your
host machine, database tools can connect to `localhost:5432` with database
`chatbot`, user `chatbot`, and password `chatbot_password`.

Example request:

```bash
curl -X POST http://localhost:8123/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"Hello\"}"
```

On macOS/Linux, use `\\` instead of `^` for multiline shell commands, or put the curl command on one line.

Stop the services with:

```bash
docker compose down
```

Do not start only the app container from Docker Desktop. Compose is required because the app and Redis must share a Docker network.

## Local tests

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python -m compileall .
```

The test suite mocks Groq and Redis boundaries, so tests do not require API keys or a running Redis server.

## GitHub Actions

The workflow in `.github/workflows/ci.yml` runs on pushes to `main` or `master` and on pull requests. It:

- installs Python dependencies
- compiles the Python source
- runs the API tests
- builds the Docker image

API keys are not needed in GitHub Actions for the current tests. Never commit `.env`; use GitHub Actions secrets for future integration tests or deployments.
