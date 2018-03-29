#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from itertools import product
from operator import itemgetter
import fileinput
import sys
import io


if __name__ == '__main__':
    for line in fileinput.input():
    # for line in io.open(sys.stdin.fileno(), 'rt'):
        try:
            wordtags, count = line.rstrip().split('\t')
            # print(count)

            # count = int(count)
            # if count < 3:
                # continue

            items = wordtags.split()
            split_index = len(items) // 2
            words, tags = items[:split_index], items[split_index:]
            ngramstr = ' '.join(words)

            candidates = [[word, ' {0}. '.format(tag), ' _ '] for word, tag in zip(words, tags)]
            for tokens in product(*candidates):
                if any(token != ' _ ' and not token.endswith('. ') for token in tokens):
                    query = ' '.join(' '.join(tokens).strip().split())
                    print('{0}\t{1}\t{2}'.format(query, count, ngramstr))
                    # print('{0}\t{1}\t{2}'.format(query, count, ''.join(words)).encode('utf-8'))
        except:
            import sys
            print(line.rstrip(), file=sys.stderr)
