#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request

from .linggle_database import linggle_it

app = Flask(__name__)

ERROR_MESSAGE = {"message": "Some problems occurred, please try again later"}


@app.route("/query/<query>", methods=['GET'])
def linggle_get(query):
    result = linggle_it(query)
    if result:
        return jsonify(result)
    return jsonify(ERROR_MESSAGE)


@app.route("/query/", methods=['POST'])
def linggle_post():
    if request.json:
        return linggle_get(request.json.get('query', ''))
    elif request.form:
        return linggle_get(request.form.get('query', ''))
    return jsonify(ERROR_MESSAGE)


if __name__ == "__main__":
    app.run()
