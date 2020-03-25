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


def to_linggle_query(tokens, delim=' '):
    candidates = [list(to_indice(token)) for token in tokens]
    for query_tokens in product(*candidates):
        # skip queries consisting of wildcards only
        # if not all(is_wildcard(token) for token in query_tokens):
        # remove redundant spaces
        yield ' '.join(delim.join(query_tokens).split())


def linggle_map(iterable):
    for line in iterable:
        ngram, count = line.strip().split('\t')
        tokens = ngram.split()
        ngram_text = ' '.join(token.split('(', 1)[0] if token.find('(', 1) else token for token in tokens)
        for query in to_linggle_query(tokens):
            if query != ngram_text:
                yield query, ngram_text, count


if __name__ == '__main__':
    import fileinput
    for items in linggle_map(fileinput.input()):
        print(*items, sep='\t')
