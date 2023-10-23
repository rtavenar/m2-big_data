#!/usr/bin/env python
"""reducer.py"""

import sys

current_month = None
current_max = -1000000
month = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    month, daily_max = line.split('\t')

    # convert daily_max (currently a string) to float
    try:
        daily_max = float(daily_max)
    except ValueError:
        # daily_max was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_month == month:
      if daily_max > current_max:
        current_max = daily_max
    else:
        if current_month:
            # write result to STDOUT
            print(f"{current_month}\t{current_max}")
        current_max = daily_max
        current_month = month

# do not forget to output the last month if needed!
if current_month == month:
    print(f"{current_month}\t{current_max}")