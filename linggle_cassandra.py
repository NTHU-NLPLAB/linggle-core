#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from collections import Counter

from linggle import Linggle
from linggle_command import POS_WILDCARD, expand_query
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from pos_table import has_pos

QUERY_CMD = "SELECT ngram, count FROM web1t WHERE query=%s;"


auth_settings = {
    'username': os.environ.get('username', 'linggle'),
    'password': os.environ.get('password', '')
}
cluster = os.environ.get('cluster', 'localhost').split(',')
keyspace = os.environ.get('keyspace', 'linggle')


class CassandraLinggle(Linggle):
    def __init__(self):
        auth_provider = PlainTextAuthProvider(**auth_settings)
        self.cluster = Cluster(cluster=cluster, auth_provider=auth_provider)
        self.session = self.cluster.connect(keyspace)

    def close(self):
        if not self.cluster.is_shutdown:
            self.cluster.shutdown()

    def query(self, querystr):
        result = Counter()
        for query_unit in expand_query(querystr):
            for ngram, count in self.__query__(query_unit):
                result[ngram] = count

    def __query__(self, querystr):
        tokens = []
        pos_condition = []
        for i, token in enumerate(querystr.split()):
            if token in POS_WILDCARD:
                pos_condition.append((i, token[:-1]))
                tokens.append('_')
            else:
                tokens.append(token)
        query = ' '.join(tokens)

        for row in self.session.execute(QUERY_CMD, (query, ), timeout=60.0):
            ngram = tuple(row.ngram.split())
            if all(i < len(ngram) and has_pos(ngram[i], pos) for i, pos in pos_condition):
                yield row.ngram, row.count
