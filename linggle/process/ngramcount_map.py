#!/usr/bin/env python
# -*- coding: utf-8 -*-

numbers = set('0123456789０１２３４５６７８９')
eng_symbols = set('{}"\'()[].,:;+!?-*/&|<>=~$%\n\t ')
ch_symbols = set('｛｝「」『』【】（）〔〕，。：；＋！？﹖——＊７｜＜＞《》〈〉＝～＄％、')
black_list = numbers | eng_symbols | ch_symbols


def ngram_is_valid(ngram):
    return all(token not in black_list for token in ngram)


def gen_ngrams(items, max_len=5):
    for n in range(1, max_len+1):
        for ngram in zip(*(items[i:] for i in range(n))):
            yield ngram


def main(iterable):
    for line in map(str.strip, iterable):
        ngrams = gen_ngrams(line.split())
        for ngram in filter(ngram_is_valid, ngrams):
            print(*ngram)


if __name__ == '__main__':
    import fileinput
    main(fileinput.input())
