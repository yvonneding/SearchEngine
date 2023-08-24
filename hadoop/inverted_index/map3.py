#!/usr/bin/env python3
"""Map third time."""

import sys

filenum = 0
with open('total_document_count.txt','r') as afile:
  filenum = afile.readline()
output_list = []
for line in sys.stdin:
  item = line.split('\t')
  #doc_id = 0
  doc_list = item[1].split()
  i = 0
  while i < len(doc_list)-1:
    print(doc_list[i] + '\t' + item[0] + ' ' + doc_list[i+1] + ' ' + doc_list[len(doc_list)-1])
    i += 2


  # for i in range(int(filenum)):
  #   if target[i] != str(0):
  #     print(target[i+int(filenum)]+'\t'+item[0]+' '+str(target[len(target)-1])+' '+str(target[i]))




