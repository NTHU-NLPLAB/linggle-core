import os
import logging

from linggle.database.sims import find_similar_words


_backend = os.getenv('LINGGLE_BACKEND', 'web1t')
if _backend == 'web1t':
    from linggle.database import Web1tLinggle as Linggle
elif _backend == 'zhpg':
    from linggle.database import ZhPgLinggle as Linggle
elif _backend == 'cassandra':
    from linggle.database import CassandraLinggle as Linggle
elif _backend in ('pg', 'postgres'):
    from linggle.database import PostgresLinggle as Linggle
else:
    from linggle.database import SqliteLinggle as Linggle

RETRY_TIMES = 3
linggle = None


def linggle_it(query):
    try:
        for _ in range(RETRY_TIMES):
            try:
                return linggle[query]
            except Exception as e:
                logging.error(str(e))
                init_linggle()
    except Exception as e:
        logging.error(str(e))
    return []


def init_linggle():
    global linggle
    linggle = Linggle(find_synonyms=find_similar_words)


init_linggle()
