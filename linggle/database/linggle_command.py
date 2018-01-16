#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import product

from ..pos import has_pos

LONGEST_LEN = 5

# TODO: pron: Nh
POS_WILDCARD = {
    'v.': 'V.',
    'n.': 'N.',
    'adj.': 'A.',
    'prep.': 'P.',
    'det.': 'DET.',
    'conj.': 'C.',
    'pron.': 'PRON.',
    'adv.': 'ADV.',
    'cl.': 'Nf.',
}


def find_synonyms_empty(word):
    return []


def item_to_candidate(item, find_synonyms=find_synonyms_empty):
    for token in item.split('/'):
        if token.startswith('?'):
            yield ''
            token = token[1:]
        if token.startswith('~'):
            for synonym in find_synonyms(token):
                yield synonym
            token = token[1:]

        if token in POS_WILDCARD:
            token = ' ' + POS_WILDCARD[token] + ' '
        elif token == '_':
            yield ' _ '
        else:
            yield token


def gen_candidates(query):
    for item in query.split():
        if item == '*':
            yield [''] + ['_'.join(' '*(n+1)) for n in range(1, LONGEST_LEN+1)]
        else:
            yield list(item_to_candidate(item))


def candidates_to_cmds(candidates):
    for tokens in product(*candidates):

        # Chinese words are compact
        tokens = ''.join(token for token in tokens if token).strip().split()
        # english words are separated by space
        # tokens = ' '.join(token for token in tokens if token).strip().split()

        if len(tokens) > LONGEST_LEN:
            continue
        yield ' '.join(tokens)


def expand_query(querystr):
    querystr = querystr.strip()
    # replace alternative symbol for selection operator `/`
    querystr = querystr.replace('@', '/')
    # generate possible candidates for each token in the query command
    candidates = list(gen_candidates(querystr))
    # generate the basic commands of linggle based on the candidates
    linggle_cmds = {cmd for cmd in candidates_to_cmds(candidates)}
    return linggle_cmds


def convert_to_nopos_query(querystr):
    tokens = []
    condition = []
    for i, token in enumerate(querystr.split()):
        if token.lower() in POS_WILDCARD:
            condition.append((i, token[:-1]))
            tokens.append('_')
        else:
            tokens.append(token)
    return ' '.join(tokens), condition


def satisfy_pos_condition(ngram, condition):
    ngram = ngram.split(' ')
    return all(has_pos(ngram[i], pos.lower()) for i, pos in condition)
