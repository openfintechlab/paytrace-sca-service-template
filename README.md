# PayTrace SCA Service Template

## Introduction

`paytrace-sca-service-template` is the reusable FastAPI starter for PayTrace API services. It provides the common bootstrap pattern for route registration, configuration loading, logging, PostgreSQL startup validation, and public health/probe endpoints.

In the PayTrace architecture, this template is the foundation for HTTP-facing services that need to follow the standard PayTrace route prefix, response envelope, environment naming, and operational health-check conventions. New SCA services should start here so they inherit consistent service shape before adding domain-specific routes.

The implementation includes:

- Service bootstrap with FastAPI lifecycle hooks
- Centralized configuration loading from environment variables and `.env`
- PostgreSQL connection initialization through SQLAlchemy
- Base health/probe routes
- Test scaffolding with `pytest`

## Project Structure

```text
src/
  main.py                 # Service entrypoint and startup lifecycle
  routes/Routes.py        # API route registration and default endpoints
  utilities/ConfigLoader.py
  utilities/DBHelper.py
  utilities/Logging.py
tests/
  test_routes.py
  test_config_loader.py
```

## Prerequisites

- Python 3.11+ (recommended)
- `uv` installed
- PostgreSQL available for runtime startup checks

## Quick Start

### 1. Create local environment file

Copy the template environment file and edit values:

```bash
cp .env.example .env
```

Essential variables should be copied from `.env.example` and updated for your environment.

### 2. Install dependencies

From the template root:

```bash
uv sync
```

If you want to install as an editable package instead:

```bash
uv pip install -e .
```

### 3. Run the service

```bash
uv run python src/main.py
```

## Docker

### 1. Build the container image

From the template root (`paytrace-sca-service-template`):

```bash
docker build -t paytrace-sca-service-template:latest .
```

The Dockerfile uses build arguments for its base images. Defaults are safe for local builds:

```text
DOCKER_PYTHON_BUILDER_IMAGE=dhi.io/python:3-debian13-sfw-dev
DOCKER_PYTHON_RUNTIME_IMAGE=dhi.io/python:3
```

Override them when needed:

```bash
docker build \
  --build-arg DOCKER_PYTHON_BUILDER_IMAGE=dhi.io/python:3-debian13-sfw-dev \
  --build-arg DOCKER_PYTHON_RUNTIME_IMAGE=dhi.io/python:3 \
  -t paytrace-sca-service-template:latest .
```

The GitHub Docker build workflow reads the same values from GitHub Actions variables named `DOCKER_PYTHON_BUILDER_IMAGE` and `DOCKER_PYTHON_RUNTIME_IMAGE`, falling back to the defaults above when the variables are not set. Published images use the Docker Hub repository `openfintechlab/paytrace-sca-service-template`.

Commit message controls:

- `[build docker]` builds the image.
- `[buildandpush docker]` builds and pushes the image.

### 2. Run the container

Use the following command pattern to run the service with required environment variables:

```bash
docker run -d \
  --name paytrace-sca-service-template \
  -p 8081:8081 \
  -e OFTL_SCA_CONTEXT_ROOT="/sca" \
  -e OFTL_SCA_VERSION="1" \
  -e OFTL_SCA_HOST="0.0.0.0" \
  -e OFTL_SCA_PORT="8081" \
  -e OFTL_LOG_LEVEL="INFO" \
  -e OFTL_LOG_FORMAT="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s" \
  -e OFTL_POSTGRESDB_USERNAME="admin" \
  -e OFTL_POSTGRESDB_PASSWORD="[CHANGE ME]" \
  -e OFTL_POSTGRESDB_HOST="host.docker.internal" \
  -e OFTL_POSTGRESDB_PORT="5432" \
  -e OFTL_POSTGRESDB_NAME="paytrace" \
  paytrace-sca-service-template:latest
```

Or use a `.env` file with `--env-file`:

```bash
docker run -d \
  --name paytrace-sca-service-template \
  -p 8081:8081 \
  --env-file .env \
  paytrace-sca-service-template:latest
```

### 3. Verify container and endpoints

```bash
docker logs -f paytrace-sca-service-template
curl http://localhost:8081/sca/v1/
curl http://localhost:8081/_healthz
curl http://localhost:8081/_probe
```

## Service Processing Flow

1. `src/main.py` loads `OFTL_*` configuration and initializes logging.
2. The FastAPI application starts with lifecycle hooks.
3. Startup validates PostgreSQL connectivity through `DBHelper`.
4. `src/routes/Routes.py` registers the versioned root route.
5. Public health endpoints remain available at `/_healthz` and `/_probe`.
6. Uvicorn serves the API on `OFTL_SCA_HOST:OFTL_SCA_PORT`.

## Configuration Reference

The core uses the following environment variables:

### Service Routing

- `OFTL_SCA_CONTEXT_ROOT`: Base API path (example: `/sca`)
- `OFTL_SCA_VERSION`: API version segment (example: `1`, exposed as `/v1`)
- `OFTL_SCA_HOST`: Bind host for Uvicorn (default fallback in code: `0.0.0.0`)
- `OFTL_SCA_PORT`: Bind port for Uvicorn (default fallback in code: `8081`)

Final route prefix is:

```text
${OFTL_SCA_CONTEXT_ROOT}/v${OFTL_SCA_VERSION}
```

Example with defaults in `.env.example`:

```text
/sca/v1
```

### Logging

- `OFTL_LOG_LEVEL`: Logger/Uvicorn log level (`INFO`, `DEBUG`, etc.)
- `OFTL_LOG_FORMAT`: Python logging format string

### Database (Required for startup DB initialization)

- `OFTL_POSTGRESDB_USERNAME`
- `OFTL_POSTGRESDB_PASSWORD`
- `OFTL_POSTGRESDB_HOST`
- `OFTL_POSTGRESDB_PORT`
- `OFTL_POSTGRESDB_NAME`

Optional:

- `OFTL_POSTGRESDB_POOLSIZE`: SQLAlchemy pool size (default: `10`)

## API Routes

Registered in `src/routes/Routes.py`:

- `GET /` under the versioned service prefix (for example: `GET /sca/v1/`)
- `GET /_healthz` (public)
- `GET /_probe` (public)

Quick check:

```bash
curl http://localhost:8081/sca/v1/
curl http://localhost:8081/_healthz
curl http://localhost:8081/_probe
```

## Create a New Route

Add new route handlers inside `Routes._register_routes` in `src/routes/Routes.py`.

Example:

```python
@self.router.get("/transactions/ping")
async def transactions_ping() -> dict[str, str]:
    return {"service": "transactions", "status": "ok"}
```

With `OFTL_SCA_CONTEXT_ROOT=/sca` and `OFTL_SCA_VERSION=1`, this route becomes:

```text
GET /sca/v1/transactions/ping
```

## Testing

Run all tests:

```bash
uv run pytest tests -v
```

Run specific tests:

```bash
uv run pytest tests/test_config_loader.py -v
uv run pytest tests/test_routes.py -v
```

## Major Libraries Used

- `fastapi`: API framework
- `uvicorn`: ASGI server
- `pydantic`: data validation (FastAPI ecosystem)
- `environs`: environment variable parsing/loading
- `sqlalchemy`: database engine and ORM utilities
- `psycopg2-binary`: PostgreSQL driver
- `pytest`: test framework
- `httpx`: HTTP client used in test/runtime scenarios
