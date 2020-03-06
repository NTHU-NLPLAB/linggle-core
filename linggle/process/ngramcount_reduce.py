#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import groupby


def uniq_count(items):
    for item, entries in groupby(items):
        yield item, sum(1 for _ in entries)


def ngramcount_reduce(ngrams, prune_threshold=2):
    for item, count in uniq_count(ngrams):
        if count > prune_threshold:
            yield item, count


if __name__ == '__main__':
    import fileinput
    iterable = map(str.strip, fileinput.input())
    for items in ngramcount_reduce(iterable):
        print(*items, sep='\t')
