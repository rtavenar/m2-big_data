#!/usr/bin/env python3.12

import sys

print(f"Nom du programme : {sys.argv[0]}")

i = 1
while i < len(sys.argv):
    if sys.argv[i].startswith("-"):
        print(f"* Nom de l'argument : {sys.argv[i]}")
        print(f"  * Valeur de l'argument : {sys.argv[i + 1]}")
        i += 2
    else:
        print(f"* Valeur de l'argument (non nommé) : {sys.argv[i]}")
        i += 1
