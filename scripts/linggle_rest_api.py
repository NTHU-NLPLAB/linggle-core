#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from starlette.responses import UJSONResponse
from fastapi import FastAPI
from pydantic import BaseModel

from .linggle_database import linggle_it


class LinggleQuery(BaseModel):
    query: str
    time: int = None
    result: list = None
    total: int = 0


app = FastAPI()


@app.get("/ngram/{cmd}", response_class=UJSONResponse)
def get_ngram(cmd: str, time: int = None):
    cmd = cmd.strip()
    ngrams = linggle_it(cmd) if cmd else []
    total = sum(map(itemgetter(-1), ngrams))
    res = {'query': cmd, 'result': ngrams, 'total': total}
    if time:
        res['time'] = time
    return res


@app.post("/ngram/", response_class=UJSONResponse)
def get_ngram_post(res: LinggleQuery):
    res = res.query.strip()
    res.result = linggle_it(res.query) if res.query else []
    res.total = sum(map(itemgetter(-1), res.result))
    return res
