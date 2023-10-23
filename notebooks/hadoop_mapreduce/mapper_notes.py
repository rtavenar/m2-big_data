#!/usr/bin/env python

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    # split the line into words
    numetu, matiere, note = line.strip().split(';')
    print(f"{numetu}\t{note}")