#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# Build paths inside the project like: os.path.join(BASE_DIR, ...)
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

POSTABLE_PATH = os.path.join(MODULE_PATH, 'data', 'spacy_tags.txt')


def load_tag_abbr():
    def parse(line):
        return line.strip('\n ').split('\t')

    tags_abbr = {}
    pos_list = set()
    for tag, _, pos_str in map(parse, open(POSTABLE_PATH)):
        if pos_str:
            tags_abbr[tag] = pos_str
            for pos in pos_str.split(','):
                pos_list.add(pos)
    return tags_abbr, pos_list


def get_abbr(tag):
    return SPACY_TAGS.get(tag, '')


def is_spacy_pos(token):
    if token == '-ing':
        return True
    return token.endswith('.') and token[:-1] in SPACY_POS_LIST


def satisfy_pos(npos, conditions):
    for index, pos_set in conditions:
        if all(pos not in pos_set for pos in npos[index].split(',')):
            return False
    return True


SPACY_TAGS, SPACY_POS_LIST = load_tag_abbr()
