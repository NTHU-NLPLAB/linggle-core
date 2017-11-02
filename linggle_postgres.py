#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from collections import Counter

import psycopg2
from linggle import Linggle
from linggle_command import expand_query

SELECT_CMD = "SELECT results FROM LINGGLEZH WHERE query=%s;"
CONNSTR = "dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'"


settings = {
    'dbname': os.environ.get('PGDATABASE', 'linggle'),
    'host': os.environ.get('PGHOST', 'localhost'),
    'user': os.environ.get('PGUSER', 'linggle'),
    'password': os.environ.get('PGPASSWORD', ''),
    'port': int(os.environ.get('PGPORT', 5432))
}


class PostgresLinggle(Linggle):
    def __init__(self):
        self.connstr = CONNSTR.format(**settings)
        self.conn = psycopg2.connect(self.connstr)

    def close(self):
        if not self.conn.closed:
            self.conn.close()

    def query(self, querystr):
        querystr = querystr.strip()
        # print(querystr)
        # expand query description and then gather results
        with self.conn.cursor() as cursor:
            result = Counter()
            for query_unit in expand_query(querystr):
                cursor.execute(SELECT_CMD, [query_unit])
                res = cursor.fetchone()
                if res:
                    for row in res:
                        for ngram, count in res[0]:
                            result[ngram] = count

            return result.most_common()
