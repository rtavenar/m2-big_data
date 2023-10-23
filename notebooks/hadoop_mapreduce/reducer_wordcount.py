#!/usr/bin/env python

import sys

# input comes from STDIN (standard input)
current_word = None
current_count = 0
for line in sys.stdin:
    line = line.strip()

    # parse the input we got from mapper.py
    w, count = line.split()

    # convert daily_max (currently a string) to float
    try:
        count = int(count)
    except ValueError:
        # daily_max was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == w:
      current_count += count
    else:
        if current_word:
            # write result to STDOUT
            print(f"{current_word}\t{current_count}")
        current_word = w
        current_count = count

# do not forget to output the last month if needed!
if current_word == w:
    print(f"{current_word}\t{current_count}")