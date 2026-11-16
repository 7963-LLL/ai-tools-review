#!/usr/bin/env python3
"""Patch index.html + daily.html for 2026-11-16. ponytail: throwaway, same shape as yesterday's."""
import re

TODAY = '2026-11-16'
PREV_DATE = '2026-11-15'
TITLE = '2500 亿美元、减半、11.5 万个签名：把黄仁勋推下台的不是绯闻'
LABEL = '行业 / 资本结构'

html = open('index.html', encoding='utf-8').read().replace('\r\n', '\n')

# ---------- 1. nf-items ----------
new_items = open('_nf_items_output.txt', encoding='utf-8').read().replace('\r\n', '\n')
start_marker = '<div class="nf-scroll" id="nf-scroll">'
end_marker = '\n\n<script>\n// AI 热点分类过滤'
i = html.index(start_marker) + len(start_marker)
j = html.index(end_marker)
assert j > i, 'nf-scroll markers not found'
html = html[:i] + '\n' + new_items + '\n' + html[j:]

# ---------- 2. review card dates ----------
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
      <p>11 月 12 日 Nvidia 董事会宣布黄仁勋即刻卸任，对外解释是绯闻；两天后《华尔街日报》给了另一个版本：真正让董事会动手的，是他主导的客户融资担保——最大一笔是对 OpenAI 俄亥俄数据中心的 <span class="key-number">2500 亿美元</span>，消息公开当天股价跌 <span class="key-number">5%</span>，临时 CEO Colette Kress 上任第一件事就是把它砍掉一半。同一周 IMF 警告 AI 循环融资已超 <span class="key-number">1 万亿美元</span>，其中三分之二靠借。请愿书收了 <span class="key-number">11.5 万</span> 个签名，一封声称有副总裁联署的信被本人指为伪造。</p>
      <div class="featured-meta">
        <span>📖 9 分钟</span><span>📅 {TODAY}</span><span>{LABEL}</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="图：NVIDIA DSX Pod AI 工厂整机柜官方产品图（来源：NVIDIA Newsroom）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
