#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


# Build paths inside the project like: os.path.join(BASE_DIR, ...)
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
POS_FILE_PATH = os.path.join(MODULE_PATH, 'data', 'bnc_pos.txt')
PREP_FILE_PATH = os.path.join(MODULE_PATH, 'data', 'prepositions.txt')


def init_postable():
    postable = {}
    for line in open(POS_FILE_PATH):
        word, *poss = line.strip().split()
        for pos in poss:
            postable.setdefault(f"{pos}.", set()).add(word)
    postable['p.'] = set(open(PREP_FILE_PATH).read().split())
    return postable


def get_pos_check_func(i, pos):
    def check(tokens):
        return tokens[i] in word_set
    word_set = POS_TABLE[pos]
    return check


POS_TABLE = init_postable()
