import os
from pathlib import Path


MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
SIM_FILE_PATH = os.environ.get('SYMNONYM_FILE_PATH') or os.path.join(MODULE_PATH, 'sims.tsv')


def parse_sim(line):
    word, sims = line.strip().split('\t')
    return word, sims.split(',')


def find_synonyms(word):
    return sim_dict.get(word, [])


if Path.is_file(SIM_FILE_PATH):
    sim_dict = dict(parse_sim(line) for line in open(SIM_FILE_PATH))
else:
    sim_dict = {}
