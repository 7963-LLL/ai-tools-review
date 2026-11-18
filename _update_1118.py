#!/usr/bin/env python3
"""Update index.html + daily.html for 2026-11-18"""
import re
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-11-18', TODAY
PREV = '2026-11-17'

with open('_nf_items_output.txt', encoding='utf-8') as f:
    nf_items_str = f.read().strip()
assert nf_items_str.count('class="nf-item"') == 50, nf_items_str.count('class="nf-item"')

FEATURED_TITLE = "&#36;115.8B、93%、&#36;130B 指引里没有中国：Nvidia 交出最强财报，同时失去创始人"
FEATURED_SUMMARY = (
    "11 月 17 日，Nvidia 第三财季营收 <span class=\"key-number\">$115.8B</span>、同比 "
    "<span class=\"key-number\">103%</span>，数据中心 $107.6B 独占 93%，净利翻倍到 "
    "<span class=\"key-number\">$65.3B</span>；Q4 指引 <span class=\"key-number\">$130B</span>、"
    "毛利率却掉到 71–72%，且明确不假设任何中国数据中心收入。同一天，临时 CEO Colette Kress "
    "确认董事会不恢复黄仁勋职务，H200 对华销售终止，SEC 民事调查的消息见报——最好看的季报，"
    "与一个空缺的创始人座位，被塞进了同一个 24 小时。"
)

# ========== index.html ==========
with open('index.html', encoding='utf-8') as f:
    idx = f.read()

# 1. review card dates
n_dates = idx.count(f'📅 {PREV}</span>')
idx = idx.replace(f'📅 {PREV}</span>', f'📅 {TODAY}</span>')
print(f"review dates updated: {n_dates}")

# 2. nf-scroll content
s = idx.find('id="nf-scroll"')
assert s >= 0
content_start = idx.find('>', s) + 1
script_marker = '<script>\n// AI 热点分类过滤'
script_pos = idx.find(script_marker, content_start)
assert script_pos >= 0
idx = idx[:content_start] + '\n' + nf_items_str + '\n\n' + idx[script_pos:]

# 3. daily banner
old_banner = f'📰 最新快报：{PREV}（今日 AI 精选 50 条）→'
assert old_banner in idx
idx = idx.replace(old_banner, f'📰 最新快报：{TODAY}（今日 AI 精选 50 条）→')
idx = idx.replace(f'href="daily-{PREV}.html">📰', f'href="daily-{TODAY}.html">📰')

# 4. featured card
f_start = idx.find('<div class="featured-card">')
f_end = idx.find('<div class="section-title" style="margin-top:12px">', f_start)
assert f_start >= 0 and f_end > f_start

new_featured = f'''  <div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">行业 / 公司治理</div>
      <h2><a href="featured-{TODAY}.html">{FEATURED_TITLE}</a></h2>
      <p>{FEATURED_SUMMARY}</p>
      <div class="featured-meta">
        <span>📖 9 分钟</span><span>📅 {TODAY}</span><span>行业 / 公司治理</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="Nvidia Vera Rubin 机架官方产品图（来源：NVIDIA 官方新闻稿）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>

  '''
idx = idx[:f_start] + new_featured + idx[f_end:]

# 5. prev-featured entry (newest first)
pl = idx.find('<div class="prev-featured-list">') + len('<div class="prev-featured-list">')
entry = f'''
            <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{FEATURED_TITLE}</span>
      <span class="prev-arrow">→</span>
    </a>'''
idx = idx[:pl] + entry + idx[pl:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print("index.html updated")

# ========== daily.html ==========
with open('daily.html', encoding='utf-8') as f:
    d = f.read()
d = d.replace(f'href="daily-{PREV}.html">📰 最新快报：{PREV}', f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}')
anchor = f'<a href="daily-{PREV}.html">📅 {PREV} 今日快报</a>'
assert anchor in d
d = d.replace(anchor, f'<a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n    ' + anchor, 1)
with open('daily.html', 'w', encoding='utf-8') as f:
    f.write(d)
print("daily.html updated")

# ========== verify ==========
idx2 = open('index.html', encoding='utf-8').read()
assert idx2.count('class="nf-item"') == 50, idx2.count('class="nf-item"')
assert idx2.count('class="nf-tab') >= 6
assert '// AI 热点分类过滤' in idx2
assert f'featured-{TODAY}.html' in idx2 and f'daily-{TODAY}.html' in idx2
print("verify OK: 50 nf-items, tabs intact, filter JS intact")
