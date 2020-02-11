#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from itertools import chain
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

try:
    import ujson as json
except ImportError:
    import json

from .linggle import DbLinggle


LINGGLE_TABLE = os.environ.get('LINGGLE_TABLE', 'LINGGLE')
QUERY_CMD = "SELECT results FROM {} WHERE query IN %s;".format(LINGGLE_TABLE)

SQLITE_DB_PATH = os.environ.get("SQLITE_DB_PATH", ":memory:")


class SqliteLinggle(DbLinggle):
    def __init__(self, *args, db_file=SQLITE_DB_PATH, **kwargs):
        super().__init__(*args, **kwargs)
        # use sqlalchemy connection pool to enable better performance for multithreading
        self.conn = create_engine('sqlite:///'+db_file, poolclass=QueuePool)

    def close(self):
        if hasattr(self, 'conn'):
            del self.conn

    def _query_many(self, cmds):
        cmdstr = '(' + ', '.join(map(repr, cmds)) + ')'
        return chain(*(json.loads(row[0]) for row in self.conn.execute(QUERY_CMD % cmdstr)))

    def _db_query(self, cmd):
        for row in self.conn.execute(QUERY_CMD % f"({cmd})"):
            for ngram, count in json.loads(row[0]):
                yield ngram, count
