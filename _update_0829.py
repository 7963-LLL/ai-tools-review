#!/usr/bin/env python3
"""Master update 2026-08-29: nf-items, banners, featured card, prev list, review dates, daily nav, featured article."""
import re, json, os
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-08-29', TODAY

# ---------- 1. nf-scroll items ----------
nf_items = open('_nf_items_output.txt', encoding='utf-8').read().strip()

idx_path = 'index.html'
idx = open(idx_path, encoding='utf-8').read()

# Replace nf-scroll content: between id="nf-scroll"> and the JS filter marker
s = idx.find('id="nf-scroll"')
content_start = idx.find('>', s) + 1
script_marker = '<script>\n// AI 热点分类过滤'
script_start = idx.find(script_marker, content_start)
assert script_start > 0, 'JS filter marker not found'
old_block = idx[content_start:script_start]
idx = idx[:content_start] + '\n' + nf_items + '\n\n' + idx[script_start:]

# ---------- 2. index banner (full-tag swap, fixes href/text mismatch) ----------
def swap_banner(html):
    m = re.search(r'<a href="daily-\d{4}-\d{2}-\d{2}\.html">📰 最新快报：[^<]*→</a>', html)
    assert m, 'index banner not found'
    new = f'<a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>'
    return html.replace(m.group(0), new)

idx = swap_banner(idx)

# ---------- 3. featured card ----------
card_start = idx.index('<div class="featured-card">')
card_end = idx.index('<div class="section-title', card_start)

featured_title = 'Qwen3.8-Flash-Next 开源：125B 主模型激活仅 6B，训练成本压到 Qwen3.7-Plus 的 1/9，Qwen4 架构提前亮相'
featured_p = ('8 月 26 日，通义千问按预告时间开源 Qwen3.8-Flash-Next：125B 主模型 + 51B N-gram Embedding，每 token 只激活 6B 参数，'
              '训练开销约为 Qwen3.7-Plus 的 1/9，编码与办公能力却更强——SWE-bench Pro 62.5 反超 Claude Opus 4.6，'
              'CoWorkBench 73.9 领跑。作为 Qwen4 架构的先导预览，它在 Attention、Residual、Embedding、优化四大方向全面换代；'
              '生产版 Qwen3.8-Flash 已上线千问 AI 平台，输入每百万 tokens 仅 0.8 元。')

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
      <img src="images/featured-{TODAY}-1.jpg" alt="Qwen3.8-Flash-Next 官方发布图 | 通义千问" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''

idx = idx[:card_start] + new_card + '\n' + idx[card_end:]

# ---------- 4. prev-featured entry ----------
plist_anchor = '<div class="prev-featured-list">'
plist_pos = idx.index(plist_anchor) + len(plist_anchor)
prev_entry = f'''
            <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{featured_title}</span>
      <span class="prev-arrow">→</span>
    </a>'''
idx = idx[:plist_pos] + prev_entry + idx[plist_pos:]

# ---------- 5. review card dates (after featured card swap, these are the review cards) ----------
n_before = idx.count('📅 2026-08-19')
idx = idx.replace('📅 2026-08-19', f'📅 {TODAY}')
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
