#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from flask import Flask, jsonify, request

from linggle.database import CassandraLinggle as Linggle

app = Flask(__name__)
miniLinggle = None

ERROR_MESSAGE = {"message": "Some problems occurred, please try again later"}
SIM_API_URL = "http://nlp-ultron.cs.nthu.edu.tw:9888/{0}"


def get_similar_words(word):
    r = requests.get(SIM_API_URL.format(word))
    if r.ok:
        for sim in r.json():
            yield sim
    else:
        return []


def init_linggle():
    global miniLinggle
    miniLinggle = Linggle(find_synonyms=get_similar_words)


@app.route("/query/<query>", methods=['GET'])
def linggle_get(query):
    result = linggleit(query)
    if result:
        return jsonify(result)
    return jsonify(ERROR_MESSAGE)


@app.route("/query", methods=['POST'])
def linggle_post():
    return linggle_get(request.json.get('query', ''))


def linggleit(query):
    query = query.strip()
    if query:
        ngrams = miniLinggle[query]
        result = {'query': query, 'result': ngrams}
        return result
    else:
        return {'query': query, 'result': []}


init_linggle()
if __name__ == "__main__":
    app.run()
