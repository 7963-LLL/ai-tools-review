#!/usr/bin/env python3
"""Patch index.html + daily.html for 2026-11-11. ponytail: throwaway, same shape as yesterday's."""
import re

TODAY = '2026-11-11'
PREV_DATE = '2026-11-10'
TITLE = '8.25 亿股、$70–78、代码 ANT：Anthropic 把万亿估值交给公开市场定价'
LABEL = '公司 / 资本市场'

html = open('index.html', encoding='utf-8').read().replace('\r\n', '\n')

# ---------- 1. nf-items ----------
new_items = open('_nf_items_output.txt', encoding='utf-8').read().replace('\r\n', '\n')
start_marker = '<div class="nf-scroll" id="nf-scroll">'
end_marker = '\n\n<script>\n// AI 热点分类过滤'
i = html.index(start_marker) + len(start_marker)
j = html.index(end_marker)
assert j > i, 'nf-scroll markers not found'
html = html[:i] + '\n' + new_items + '\n' + html[j:]

# ---------- 2. banner ----------
html, n = re.subn(
    r'<div class="daily-banner">\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*</div>',
    f'<div class="daily-banner">\n  <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    html, count=1)
assert n == 1, 'banner not patched'

# ---------- 3. featured card ----------
new_card = f'''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">{LABEL}</div>
      <h2><a href="featured-{TODAY}.html">{TITLE}</a></h2>
      <p>Anthropic 11 月 10 日启动 IPO 路演：<span class="key-number">8.25</span> 亿股 A 类股、每股 <span class="key-number">70</span> 至 <span class="key-number">78</span> 美元、纳斯达克代码 <span class="key-number">ANT</span>。按区间计入期权与受限股，对应 <span class="key-number">1.26</span> 万亿至 <span class="key-number">1.41</span> 万亿美元；FT 称认购太热，承销商正考虑把目标估值拉回 <span class="key-number">1.5</span> 万亿以上，若定价冲出区间，募资将超过 <span class="key-number">1000</span> 亿美元，Google、Nvidia、Microsoft 按发行价认购 <span class="key-number">260</span> 亿。同日修订的 S-1 还披露两笔不可撤销算力承诺——Microsoft 到 2033 年至少 <span class="key-number">472</span> 亿、Google 最低 <span class="key-number">1213</span> 亿美元，以及公司已越过 RSP 能力阈值。Gary Marcus 的反驳同样具体：Q2 环比 <span class="key-number">147%</span>、Q3 只剩 <span class="key-number">47%</span>，未来负债近 <span class="key-number">9000</span> 亿美元。</p>
      <div class="featured-meta">
        <span>📖 11 分钟</span><span>📅 {TODAY}</span><span>{LABEL}</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="图：Anthropic 官方品牌标识（来源：anthropic.com 官方新闻稿）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''
m = re.search(r'<div class="featured-card">.*?\n  </div>\n<div class="section-title" style="margin-top:12px">', html, re.S)
assert m, 'featured card not found'
html = html[:m.start()] + new_card + '\n<div class="section-title" style="margin-top:12px">' + html[m.end():]

# ---------- 4. prev-featured prepend ----------
prev_marker = '<div class="prev-featured-list">\n'
k = html.index(prev_marker) + len(prev_marker)
if f'prev-date">{TODAY}' not in html:
    html = html[:k] + f'''            <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{TITLE}</span>
      <span class="prev-arrow">→</span>
    </a>
''' + html[k:]

# ---------- 5. review card dates ----------
n_dates = html.count(f'<div class="meta"><span>📅 {PREV_DATE}</span>')
html = html.replace(f'<div class="meta"><span>📅 {PREV_DATE}</span>', f'<div class="meta"><span>📅 {TODAY}</span>')

open('index.html', 'w', encoding='utf-8', newline='\n').write(html)
print('nf-item count:', html.count('class="nf-item"'))
print('tabs kept:', html.count('<div class="nf-tabs"'), '| filter js:', 'AI 热点分类过滤' in html)
print('review dates updated from', n_dates, '-> now today:', html.count(f'<div class="meta"><span>📅 {TODAY}</span>'))
print('prev items:', html.count('class="prev-featured-item"'))

# ---------- 6. daily.html nav ----------
d = open('daily.html', encoding='utf-8').read().replace('\r\n', '\n')
d, n = re.subn(
    r'<div class="daily-banner">\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*</div>',
    f'<div class="daily-banner">\n      <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    d, count=1)
assert n == 1, 'daily banner not patched'
nav_marker = '<div class="daily-nav">\n'
p = d.index(nav_marker) + len(nav_marker)
if f'daily-{TODAY}.html' not in d[p:d.index('</div>', p)]:
    line = f'    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n'
    d = d[:p] + line + d[p:]
open('daily.html', 'w', encoding='utf-8', newline='\n').write(d)
print('daily nav entries:', d.count('今日快报</a>'))
