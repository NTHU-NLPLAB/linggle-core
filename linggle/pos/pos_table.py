#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from .abbr import POS_WILDCARD

# Build paths inside the project like: os.path.join(BASE_DIR, ...)
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
POS_FILE_PATH = os.path.join(MODULE_PATH, 'data', 'bnc_pos.txt')
PREP_FILE_PATH = os.path.join(MODULE_PATH, 'data', 'prepositions.txt')


def init_postable():
    postable = {abbr: set() for abbr in POS_WILDCARD.values()}
    for line in open(POS_FILE_PATH):
        word, *poss = line.strip().split()
        for pos in poss:
            postable[f"{pos}."].add(word)
    postable['p.'] = set(open(PREP_FILE_PATH).read().split())
    return postable


def has_pos(word, pos):
    return pos in POS_TABLE and word in POS_TABLE[pos]


POS_TABLE = init_postable()
