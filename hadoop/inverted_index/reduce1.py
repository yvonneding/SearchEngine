#!/usr/bin/env python3
"""Reduce first time."""
import sys

# filenum = 0
# with open('total_document_count.txt','r') as afile:
#   filenum = afile.readline()
previous = ' '
doc_dict = {} # eg: {25:1, 30:2}(occur once in doc25 and twice in doc30)
term_dict = {} # eg:{document: {25:1, 30:2}}
for line in sys.stdin:
  item = line.split('\t')
  if previous != item[0]:
    doc_dict = {}
  if item[1] in doc_dict: 
    # if this doc_id already in the dictionary, occurance plus one
    doc_dict[item[1]] += 1
  else:
    doc_dict[item[1]] = 1
  # term_dict will be continuosly overwritten
  term_dict[item[0]] = doc_dict
  previous = item[0]

for key,value in term_dict.items():
  print(key, end = '\t')
  for keys, values in value.items():
    print(keys.strip() + ' ' + str(values), end = ' ')
  print('')
