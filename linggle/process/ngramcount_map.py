#!/usr/bin/env python
# -*- coding: utf-8 -*-


def gen_ngrams(items, max_len=5):
    for n in range(1, max_len+1):
        for ngram in zip(*(items[i:] for i in range(n))):
            yield ngram


def ngramcount_map(lines):
    for tokens in map(str.split, lines):
        for ngram in gen_ngrams(tokens):
            yield ngram


if __name__ == '__main__':
    import fileinput
    for ngram in ngramcount_map(fileinput.input()):
        print(*ngram)
