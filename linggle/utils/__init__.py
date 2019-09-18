from math import ceil, log10
from operator import itemgetter
import bottleneck as bn
import numpy as np


def to_old_linggle_format(result):
    def roundsig(number, digit=2):
        return int(round(number, -int(ceil(log10(number)))+digit))

    total = sum(map(itemgetter(1), result)) / 100
    old_format_result = []
    for ngram, count in result:
        old_format_result.append({
            'count': int(count),
            'phrase': ngram,
            'count_str': '{0:,}'.format(roundsig(count)),
            'percent': '{0}%'.format(round(count / total, 1))
        })

    return old_format_result


def nlargest(a, n, sort=True):
    m = len(a)
    n = min(m, n)
    nlargest_list = bn.partition(a, m-n)[-n:]
    if sort:
        nlargest_list[::-1].sort()
    return nlargest_list


# def nlargest(a, n):
#     pd.Series(test).nlargest(5).tolist()