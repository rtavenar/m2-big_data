#!/usr/bin/env python

import sys

# input comes from STDIN (standard input)
current_numetu = None
current_somme = 0
current_count = 0
for line in sys.stdin:
    line = line.strip()

    # parse the input we got from mapper.py
    numetu, note = line.split()

    # convert daily_max (currently a string) to float
    try:
        note = int(note)
    except ValueError:
        # daily_max was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if (current_numetu) == (numetu):
      current_count += 1
      current_somme += note
    else:
        if current_numetu:
            # write result to STDOUT
            moyenne = current_somme / current_count
            print(f"{current_numetu}\t{moyenne}")
        current_numetu = numetu
        current_somme = note
        current_count = 1

# do not forget to output the last month if needed!
if (current_numetu) == (numetu):
  moyenne = current_somme / current_count
  print(f"{current_numetu}\t{moyenne}")