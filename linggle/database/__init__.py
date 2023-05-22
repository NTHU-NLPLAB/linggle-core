from .linggle import BaseLinggle, DbLinggle, NoPosLinggle
from .linggle_sqlite import SqliteLinggle

__all__ = ['BaseLinggle', 'DbLinggle', 'NoPosLinggle', "SqliteLinggle"]


class EnLinggle(BaseLinggle):
    """English Version of Linggle"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, word_delimiter=' ', **kwargs)


class ZhLinggle(BaseLinggle):
    """Chinese Version of Linggle"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, word_delimiter='', **kwargs)


try:
    from .linggle_cassandra import CassandraLinggle
    __all__.append("CassandraLinggle")
except ImportError:
    pass

try:
    from .linggle_postgres import PostgresLinggle
    __all__.append("PostgresLinggle")
except ImportError:
    pass


if "PostgresLinggle" in __all__:
    class ZhPgLinggle(ZhLinggle, PostgresLinggle):
        """For udn and cna, the language is chinese and we use postgres as our dbms"""

    __all__.append('ZhPgLinggle')

if "CassandraLinggle" in __all__:
    class Web1tLinggle(EnLinggle, NoPosLinggle, CassandraLinggle):
        """For web1t, the language is english, PoS is not included and we use cassandra as our dbms"""

    __all__.append('Web1tLinggle')
