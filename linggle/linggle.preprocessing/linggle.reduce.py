#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import sys
# import io
import json
import csv
import fileinput
# from collections import Counter
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
try:
    from itertools import imap as map
except:
    pass


def parse_line(line):
    query, count, ngram = line.strip().split('\t')
    return query, int(count), ngram


if __name__ == '__main__':
    # iterable = map(parse_line, fileinput.input())
    iterable = map(parse_line, fileinput.input())
    # group values with the same query
    spamwriter = csv.writer(sys.stdout, delimiter='\t')
    for query, results in groupby(iterable, key=itemgetter(0)):
        # counter = Counter()
        counter = defaultdict(int)
        for _, count, ngram in results:
            counter[ngram] += count

        result = sorted(counter.items(), key=itemgetter(1), reverse=True)[:50]
        if result:
            spamwriter.writerow([query, json.dumps(result, ensure_ascii=False)])
            # print(query, json.dumps(result), sep='\t')
        # print(query.encode('utf-8'), json.dumps(result))
        # print(query, end='')
        # print(query.encode('utf-8'), end='')
        # for result, count in counter.most_common(50):
        #     # print('\t{0} {1}'.format(result, count), end='')
        #     print('\t{0} {1}'.format(result, count).encode('utf-8'), end='')
        # print()
