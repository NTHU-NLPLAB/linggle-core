#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import product, permutations
from functools import partial
import re

from ..pos import is_spacy_pos, has_pos, satisfy_pos, POS_WILDCARD

query_re = re.compile(r'\{[^}]+\}|\S+')
LONGEST_LEN = 5


def find_synonyms_empty(word):
    return []


def item_to_candidate(item, find_synonyms=find_synonyms_empty):
    for token in item.split('/'):
        if not token:
            continue
        if token.startswith('~'):
            token = token[1:]
            for synonym in find_synonyms(token):
                yield synonym

        if token == '_':
            yield ' _ '
        elif token in POS_WILDCARD:
            yield f' {POS_WILDCARD[token]} '
        else:
            yield token


def gen_candidates(query, find_synonyms=find_synonyms_empty, delim=' '):
    # for item in query.split():
    for item in query_re.findall(query):
        if item == '*':
            yield ('', *('_'.join(' '*(n+1)) for n in range(1, LONGEST_LEN+1)))
        elif item.startswith('?'):
            yield ('', *item_to_candidate(item, find_synonyms))
        elif item.startswith('{') and item.endswith('}'):
            items = item[1:-1].split()
            print('-'+delim+'-')
            yield [cmd for tokens in permutations(items)
                   for cmd in expand_query(delim.join(tokens), find_synonyms, delim)]
        else:
            yield tuple(item_to_candidate(item, find_synonyms))


def candidates_to_cmds(candidates, delim=' '):
    for tokens in product(*candidates):

        # Chinese: words are compact (delim: '')
        # English: words are separated by space (delim: ' ')
        tokens = delim.join(token for token in tokens if token).strip().split()

        if len(tokens) > LONGEST_LEN:
            continue
        yield ' '.join(tokens)


def expand_query(querystr, find_synonyms=find_synonyms_empty, delim=' '):
    querystr = querystr.strip()
    # replace alternative symbol for selection operator `/`
    querystr = querystr.replace('@', '/')
    # generate possible candidates for each token in the query command
    candidates = list(gen_candidates(querystr, find_synonyms, delim))
    # generate the basic commands of linggle based on the candidates
    linggle_cmds = tuple({cmd for cmd in candidates_to_cmds(candidates, delim)})
    return linggle_cmds


def convert_to_nopos_query(cmd):
    tokens = []
    condition = []
    for i, token in enumerate(cmd.split()):
        if is_spacy_pos(token.lower()):
            condition.append((i, token.rstrip('.')))
            tokens.append('_')
        else:
            tokens.append(token)
    return ' '.join(tokens), condition


def satisfy_pos_condition(ngram, condition):
    ngram = ngram.split()
    return all(i < len(ngram) and has_pos(ngram[i], pos.lower()) for i, pos in condition)


def query_to_cmds(query, delim=' '):
    # transform pos conditions to a function
    def to_func(conditions):
        if not conditions:
            return False
        return partial(satisfy_pos, conditions=list(conditions.items()))

    cmds_pool = defaultdict(partial(defaultdict, set))
    # generate possible candidates for each token in the query command
    candidates = list(gen_candidates(query))
    for tokens in product(*candidates):
        # Chinese: words are compact (delimiter: '')
        # English: words are separated by space (delimiter: ' ')
        tokens = delim.join(token for token in tokens if token).strip().split()
        length = len(tokens)

        # ignore commands longer than 5
        if length <= LONGEST_LEN:
            # replace pos token to `_`, and use pos as conditions
            if any(is_spacy_pos(token) for token in tokens):
                cmd = ' '.join('_' if is_spacy_pos(token) else token
                               for token in tokens)
                for i, token in enumerate(tokens):
                    if is_spacy_pos(token) and type(cmds_pool[cmd]) is defaultdict:
                        cmds_pool[cmd][i].add(token.rstrip('.'))
            else:
                cmds_pool[' '.join(tokens)] = False

    return {cmd: to_func(conditions) for cmd, conditions in cmds_pool.items()}
