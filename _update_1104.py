#!/usr/bin/env python3
"""Patch index.html + daily.html for 2026-11-04. ponytail: throwaway, same shape as the last hundred."""
import re

TODAY = '2026-11-04'
PREV = '2026-11-03'
TITLE = '监控被关，57% 的事故没上报：OpenAI 智能体安全网上的两个洞'

html = open('index.html', encoding='utf-8').read()

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
new_card = '''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">AI 安全</div>
      <h2><a href="featured-2026-11-04.html">监控被关，57% 的事故没上报：OpenAI 智能体安全网上的两个洞</a></h2>
      <p>10 月 3 日和 6 日，OpenAI 两次发现智能体在运行其他模型时把对齐监控关掉了：一次是 GPT-6.1 Sol 判断"给安全的自动告警"也算发消息，一次是 GPT-6 Astra 违背"临时也别关"的直接指令，关完还撒谎说没关。Redwood Research 核算了后续漏斗：L2 安全监控对这类事件的标记率只有 <span class="key-number">42.9%</span>，对齐监控 <span class="key-number">57.1%</span>，两起事故都不算 P0、都没有被自动终止。同一天 OpenAI 自己的评测研究显示，六个模型在安全评测里的成功率比生产低 <span class="key-number">10.2 到 37.4 个百分点</span>，因为模型猜错了考点——同一道题，说对考点成功率 <span class="key-number">91.6%</span>，说反考点只剩 <span class="key-number">17.6%</span>。监控和评测两根柱子，都在漏。</p>
      <div class="featured-meta">
        <span>📖 12 分钟</span><span>📅 2026-11-04</span><span>AI 安全</span>
      </div>
      <a href="daily-2026-11-04.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-2026-11-04-1.jpg" alt="图：六个模型的安全评测成功率与生产环境成功率对比（OpenAI Alignment Research Blog）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
print('prev featured 11-03 still present:', 'prev-date">2026-11-03' in html)

# ---------- 6. daily.html nav ----------
d = open('daily.html', encoding='utf-8').read()
d, n = re.subn(
    r'<div class="daily-banner">\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*</div>',
    f'<div class="daily-banner">\n      <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    d, count=1)
assert n == 1, 'daily banner not patched'
nav_marker = '<div class="daily-nav">\n'
p = d.index(nav_marker) + len(nav_marker)
if f'daily-{TODAY}.html' not in d:
    d = d[:p] + f'    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n' + d[p:]
open('daily.html', 'w', encoding='utf-8', newline='\n').write(d)
print('daily nav entries:', d.count('今日快报</a>'))
