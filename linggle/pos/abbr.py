#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


posabbr = load_posabbr()

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
