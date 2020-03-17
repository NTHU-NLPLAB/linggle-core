import os
from pathlib import Path


MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
SIM_FILE_PATH = os.environ.get('SIM_FILE_PATH') or os.path.join(MODULE_PATH, 'sims.tsv')


def parse_sim(line):
    word, sims = line.strip().split('\t')
    return word, sims.split(',')


def find_similar_words(word, default=()):
    return sim_dict.get(word, default)


if Path(SIM_FILE_PATH).is_file():
    sim_dict = dict(map(parse_sim, open(SIM_FILE_PATH)))
else:
    sim_dict = {}
