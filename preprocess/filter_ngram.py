#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

ITEM_RE = re.compile(r'\(([^()]+)\)?')

numbers = set('0123456789０１２３４５６７８９')
eng_symbols = set('{}"\'()[].,:;+!?-*/&|<>=~$%\n\t ')
ch_symbols = set('｛｝「」『』【】（）〔〕，。：；＋！？﹖——＊７｜＜＞《》〈〉＝～＄％、')
black_list = numbers | eng_symbols | ch_symbols


def ngram_is_valid(ngram):
    return all(ITEM_RE.findall(token) for token in ngram.split())


if __name__ == "__main__":
    import fileinput
    for line in map(str.strip, fileinput.input()):
        ngram, _ = line.split('\t', 1)
        if ngram_is_valid(ngram):
            print(line)
