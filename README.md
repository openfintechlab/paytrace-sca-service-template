# paytrace-sca-service-template
Service Template for Service Component exposing APIs

## Routes and Environment

Routes are defined in `src/routes/Routes.py` and registered in `src/main.py` with `app.include_router(Routes().router)`. The route class builds a common prefix for every endpoint using two environment variables:

- `OFTL_SCA_CONTEXT_ROOT` for the base context path (example: `/paytrace/sca`)
- `OFTL_SCA_VERSION` for the API version (example: `1` becomes `/v1`)

Combined, the prefix becomes `${OFTL_SCA_CONTEXT_ROOT}/v${OFTL_SCA_VERSION}`. The boilerplate includes:

- `GET /` (root status)
- `GET /_healthz`
- `GET /_probe`

Example `.env`:

```dotenv
OFTL_SCA_CONTEXT_ROOT=/paytrace/sca
OFTL_SCA_VERSION=1
```

Example curl:

```bash
curl http://localhost:8081/paytrace/sca/v1/
```

## Install dependencies

```bash
uv pip install -e .
```

## Run test cases

Install test dependency:

```bash
uv pip install pytest
```

Run only `ConfigLoader` tests:

```bash
python -m pytest tests/test_config_loader.py -v
```

Run all tests:

```bash
python -m pytest tests -v
```
