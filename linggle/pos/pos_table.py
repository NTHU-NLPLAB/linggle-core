#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from collections import defaultdict

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

PREPROSITION_FILE_PATH = os.path.join(MODULE_PATH, 'pg.prep.txt')
PREPROSITIONS = set(line.strip() for line in open(PREPROSITION_FILE_PATH))

POSTABLE_PATH = os.path.join(MODULE_PATH, 'postable.norm.txt')


def init_postable():
    postable = defaultdict(set)
    for line in open(POSTABLE_PATH):
        word, pos = line.strip('"\n\r ').split('"\t"')
        postable[pos].add(word)
    return postable


def has_pos(word, pos):
    if pos == 'prep':
        return word in PREPROSITIONS
    return word in POS_TABLE[pos]


POS_TABLE = init_postable()
