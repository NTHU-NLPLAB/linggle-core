#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import psycopg2
from linggle import Linggle

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

    def query(self, cmd):
        with self.conn.cursor() as cursor:
            cursor.execute(SELECT_CMD, [cmd])
            res = cursor.fetchone()
            if res:
                return res[0]
        return []
