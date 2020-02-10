#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import product, permutations
from functools import partial
import re

from ..pos import is_spacy_pos, satisfy_pos, POS_WILDCARD
from ..pos import has_pos


# TODO: parse for nested reorder query
QUERY_RE = re.compile(r'\{[^}]+\}|\S+')
LONGEST_LEN = 5


class LinggleCommand:
    def __init__(self, *args, find_synonyms=None,
                 word_delimiter=' ', **kwargs):
        if find_synonyms:
            self.find_synonyms = find_synonyms
        self.word_delimiter = word_delimiter

    def find_synonyms(self, word):
        return ()

    def item_to_candidate(self, item):
        for token in filter(None, item.split('/')):
            if token.startswith('?'):
                yield ''
                token = token[1:]
            if token.startswith('~'):
                token = token[1:]
                for synonym in self.find_synonyms(token):
                    yield synonym

            if token == '_':
                yield ' _ '
            elif token in POS_WILDCARD:
                yield f' {POS_WILDCARD[token]} '
            elif token:
                # restore multiword unit: look_forward_to
                yield self.word_delimiter.join(token.split('_'))

    def gen_candidates(self, query):
        for item in QUERY_RE.findall(query):
            if item == '*':
                yield ('', *('_'.join(' '*(n+1)) for n in range(1, LONGEST_LEN+1)))
            elif item.startswith('{') and item.endswith('}'):
                items = QUERY_RE.findall(item[1:-1])
                yield tuple(cmd for tokens in permutations(items)
                            for cmd in self.expand_query(' '.join(tokens)))
            else:
                yield tuple(self.item_to_candidate(item))

    def candidates_to_cmds(self, candidates, return_str=True):
        for tokens in product(*candidates):
            # Chinese: words are compact (delim: '')
            # English: words are separated by space (delim: ' ')
            tokens = self.word_delimiter.join(token for token in tokens if token).strip().split()
            if len(tokens) <= LONGEST_LEN:
                yield ' '.join(tokens) if return_str else tuple(tokens)

    def expand_query(self, querystr, return_str=True):
        querystr = LinggleCommand.normalize_query(querystr)
        # generate possible candidates for each token in the query command
        candidates = list(self.gen_candidates(querystr))
        # generate the basic commands of linggle based on the candidates
        # (i.e., remove ['/', '*', '~', '?', '{}'] and normalize PoS wildcards)
        linggle_cmds = tuple({cmd for cmd in self.candidates_to_cmds(candidates, return_str)})
        return linggle_cmds

    @staticmethod
    def normalize_query(query):
        return query.strip().replace('@', '/')


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


def add_candidate(target, candidates):
    assert len(target) == len(candidates)
    for t, c in zip(target, candidates):
        t.add(c)
        if c[-1] == '.':
            t.add('.')


def to_nopos_query(cmds):
    cmds_by_len = {}
    for cmd in cmds:
        cmd = cmd.split()
        length = len(cmd)
        if length in cmds_by_len:
            add_candidate(cmds_by_len[length], cmd)
        else:
            cmds_by_len[length] = [{token} for token in cmd]

    for length in sorted(cmds_by_len):
        for cmd in to_nopos_cmd(cmds_by_len[length]):
            yield cmd


def to_nopos_cmd(cmd_candidates, threshold=99):
    cmd = [''] * len(cmd_candidates)
    conditions = {}
    for i, candidates in enumerate(cmd_candidates):
        if '_' in candidates:
            cmd[i] = '_'
        elif '.' in candidates:
            cmd[i] = '_'
            candidates.remove('.')
            conditions[i] = candidates
        elif len(candidates) > threshold:
            cmd[i] = '_'
            conditions[i] = candidates
        else:
            cmd[i] = candidates

    for tokens in product(*cmd):
        yield ' '.join(tokens), conditions


def satisfy_conditions(ngram, conditions):
    ngram = ngram.split()
    return all(ngram[i] in condition or has_pos(ngram[i], conditions) for i, condition in conditions)
