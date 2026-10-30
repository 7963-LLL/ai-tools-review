#!/usr/bin/env python3
"""One-off: patch index.html + daily.html for 2026-10-30. ponytail: throwaway, like the 100 before it."""
import re

TODAY = '2026-10-30'
PREV = '2026-10-28'   # last published featured/banner (10-29 run never patched index)
TITLE = '8500 亿美元算力承诺、900% 净留存：Anthropic 的 S-1 是一份「增长不可选」的招股书'
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
new_card = '''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">行业动态</div>
      <h2><a href="featured-2026-10-30.html">8500 亿美元算力承诺、900% 净留存：Anthropic 的 S-1 是一份「增长不可选」的招股书</a></h2>
      <p>Anthropic 10 月 26 日递交 S-1，拟以代码 <span class="key-number">ANT</span> 登陆纳斯达克，高盛与摩根士丹利主承销。招股书里两组数字互为因果：2026 上半年营收 <span class="key-number">163 亿美元</span>、调整后利润 <span class="key-number">16.2 亿美元</span>、净收入留存率 <span class="key-number">900%</span>、四分之三客户年支出超 10 万美元——这是能上市的底气；另一边是固定采购承诺 2656 亿 + 未起租算力租赁 3214 亿 + 新增协议 2450 亿 + 待定项 1250~1500 亿，合计约 <span class="key-number">8500 亿美元</span>，排到 2045 年。按此测算，年营收得长到 <span class="key-number">1880 亿美元</span> 才撑得住。而季度营收增速已从 147% 放缓到 45%。增长，不再是可选项。</p>
      <div class="featured-meta">
        <span>📖 12 分钟</span><span>📅 2026-10-30</span><span>行业动态</span>
      </div>
      <a href="daily-2026-10-30.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-2026-10-30-1.jpg" alt="Dario Amodei 与 SEC Form S-1 注册声明封面（The Verge 制图）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
html = html.replace('<div class="meta"><span>📅 2026-10-28</span>',
                    '<div class="meta"><span>📅 2026-10-30</span>')

open('index.html', 'w', encoding='utf-8', newline='\n').write(html)

# ---------- 6. daily.html nav ----------
d = open('daily.html', encoding='utf-8').read()
d = d.replace(f'<a href="daily-{PREV}.html">📰 最新快报：{PREV}（今日 AI 精选 50 条）→</a>',
              f'<a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>')
if f'daily-{TODAY}.html">📅' not in d:
    d = d.replace(f'<a href="daily-{PREV}.html">📅 {PREV} 今日快报</a>',
                  f'<a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n    ' +
                  f'<a href="daily-{PREV}.html">📅 {PREV} 今日快报</a>')
open('daily.html', 'w', encoding='utf-8', newline='\n').write(d)

# ---------- verify ----------
h = open('index.html', encoding='utf-8').read()
print('nf-items:', h.count('class="nf-item"'))
print('tabs:', h.count('class="nf-tab'))
print('filter js:', 'AI 热点分类过滤' in h)
print('banner:', f'daily-{TODAY}.html">📰' in h)
print('featured h2:', f'featured-{TODAY}.html">' in h)
print('featured btn -> daily:', f'<a href="daily-{TODAY}.html" class="affiliate-btn">' in h)
print('prev first:', f'prev-date">{TODAY}' in h, '| total:', h.count('prev-featured-item">'))
print('review dates 10-30:', h.count('📅 2026-10-30'), '| leftovers 10-28:', h.count('📅 2026-10-28'))
print('daily.html new link:', f'daily-{TODAY}.html' in open('daily.html', encoding='utf-8').read())
