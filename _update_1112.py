#!/usr/bin/env python3
"""Patch index.html + daily.html for 2026-11-12. ponytail: throwaway, same shape as yesterday's."""
import re

TODAY = '2026-11-12'
PREV_DATE = '2026-11-11'
TITLE = '88.2% 找到、54.8% 打通、71.0% 修好：Gemini 4 Carbon 把前沿模型的卖点换成了「能修漏洞」'
LABEL = '模型 / 安全'

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
      <p>Google DeepMind 11 月 10 日开放 Gemini 4 Carbon：Artificial Analysis 智能指数 <span class="key-number">59</span> 分居首，SEC-bench Pro <span class="key-number">88.2%</span> 找漏洞、ExploitGym <span class="key-number">54.8%</span> 验证可利用、CWE-bench <span class="key-number">71.0%</span> 出根因补丁。Cursor 实测 high effort 下 CursorBench 4.0 拿 <span class="key-number">60.4%</span> 第一，Perplexity 的 WANDR、Zapier 的 AutomationBench 同样第一，单任务成本比第二名外部模型低 <span class="key-number">2</span> 倍以上。定价与 Argon 同为每百万 token <span class="key-number">2</span>/<span class="key-number">10</span> 美元，<span class="key-number">11 月 30 日</span>后回到 <span class="key-number">4</span>/<span class="key-number">20</span> 美元。同步预览的 Antigravity <code>/swarm</code> 把一条提示词变成可追踪的智能体团队，一夜 <span class="key-number">10</span> 轮循环重建出 <span class="key-number">90.6</span> 万三角面的办公楼。</p>
      <div class="featured-meta">
        <span>📖 9 分钟</span><span>📅 {TODAY}</span><span>{LABEL}</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="图：Gemini 4 Carbon 官方主视觉（来源：Google DeepMind 官方博客）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
