#!/usr/bin/env python3
"""One-off: patch index.html + daily.html for 2026-10-28. ponytail: throwaway, like the 100 before it."""
import re

TODAY = '2026-10-28'
YDAY = '2026-10-27'
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
html = re.sub(
    r'<div class="daily-banner">\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*</div>',
    f'<div class="daily-banner">\n  <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    html, count=1)

# ---------- 3. featured card ----------
TITLE = '输入 $1、输出 $5：GPT-6.1 Terra 半价卖前沿智能，把最难的那档让给了 Sol'
new_card = '''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">模型发布</div>
      <h2><a href="featured-2026-10-28.html">输入 $1、输出 $5：GPT-6.1 Terra 半价卖前沿智能，把最难的那档让给了 Sol</a></h2>
      <p>OpenAI 上线 GPT-6.1 Terra，标准 API 每百万 token 输入 <span class="key-number">1 美元</span>、输出 <span class="key-number">5 美元</span>，比 GPT-5.6 Terra（2/12）和自家旗舰 GPT-6.1 Sol 都便宜 <span class="key-number">50%</span>。Artificial Analysis 独立复跑：最高档单任务成本 <span class="key-number">0.40 美元</span>，约为上一代的 1/3；低中档落在成本效率帕累托前沿，最高档却比 Sol 低 4 分——分层是刻意的。更被低估的是事实性：低档错误率从 53.6% 降到 <span class="key-number">16.7%</span>，硬猜比例 88%→<span class="key-number">38%</span>。前沿智能开始按天使用，而不是按次调用。</p>
      <div class="featured-meta">
        <span>📖 11 分钟</span><span>📅 2026-10-28</span><span>模型发布</span>
      </div>
      <a href="daily-2026-10-28.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-2026-10-28-1.jpg" alt="Artificial Analysis 的 GPT-6.1 Terra 智能与成本对比图" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''
m = re.search(r'<div class="featured-card">.*?\n  </div>\n<div class="section-title" style="margin-top:12px">', html, re.S)
assert m, 'featured card not found'
html = html[:m.start()] + new_card + '\n<div class="section-title" style="margin-top:12px">' + html[m.end():]

# ---------- 4. prev-featured prepend ----------
prev_new = '''  <div class="prev-featured-list">
            <a href="featured-2026-10-28.html" class="prev-featured-item">
      <span class="prev-date">2026-10-28</span>
      <span class="prev-title">输入 $1、输出 $5：GPT-6.1 Terra 半价卖前沿智能，把最难的那档让给了 Sol</span>
      <span class="prev-arrow">→</span>
    </a>
'''
old_marker = '<div class="prev-featured-list">\n'
k = html.index(old_marker) + len(old_marker)
html = html[:k] + prev_new[len('  <div class="prev-featured-list">\n'):] + html[k:]

# ---------- 5. review card dates ----------
html = html.replace('<div class="meta"><span>📅 2026-10-27</span>',
                    '<div class="meta"><span>📅 2026-10-28</span>')

open('index.html', 'w', encoding='utf-8', newline='\n').write(html)

# ---------- 6. daily.html nav ----------
d = open('daily.html', encoding='utf-8').read()
d = d.replace(f'<a href="daily-{YDAY}.html">📰 最新快报：{YDAY}（今日 AI 精选 50 条）→</a>',
              f'<a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>')
if f'daily-{TODAY}.html">📅' not in d:
    d = d.replace(f'<a href="daily-{YDAY}.html">📅 {YDAY} 今日快报</a>',
                  f'<a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>' + '\n    ' +
                  f'<a href="daily-{YDAY}.html">📅 {YDAY} 今日快报</a>')
open('daily.html', 'w', encoding='utf-8', newline='\n').write(d)

# ---------- verify ----------
h = open('index.html', encoding='utf-8').read()
print('nf-items:', h.count('class="nf-item"'))
print('tabs:', h.count('class="nf-tab'))
print('filter js:', 'AI 热点分类过滤' in h)
print('banner:', f'daily-{TODAY}.html">📰' in h)
print('featured h2:', f'featured-{TODAY}.html">' in h)
print('featured btn -> daily:', f'<a href="daily-{TODAY}.html" class="affiliate-btn">' in h)
print('prev item:', h.count('prev-featured-item">'), '| today first:', f'prev-date">{TODAY}' in h)
print('review dates 10-28:', h.count('📅 2026-10-28'), '| leftovers 10-27:', h.count('📅 2026-10-27'))
print('daily.html new link:', f'daily-{TODAY}.html' in open('daily.html', encoding='utf-8').read())
