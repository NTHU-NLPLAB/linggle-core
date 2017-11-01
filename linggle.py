#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import islice


class Linggle:
    def __init__(self):
        pass

    def __del__(self):
        self.close()

    def __getitem__(self, querystr):
        return self.__query(querystr)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __query(self, querystr, topn=50):
        results = self.query(querystr)
        return list(islice(results, topn))

    def query(self):
        return []

    def close(self):
        pass
