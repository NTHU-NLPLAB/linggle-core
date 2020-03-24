#!/usr/bin/env python
# -*- coding: utf-8 -*-
numbers = set('0123456789０１２３４５６７８９')
eng_symbols = set('{}"\'()[].,:;+!?-*/&|<>=~$%\n\t ')
ch_symbols = set('｛｝「」『』【】（）〔〕，。：；＋！？﹖——＊７｜＜＞《》〈〉＝～＄％、')
black_list = numbers | eng_symbols | ch_symbols


def text_till(text, sep='(', start=0):
    i = text.find(sep, start)
    return '' if i < 0 else text[:i]


def ngram_is_valid(ngram):
    return all(text_till(token, start=1).strip() not in black_list for token in ngram)


if __name__ == "__main__":
    import fileinput
    for line in map(str.strip, fileinput.input()):
        ngram, _ = line.split('\t', 1)
        if ngram_is_valid(ngram):
            print(line)