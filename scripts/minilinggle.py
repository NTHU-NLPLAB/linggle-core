#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from operator import itemgetter

from linggle.database import Web1tLinggle as Linggle

app = Flask(__name__)
miniLinggle = None

ERROR_MESSAGE = {"message": "Some problems occurred, please try again later"}


def init_linggle():
    global miniLinggle
    miniLinggle = Linggle()


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
        result = {'query': query, 'result': ngrams, 'total': sum(map(itemgetter(-1), ngrams))}
        return result
    else:
        return {'query': query, 'result': []}


init_linggle()


if __name__ == "__main__":
    app.run()
