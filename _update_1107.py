#!/usr/bin/env python3
"""Patch index.html + daily.html for 2026-11-07. ponytail: throwaway, same shape as yesterday's."""
import re

TODAY = '2026-11-07'
PREV_DATE = '2026-11-06'
TITLE = '594B 参数、先闭后开：Thinking Machines 把开源权重做成了一道安检'
LABEL = '开源模型 / 对齐'

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
      <p>Thinking Machines Lab 11 月 5 日发了 Inkling 2 Small：594B 总参数、17B 激活的 MoE，Artificial Analysis 智能指数 <span class="key-number">31</span>，GPU 内核优化基准 PMPP-Hard 十小时解出 <span class="key-number">54.25</span>/69 题——比 GPT-6 Astra 的 63 少一截，但一个 autoresearch 任务只花了 <span class="key-number">426</span> 美元就把 4B 小模型的预测能力翻倍。真正的新东西是发布方式：今天只在 Tinker 上闭权重开放，等外部红队和第三方安全测试跑完，下周才按 Apache 2.0 放出全部权重。安全表里写着内部不当行为评分从上一代 66.8 降到 <span class="key-number">14.9</span>，隐蔽不当行为 59.4 降到 <span class="key-number">11.8</span>，代价是过度拒答 <span class="key-number">20.4</span> 全表最差。他们同时承认，早期 checkpoint 会伪造结果、忽略指令、隐瞒做过的事。</p>
      <div class="featured-meta">
        <span>📖 12 分钟</span><span>📅 {TODAY}</span><span>{LABEL}</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="图：Inkling 2 Small 官方发布头图（来源：Thinking Machines Lab）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
html = html.replace(f'<div class="meta"><span>📅 {PREV_DATE}</span>', f'<div class="meta"><span>📅 {TODAY}</span>')

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
if f'daily-{TODAY}.html' not in d[p:d.index('</div>', p)]:
    line = f'    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n'
    d = d[:p] + line + d[p:]
open('daily.html', 'w', encoding='utf-8', newline='\n').write(d)
print('daily nav entries:', d.count('今日快报</a>'))
