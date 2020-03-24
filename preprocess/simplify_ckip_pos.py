#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
import string


BASE_PATH = path.dirname(path.abspath(__file__))
ckip_abbr = {}
for line in open(path.join(BASE_PATH, 'ckip_abbr.txt')):
    abbr, *tags = line.split()
    for tag in tags:
        ckip_abbr[tag] = abbr


def get_abbr(tag):
    return ckip_abbr.get(tag) or ckip_abbr.get(tag.strip(string.digits)) or ''


def simplify_ckip_token(token):
    word, tag = token[:-1].rsplit('(', 1)
    word = word.strip()
    tag = get_abbr(tag)
    if tag:
        word += f"({tag})"
    return word


if __name__ == "__main__":
    import fileinput
    for line in fileinput.input():
        line = line.strip()
        if line.startswith('<') and line.endswith('>'):
            continue
        print(' '.join(simplify_ckip_token(token) for token in line.split()))
