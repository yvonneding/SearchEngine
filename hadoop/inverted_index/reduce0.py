#!/usr/bin/env python3
"""Reduce 0."""
import sys

count = 0
for line in sys.stdin:
  count += 1
with open('total_document_count.txt','w') as afile:
  afile.write(str(count))

