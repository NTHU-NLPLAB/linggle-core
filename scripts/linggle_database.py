import os
import logging

from linggle.database.sims import find_similar_words


_backend = os.getenv('LINGGLE_BACKEND', 'web1t')
if _backend == 'web1t':
    from linggle.database import Web1tLinggle as Linggle
elif _backend == 'zhpg':
    from linggle.database import ZhPgLinggle as Linggle


RETRY_TIMES = 3
linggle = None


def linggle_it(query):
    for _ in range(RETRY_TIMES):
        try:
            return linggle[query]
        except Exception as e:
            logging.error(str(e))
            init_linggle(find_synonyms=find_similar_words)
    return []


def init_linggle():
    global linggle
    linggle = Linggle()


init_linggle(find_synonyms=find_similar_words)
