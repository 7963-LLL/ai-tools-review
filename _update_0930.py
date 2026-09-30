#!/usr/bin/env python3
"""Master update 2026-09-30: nf-items, banner, featured card, prev list, review dates, daily nav."""
import re
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-09-30', TODAY
OLD = '2026-09-29'

featured_title = 'Anthropic 与 SpaceX 签下最高 845 亿美元算力协议：每月付 12.5 亿，90 天通知即可解约'
featured_p = ('9 月 30 日，路透查阅的申报文件揭开了 Anthropic 与 SpaceX 的算力协议：覆盖 Colossus 一号、二号数据中心，'
              '每月支付 12.5 亿美元至 2029 年 5 月，合同上限 845 亿美元（剔除爬坡月约 425 亿），条款允许提前 90 天通知解约。'
              '对正在冲击 2 万亿美元估值的 Anthropic 来说，这既是补给，也是一份随时可以抽身的灵活性。')
featured_label = '行业动态'
featured_img = f'images/featured-{TODAY}-1.jpg'
featured_img_alt = 'Anthropic 官方公告配图：节点相连的地球插画 | anthropic.com'

# ---------- 1. nf-scroll items ----------
nf_items = open('_nf_items_output.txt', encoding='utf-8').read().strip()
assert nf_items.count('class="nf-item"') == 50, nf_items.count('class="nf-item"')

idx_path = 'index.html'
idx = open(idx_path, encoding='utf-8').read()

s = idx.find('id="nf-scroll"')
content_start = idx.find('>', s) + 1
script_marker = '<script>\n// AI 热点分类过滤'
script_start = idx.find(script_marker, content_start)
assert script_start > 0, 'JS filter marker not found'
tabs_kept = idx.count('<div class="nf-tabs"')
idx = idx[:content_start] + '\n' + nf_items + '\n\n' + idx[script_start:]

# ---------- 2. index banner (full-tag swap) ----------
def swap_banner(html):
    m = re.search(r'<a href="daily-\d{4}-\d{2}-\d{2}\.html">📰 最新快报：[^<]*→</a>', html)
    assert m, 'banner not found'
    new = f'<a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>'
    return html.replace(m.group(0), new)

idx = swap_banner(idx)

# ---------- 3. featured card ----------
card_start = idx.index('<div class="featured-card">')
card_end = idx.index('<div class="section-title', card_start)

new_card = f'''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">{featured_label}</div>
      <h2><a href="featured-{TODAY}.html">{featured_title}</a></h2>
      <p>{featured_p}</p>
      <div class="featured-meta">
        <span>📖 8 分钟</span><span>📅 {TODAY}</span><span>{featured_label}</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="{featured_img}" alt="{featured_img_alt}" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''

idx = idx[:card_start] + new_card + '\n' + idx[card_end:]

# ---------- 4. prev-featured entry (top of list) ----------
plist_anchor = '<div class="prev-featured-list">'
plist_pos = idx.index(plist_anchor) + len(plist_anchor)
prev_entry = f'''
            <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{featured_title}</span>
      <span class="prev-arrow">→</span>
    </a>'''
idx = idx[:plist_pos] + prev_entry + idx[plist_pos:]

# ---------- 5. review card dates ----------
n_before = idx.count(f'📅 {OLD}')
idx = idx.replace(f'📅 {OLD}', f'📅 {TODAY}')
print(f'review dates replaced: {n_before}')

# guards
assert idx.count('<div class="nf-tabs"') == tabs_kept, 'nf-tabs changed!'
assert idx.count('class="nf-item"') == 50, idx.count('class="nf-item"')
assert 'AI 热点分类过滤' in idx, 'tab filter JS lost!'
assert idx.count(f'📅 {TODAY}') >= 7, idx.count(f'📅 {TODAY}')
assert idx.count('nf-scroll') == 2, idx.count('nf-scroll')
assert f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>' in idx, 'banner mismatch'

open(idx_path, 'w', encoding='utf-8').write(idx)

# ---------- 6. daily.html ----------
dl_path = 'daily.html'
dl = open(dl_path, encoding='utf-8').read()
dl = swap_banner(dl)

nav_anchor = '<div class="daily-nav">'
nav_pos = dl.index(nav_anchor) + len(nav_anchor)
nav_entry = f'\n    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>'
dl = dl[:nav_pos] + nav_entry + dl[nav_pos:]
assert dl.count(f'daily-{TODAY}.html') == 2, dl.count(f'daily-{TODAY}.html')
open(dl_path, 'w', encoding='utf-8').write(dl)

print(f'✅ index.html + daily.html updated for {TODAY}  (review dates: {n_before})')
