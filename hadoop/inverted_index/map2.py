#!/usr/bin/env python3
"""Map second time."""

import sys
import math

filenum = 0
with open('total_document_count.txt','r') as afile:
  filenum = afile.readline()
for line in sys.stdin:
  item = line.split('\t') #split key and value(list)
  doc_list = item[1].split()
  contain = len(doc_list) / 2
  total = math.log10(int(filenum) / contain)
  doc_list.append(str(total)) # add idf to the end of value list
  output = ''
  for temp in doc_list:
    output = output + temp + ' '       
  print(item[0]+'\t'+output)