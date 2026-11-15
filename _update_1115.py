#!/usr/bin/env python3
"""Patch index.html + daily.html for 2026-11-15. ponytail: throwaway, same shape as yesterday's."""
import re

TODAY = '2026-11-15'
PREV_DATE = '2026-11-14'
TITLE = '200 万颗、275,000 颗、600,000 颗：模型权重里藏着被禁的 Blackwell'
LABEL = '行业 / 出口管制'

html = open('index.html', encoding='utf-8').read().replace('\r\n', '\n')

# ---------- 1. nf-items ----------
new_items = open('_nf_items_output.txt', encoding='utf-8').read().replace('\r\n', '\n')
start_marker = '<div class="nf-scroll" id="nf-scroll">'
end_marker = '\n\n<script>\n// AI 热点分类过滤'
i = html.index(start_marker) + len(start_marker)
j = html.index(end_marker)
assert j > i, 'nf-scroll markers not found'
html = html[:i] + '\n' + new_items + '\n' + html[j:]

# ---------- 2. review card dates (before featured card insert) ----------
n_dates = html.count(f'<div class="meta"><span>📅 {PREV_DATE}</span>')
html = html.replace(f'<div class="meta"><span>📅 {PREV_DATE}</span>', f'<div class="meta"><span>📅 {TODAY}</span>')

# ---------- 3. banner ----------
html, n = re.subn(
    r'<div class="daily-banner">\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*</div>',
    f'<div class="daily-banner">\n  <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    html, count=1)
assert n == 1, 'banner not patched'

# ---------- 4. featured card ----------
new_card = f'''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">{LABEL}</div>
      <h2><a href="featured-{TODAY}.html">{TITLE}</a></h2>
      <p>11 月 13 日，前 OpenAI 研究员 Will DePue 带着非营利机构 Unemployment Labs 做了件很像法医的事：把 DeepSeek、月之暗面、MiniMax、蚂蚁的开源权重下载下来逐一比对，发现 Kimi K3 和 DeepSeek V4 身上带着 Blackwell 芯片的训练指纹——而这种芯片从 2025 年起就被禁止卖到中国。Epoch AI 估计 2024–2025 年约 <span class="key-number">200 万</span> 颗先进芯片经隐蔽路径进入中国，<span class="key-number">27.5 万</span> 颗进了马来西亚，另有 <span class="key-number">60 万</span> 颗 H200 堆在香港等进关。禁令管得住芯片的去向，管不住算力被谁租用。</p>
      <div class="featured-meta">
        <span>📖 8 分钟</span><span>📅 {TODAY}</span><span>{LABEL}</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="图：NVIDIA GB200 NVL72 整机柜官方产品图（来源：NVIDIA Newsroom）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''
m = re.search(r'<div class="featured-card">.*?\n  </div>\n<div class="section-title" style="margin-top:12px">', html, re.S)
assert m, 'featured card not found'
html = html[:m.start()] + new_card + '\n<div class="section-title" style="margin-top:12px">' + html[m.end():]

# ---------- 5. prev-featured prepend ----------
prev_marker = '<div class="prev-featured-list">\n'
k = html.index(prev_marker) + len(prev_marker)
if f'prev-date">{TODAY}' not in html:
    html = html[:k] + f'''            <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{TITLE}</span>
      <span class="prev-arrow">→</span>
    </a>
''' + html[k:]

open('index.html', 'w', encoding='utf-8', newline='\n').write(html)
print('nf-item count:', html.count('class="nf-item"'))
print('tabs kept:', html.count('<div class="nf-tabs"'), '| filter js:', 'AI 热点分类过滤' in html)
print('review dates updated:', n_dates, '| today meta count:', html.count(f'<div class="meta"><span>📅 {TODAY}</span>'))
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
