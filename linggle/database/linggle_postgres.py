#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from itertools import chain

import psycopg2

from .linggle import DbLinggle

LINGGLE_TABLE = os.environ.get('LINGGLE_TABLE', 'LINGGLE')
QUERY_CMD = "SELECT results FROM {} WHERE query IN %s;".format(LINGGLE_TABLE)

settings = {
    'dbname': os.environ.get('PGDATABASE', 'linggle'),
    'host': os.environ.get('PGHOST', 'localhost'),
    'user': os.environ.get('PGUSER', 'linggle'),
    'password': os.environ.get('PGPASSWORD', ''),
    'port': int(os.environ.get('PGPORT', 5432))
}


class PostgresLinggle(DbLinggle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = psycopg2.connect(**settings)

    def _query_many(self, cmds):
        with self.conn.cursor() as cursor:
            cursor.execute(QUERY_CMD, [cmds])
            return chain(*(row[0] for row in cursor))

    def _db_query(self, cmd):
        with self.conn.cursor() as cursor:
            cursor.execute(QUERY_CMD, [(cmd,)])
            for row in cursor:
                for ngram, count in row[0]:
                    yield ngram, count
