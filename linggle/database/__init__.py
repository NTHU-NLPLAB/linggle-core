from .linggle import BaseLinggle, DbLinggle, NoPosDbLinggle
from .linggle_cassandra import CassandraLinggle
from .linggle_postgres import PostgresLinggle
from .linggle_sqlite import SqliteLinggle


__all__ = ['BaseLinggle', 'DbLinggle', 'NoPosDbLinggle', 'CassandraLinggle', 'PostgresLinggle', 'SqliteLinggle']


class EnLinggle(BaseLinggle):
    """English Version of Linggle"""
    def __init__(self, *args, **kwargs):
        self.word_delimiter = ' '
        super().__init__(*args, **kwargs)


class ZhLinggle(BaseLinggle):
    """Chinese Version of Linggle"""
    def __init__(self, *args, **kwargs):
        self.word_delimiter = ''
        super().__init__(*args, **kwargs)


class Web1tLinggle(EnLinggle, CassandraLinggle, NoPosDbLinggle):
    """For web1t, the language is english, PoS is not included and we use cassandra as our dbms"""


class UcdLinggle(ZhLinggle, PostgresLinggle):
    """For udn and cna, the language is chinese and we use postgres as our dbms"""
