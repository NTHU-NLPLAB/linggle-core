from math import ceil, log10
from operator import itemgetter


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
