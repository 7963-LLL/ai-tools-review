#!/usr/bin/env python3
"""Comprehensive daily update script for suduai.top - 2026-07-08"""
import json, re, os
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
TODAY_STR = f'{TODAY[:4]}年{TODAY[5:7]}月{TODAY[8:10]}日'

print(f"Running update for {TODAY}")

# ========== Read data ==========
data = json.load(open('aihot_selected.json', encoding='utf-8'))
items = data['items']

# ========== Read generated nf-items ==========
with open('_nf_items_output.txt', encoding='utf-8') as f:
    nf_items_str = f.read()

# ========== Read current index.html ==========
with open('index.html', encoding='utf-8') as f:
    index_html = f.read()

# === Step 1: Replace nf-items in index.html ===
pattern_start = '<div class="nf-scroll" id="nf-scroll">'
idx_start = index_html.find(pattern_start)
idx_end = index_html.find('</div>\n\n</div>', idx_start)

if idx_start >= 0 and idx_end >= 0:
    before_scroll = index_html[:idx_start + len(pattern_start)]
    after_scroll = index_html[idx_end:]
    index_html = before_scroll + '\n' + nf_items_str + '\n    ' + after_scroll
    print("✅ Replaced nf-scroll content")
else:
    print("⚠️ Could not find nf-scroll pattern, trying fallback...")
    ss = index_html.find('id="nf-scroll"')
    if ss >= 0:
        div_start = index_html.rfind('<div', 0, ss)
        div_close_tag = index_html.find('>', div_start)
        content_start = div_close_tag + 1
        depth = 1
        i = content_start
        while depth > 0 and i < len(index_html):
            if index_html[i:i+4] == '<div':
                depth += 1
                i += 4
            elif index_html[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    break
                i += 6
            else:
                i += 1
        if depth == 0:
            index_html = index_html[:content_start] + '\n' + nf_items_str + '\n    ' + index_html[i:]
            print("✅ Replaced nf-scroll (fallback)")
        else:
            print("❌ Could not parse nf-scroll")

# === Step 2: Update daily-banner ===
banner_match = re.search(r'href="daily-(\d{4}-\d{2}-\d{2})\.html">📰 最新快报：\d{4}-\d{2}-\d{2}', index_html)
if banner_match:
    old_banner = banner_match.group(0)
    new_banner = f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→'
    index_html = index_html.replace(old_banner, new_banner)
    print(f"✅ Updated daily-banner to {TODAY}")
else:
    print("⚠️ Could not find daily-banner")

# === Step 3: Update featured section - Meta's Prometheus gigawatt AI cluster ===
featured_title = "扎克伯格披露 Meta 千兆瓦级 AI 集群计划：Prometheus 超级计算机 2026 年上线"
featured_label = "行业动态"
featured_summary = "Meta CEO 扎克伯格近日披露了公司在 AI 基础设施上的宏大蓝图：首座名为 Prometheus 的千兆瓦级 AI 超级集群将于 2026 年上线，后续还有规模达 5 GW 的 Hyperion 集群。Meta 已组建由 Alexandr Wang、Daniel Gross、Nat Friedman 等顶级 AI 人才组成的超级智能实验室，并斥资 143 亿美元收购 Scale AI 解决 Llama 模型数据质量问题。这批 gigawatt 级超算中心将重新定义 AI 训练的基础设施标准，使 Meta 跻身 AI 算力竞赛第一梯队。"
featured_detail_url = f"featured-{TODAY}.html"
daily_url = f"daily-{TODAY}.html"
img_path = f"images/featured-{TODAY}-1.jpg"

# Find and replace featured-card section
old_featured_start = index_html.find('<div class="featured-card">')
old_featured_end = index_html.find('<div class="section-title" style="margin-top:12px">', old_featured_start)

# Check if we have featured-visual with image
img_exists = os.path.isfile(f'images/featured-{TODAY}-1.jpg') and os.path.getsize(f'images/featured-{TODAY}-1.jpg') > 10240

if img_exists:
    new_featured = f'''  <div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">{featured_label}</div>
      <h2><a href="{featured_detail_url}">{featured_title}</a></h2>
      <p>{featured_summary}</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 {TODAY}</span><span>{featured_label}</span>
      </div>
      <a href="{daily_url}" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="{img_path}" alt="Meta Prometheus 千兆瓦级 AI 超级集群" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''
else:
    new_featured = f'''  <div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">{featured_label}</div>
      <h2><a href="{featured_detail_url}">{featured_title}</a></h2>
      <p>{featured_summary}</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 {TODAY}</span><span>{featured_label}</span>
      </div>
      <a href="{daily_url}" class="affiliate-btn">看今日完整快报 →</a>
    </div>
  </div>'''

if old_featured_start >= 0 and old_featured_end >= 0:
    index_html = index_html[:old_featured_start] + new_featured + '\n\n' + index_html[old_featured_end:]
    print("✅ Updated featured section")
else:
    print("❌ Could not find featured section")

# === Step 4: Add to prev-featured-list ===
first_prev_entry = index_html.find('<a href="featured-', index_html.find('<div class="prev-featured-list">'))

new_prev_entry = f'''    <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">扎克伯格披露 Meta 千兆瓦级 AI 集群计划：Prometheus 超级计算机 2026 年上线</span>
      <span class="prev-arrow">→</span>
    </a>
'''

if first_prev_entry >= 0:
    index_html = index_html[:first_prev_entry] + new_prev_entry + index_html[first_prev_entry:]
    print("✅ Added prev-featured entry")
else:
    print("❌ Could not find prev-featured-list")

# === Step 5: Update review card dates ===
date_matches = re.findall(r'📅 (\d{4}-\d{2}-\d{2})</span>', index_html)
if date_matches:
    from collections import Counter
    common_date = Counter(date_matches).most_common(1)[0][0]
    old_date = common_date
    index_html = index_html.replace(f'📅 {common_date}</span>', f'📅 {TODAY}</span>')
    print(f"✅ Updated review card dates: {common_date} → {TODAY}")
else:
    print("⚠️ No review card dates found to update")

# === Step 6: Write updated index.html ===
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("✅ Updated index.html")

# ========== Step 7: Update daily.html ==========
with open('daily.html', 'r', encoding='utf-8') as f:
    daily_html = f.read()

# Update daily-banner in daily.html
banner_match = re.search(r'href="daily-(\d{4}-\d{2}-\d{2})\.html">📰 最新快报：\d{4}-\d{2}-\d{2}', daily_html)
if banner_match:
    daily_html = daily_html.replace(banner_match.group(0), f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→')
    print("✅ Updated daily.html banner")

# Add today's entry at top of daily-nav if not already there
if f'daily-{TODAY}.html' in daily_html:
    print("⚠️ daily.html already has today's nav link, skipping")
else:
    daily_nav_start = daily_html.find('<div class="daily-nav">')
    first_nav_link = daily_html.find('<a href="daily-', daily_nav_start)
    new_nav_link = f'    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n'
    if first_nav_link >= 0:
        daily_html = daily_html[:first_nav_link] + new_nav_link + daily_html[first_nav_link:]
        print("✅ Added daily.html nav link")
    else:
        print("❌ Could not find daily-nav")

with open('daily.html', 'w', encoding='utf-8') as f:
    f.write(daily_html)
print("✅ Updated daily.html")

print(f"\n{'='*50}")
print(f"✅ All updates complete for {TODAY}")
print(f"{'='*50}")
