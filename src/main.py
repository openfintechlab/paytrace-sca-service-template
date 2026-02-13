# -*- coding: utf-8 -*-
"""                                                ___  _        _             _    _       _   
 ___  ___  ___ ._ _ | | '<_>._ _ _| |_ ___  ___ | |_ | | ___ | |_ 
/ . \| . \/ ._>| ' || |- | || ' | | | / ._>/ | '| . || |<_> || . \
\___/|  _/\___.|_|_||_|  |_||_|_| |_| \___.\_|_.|_|_||_|<___||___/
     |_|                                                          
                                                                                             
                           
Copyright 2026-2028 openfintechlab.com, Inc. All rights reserved.
Licenses: LICENSE.md
Description: Service Template / starter code for PayTrace SCA Service build on fastapi.
Reference: https://spiretech.atlassian.net/jira/software/projects/SIN/boards/13/backlog?selectedIssue=SIN-1746
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
