import re
import fileinput
from nltk.tokenize import sent_tokenize


paragraph_re = re.compile('<p>', re.IGNORECASE)
masked_token = re.compile('(@\s*)+@')


def parse_coca_line(line):
    *_, content = line.split(' ', 1)
    content = ' '.join(content.split())
    content = masked_token.sub('@@', content)
    # tid = int(tid.strip('#'))
    for paragraph in paragraph_re.split(content):
        for sent in sent_tokenize(paragraph.strip()):
            sent = sent.strip()
            if sent:
                yield sent


def parse_coca_text(iterable):
    for line in iterable:
        line = line.strip()
        if line:
            for sent in parse_coca_line(line):
                yield sent


if __name__ == '__main__':
    for sent in parse_coca_text(fileinput.input()):
        print(sent)
