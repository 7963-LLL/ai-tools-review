#!/usr/bin/env python3
"""Master update 2026-09-03: nf-items, banners, featured card, prev list, review dates, daily nav."""
import re
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-09-03', TODAY

# ---------- 1. nf-scroll items ----------
nf_items = open('_nf_items_output.txt', encoding='utf-8').read().strip()

idx_path = 'index.html'
idx = open(idx_path, encoding='utf-8').read()

s = idx.find('id="nf-scroll"')
content_start = idx.find('>', s) + 1
script_marker = '<script>\n// AI 热点分类过滤'
script_start = idx.find(script_marker, content_start)
assert script_start > 0, 'JS filter marker not found'
old_block = idx[content_start:script_start]
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

featured_title = 'Claude Fable 5.1 与 Mythos 5.1 同日发布：同一模型两种安全档，缓存读取降价 75%，编码与科研智能体双双破纪录'
featured_p = ('9 月 3 日，Anthropic 发布 Claude Fable 5.1 与 Claude Mythos 5.1——同一模型、两种安全档位。'
              'Fable 5.1 即日在 AWS、Azure、Google Cloud 与 Claude API 全平台上线，缓存读取降价 75% 至每百万 tokens 0.25 美元，'
              '典型负载成本比 Fable 5 低约 25%，重度 Agent 场景最高省 45%。科研智能体 Terminal-Bench-Science 拿下 52.6%，'
              '较 Fable 5 的 24.7% 翻倍以上；Mythos 5.1 仅向网络安全与生命科学可信访问计划开放，生物能力配合美国政府计划分级放行。')

new_card = f'''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">模型发布/更新</div>
      <h2><a href="featured-{TODAY}.html">{featured_title}</a></h2>
      <p>{featured_p}</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 {TODAY}</span><span>模型发布/更新</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="Claude Fable 5.1 与 Claude Mythos 5.1 官方发布横幅 | Anthropic" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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

# ---------- 5. review card dates (only remaining 📅 OLD after featured swap = review cards) ----------
n_before = idx.count('📅 2026-08-29')
idx = idx.replace('📅 2026-08-29', f'📅 {TODAY}')
print(f'review dates replaced: {n_before}')

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
