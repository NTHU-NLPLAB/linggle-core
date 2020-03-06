#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import groupby


def uniq_count(items):
    for item, entries in groupby(items):
        yield item, sum(1 for _ in entries)


def ngramcount_reduce(ngrams, min_count=2):
    return filter(lambda item: item[1] >= min_count, uniq_count(ngrams))


if __name__ == '__main__':
    import fileinput
    iterable = map(str.strip, fileinput.input())
    for items in ngramcount_reduce(iterable):
        print(*items, sep='\t')

# similar to:
# uniq -c
