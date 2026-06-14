#!/usr/bin/env python3
import json
data = json.load(open('aihot_selected.json'))
print(f'Total items: {len(data["items"])}')
cats = {}
for i in data['items']:
    cat = i.get('category')
    cats[cat] = cats.get(cat, 0) + 1
print('Categories:', json.dumps(cats, ensure_ascii=False))
print('First item title:', data['items'][0]['title'])
print('First item publishedAt:', data['items'][0].get('publishedAt'))
