#!/usr/bin/env python3
"""Patch index.html + daily.html for 2026-11-05. ponytail: throwaway, same shape as the last hundred."""
import re

TODAY = '2026-11-05'
PREV = '2026-11-04'
TITLE = '2.8 万亿参数、5.6TB 权重：Kimi K3.1 Pro 开源了，也把「本地跑不动」一起开源了'

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
      <div class="featured-label">开源模型</div>
      <h2><a href="featured-{TODAY}.html">{TITLE}</a></h2>
      <p>10 月 24 日发布时承诺的权重，11 月 5 日兑现：月之暗面在 Hugging Face 开放 Kimi K3.1 Pro，2.8 万亿总参数、单次推理只激活约 1040 亿、100 万 Token 上下文。Agent Arena 从 1.75 万次真实智能体会话里抽信号做因果推断，它净改进率 <span class="key-number">+5.1%</span>（上一代 K3 是 +0.9%），开放权重第一、全部模型第 13；Bash 可靠性从 -4.5% 翻到 <span class="key-number">+7.9%</span>。Terminal-Bench 4.0 拿 <span class="key-number">65.7%</span>，压过 GPT-6 Astra 的 58.2%，离 Claude Opus 5.5 的 66.4% 只差 0.7 个点。代价写在存储上：BF16 权重 <span class="key-number">5.6TB</span>，INT4 量化仍要 1.4TB。</p>
      <div class="featured-meta">
        <span>📖 11 分钟</span><span>📅 {TODAY}</span><span>开源模型</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="图：Kimi K3.1 Pro 官方发布视觉（来源：kimi.com 官方技术博客）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
html = html.replace(f'<div class="meta"><span>📅 {PREV}</span>', f'<div class="meta"><span>📅 {TODAY}</span>')

open('index.html', 'w', encoding='utf-8', newline='\n').write(html)
print('nf-item count:', html.count('class="nf-item"'))
print('tabs kept:', html.count('<div class="nf-tabs"'), '| filter js:', 'AI 热点分类过滤' in html)
print('review dates now today:', html.count(f'<div class="meta"><span>📅 {TODAY}</span>'))

# ---------- 6. daily.html nav ----------
d = open('daily.html', encoding='utf-8').read().replace('\r\n', '\n')
d, n = re.subn(
    r'<div class="daily-banner">\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*</div>',
    f'<div class="daily-banner">\n      <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    d, count=1)
assert n == 1, 'daily banner not patched'
nav_marker = '<div class="daily-nav">\n'
p = d.index(nav_marker) + len(nav_marker)
nav_end = d.index('</div>', p)
nav = d[p:nav_end]
for day in (TODAY, PREV):          # backfill 11-04, which the old script skipped
    if f'daily-{day}.html' not in nav:
        d = d[:p] + f'    <a href="daily-{day}.html">📅 {day} 今日快报</a>\n' + d[p:]
        p += len(f'    <a href="daily-{day}.html">📅 {day} 今日快报</a>\n')
        nav_end = d.index('</div>', p)
        nav = d[p:nav_end]
open('daily.html', 'w', encoding='utf-8', newline='\n').write(d)
print('daily nav entries:', d.count('今日快报</a>'))
