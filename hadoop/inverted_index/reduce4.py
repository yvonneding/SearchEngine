#!/usr/bin/env python3
"""Reduce fourth time."""
import sys

output_dic = {}
for line in sys.stdin:
  item = line.split('\t')
  target = item[1].split()
  if item[0] in output_dic:
    output_dic[item[0]].append(target[1])
    output_dic[item[0]].append(target[2])
    output_dic[item[0]].append(target[3])
  else:
    output_dic[item[0]] = target

for key in output_dic:
  output = ''
  for temp in output_dic[key]:
    output = output + temp + ' '
  print(key+'\t'+output)