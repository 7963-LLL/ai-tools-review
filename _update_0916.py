#!/usr/bin/env python3
"""Master update 2026-09-16: nf-items, banners, featured card, prev list, review dates, daily nav."""
import re
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-09-16', TODAY
OLD = '2026-09-14'

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

featured_title = 'Anthropic 9 月威胁报告：也门小组用 Claude Code 写导弹制导，AI 在攻击链上从助手变成编排者'
featured_p = ('Anthropic 9 月 16 日发布威胁情报报告，把 2025 年 12 月至 2026 年 8 月间被中断的七类滥用一次摊开。'
              '一个被评估极可能关联胡塞武装的也门小组，用 Claude Code 替代人类工程师写完制导软件，'
              '涉及射程目标 2,000 公里以上的多级弹道导弹与代号 R2000 的高超声速滑翔载具；'
              '被评估与 Midnight Blizzard 一致的行动者则让 AI 在植入物被检出后自动改写重编译，直到绕过检测，行动覆盖 20 多个组织。'
              '商业侧同样具体：自 2 月起 Anthropic 已中断七家中国实验室的蒸馏攻击——阿里相关活动峰值一天近 300 万次交换、'
              '5 至 7 月累计超 1.51 亿次，Moonshot、DeepSeek、智谱分别被记录到 2,300 万、1,210 万与 77 万次量级的交换。')

new_card = f'''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">行业动态</div>
      <h2><a href="featured-{TODAY}.html">{featured_title}</a></h2>
      <p>{featured_p}</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 {TODAY}</span><span>行业动态</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="Anthropic 2026 年 9 月威胁情报报告官方封面《Detecting and countering misuse of AI》 | Anthropic 官方" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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

# ---------- 5. review card dates (remaining 📅 OLD after featured swap = review cards) ----------
n_before = idx.count(f'📅 {OLD}')
idx = idx.replace(f'📅 {OLD}', f'📅 {TODAY}')
print(f'review dates replaced: {n_before}')

# tabs must survive
assert idx.count('<div class="nf-tabs"') == tabs_kept, 'nf-tabs changed!'
assert idx.count('class="nf-item"') == 50, idx.count('class="nf-item"')
assert 'AI 热点分类过滤' in idx, 'tab filter JS lost!'
assert idx.count(f'📅 {TODAY}') >= 1

open(idx_path, 'w', encoding='utf-8').write(idx)

# ---------- 6. daily.html ----------
dl_path = 'daily.html'
dl = open(dl_path, encoding='utf-8').read()
dl = swap_banner(dl)

nav_anchor = '<div class="daily-nav">'
nav_pos = dl.index(nav_anchor) + len(nav_anchor)
nav_entry = f'\n    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>'
dl = dl[:nav_pos] + nav_entry + dl[nav_pos:]
open(dl_path, 'w', encoding='utf-8').write(dl)

print('index.html + daily.html updated')
