#!/usr/bin/env python3
"""Update index.html + daily.html for 2026-08-19"""
import json, re
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-08-19', TODAY

# ========== 1. Read nf-items ==========
with open('_nf_items_output.txt', encoding='utf-8') as f:
    nf_items_str = f.read().strip()
nf_count = nf_items_str.count('class="nf-item"')
print(f"nf-items loaded: {nf_count}")
assert nf_count == 50, f"Expected 50 nf-items, got {nf_count}"

featured_title = "智谱发布 GLM-5.3：AA 智能指数 60 分并列开源第一，编程与网络安全能力双突破"
featured_summary = ("8 月 19 日，智谱宣布 GLM-5.3 正式上线：基座与 GLM-5.2 完全相同，仅靠后训练 Scaling 就把编程能力"
                    "提升 50%，AA 智能指数 60 分并列开源第一，成本更低。更值得注意的是，它在漏洞挖掘等网络安全任务上"
                    "持平闭源前沿 Mythos 5——联合多家安全实验室累计发现漏洞 2436 个，经济价值约 3000 万元。智谱计划两周后"
                    "开源完整权重，并启动「开源的盾」计划，把安全能力做成开源公共品。")

# ========== 2. index.html ==========
with open('index.html', encoding='utf-8') as f:
    idx = f.read()

# --- 2e. Review card dates FIRST ---
# Find the previous date used in review cards (📅 YYYY-MM-DD</span> pattern)
date_matches = re.findall(r'📅 (\d{4}-\d{2}-\d{2})</span>', idx)
print(f"Dates found in index.html: {sorted(set(date_matches))}")
count = idx.count('📅 2026-08-18</span>')
idx = idx.replace('📅 2026-08-18</span>', f'📅 {TODAY}</span>')
print(f"✅ review dates updated: {count}")

# --- 2a. Replace nf-scroll content ---
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
f_start = idx.find('<div class="featured-card">')
f_end = idx.find('<div class="section-title" style="margin-top:12px">', f_start)
assert f_start >= 0 and f_end >= 0, "featured section not found"

new_featured = f'''  <div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">产品发布/更新</div>
      <h2><a href="featured-{TODAY}.html">{featured_title}</a></h2>
      <p>{featured_summary}</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 {TODAY}</span><span>产品发布/更新</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="GLM-5.3 编程能力体感评测官方图 | 智谱" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
