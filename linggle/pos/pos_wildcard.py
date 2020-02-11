import os


# Build paths inside the project like: os.path.join(BASE_DIR, ...)
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
# TODO: pron: Nh
POSABBR_TABLE_PATH = os.path.join(MODULE_PATH, 'data', 'wildcards.txt')


def init_wildcard_dict():
    wildcard_dict = {}
    for line in open(POSABBR_TABLE_PATH):
        wildcards = line.strip().split('\t')
        for wildcard in wildcards:
            wildcard_dict[wildcard] = wildcards[0]
    return wildcard_dict


def normalize_wildcard(wildcard):
    wildcard = wildcard.lower()
    return POS_WILDCARDS.get(wildcard, wildcard)


POS_WILDCARDS = init_wildcard_dict()
