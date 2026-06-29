#!/usr/bin/env python3
"""Verify everything for today's update"""
import re, os, glob

html = open('index.html', encoding='utf-8').read()
items = re.findall(r'class="nf-item"', html)
print('=== index.html ===')
print(f'n-items: {len(items)} (need 50)')
print(f'nf-tabs exists: {"nf-tabs" in html and "nf-box" in html}')
print(f'Tab filter JS: {"querySelectorAll" in html and "nf-tab" in html}')
print(f'Featured has Grok 4.5: {"Grok 4.5" in html}')
print(f'Featured has visual: {"featured-visual" in html}')

banner_m = re.search(r'href="(daily-\d{4}-\d{2}-\d{2}\.html)"', html)
print(f'Banner link: {banner_m.group(1) if banner_m else "NOT FOUND"}')

# Find date patterns in meta spans
card_dates = set()
for m in re.finditer(r'meta.*?(\d{4}-\d{2}-\d{2})', html):
    card_dates.add(m.group(1))
print(f'Dates in meta: {card_dates}')

prev_count = len(re.findall(r'class="prev-featured-item"', html))
print(f'Prev featured count: {prev_count}')

print()
print('=== Files ===')
print(f'daily-2026-06-29.html exists: {os.path.exists("daily-2026-06-29.html")}')
print(f'featured-2026-06-29.html exists: {os.path.exists("featured-2026-06-29.html")}')

print()
print('=== Featured article ===')
article = open('featured-2026-06-29.html', encoding='utf-8').read()
body_start = article.find('<div class="article-body">')
body_end = article.find('<div class="bottom-cta">')
if body_start >= 0 and body_end > body_start:
    body_text = article[body_start:body_end]
    non_html = re.sub(r'<[^>]+>', '', body_text).strip()
    print(f'Article body ~{len(non_html)} chars')
print(f'Featured has Grok 4.5: {"Grok 4.5" in article}')

print()
print('=== Images ===')
for img in sorted(glob.glob('images/featured-2026-06-29*')):
    size = os.path.getsize(img)
    status = 'OK' if size > 10000 else 'TOO SMALL'
    print(f'{status}: {img} ({size} bytes)')
