#!/usr/bin/env python
# -*- coding: utf-8 -*-
from starlette.responses import UJSONResponse
from fastapi import FastAPI, Header
from pydantic import BaseModel
import logging

from .linggle_database import linggle_it


class LinggleQuery(BaseModel):
    query: str
    time: int = None
    ngrams: list = None


app = FastAPI()
logger = logging.getLogger('uvicorn.access')


@app.get("/ngram/{cmd:path}", response_class=UJSONResponse)
def get_ngram(cmd: str, time: int = None, usertokenid: str = Header(None)):
    return get_ngram_post(LinggleQuery(query=cmd, time=time), usertokenid=usertokenid)


@app.post("/ngram/", response_class=UJSONResponse)
def get_ngram_post(res: LinggleQuery, usertokenid: str = Header(None)):
    res.query = res.query.strip()
    res.ngrams = linggle_it(res.query) if res.query else []
    if usertokenid:
        logger.info(f"[QUERY] {usertokenid}: {res.query}")
    return res
