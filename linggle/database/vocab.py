import os
from pathlib import Path
from collections import Counter


MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
VOCAB_FILE_PATH = os.environ.get('VOCAB_FILE_PATH') or os.path.join(MODULE_PATH, 'vocab.txt')


def parse_line(line):
    word, count = line.strip().split('\t')
    return word, int(count)


if Path(VOCAB_FILE_PATH).is_file():
    VOCABULARY = Counter(dict(map(parse_line, open(VOCAB_FILE_PATH))))
else:
    VOCABULARY = {}
