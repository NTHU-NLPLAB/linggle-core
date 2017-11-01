#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import Flask, jsonify, request

from linggle_postgres import PostgresLinggle

app = Flask(__name__)
miniLinggle = PostgresLinggle()

ERROR_MESSAGE = {"message": "Some problems occurred, please try again later"}


@app.route("/", methods=['GET'])
def index():
    search = request.args.get('search', '')
    if search:
        return jsonify(linggleit(search))
    return "mini linggle api: \/?=<query>"


@app.route("/query", methods=['POST'])
@app.route("/query/<query>", methods=['GET'])
def linggle(query):
    if request.method == 'POST':
        query = request.form.get('query', '')

    result = linggleit(query)
    return jsonify(result)


def linggleit(query):
    ngrams = miniLinggle[query]
    result = {'query': query, 'result': ngrams}
    return result


if __name__ == "__main__":
    app.run()
