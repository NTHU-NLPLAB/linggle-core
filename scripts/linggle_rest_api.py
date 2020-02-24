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
    ngrams: list = None
    total: int = 0


app = FastAPI()


@app.get("/ngram/{cmd}", response_class=UJSONResponse)
def get_ngram(cmd: str, time: int = None):
    return get_ngram_post(LinggleQuery(query=cmd, time=time))


@app.post("/ngram/", response_class=UJSONResponse)
def get_ngram_post(res: LinggleQuery):
    res.query = res.query.strip()
    res.ngrams = linggle_it(res.query) if res.query else []
    # TODO: leave the total counting in the client side
    res.total = sum(map(itemgetter(-1), res.ngrams))
    return res
