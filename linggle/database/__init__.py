from .linggle import BaseLinggle, DbLinggle, NoPosLinggle


class EnLinggle(BaseLinggle):
    """English Version of Linggle"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, word_delimiter=' ', **kwargs)


class ZhLinggle(BaseLinggle):
    """Chinese Version of Linggle"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, word_delimiter='', **kwargs)


_linggle_classes = []

try:
    from .linggle_cassandra import CassandraLinggle
    _linggle_classes.append(CassandraLinggle.__name__)
except ImportError:
    pass

try:
    from .linggle_postgres import PostgresLinggle
    _linggle_classes.append(PostgresLinggle.__name__)
except ImportError:
    pass

try:
    from .linggle_sqlite import SqliteLinggle
    _linggle_classes.append(SqliteLinggle.__name__)
except ImportError:
    pass

if "PostgresLinggle" in dir():
    class ZhPgLinggle(ZhLinggle, PostgresLinggle):
        """For udn and cna, the language is chinese and we use postgres as our dbms"""

    _linggle_classes.append("ZhPgLinggle")

if "CassandraLinggle" in dir():
    class Web1tLinggle(EnLinggle, NoPosLinggle, CassandraLinggle):
        """For web1t, the language is english, PoS is not included and we use cassandra as our dbms"""

    _linggle_classes.append("Web1tLinggle")


__all__ = [
    'BaseLinggle', 'DbLinggle', 'NoPosLinggle', 'EnLinggle', 'ZhLinggle',
    *_linggle_classes,
]
