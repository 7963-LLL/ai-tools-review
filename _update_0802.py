#!/usr/bin/env python3
"""Update index.html + daily.html for 2026-08-02"""
import json, re
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')

# ========== 1. Read nf-items ==========
with open('_nf_items_output.txt', encoding='utf-8') as f:
    nf_items_str = f.read().strip()
nf_count = nf_items_str.count('class="nf-item"')
print(f"nf-items loaded: {nf_count}")

# ========== 2. index.html ==========
with open('index.html', encoding='utf-8') as f:
    idx = f.read()

# --- 2a. Replace nf-scroll content ---
start_marker = '<div class="nf-scroll" id="nf-scroll">'
s = idx.find(start_marker)
assert s >= 0, "nf-scroll not found"
content_start = s + len(start_marker)
# depth-count to find matching </div>
depth = 1
i = content_start
while depth > 0 and i < len(idx):
    if idx[i:i+4] == '<div':
        depth += 1
        i += 4
    elif idx[i:i+6] == '</div>':
        depth -= 1
        i += 6
    else:
        i += 1
assert depth == 0, "nf-scroll not closed"
idx = idx[:content_start] + '\n' + nf_items_str + '\n' + idx[i:]
print("✅ nf-scroll replaced")

# --- 2b. Update daily-banner ---
idx = idx.replace('href="daily-2026-07-30.html">📰 最新快报：2026-07-30（今日 AI 精选 50 条）→</a>',
                  f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>')
print("✅ daily-banner updated")

# --- 2c. Replace featured section ---
featured_title = "字节跳动发布 Seedance 2.5：单次生成 30 秒视频，长叙事与多模态参考成核心卖点"
featured_summary = ("2026 年 7 月 31 日，字节跳动 Seed 团队发布新一代视频创作模型 Seedance 2.5：单次生成时长从 15 秒翻倍到 "
                    "30 秒并支持多轮延长，单次最多可输入 30 张图片、10 段视频、10 段音频作为多模态参考，还支持基于时间戳的精准编辑。"
                    "模型已在即梦 AI、豆包专业版上线，API 即将登陆火山方舟。从『生成一个片段』到『完成一段创作』，视频大模型的竞争焦点正式转向长叙事。")
f_start = idx.find('<div class="featured-card">')
f_end = idx.find('<div class="section-title" style="margin-top:12px">', f_start)
assert f_start >= 0 and f_end >= 0, "featured section not found"

new_featured = f'''  <div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">模型发布</div>
      <h2><a href="featured-{TODAY}.html">{featured_title}</a></h2>
      <p>{featured_summary}</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 {TODAY}</span><span>模型发布</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="Seedance 2.5 官方演示画面 | 字节跳动 Seed" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''
idx = idx[:f_start] + new_featured + '\n\n' + idx[f_end:]
print("✅ featured section replaced")

# --- 2d. Add prev-featured entry ---
pl = idx.find('<div class="prev-featured-list">')
first_entry = idx.find('<a href="featured-', pl)
assert first_entry >= 0, "prev-featured-list not found"
new_entry = f'''    <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{featured_title}</span>
      <span class="prev-arrow">→</span>
    </a>
'''
idx = idx[:first_entry] + new_entry + idx[first_entry:]
print("✅ prev-featured entry added")

# --- 2e. Review card dates ---
count = idx.count('📅 2026-07-30</span>')
idx = idx.replace('📅 2026-07-30</span>', f'📅 {TODAY}</span>')
print(f"✅ review dates updated: {count}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print("✅ index.html written")

# ========== 3. daily.html ==========
with open('daily.html', encoding='utf-8') as f:
    dly = f.read()

dly = dly.replace('href="daily-2026-07-30.html">📰 最新快报：2026-07-30（今日 AI 精选 50 条）→</a>',
                  f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>')
print("✅ daily.html banner updated")

dn = dly.find('<div class="daily-nav">')
first_nav = dly.find('<a href="daily-', dn)
assert first_nav >= 0, "daily-nav not found"
new_nav = f'    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n'
dly = dly[:first_nav] + new_nav + dly[first_nav:]
print("✅ daily.html nav updated")

with open('daily.html', 'w', encoding='utf-8') as f:
    f.write(dly)
print("✅ daily.html written")

print(f"\n{'='*50}\n✅ All updates complete for {TODAY}\n{'='*50}")
