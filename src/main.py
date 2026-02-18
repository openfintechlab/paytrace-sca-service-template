# -*- coding: utf-8 -*-
"""
Copyright 2026-2028 openfintechlab.com, Inc. All rights reserved.
Licenses: LICENSE.md
Description: Service Template / starter code for PayTrace SCA Service build on fastapi.
Reference: https://github.com/openfintechlab/pytrace-backlogs/issues/12
"""

from fastapi import FastAPI
from routes.Routes import Routes
from utilities.Logging import Logging
import uvicorn

app = FastAPI()
routes = Routes()
app.include_router(routes.router)
app.include_router(routes.public_router)


# @app.get("/")
# async def root() -> dict[str, str]:
#     return {"status": "ok"}


if __name__ == "__main__":
    Logging.info("Starting PayTrace SCA Service...")
    uvicorn.run(app, host="0.0.0.0", port=8081)
