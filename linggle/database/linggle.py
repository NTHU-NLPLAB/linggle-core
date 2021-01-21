#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc
import logging
from heapq import nlargest
from operator import itemgetter
from functools import partial

from .linggle_command import LinggleCommand
from .partial import convert_partial_cmd, fit_partial_condition

from linggle.pos.bnc import has_pos
from linggle.pos import is_pos_wildcard

from itertools import chain


class BaseLinggle(LinggleCommand):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, cmd):
        return self.query(cmd)

    def query(self, cmd, topn=50):
        logging.info(f"Linggle query: {cmd}")
        cmds = self.expand_query(cmd)
        logging.info(f"Expand query: {cmds}")

        lt_cmds = [cmd for cmd in cmds if '*' in cmd]
        # TODO: rewrite
        if lt_cmds:
            nolt_cmds = [cmd for cmd in cmds if '*' not in cmd]
            ngrams = chain(self._query_many(nolt_cmds), self._query_many(lt_cmds, query_func=self._lt_query))
        else:
            ngrams = self._query_many(cmds)

        # TODO: use more efficient nlargest function (bottleneck, pandas, ...)
        # TODO: remove repetitive ngrams
        return nlargest(topn, ngrams, key=itemgetter(-1))

    def _query_many(self, cmds, query_func=None, **kwargs):
        """accept queries and return list of ngrams with counts"""
        query_func = query_func if query_func else self._query
        return chain(*(query_func(cmd) for cmd in cmds))

    def _lt_query(self, cmd):
        cmd, re_conditions = convert_partial_cmd(cmd)
        logging.info(f"Lead-tail query: {cmd} {str(re_conditions)}")
        return [(ngram, count) for ngram, count in self._query(cmd)
                if fit_partial_condition(re_conditions, ngram.split())]

    def _query(self, cmd):
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

    def _query(self, cmd):
        return self._db_query(cmd)

    @abc.abstractmethod
    def _db_query(self, cmd):
        """query db and return list of ngrams with counts"""


class NoPosLinggle(BaseLinggle):
    def _query(self, cmd):
        nopos_cmd, conditions = NoPosLinggle.to_nopos_cmd(cmd)
        logging.info(f"Convert to No-PoS Cmd: {cmd} -> {nopos_cmd}:{conditions}")
        if conditions:
            fileter_func = partial(NoPosLinggle.satisfy_conditions, conditions=conditions)
            return filter(fileter_func, super()._query(nopos_cmd))
        else:
            return super()._query(nopos_cmd)

    @staticmethod
    def to_nopos_cmd(cmd):
        tokens = cmd.split()
        conditions = tuple((i, token) for i, token in enumerate(tokens) if is_pos_wildcard(token))
        for i, _ in conditions:
            tokens[i] = '_'
        return ' '.join(tokens), conditions

    @staticmethod
    def satisfy_conditions(row, conditions=()):
        ngram = row[0].split()
        return all(has_pos(ngram[i], condition) for i, condition in conditions)
