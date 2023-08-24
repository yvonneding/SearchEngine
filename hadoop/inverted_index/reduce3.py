#!/usr/bin/env python3
"""Reduce third time."""
import sys

calc = 0
previous = ''
lines = sys.stdin.readlines()
docdict = {}
for line in lines:
  item = line.split('\t')
  target = item[1].split() # target: word + occurance + log
  if previous != item[0]:
    calc = 0
  calc += (float(target[1])**2) * (float(target[2])**2) # normalization
  docdict[item[0]] = calc
  previous = item[0]

for line in lines:
  item = line.split('\t')
  target = item[1].split()
  print(target[0]+'\t'+target[2]+' '+item[0]+' '+target[1]+' '+str(docdict[item[0]])) # word becomes key
