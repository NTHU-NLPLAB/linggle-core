#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import groupby


def uniq_count(items):
    for item, entries in groupby(items):
        yield item, sum(1 for _ in entries)


def ngramcount_reduce(ngrams, min_count=2):
    ngramcounts = uniq_count(ngrams)
    return filter(lambda item: item[1] >= min_count, ngramcounts)


if __name__ == '__main__':
    import fileinput
    iterable = map(str.strip, fileinput.input())
    for items in ngramcount_reduce(iterable):
        print(*items, sep='\t')

# similar to:
# LC_ALL=C uniq -c | LC_ALL=C awk '{ if ($1 > 2) print $0 }'
# use awk to produce to the same format
# LC_ALL=C uniq -c | LC_ALL=C awk '{c=$1; $1=""; if (c > 2) print $0 "\t" c }'
