#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from itertools import groupby
import spacy
import sys
import os
import io


nlp = None


def ngram_is_valid(ngram):
    if any(token.is_punct or token.is_digit for token in ngram):
        return False
    return True


def to_ngrams(doc, n):
    for i in range(len(doc)-n+1):
        yield doc[i:i+n]


def sentence_to_ngrams(doc):
    for n in range(1, 6):
        for ngram in to_ngrams(doc, n):
            if ngram_is_valid(ngram):
                yield ngram


def normalize_sent(sent):
    return ' '.join(sent.split())


def map_ngrams(iterable):
    def chunk_str(token):
        if token.i+1 in invalid_bound:
            return ''
        elif token.i in np_head_i:
            return 'NP'
        else:
            return token.tag_

    # iterable = fileinput.input()
    for sent in map(normalize_sent, iterable):
        doc = nlp(sent)
        np_head_i = {chunk.end-1 for chunk in doc.noun_chunks}
        invalid_bound = {i for chunk in doc.noun_chunks
                         for i in range(chunk.start+1, chunk.end)}

        for ngram in sentence_to_ngrams(doc):
            ngram_str = ngram.text.strip()
            npos_str = ' '.join(token.tag_ for token in ngram)
            nchunk_str = ''
            if not(ngram.start in invalid_bound or ngram.end in invalid_bound):
                nchunk_str = ' '.join(chunk_str(token) for token in ngram)

            yield ngram_str, npos_str, nchunk_str


def parse_reduce_input(line):
    line = line.strip('\r\n')
    # [tuple(item.split(' ')) for item in line.split('\t')]
    ngram, npos, nchunk = line.split('\u3000')
    return ngram, npos, nchunk


def reduce_ngrams(ngrams):
    # info = Counter()
    for (ngram, npos, nchunk), items in groupby(ngrams):
        count = sum(1 for _ in items)
        yield ngram, npos, nchunk, count
        # for _, npos, nchunk in items:
        #     info[npos, nchunk] += 1
        # for (npos, nchunk), count in info.most_common():
        #     print(ngram, npos, nchunk, count, sep='\t')
        # info.clear()


def do_map():
    iterable = io.open(sys.stdin.fileno(), 'rt')
    for ngram, npos, nchunk in map_ngrams(iterable):
        print(ngram, npos, nchunk, sep='\u3000')


def do_reduce():
    iterable = io.open(sys.stdin.fileno(), 'rt')
    ngrams = map(parse_reduce_input, iterable)
    for ngram, npos, nchunk, count in reduce_ngrams(ngrams):
        print(ngram, npos, nchunk, count, sep='\t')
        # for _, npos, nchunk in items:
        #     info[npos, nchunk] += 1
        # for (npos, nchunk), count in info.most_common():
        #     print(ngram, npos, nchunk, count, sep='\t')
        # info.clear()
    # uniq -c


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''

    if mode == 'map':
        # load spacy model
        nlp = spacy.load(os.environ.get('SPACY_MODEL', 'en'))
        do_map()
    elif mode == 'reduce':
        do_reduce()
    else:
        from collections import Counter
        nlp = spacy.load(os.environ.get('SPACY_MODEL', 'en'))
        iterable = io.open(sys.stdin.fileno(), 'rt')
        ngram_count = Counter(map_ngrams(iterable))
        for (ngram, npos, nchunk), count in ngram_count.most_common():
            print(ngram, npos, nchunk, count, sep='\t')
