# paytrace-sca-service-template
Service Template for Service Component exposing APIs

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
