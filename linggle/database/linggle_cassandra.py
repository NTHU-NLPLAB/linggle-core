#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.query import tuple_factory

from .linggle import DbLinggle

LINGGLE_TABLE = os.environ.get('LINGGLE_TABLE', 'LINGGLE')
QUERY_CMD = "SELECT ngram, count FROM {} WHERE query=? ;".format(LINGGLE_TABLE)
NGRAM_TABLES = (None, 'unigram', 'bigram', 'trigram', 'fourgram', 'fivegram')


keyspace = os.environ.get('keyspace', 'linggle')


class CassandraLinggle(DbLinggle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cluster = Cluster(
            load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1'),
            protocol_version=4)
        self.session = self.cluster.connect(keyspace)
        self.session.row_factory = tuple_factory
        self.prepared = self.session.prepare(QUERY_CMD)

    def close(self):
        if not self.cluster.is_shutdown:
            self.cluster.shutdown()

    def _db_query(self, cmd):
        logging.info(f"Cassandra query: {cmd}")
        tokens = cmd.split()
        if all(token != '_' for token in tokens):
            return self._ngram_query(len(tokens), ngram=cmd)
        elif all(token == '_' for token in tokens):
            # TODO: extracting all ngrams with n > 1 can be very problematic because it's too BIG!
            if len(tokens) > 1:
                return ()
            return self._ngram_query(len(tokens))
        else:
            # TODO: log if timeout
            # TODO: try cassandra.concurrent.execute_concurrent_with_args
            # force int type to prevent serialization error (ex., Decimal in Cassandra)
            return ((ngram, count) for ngram, count in self.session.execute(self.prepared, (cmd,)))

    def _ngram_query(self, n, ngram=None):
        table = NGRAM_TABLES[n]
        if ngram:
            cmd = f"SELECT ngram, count FROM {table} WHERE ngram=%s ;"
            return ((ngram, int(count)) for ngram, count in self.session.execute(cmd, (ngram,)))
        else:
            cmd = f"SELECT ngram, count FROM {table} ;"
            return ((ngram, int(count)) for ngram, count in self.session.execute(cmd))
