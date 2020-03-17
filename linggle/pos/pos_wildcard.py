import os


# Build paths inside the project like: os.path.join(BASE_DIR, ...)
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
POSABBR_TABLE_PATH = os.path.join(MODULE_PATH, 'data', 'wildcards.txt')


def init_wildcard_dict():
    wildcard_dict = {}
    for line in open(POSABBR_TABLE_PATH):
        wildcards = line.split()
        for wildcard in wildcards:
            wildcard_dict[wildcard] = wildcards[0]
    return wildcard_dict


def normalize_wildcard(wildcard):
    wildcard = wildcard.lower()
    return POS_WILDCARDS.get(wildcard, wildcard)


def is_pos_wildcard(token):
    return token.lower() in POS_WILDCARDS


POS_WILDCARDS = init_wildcard_dict()
