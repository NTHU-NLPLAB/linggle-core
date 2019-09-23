#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import product
import re


ITEM_RE = re.compile(r'\(([^()]+)\)?')


def to_indice(token):
    yield ' _ '
    end = 0
    for match in ITEM_RE.finditer(token):
        if end < match.start():
            yield token[end:match.start()]
        yield match.group(1)
        end = match.end()
    if end < len(token):
        yield token[end:]


def to_linggle_query(ngram, delim=' '):
    candidates = [list(to_indice(token)) for token in ngram.split()]
    for tokens in product(*candidates):
        if any(token != ' _ ' for token in tokens):
            yield delim.join(' '.join(tokens).split())


if __name__ == '__main__':
    # import sys
    # import io
    # for line in io.open(sys.stdin.fileno(), 'rt'):
    import fileinput
    for line in fileinput.input():
        ngram, count = line.rstrip().split('\t')
        for query in to_linggle_query(ngram):
            print(query, count, ngram, sep='\t')
