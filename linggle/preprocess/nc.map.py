#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fileinput

numbers = set('0123456789０１２３４５６７８９')
eng_symbols = set('{}"\'()[].,:;+!?-*/&|<>=~$%\n\t ')
ch_symbols = set('｛｝「」『』【】（）〔〕，。：；＋！？﹖——＊７｜＜＞《》〈〉＝～＄％、')
black_list = numbers | eng_symbols | ch_symbols


def ngram_is_valid(ngram):
    return all(token not in black_list for token in ngram)


def to_ngrams(items, length):
    return zip(*(items[i:] for i in range(length)))


def ngram_count_map(items, max_len=5):
    for i in range(1, max_len+1):
        for ngram in to_ngrams(items, i):
            yield ngram


def read_text(iterable):
    for line in iterable:
        line = line.strip()
        # <P>, </P>, </HEADLINE>, <DATELINE>, ...
        if line.startswith('<') and line.endswith('>'):
            continue
        else:
            yield line.split()


def main():
    for tokens in read_text(fileinput.input()):
        ngrams = ngram_count_map(tokens)
        for ngram in filter(ngram_is_valid, ngrams):
            print(*ngram)


if __name__ == '__main__':
    main()
