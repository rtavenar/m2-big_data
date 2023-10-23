#!/usr/bin/env python

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    # split the line into words
    words = line.strip().split()
    for punct in [',', '.', '?']:
      words = words.replace(punct, ' ')
    for w in words:
      if w != '':
        print(f"{w.replace(',', '').replace('.', '')} 1")