#!/usr/bin/env python3
"""One-off: patch index.html + daily.html for 2026-11-02. ponytail: throwaway, same shape as the last hundred."""
import re

TODAY = '2026-11-02'
PREV = '2026-11-01'
TITLE = '3 万亿美元承诺，5000 亿美元蒸发：AI 资本开支第一次被市场投票'
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
      <h2><a href="featured-2026-11-02.html">3 万亿美元承诺，5000 亿美元蒸发：AI 资本开支第一次被市场投票</a></h2>
      <p>10 月 28 日 Alphabet 交出一份漂亮的 Q3：营收 <span class="key-number">1276 亿美元</span>、同比 +25%，Google Cloud <span class="key-number">307 亿</span> +103%，Gemini App 月活破 <span class="key-number">10 亿</span>。市场盯着的是另一栏——自由现金流 <span class="key-number">负 90.7 亿美元</span>，股价单日跌 12.6%，市值蒸发超 <span class="key-number">5000 亿</span>，史上第二大单日缩水。同一周彭博社统计，五大巨头为 AI 基建签下的长期承诺已超 <span class="key-number">3 万亿美元</span>：Google 一家超过 1 万亿、接近一年前的八倍，Meta 那 8000 亿里近一半是分 30 年付的租约，甲骨文成了第一家因建数据中心而自由现金流转负的巨头。四大云厂商 2026 年资本开支合计超 <span class="key-number">7400 亿</span>，Anthropic 的招股文件里还压着近 9000 亿的表外采购义务。需求是真的，钱也是真的——问题只剩一个：什么时候赚回来。</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 2026-11-02</span><span>行业动态</span>
      </div>
      <a href="daily-2026-11-02.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-2026-11-02-1.jpg" alt="Alphabet 2026 年第三季度财报官方图（Google 官方博客配图）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
print('tabs:', h.count('class="nf-tab"'))
print('filter js:', 'AI 热点分类过滤' in h)
print('banner:', f'daily-{TODAY}.html">📰' in h)
print('featured h2:', f'featured-{TODAY}.html">' in h)
print('featured btn -> daily:', f'<a href="daily-{TODAY}.html" class="affiliate-btn">' in h)
print('prev first:', f'prev-date">{TODAY}' in h, '| total:', h.count('prev-featured-item">'))
print('review dates today:', h.count(f'📅 {TODAY}'), '| leftovers:', h.count(f'📅 {PREV}'))
print('daily.html new link:', f'daily-{TODAY}.html' in open('daily.html', encoding='utf-8').read())
