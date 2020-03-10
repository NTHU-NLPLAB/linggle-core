#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodedata

numbers = set('0123456789０１２３４５６７８９')
eng_symbols = set('{}"\'()[].,:;+!?-*/&|<>=~$%\n\t ')
ch_symbols = set('｛｝「」『』【】（）〔〕，。：；＋！？﹖——＊７｜＜＞《》〈〉＝～＄％、')
black_list = numbers | eng_symbols | ch_symbols
black_list.add('')


def text_till(text, sep='(', start=0):
    i = text.find(sep, start)
    return '' if i < 0 else text[:i]


def ngram_is_valid(ngram):
    return all(text_till(token, start=1).strip() not in black_list for token in ngram)


def gen_ngrams(items, max_len=5):
    for n in range(1, max_len+1):
        for ngram in zip(*(items[i:] for i in range(n))):
            yield ngram


def line_is_valid(line):
    return all(unicodedata.category(ch)[0] != "C" for ch in line.strip())


def ngramcount_map(lines):
    lines = map(line_is_valid, lines)
    for tokens in map(str.split, lines):
        ngrams = gen_ngrams(tokens)
        # comment the following line if you don't want filtering
        ngrams = filter(ngram_is_valid, ngrams)
        for ngram in ngrams:
            yield ngram


if __name__ == '__main__':
    import fileinput
    for ngram in ngramcount_map(fileinput.input()):
        print(*ngram)
