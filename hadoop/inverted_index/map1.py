#!/usr/bin/env python3
"""Map 1."""
import sys
import re
import csv
import os
import glob

csv.field_size_limit(sys.maxsize)
csv_reader = csv.reader(sys.stdin, delimiter=',')

for row in csv_reader:
  # get word from title and content
  row_word = row[1] + " " + row[2]
  word_list = row_word.split()
  target = []
  for word in word_list:
    # only alphabetic word
    word = re.sub(r'[^a-zA-Z0-9]+', '', word)
    if word: 
      target.append(word.lower()) # target is a list of all words in specific document
  with open("stopwords.txt", "r") as stopwords:
    # remove stop word from target list
    for line in stopwords:
      for eachword in target:
        if eachword == line.strip():
          target.remove(eachword)
  # print all words in this document
  for word in target:
    print(word + "\t" + str(row[0]))