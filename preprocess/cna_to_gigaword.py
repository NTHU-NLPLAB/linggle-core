#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque

from zh_sent_tokenize import ckip_sent_tokenize


def cna_to_gigaword(lines):
    stack = deque()
    for line in lines:
        line = line.strip()

        # tag
        if line.startswith('<') and line.endswith('>'):
            if stack:
                for sent in ckip_sent_tokenize('\u3000'.join(stack)):
                    print(sent)
                stack.clear()
            print(line)
        # text
        elif line:
            stack.append(line)
        # empty
        else:
            if stack:
                for sent in ckip_sent_tokenize('\u3000'.join(stack)):
                    print(sent)
                stack.clear()

    if stack:
        for sent in ckip_sent_tokenize('\u3000'.join(stack)):
            print(sent)


if __name__ == '__main__':
    import fileinput
    cna_to_gigaword(fileinput.input())
