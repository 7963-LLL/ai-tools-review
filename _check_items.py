#!/usr/bin/env python3
import re
from collections import Counter

html = open('index.html','r').read()
items = re.findall(r'href="([^"]+)"[^>]*class="nf-item"', html)
print(f'Total nf-items: {len(items)}')
c = Counter(items)
dupes = [k for k,v in c.items() if v > 1]
if dupes:
    print(f'Duplicates ({len(dupes)}):')
    for d in dupes[:5]:
        print(f'  {d} (count: {c[d]})')
else:
    print('No duplicates found')
print('\nLast 10 items:')
for u in items[-10:]:
    print(f'  {u}')
