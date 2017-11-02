#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict

PREPROSITIONS = set(line.strip() for line in open('pg.prep.txt'))


def init_postable():
    postable = defaultdict(set)
    for line in open('postable.norm.txt'):
        word, pos = line.strip('"\n\r ').split('"\t"')
        postable[pos].add(word)
    return postable


def has_pos(word, pos):
    if pos == 'prep':
        return word in PREPROSITIONS
    return word in POS_TABLE[pos]


POS_TABLE = init_postable()
