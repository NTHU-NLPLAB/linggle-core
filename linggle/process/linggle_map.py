#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import product
import re


ITEM_RE = re.compile(r'\(([^()]+)\)?')
WILDCARDS = (' _ ',)


def is_wildcard(token):
    return token in WILDCARDS or token.endswith('.')


def to_indice(token):
    yield ' _ '
    end = 0
    for match in ITEM_RE.finditer(token):
        if end < match.start():
            yield token[end:match.start()]
        yield f' {match.group(1)} '
        end = match.end()
    if end < len(token):
        yield token[end:]


def to_linggle_query(ngram, delim=' '):
    candidates = [list(to_indice(token)) for token in ngram.split()]
    for tokens in product(*candidates):
        # skip queries consisting of wildcards only
        # if not all(is_wildcard(token) for token in tokens):
        # remove redundant spaces
        yield ' '.join(delim.join(tokens).split())


def linggle_map(iterable):
    for line in iterable:
        ngram, count = line.rstrip().split('\t')
        for query in to_linggle_query(ngram):
            yield query, ngram, count


if __name__ == '__main__':
    # import sys
    # import io
    # for line in io.open(sys.stdin.fileno(), 'rt'):
    import fileinput
    for items in linggle_map(fileinput.input()):
        print(*items, sep='\t')
