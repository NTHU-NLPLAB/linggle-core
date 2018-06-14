#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from itertools import groupby
# import fileinput
import string
import spacy
import sys
import os
import io

from linggle.parse import parse_coca_text

numbers = set('0123456789０１２３４５６７８９')
ch_symbols = set('｛｝「」『』【】（）〔〕，。：；＋！？﹖——＊７｜＜＞《》〈〉＝～＄％、')
ALL_SYMBOLS = set(string.punctuation) | ch_symbols

nlp = None


def spacy_parse(sent):
    for token in nlp(sent):
        yield token.text, token.tag_


def ngram_is_valid(ngram):
    if any(word in ALL_SYMBOLS or word in numbers for word in ngram):
        return False
    return True


def tokens_to_ngrams(tokens, length):
    return zip(*([tokens[i:] for i in range(length)]))


def to_tokens(sent, pos_abbr=lambda x: x, tokenizer=spacy_parse):
    for word, tag in tokenizer(sent):
        tag = pos_abbr(tag)
        yield word, tag


def sentence_to_ngrams(sent):
    tokens = list(to_tokens(sent))

    for n in range(1, 6):
        for ngram_tags in tokens_to_ngrams(tokens, n):
            ngram, tags = list(zip(*ngram_tags))
            if ngram_is_valid(ngram):
                yield ngram


def map():
    # iterable = fileinput.input()
    iterable = io.open(sys.stdin.fileno(), 'rt')
    for sent in parse_coca_text(iterable):
        for ngram in sentence_to_ngrams(sent):
            print(' '.join(ngram))


def reduce():
    # py2
    # iterable = fileinput.input()
    iterable = io.open(sys.stdin.fileno(), 'rt')
    for line, lines in groupby(iterable):
        count = sum(1 for _ in lines)
        print(line.strip(), count, sep='\t')
    # uniq -c


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''

    if mode == 'map':
        # load spacy model
        nlp = spacy.load(os.environ.get('SPACY_MODEL', 'en'))
        for ngram in map():
            print(ngram)
    elif mode == 'reduce':
        reduce()
    else:
        pass
        # from collections import Counter
        # for ngram, count in Counter(map()).most_common():
        #     print(ngram, count, sep='\t')
