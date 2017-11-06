#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request

from linggle_postgres import PostgresLinggle

app = Flask(__name__)
miniLinggle = PostgresLinggle()

ERROR_MESSAGE = {"message": "Some problems occurred, please try again later"}


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


if __name__ == "__main__":
    app.run()
