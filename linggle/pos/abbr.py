import os


# Build paths inside the project like: os.path.join(BASE_DIR, ...)
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
# TODO: pron: Nh
POSABBR_TABLE_PATH = os.path.join(MODULE_PATH, 'data', 'abbr.txt')


def init_abbr_dict():
    abbr_dict = {}
    for line in open(POSABBR_TABLE_PATH):
        abbr, *poss = line.strip().split('\t')
        abbr_dict[abbr] = abbr
        for pos in poss:
            abbr_dict[pos] = abbr
    return abbr_dict


POS_WILDCARD = init_abbr_dict()
