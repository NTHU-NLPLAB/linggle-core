#!/usr/bin/env python
# -*- coding: utf-8 -*-
from starlette.responses import UJSONResponse
from fastapi import FastAPI
from pydantic import BaseModel

from .linggle_database import linggle_it


class LinggleQuery(BaseModel):
    query: str
    time: int = None
    ngrams: list = None


app = FastAPI()


@app.get("/ngram/{cmd:path}", response_class=UJSONResponse)
def get_ngram(cmd: str, time: int = None):
    return get_ngram_post(LinggleQuery(query=cmd, time=time))


@app.post("/ngram/", response_class=UJSONResponse)
def get_ngram_post(res: LinggleQuery):
    res.query = res.query.strip()
    res.ngrams = linggle_it(res.query) if res.query else []
    return res
