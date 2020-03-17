#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from itertools import chain

import psycopg2

from .linggle import DbLinggle
from .lead_tail import convert_lt_cmd, fit_lt_condition

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
        lt_cmds = [cmd for cmd in cmds if '$' in cmd]
        if lt_cmds:
            nolt_cmds = [cmd for cmd in cmds if '$' not in cmd]
            return chain(self.__query(nolt_cmds), *(self._lt_query(cmd) for cmd in lt_cmds))
        else:
            return self.__query(cmds)

    def _lt_query(self, cmd):
        cmd, re_conditions = convert_lt_cmd(cmd)
        logging.info(f"Lead-tail query: {cmd} {str(re_conditions)}")
        for ngram, count in self._db_query(cmd):
            if not re_conditions or fit_lt_condition(re_conditions, ngram):
                yield ngram, count

    def _db_query(self, cmd):
        return self.__query((cmd,))

    def __query(self, cmds):
        if not cmds:
            return ()
        logging.info(f"PostgreSQL queries: {cmds}")
        with self.conn.cursor() as cursor:
            cursor.execute(QUERY_CMD, (cmds,))
            return chain(*(row[0] for row in cursor))
