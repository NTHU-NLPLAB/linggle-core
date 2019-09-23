#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import groupby


def ngram_count(items):
    for line, lines in groupby(items):
        yield line, sum(1 for _ in lines)


if __name__ == '__main__':
    import fileinput
    ngrams = map(str.strip, fileinput.input())
    for item, count in ngram_count(ngrams):
        if count > 1:
            print(item, count, sep='\t')
