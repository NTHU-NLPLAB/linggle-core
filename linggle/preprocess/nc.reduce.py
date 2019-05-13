#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from itertools import groupby
import fileinput
import sys
import io


if __name__ == '__main__':
    for line, lines in groupby(fileinput.input()):
    # for line, lines in groupby(io.open(sys.stdin.fileno(), 'rt')):
        try:
            count = sum(1 for _ in lines)
            # print(line.strip(), count, sep='\t')
            print(line.strip(), count, sep='\t')
        except:
            import sys
            print(line, file=sys.stderr)
