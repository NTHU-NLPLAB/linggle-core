#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import psycopg2

from .linggle import BaseLinggle

LINGGLE_TABLE = os.environ.get('LINGGLE_TABLE', 'LINGGLE')
QUERY_CMD = "SELECT ngrams FROM {} WHERE query = %s;".format(LINGGLE_TABLE)

settings = {
    'dbname': os.environ.get('PGDATABASE', 'linggle'),
    'host': os.environ.get('PGHOST', 'localhost'),
    'user': os.environ.get('PGUSER', 'linggle'),
    'password': os.environ.get('PGPASSWORD', ''),
    'port': int(os.environ.get('PGPORT', 5432))
}


class PostgresLinggle(BaseLinggle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = psycopg2.connect(**settings)

    def close(self):
        if hasattr(self, 'conn') and not self.conn.closed:
            self.conn.close()

    def query(self, cmd):
        with self.conn.cursor() as cursor:
            cursor.execute(QUERY_CMD, [cmd])
            for result, *_ in cursor:
                for ngram, count, npos_list in result.get('ngrams'):
                    yield ngram, count, npos_list
