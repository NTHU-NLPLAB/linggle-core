#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

from .linggle import Linggle
from .linggle_command import convert_to_nopos_query, satisfy_pos_condition

LINGGLE_TABLE = os.environ.get('LINGGLE_TABLE', 'LINGGLE')
QUERY_CMD = "SELECT ngram, count FROM {} WHERE query=%s;".format(LINGGLE_TABLE)


auth_settings = {
    'username': os.environ.get('username', 'linggle'),
    'password': os.environ.get('password', '')
}
cluster = os.environ.get('cluster', 'localhost').split(',')
keyspace = os.environ.get('keyspace', 'linggle')


class CassandraLinggle(Linggle):
    def __init__(self):
        auth_provider = PlainTextAuthProvider(**auth_settings)
        self.cluster = Cluster(cluster, auth_provider=auth_provider)
        self.session = self.cluster.connect(keyspace)

    def close(self):
        if not self.cluster.is_shutdown:
            self.cluster.shutdown()

    def query(self, cmd):
        cmd, condition = convert_to_nopos_query(cmd)

        for row in self.session.execute(QUERY_CMD, (cmd, ), timeout=60.0):
            if satisfy_pos_condition(row.ngram, condition):
                yield row.ngram, row.count
