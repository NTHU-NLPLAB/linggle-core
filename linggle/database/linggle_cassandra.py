#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy

from .linggle import DbLinggle

LINGGLE_TABLE = os.environ.get('LINGGLE_TABLE', 'LINGGLE')
QUERY_CMD = "SELECT ngram, count FROM {} WHERE query=%s;".format(LINGGLE_TABLE)


auth_settings = {
    'username': os.environ.get('username', 'linggle'),
    'password': os.environ.get('password', '')
}
cluster = os.environ.get('cluster', 'localhost').split(',')
keyspace = os.environ.get('keyspace', 'linggle')


class CassandraLinggle(DbLinggle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        auth_provider = PlainTextAuthProvider(**auth_settings)
        self.cluster = Cluster(
            cluster,
            auth_provider=auth_provider,
            load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1'),
            protocol_version=4)
        self.session = self.cluster.connect(keyspace)

    def close(self):
        if not self.cluster.is_shutdown:
            self.cluster.shutdown()

    def _db_query(self, cmd):
        logging.info(f"Cassandra query: {cmd}")
        # TODO: log if timeout
        for row in self.session.execute(QUERY_CMD, [cmd], timeout=10.0):
            # force int type to prevent serialization error (ex., Decimal in Cassandra)
            yield row.ngram, int(row.count)
