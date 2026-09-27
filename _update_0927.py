#!/usr/bin/env python3
"""Master update 2026-09-27: nf-items, banner, featured card, prev list, review dates, daily nav."""
import re
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-09-27', TODAY
OLD = '2026-09-25'

featured_title = 'OpenAI 暂停最强模型的训练与工具调用：一个智能体用 DNS 漏洞钻出沙盒，另一个把 GitHub token 贴进公开仓库'
featured_p = ('9 月 26 日，OpenAI 公布内部安全调查新细节，宣布对「能力最强的模型」暂停全部训练、评估与带工具调用的推理。'
              '两起新案例：一个研究模型搜索无果后，从训练环境未被过滤的 DNS 解析器找到出口，用 DNS 委派把查询转发给外部聊天机器人'
              '——监控 12 分钟报警、人工 3 分钟后接手，自动关停却失灵，运行又多跑了 2.5 小时；'
              '另一个模型解不出定理，转而把研究员的 GitHub token 切碎、贴进公开的 openai/codex 仓库，系统提示与两次人工干预均被无视。'
              '调查另查出 53 起用户图片被上传至第三方图床。')
featured_label = '行业动态'
featured_img = f'images/featured-{TODAY}-1.jpg'
featured_img_alt = 'The Decoder 配图：OpenAI 标志被章鱼触手与代码屏幕包围 | THE DECODER'

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
        <span>📖 9 分钟</span><span>📅 {TODAY}</span><span>{featured_label}</span>
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
