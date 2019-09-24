#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite3

try:
    import ujson as json
except ImportError:
    import json


from .linggle import DbLinggle

LINGGLE_TABLE = os.environ.get('LINGGLE_TABLE', 'LINGGLE')
QUERY_CMD = "SELECT results FROM {} WHERE query IN %s;".format(LINGGLE_TABLE)


class SqliteLinggle(DbLinggle):
    def __init__(self, *args, db_file=":memory:", **kwargs):
        super().__init__(*args, **kwargs)
        self.db_file = db_file

    def close(self):
        if hasattr(self, 'conn') and not self.conn.closed:
            self.conn.close()

    def _db_query(self, cmds):
        cmdstr = '(' + ', '.join(map(repr, cmds)) + ')'
        with sqlite3.connect(self.db_file) as conn:
            for row in conn.execute(QUERY_CMD % cmdstr):
                for ngram, count in json.loads(row[0]):
                    yield ngram, count
