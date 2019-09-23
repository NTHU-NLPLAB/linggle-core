#!/usr/bin/env python
# -*- coding: utf-8 -*-

numbers = set('0123456789０１２３４５６７８９')
eng_symbols = set('{}"\'()[].,:;+!?-*/&|<>=~$%\n\t ')
ch_symbols = set('｛｝「」『』【】（）〔〕，。：；＋！？﹖——＊７｜＜＞《》〈〉＝～＄％、')
black_list = numbers | eng_symbols | ch_symbols


def ngram_is_valid(ngram):
    return all(token not in black_list for token in ngram)


def to_ngrams(items, length):
    return zip(*(items[i:] for i in range(length)))


def gen_ngrams(items, max_len=5):
    for i in range(1, max_len+1):
        for ngram in to_ngrams(items, i):
            yield ngram


def main(iterable):
    lines = map(str.strip, iterable)
    for line in lines:
        ngrams = gen_ngrams(line.split())
        for ngram in filter(ngram_is_valid, ngrams):
            print(*ngram)


if __name__ == '__main__':
    import fileinput
    main(fileinput.input())
