#!/usr/bin/env python
"""mapper.py"""

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    # split the line into words
    fields = line.strip().split()
    month = fields[1][4:6]
    daily_max = fields[5]
    print(f"{month}\t{daily_max}")