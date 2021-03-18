#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import product, permutations
import unicodedata
import logging
import re

from .vocab import VOCABULARY
from ..pos import normalize_wildcard, is_pos_wildcard


# TODO: parse for nested reorder query
QUERY_RE = re.compile(r'\{[^}]+\}|\S+')
LONGEST_LEN = 5


class LinggleCommand:
    def __init__(self, *args, find_synonyms=None, word_delimiter=' ', vocab=VOCABULARY,
                 **kwargs):
        if find_synonyms:
            self.find_synonyms = find_synonyms
        self.word_delimiter = word_delimiter
        self.vocab = vocab

    def get_unigram(self, query):
        if query == '_':
            return self.vocab.most_common()
        elif query in self.vocab:
            return ((query, self.vocab[query]),)
        return ()

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

            if token in '_' or '*' in token:
                yield f" {token} "
            elif '_' in token:
                # restore multiword unit: look_forward_to
                for cmd in self.expand_query(' '.join(token.split('_'))):
                    yield cmd
            elif is_pos_wildcard(token):
                yield f' {normalize_wildcard(token)} '
            elif token:
                yield token

    def gen_candidates(self, query):
        for item in QUERY_RE.findall(query):
            if item == '*':
                yield ('', *('_'.join(' '*(n+1)) for n in range(1, LONGEST_LEN+1)))
            elif item.startswith('{') and item.endswith('}'):
                items = QUERY_RE.findall(item[1:-1])
                yield tuple(cmd for tokens in permutations(items)
                            for cmd in self.expand_query(' '.join(tokens)))
            else:
                item = LinggleCommand.normalize_query_token(item)
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
        logging.info(f"Expand query: {querystr} -> {linggle_cmds}")
        return linggle_cmds

    @staticmethod
    def normalize_query_token(token):
        return token.replace('%', '*').replace('$', '*')

    @staticmethod
    def normalize_query(query):
        query = unicodedata.normalize('NFKC', query)
        return query.strip().replace('@', '/').replace('...', '*')
