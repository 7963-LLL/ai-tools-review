#!/usr/bin/env python3
"""Update index.html + daily.html for 2026-08-16"""
import json, re
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')

# ========== 1. Read nf-items ==========
with open('_nf_items_output.txt', encoding='utf-8') as f:
    nf_items_str = f.read().strip()
nf_count = nf_items_str.count('class="nf-item"')
print(f"nf-items loaded: {nf_count}")
assert nf_count == 50, f"Expected 50 nf-items, got {nf_count}"

# ========== 2. index.html ==========
with open('index.html', encoding='utf-8') as f:
    idx = f.read()

# --- 2a. Replace nf-scroll content ---
# NOTE: nf-box/nf-scroll are historically unclosed in this file (script follows
# items directly; browser auto-closes). Anchor end on the filter JS script.
s = idx.find('id="nf-scroll"')
assert s >= 0, "nf-scroll not found"
content_start = idx.find('>', s) + 1
script_marker = '<script>\n// AI 热点分类过滤'
script_pos = idx.find(script_marker, content_start)
assert script_pos >= 0, "AI hotspot filter script not found"
idx = idx[:content_start + 1] + '\n' + nf_items_str + '\n\n' + idx[script_pos:]
print("✅ nf-scroll replaced")

# --- 2b. Update daily-banner (full <a> tag match) ---
banner_re = re.compile(r'href="daily-\d{4}-\d{2}-\d{2}\.html">([^<]+)</a>')
bm = banner_re.search(idx)
assert bm, "banner not found in index.html"
old_full = bm.group(1)
new_full = f"📰 最新快报：{TODAY}（今日 AI 精选 50 条）→"
idx = idx.replace(old_full, new_full)
print(f"✅ daily-banner updated: {old_full} -> {new_full}")

# --- 2c. Replace featured section ---
featured_title = "DeepSeek-V4-Pro 正式版上线：Terminal Bench 87.9 领跑 Agent 基准，峰谷定价开启新一轮价格战"
featured_summary = ("2026 年 8 月 13 日，DeepSeek-V4-Pro 正式版在 APP、网页端和 API 同步上线。官方 Agent 基准全面拉升："
                    "Terminal Bench 2.1 达 87.9，HLE（带工具）60.0，原生支持 OpenAI Responses API 并一键适配 Codex，"
                    "思考强度新增 low/high/max 三档。API 同步引入峰谷定价，闲时价格低至高峰一半，8 月 17 日生效。"
                    "发布前后 Grok 4.6、Gemini 3.7 Flash 接连登场，Agent 竞赛进入白热化。")
f_start = idx.find('<div class="featured-card">')
f_end = idx.find('<div class="section-title" style="margin-top:12px">', f_start)
assert f_start >= 0 and f_end >= 0, "featured section not found"

new_featured = f'''  <div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">模型发布/更新</div>
      <h2><a href="featured-{TODAY}.html">{featured_title}</a></h2>
      <p>{featured_summary}</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 {TODAY}</span><span>模型发布/更新</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="DeepSeek-V4-Pro 官方发布图 | DeepSeek" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''
idx = idx[:f_start] + new_featured + '\n\n' + idx[f_end:]
print("✅ featured section replaced")

# --- 2d. Add prev-featured entry at TOP of prev-featured-list ---
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

# --- 2e. Review card dates (only 📅 pattern; prev-date entries untouched) ---
count = idx.count('📅 2026-08-02</span>')
idx = idx.replace('📅 2026-08-02</span>', f'📅 {TODAY}</span>')
print(f"✅ review dates updated: {count}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print("✅ index.html written")

# ========== 3. daily.html ==========
with open('daily.html', encoding='utf-8') as f:
    dly = f.read()

# --- 3a. Update banner (match the 📰 最新快报 link specifically) ---
banner_re2 = re.compile(r'href="daily-\d{4}-\d{2}-\d{2}\.html">([^<]*最新快报[^<]*)</a>')
bm2 = banner_re2.search(dly)
assert bm2, f"banner not found in daily.html: {banner_re2.pattern}"
old_full2 = bm2.group(1)
dly = dly.replace(old_full2, new_full)
print(f"✅ daily.html banner updated: {old_full2} -> {new_full}")

# --- 3b. Add today's nav link at TOP of daily-nav ---
dn = dly.find('<div class="daily-nav">')
assert dn >= 0, "daily-nav not found"
first_nav = dly.find('<a href="daily-', dn)
assert first_nav >= 0, "no nav link found"
new_nav = f'    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n'
dly = dly[:first_nav] + new_nav + dly[first_nav:]
print("✅ daily.html nav updated")

with open('daily.html', 'w', encoding='utf-8') as f:
    f.write(dly)
print("✅ daily.html written")

print(f"\n{'='*50}\n✅ All updates complete for {TODAY}\n{'='*50}")
