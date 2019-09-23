#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter
from itertools import groupby
from operator import itemgetter


def parse_line(line):
    query, count, ngram = line.strip().split('\t')
    return query, int(count), ngram


def linggle_reduce(iterable):
    # group values with the same query
    for query, results in groupby(iterable, key=itemgetter(0)):
        counter = Counter()
        for _, count, ngram in results:
            counter[ngram] += count
        yield query, counter.most_common(50)


if __name__ == '__main__':
    import fileinput
    import sys
    import json
    import csv
    iterable = map(parse_line, fileinput.input())
    spamwriter = csv.writer(sys.stdout, delimiter='\t')
    for query, result in linggle_reduce(iterable):
        spamwriter.writerow([query, json.dumps(result, ensure_ascii=False)])
