#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter

from .linggle_command import expand_query


class Linggle:
    def __del__(self):
        self.close()

    def __getitem__(self, cmd):
        return self.__query(cmd)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __query(self, cmd, topn=50):
        result = Counter()
        simple_cmds = expand_query(cmd)
        print(simple_cmds)
        # TODO: handle same ngram with different pos
        for ngram, count in self.query(simple_cmds):
            # force int type to prevent json serialization error
            # (ex., Decimal in Cassandra)
            result[ngram] = int(count)
        return result.most_common(topn)

    def query(self, query):
        return []

    def close(self):
        pass
