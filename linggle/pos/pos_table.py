#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


# Build paths inside the project like: os.path.join(BASE_DIR, ...)
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))


def init_postable():
    postable = {}
    postable_path = os.path.join(MODULE_PATH, 'data', 'bnc_postable.txt')
    for line in open(postable_path):
        word, pos = line.strip('"\n\r ').split('"\t"')
        postable.setdefault(pos, set()).add(word)
    prep_file_path = os.path.join(MODULE_PATH, 'data', 'prepositions.txt')
    postable['prep'] = set(open(prep_file_path).read().split())
    return postable


def has_pos(word, pos):
    return word in POS_TABLE[pos]


POS_TABLE = init_postable()
