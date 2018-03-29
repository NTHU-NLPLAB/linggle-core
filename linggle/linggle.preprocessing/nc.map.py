#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import fileinput
import sys
import io

numbers = set('0123456789０１２３４５６７８９')
eng_symbols = set('{}"\'()[].,:;+!?-*/&|<>=~$%\n\t ')
ch_symbols = set('｛｝「」『』【】（）〔〕，。：；＋！？﹖——＊７｜＜＞《》〈〉＝～＄％、')


def parse_line(line):
    un, abbr, simpleTag, ckipTags = line.strip().split('\t')
    # ckipTags = ckipTags.split(', ')
    return abbr, simpleTag


# def load_posabbr():
#     posabbr = {}
#     # for abbr, simpleTag, ckipTags in map(parse_line, open('pos_list.txt')):
#     for abbr, simpleTag, ckipTags in map(parse_line, io.open('pos_list.txt', 'rt')):
#         posabbr[simpleTag] = abbr
#         for ckipTag in ckipTags:
#             posabbr[ckipTag] = abbr
#     return posabbr

def load_posabbr():
    posabbr = {}
    # for abbr, simpleTag in map(parse_line, open('pos_list.txt')):
    f = open('pos.txt','rt')
    for line in f .readlines():
        if len(line.strip().split('\t')) == 3:
            posabbr[line.strip().split('\t')[1].lower()] = line.strip().split('\t')[0]
        # print(line.strip().split('\t')[1])
        else:
            posabbr[line.strip().split('\t')[2].lower()] = line.strip().split('\t')[1]
    # for abbr, old_tag,b in map(parse_line, io.open('new_pos_text _cy.txt', 'rt')):
        # posabbr[old_tag.lower()] = abbr

    return posabbr


# def get_abbr(tag):
#     # Vh11, vh13, vh15, vh16, vh2
#     if tag.startswith('V') or tag=='SHI':
#         if tag in ['VH11', 'VH13', 'VH15', 'VH16', 'VH21', 'VH22']:
#             return 'ADJ'
#         return 'V'
#     elif tag in posabbr:
#         return posabbr[tag]
#     elif tag.startswith('P'):
#         return 'P'
#     else:
#         return tag

def get_abbr(tag):
    if tag in posabbr:
        return posabbr[tag]
    for t in posabbr:
        if tag.startswith(t):
            return posabbr[t]
    else:
        # for t in posabbr:
        #     if tag.startswith(t):
        #         return t
    # else:
        return 'un'


def ngram_is_valid(ngram):
    if any(len(word.strip()) == 0 for word in ngram):
        return False
    if any(ch in eng_symbols|ch_symbols or word in numbers for word in ngram for ch in word):
        return False
    return True


def to_ngrams(items, length):
    return zip(*([items[i:] for i in range(length)]))


def to_tokens(line):
    for token in line.split():
        split_i = token.rfind('(')
        word, tag = token[:split_i], token[split_i+1:-1]
        tag = get_abbr(tag)
        yield word, tag


posabbr = load_posabbr()
# for i in posabbr:
    # print(i)
# print(posabbr)

if __name__ == '__main__':
    for line in fileinput.input():
    # for line in io.open(sys.stdin.fileno(), 'rt'):
        line = line.strip()
        # <P>, </P>, </HEADLINE>, <DATELINE>, ...
        if line.startswith('<') and line.endswith('>'):
            continue

        tokens = list(to_tokens(line))
        # print('token')

        for n in range(1, 6):
            for ngramtags in to_ngrams(tokens, n):
                ngram, tags = list(zip(*ngramtags))
                # if len(ngram) == 2 and ngram[-1] == '的':
                #     continue
                if ngram_is_valid(ngram):
                    # print(' '.join(ngram), ' '.join(tags))
                    print(' '.join(ngram), ' '.join(tags))
