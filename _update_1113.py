#!/usr/bin/env python3
"""Patch index.html + daily.html for 2026-11-13. ponytail: throwaway, same shape as yesterday's."""
import re

TODAY = '2026-11-13'
PREV_DATE = '2026-11-12'
TITLE = '33 年、14 天、85%：黄仁勋离场，Nvidia 第一次没有创始人'
LABEL = '行业 / 公司治理'

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
      <p>NVIDIA 董事会 11 月 12 日公告：黄仁勋辞去总裁、CEO 及董事职务，<span class="key-number">即刻生效</span>。从 10 月 29 日启动独立调查到落地只用了 <span class="key-number">14</span> 天，NVDA 开盘跌 <span class="key-number">14</span> 个点。CFO Colette Kress（2013 年入职，此前在 Cisco、Microsoft 做财务近 <span class="key-number">25</span> 年）出任临时 CEO，Synopsys 前 CEO Harvey C. Jones 成为公司史上首任董事会主席，永久继任者内外遴选同步启动。尴尬的是，NVIDIA 手里握着 AI 加速器约 <span class="key-number">85%</span> 的份额、五年卖出近 <span class="key-number">1400</span> 万颗旗舰芯片、过去一年在欧洲投了近 <span class="key-number">100</span> 亿美元，却没有一位准备好的接班人；内部建议箱一则帖文已积累超 <span class="key-number">1600</span> 条评论要求恢复其职位。11 月 17 日 Q3 FY2027 财报照旧，这是 Kress 的第一场考试。</p>
      <div class="featured-meta">
        <span>📖 8 分钟</span><span>📅 {TODAY}</span><span>{LABEL}</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="图：NVIDIA 官方产品图，NVLink Fusion 互联模块（来源：NVIDIA Newsroom）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
