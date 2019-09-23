#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import groupby


def uniq_count(items):
    for item, entries in groupby(items):
        yield item, sum(1 for _ in entries)


def main(iterable):
    ngrams = map(str.strip, iterable)
    for item, count in uniq_count(ngrams):
        if count > 1:
            print(item, count, sep='\t')


if __name__ == '__main__':
    import fileinput
    main(fileinput.input())
