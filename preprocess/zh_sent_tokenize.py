#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
import fileinput
import re

PARENTHESES_START = set(r'(（﹙[［{｛<〔【〖「『《〈')
PARENTHESES_END = set(r')）﹚]］}｝>〕】〗」』》〉')
NEWSENT_TAGS = {
    # 'COLONCATEGORY',
    # 'COMMACATEGORY',
    # 'ETCCATEGORY',
    'EXCLAMATIONCATEGORY',
    # consider only '。'; not consider '．', '·', and '・'
    # 'PERIODCATEGORY',
    'QUESTIONCATEGORY',
    'SEMICOLONCATEGORY',
    # typo in tagged corpus
    'EXCLANATIONCATEGORY',
}
NEWSENT_PUNCT = tuple('。'.split(' '))

NEWSENT_SPLITTER_RE = re.compile("。|！|？")


def simple_zh_sent_tokenize(text):
    return NEWSENT_SPLITTER_RE.split(text)


def ckip_sent_tokenize(text):
    tokens = deque()
    newsent = False
    parentheses_level = 0

    for token in text.strip().split('\u3000'):
        # malformed token
        if '(' not in token or not token.endswith(')'):
            continue

        word, tag = token[:-1].rsplit('(', 1)
        word = word.strip()
        if word:
            tokens.append(f"{word}({tag})")

        if tag in NEWSENT_TAGS or word in NEWSENT_PUNCT:
            newsent = True
        elif word in PARENTHESES_START:
            parentheses_level += 1
        elif word in PARENTHESES_END:
            parentheses_level -= 1
        else:
            newsent = False

        if newsent and parentheses_level == 0:
            yield '\u3000'.join(tokens)
            tokens.clear()
            newsent = False
    # output tokens left
    if tokens:
        yield '\u3000'.join(tokens)


def main():
    for line in fileinput.input():
        for sent in ckip_sent_tokenize(line):
            print(sent)


if __name__ == '__main__':
    main()
