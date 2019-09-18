#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc
import logging
from heapq import nlargest
from operator import itemgetter

from .sims import find_synonyms
from .linggle_command import convert_to_nopos_query, satisfy_pos_condition, expand_query


class BaseLinggle:
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, cmd):
        return self.query(cmd)

    def query(self, cmd, topn=50):
        # print('Linggle query:', cmd)
        # TODO: use more efficient nlargest function (bottleneck, pandas, ...)
        return nlargest(topn, self._query(cmd), key=itemgetter(-1))

    @abc.abstractmethod
    def _query(self, cmd):
        """return list of ngrams with counts"""


class DbLinggle(BaseLinggle):
    def __init__(self, *args, find_synonyms=find_synonyms,
                 word_delimiter=' ', **kwargs):
        self.find_synonyms = find_synonyms
        self.word_delimiter = word_delimiter

    def _query(self, cmd):
        cmds = expand_query(cmd, self.find_synonyms, self.word_delimiter)
        return self._db_query(cmds)

    @abc.abstractmethod
    def _db_query(self, cmds):
        """clean connection object"""
        return []

    @abc.abstractmethod
    def close(self):
        """clean connection object"""
        pass

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class NoPosDbLinggle(DbLinggle):
    def _query(self, cmd):
        cmds = expand_query(cmd, self.find_synonyms, self.word_delimiter)
        for cmd in cmds:
            # TODO: handle same ngram with different pos
            cmd, condition = convert_to_nopos_query(cmd)
            for ngram, count in self._db_query(cmd):
                if satisfy_pos_condition(ngram, condition):
                    yield ngram, count
