#!/usr/bin/env python
# -*- coding: utf-8 -*-

numbers = set('0123456789０１２３４５６７８９')
eng_symbols = set('{}"\'()[].,:;+!?-*/&|<>=~$%\n\t ')
ch_symbols = set('｛｝「」『』【】（）〔〕，。：；＋！？﹖——＊７｜＜＞《》〈〉＝～＄％、')
black_list = numbers | eng_symbols | ch_symbols


def text_till(text, sep='('):
    i = text.find(sep, 1)
    return text if i < 0 else text[:i]


def ngram_is_valid(ngram):
    return all(text_till(token).strip() not in black_list for token in ngram)


def gen_ngrams(items, max_len=5):
    for n in range(1, max_len+1):
        for ngram in zip(*(items[i:] for i in range(n))):
            yield ngram


def ngramcount_map(lines, delimiter=None):
    for line in map(str.strip, lines):
        tokens = line.split(delimiter) if delimiter else line.split()
        ngrams = gen_ngrams(tokens)
        # comment the following line if you don't want filtering
        ngrams = filter(ngram_is_valid, ngrams)
        for ngram in ngrams:
            yield ngram


if __name__ == '__main__':
    import fileinput
    for ngram in ngramcount_map(fileinput.input()):
        print(*ngram)
