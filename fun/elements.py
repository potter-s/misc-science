#!/usr/bin/env python3

# Credit for finding all ways to split a string:
# https://www.geeksforgeeks.org/find-all-possible-ways-to-split-the-given-string-into-primes/
# Simple (non-recursive) approach

import sys

if len(sys.argv) != 2:
    sys.exit(1)
word = sys.argv[1]

elements = {}
with open('elements.csv') as fh:
    for line in fh:
        symbol = line.rstrip()
        elements[symbol.lower()] = symbol

wlen = len(word)
nsplits = 2 ** (wlen - 1)

for i in range(nsplits):
    idx = 0
    splitc = []
    for j in range(wlen):
        splitc.append(word[j])
        splitc.append(" " if i & 1 << j else "")
    splitc.pop()
    words = ''.join(splitc).split(' ')
    words = [elements[x] if x in elements else "" for x in words]
    if '' in words:
        continue
    print('-'.join(words))
