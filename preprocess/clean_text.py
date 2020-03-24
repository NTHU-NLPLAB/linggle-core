#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodedata

if __name__ == "__main__":
    import fileinput
    for line in map(str.rstrip, fileinput.input()):
        if all(unicodedata.category(ch)[0] != "C" for ch in line):
            print(line)
