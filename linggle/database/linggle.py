#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter

from .linggle_command import expand_query


class Linggle:
    def __init__(self):
        pass

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
        for simple_cmd in expand_query(cmd):
            # TODO: handle same ngram with different pos
            for ngram, count in self.query(simple_cmd):
                result[ngram] = count
        return result.most_common(topn)

    def query(self, query):
        return []

    def close(self):
        pass
