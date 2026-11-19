#!/usr/bin/env python3
"""Fill index.html nf-items / banner / review dates / daily nav from today's data."""
import re, json
from datetime import datetime, timezone, timedelta

TODAY = '2026-11-19'
BJT = timezone(timedelta(hours=8))

nf = open('_nf_items_output.txt', encoding='utf-8').read().strip()
html = open('index.html', encoding='utf-8').read()

# 1. nf-items block
start_marker = '<div class="nf-scroll" id="nf-scroll">\n'
i = html.index(start_marker) + len(start_marker)
j = html.index('\n\n<script>', i)
html = html[:i] + '\n' + nf + '\n' + html[j:]
assert html.count('class="nf-item"') == 50, html.count('class="nf-item"')

# 2. daily banner
html, n = re.subn(r'<div class="daily-banner">\s*\n\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*\n</div>',
    f'<div class="daily-banner">\n  <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    html, count=1)
assert n == 1

# 3. review card dates
html = re.sub(r'<span>📅 2026-11-1[0-9]</span><span>📖', f'<span>📅 {TODAY}</span><span>📖', html)
html, n = re.subn(r'(<div class="meta"><span>📅 )2026-11-1[0-9](</span>)', rf'\g<1>{TODAY}\g<2>', html)
print('review dates updated:', n)

open('index.html', 'w', encoding='utf-8').write(html)

# 4. daily.html nav + banner
d = open('daily.html', encoding='utf-8').read()
d, n1 = re.subn(r'<div class="daily-banner">\s*\n\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*\n</div>',
    f'<div class="daily-banner">\n      <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>', d, count=1)
d, n2 = re.subn(r'(<div class="daily-nav">\n)',
    rf'\g<1>    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n', d, count=1)
assert n1 == 1 and n2 == 1
open('daily.html', 'w', encoding='utf-8').write(d)
print('OK index + daily')
