from .linggle import BaseLinggle, DbLinggle, NoPosLinggle


try:
    from .linggle_cassandra import CassandraLinggle
except ImportError:
    pass

try:
    from .linggle_postgres import PostgresLinggle
except ImportError:
    pass

try:
    from .linggle_sqlite import SqliteLinggle
except ImportError:
    pass

__all__ = ['BaseLinggle', 'DbLinggle', 'NoPosLinggle', 'CassandraLinggle', 'PostgresLinggle', 'SqliteLinggle']


class EnLinggle(BaseLinggle):
    """English Version of Linggle"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, word_delimiter=' ', **kwargs)


class ZhLinggle(BaseLinggle):
    """Chinese Version of Linggle"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, word_delimiter='', **kwargs)


class Web1tLinggle(EnLinggle, NoPosLinggle, CassandraLinggle):
    """For web1t, the language is english, PoS is not included and we use cassandra as our dbms"""


class ZhPgLinggle(ZhLinggle, PostgresLinggle):
    """For udn and cna, the language is chinese and we use postgres as our dbms"""
