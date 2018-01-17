#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from collections import defaultdict

# Build paths inside the project like: os.path.join(BASE_DIR, ...)
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

# preposition table
PREPROSITION_FILE_PATH = os.path.join(MODULE_PATH, 'pg.prep.txt')
PREPROSITIONS = set(line.strip() for line in open(PREPROSITION_FILE_PATH))

POSTABLE_PATH = os.path.join(MODULE_PATH, 'postable.norm.txt')

# TODO: pron: Nh
POSABBR_TABLE_PATH = os.path.join(MODULE_PATH, 'posabbr.txt')


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


def init_pos_abbr():
    abbr_dict = {}
    for line in open(POSABBR_TABLE_PATH):
        pos_tokens = line.strip().split('\t')
        for pos_token in pos_tokens:
            abbr_dict[pos_token] = pos_token[0]
    return abbr_dict


POS_TABLE = init_postable()
POS_WILDCARD = init_pos_abbr()
