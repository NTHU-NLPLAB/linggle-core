#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple
import requests
import urllib

NGRAM_API_URI = "https://{0}.linggle.com/query/"
EXP_API_URI = "https://{0}.linggle.com/example/"


NgramResult = namedtuple("NgramResult", ["query", "ngrams", "total"])


class LinggleAPI(dict):
    # ver: Version can be `www`, `coca`, `cna`, `udn`, `zh`
    def __init__(self, ver='www'):
        self.ngram_api = NGRAM_API_URI.format(ver)
        self.example_api = EXP_API_URI.format(ver)

    def __getitem__(self, query):
        return self.query(query)

    def query(self, query):
        query = query.replace('/', '@')
        query = urllib.parse.quote(query, safe='')
        req = requests.get(self.ngram_api + query)
        if req.status_code == 200:
            return NgramResult(**req.json())

    def get_example(self, ngram_str):
        req = requests.post(self.example_api, json={'ngram': ngram_str})
        if req.status_code == 200:
            result = req.json()
            return result.get("examples", [])


if __name__ == "__main__":
    linggle = LinggleAPI()

    result = linggle["adj. beach"]
    print("Total:", result.total)
    for ngram, count in result.ngrams[:3]:
        print(ngram, count)
    for sent in linggle.get_example("sandy beach")[:3]:
        print(sent)

    linggle = LinggleAPI('zh')
    for ngram, count in linggle.query("提出 n.").ngrams[:3]:
        print(ngram, count)
    for sent in linggle.get_example("提出 報告")[:3]:
        print(sent)
