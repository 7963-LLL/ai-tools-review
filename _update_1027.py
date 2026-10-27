#!/usr/bin/env python3
"""One-off: patch index.html + daily.html for 2026-10-27. ponytail: throwaway, like the 100 before it."""
import re

TODAY = '2026-10-27'
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
      <div class="featured-label">AI 商业</div>
      <h2><a href="featured-2026-10-27.html">1000 亿美元募资、900% 净留存、807 亿账面亏损：Anthropic 招股书里的三个真相</a></h2>
      <p>10 月 26 日 Anthropic 递交 300 多页 S-1，拟以代码 <span class="key-number">ANT</span> 登陆纳斯达克。营收从 2025 年一季度的 3.76 亿美元涨到二季度的 <span class="key-number">116 亿美元</span>，同比 1368%；净收入留存率约 <span class="key-number">900%</span>，历史最好 SaaS 是 Snowflake 的 189%。上半年「亏损 807 亿」里 724 亿是亚马逊可转债的公允价值变动，实际经营亏损 6.93 亿——而真正的问题是另一头：对 SpaceX、谷歌、亚马逊、微软的不可取消算力承诺合计约 <span class="key-number">8000 亿美元</span>。软件毛利，硬件风险。</p>
      <div class="featured-meta">
        <span>📖 12 分钟</span><span>📅 2026-10-27</span><span>AI 商业</span>
      </div>
      <a href="daily-2026-10-27.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-2026-10-27-1.jpg" alt="Anthropic 官方 wordmark 标志" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''
m = re.search(r'<div class="featured-card">.*?\n  </div>\n<div class="section-title" style="margin-top:12px">', html, re.S)
assert m, 'featured card not found'
html = html[:m.start()] + new_card + '\n<div class="section-title" style="margin-top:12px">' + html[m.end():]

# ---------- 4. prev-featured prepend ----------
prev_new = '''  <div class="prev-featured-list">
            <a href="featured-2026-10-27.html" class="prev-featured-item">
      <span class="prev-date">2026-10-27</span>
      <span class="prev-title">1000 亿美元募资、900% 净留存、807 亿账面亏损：Anthropic 招股书里的三个真相</span>
      <span class="prev-arrow">→</span>
    </a>
'''
old_marker = '<div class="prev-featured-list">\n'
k = html.index(old_marker) + len(old_marker)
html = html[:k] + prev_new[len('  <div class="prev-featured-list">\n'):] + html[k:]

# ---------- 5. review card dates ----------
html = html.replace('<div class="meta"><span>📅 2026-10-26</span>',
                    '<div class="meta"><span>📅 2026-10-27</span>')

open('index.html', 'w', encoding='utf-8', newline='\n').write(html)

# ---------- 6. daily.html nav ----------
d = open('daily.html', encoding='utf-8').read()
d = d.replace(f'<a href="daily-2026-10-26.html">📰 最新快报：2026-10-26（今日 AI 精选 50 条）→</a>',
              f'<a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>')
if f'daily-{TODAY}.html">📅' not in d:
    d = d.replace('<a href="daily-2026-10-26.html">📅 2026-10-26 今日快报</a>',
                  f'<a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>' + '\n    ' +
                  '<a href="daily-2026-10-26.html">📅 2026-10-26 今日快报</a>')
open('daily.html', 'w', encoding='utf-8', newline='\n').write(d)

# ---------- verify ----------
h = open('index.html', encoding='utf-8').read()
print('nf-items:', h.count('class="nf-item"'))
print('tabs:', h.count('class="nf-tab'))
print('filter js:', 'AI 热点分类过滤' in h)
print('banner:', f'daily-{TODAY}.html">📰' in h)
print('featured h2:', f'featured-{TODAY}.html">' in h)
print('featured btn -> daily:', f'<a href="daily-{TODAY}.html" class="affiliate-btn">' in h)
print('prev item:', h.count(f'prev-featured-item">'), '| today in prev:', f'prev-date">{TODAY}' in h)
print('review dates 10-27:', h.count('📅 2026-10-27'), '| leftovers 10-26:', h.count('📅 2026-10-26'))
print('daily.html new link:', f'daily-{TODAY}.html' in open('daily.html', encoding='utf-8').read())
