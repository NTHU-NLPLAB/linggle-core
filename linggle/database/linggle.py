#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc
import logging
from collections import Counter

from .linggle_command import LinggleCommand
from .partial import convert_partial_cmd

from linggle.pos.bnc import get_pos_check_func
from linggle.pos import is_pos_wildcard

from itertools import chain


class BaseLinggle(LinggleCommand):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.vocab:
            self.get_unigram = self.query

    def __getitem__(self, cmd):
        return self.__query(cmd)

    def get(self, cmd, default=(), topn=None):
        return self.__query(cmd, topn=topn) or default

    def __query(self, cmd, topn=50):
        cmds = self.expand_query(cmd)
        ngrams = self._query_many(cmds)
        # TODO: use more efficient nlargest function (bottleneck, pandas, ...)
        return Counter(dict(ngrams)).most_common(topn)

    def _query_many(self, cmds, query_func=None, **kwargs):
        """accept queries and return list of ngrams with counts"""
        return chain(*(self._query(cmd) for cmd in cmds))

    def _query(self, cmd, conditions=()):
        cmd, partial_conditions = convert_partial_cmd(cmd)
        conditions += partial_conditions
        logging.info(f"plain query: {cmd} {str(conditions)}")
        # if the token length of the query is 1, use `get_unigram` method to speed up
        rows = self.query(cmd) if len(cmd.split()) > 1 else self.get_unigram(cmd)
        return [(ngram, count) for ngram, count in rows if BaseLinggle.check_condition(ngram, conditions)]

    @staticmethod
    def check_condition(ngram, conditions):
        tokens = ngram.split()
        return all(condition(tokens) for condition in conditions)

    @abc.abstractmethod
    def query(self, cmd):
        """return list of ngrams with counts"""
        # TODO: hightlight wildcards
        # highlight = tuple(i for i, token in enumerate(cmd.split()) if token == '_')
        return []


class DbLinggle(BaseLinggle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def close(self):
        """clean connection object"""
        if hasattr(self, 'conn') and not self.conn.closed:
            self.conn.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def query(self, cmd):
        return self._db_query(cmd)

    @abc.abstractmethod
    def _db_query(self, cmd):
        """query db and return list of ngrams with counts"""


class NoPosLinggle(BaseLinggle):
    def _query(self, cmd, conditions=()):
        nopos_cmd, pos_conditions = NoPosLinggle.to_nopos_cmd(cmd)
        logging.info(f"Convert to No-PoS query: {cmd} -> {nopos_cmd}:{pos_conditions}")
        return super()._query(nopos_cmd, conditions=pos_conditions+conditions)

    @staticmethod
    def to_nopos_cmd(cmd):
        tokens = cmd.split()
        conditions = []
        for i, token in enumerate(tokens):
            if is_pos_wildcard(token):
                tokens[i] = '_'
                conditions.append(get_pos_check_func(i, token))
        return ' '.join(tokens), tuple(conditions)
