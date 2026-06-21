#!/usr/bin/env python3
"""Comprehensive update script for suduai.top daily update"""
import json, re, os
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')

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
# Find the nf-scroll section
nf_start = index_html.find('<div class="nf-scroll" id="nf-scroll">')
nf_end = index_html.find('</div>', nf_start)
# Find the closing </div> of the nf-scroll - need to find the second </div> 
# Actually nf-scroll ends at </div> then nf-box ends just after
# Let's find the end of the scroll div
scroll_start = index_html.find('<div class="nf-scroll" id="nf-scroll">')
# Find the closing tag - it's the one after all nf-items
# Pattern: after the last nf-item, there's a closing </div> for nf-scroll
scroll_start_tag_end = scroll_start + len('<div class="nf-scroll" id="nf-scroll">')
# Find the corresponding closing </div>
# The nf-scroll div ends with </div> then the nf-box ends with </div>
# Let's find the last nf-item closing
last_item_end = index_html.rfind('</a>', scroll_start, index_html.find('</div>\n\n</div>', scroll_start))
# The scroll div closing is after all items
scroll_close = index_html.find('</div>', last_item_end)
# Now the nf-box close is right after
nf_box_close = index_html.find('</div>', scroll_close + 6)

# More precise: find the nf-scroll div
pattern_start = '<div class="nf-scroll" id="nf-scroll">'
pattern_end = '</div>\n  </div>\n\n</div>'

idx_start = index_html.find(pattern_start)
idx_end = index_html.find(pattern_end, idx_start)

if idx_start >= 0 and idx_end >= 0:
    before_scroll = index_html[:idx_start + len(pattern_start)]
    after_scroll = index_html[idx_end:]
    new_index = before_scroll + '\n' + nf_items_str + '\n    ' + after_scroll
    print(f"✅ Replaced nf-scroll content (scroll_start={idx_start}, scroll_end={idx_end})")
else:
    # Fallback method
    print("⚠️ Could not find exact pattern, trying fallback...")
    # Just find the closing tag of nf-scroll
    ss = index_html.find('id="nf-scroll"')
    if ss >= 0:
        # Find the div start
        div_start = index_html.rfind('<div', 0, ss)
        div_close_tag = index_html.find('>', div_start)
        content_start = div_close_tag + 1
        # Find the closing </div> for this div
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
            new_index = index_html[:content_start] + '\n' + nf_items_str + '\n    ' + index_html[i:]
            print(f"✅ Replaced nf-scroll content (fallback method)")
        else:
            print("❌ Could not parse nf-scroll")
            new_index = index_html
    else:
        print("❌ Could not find nf-scroll at all")
        new_index = index_html

index_html = new_index

# === Step 2: Update daily-banner ===
old_banner = f'daily-2026-06-20.html'
new_banner = f'daily-{TODAY}.html'
# The daily-banner line
index_html = index_html.replace(
    f'href="daily-2026-06-20.html">📰 最新快报：2026-06-20',
    f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}'
)

# === Step 3: Update featured section ===
# Figure out which story to feature
# Let's pick "Figure机器人数首超人类员工" - score 78, highest score
featured_title = "Figure 机器人数首次超过人类员工：人形机器人工厂已经到来"
featured_label = "行业动态"
featured_summary = "2026年6月，Figure AI 宣布其工厂中人形机器人数量首次超过人类员工，成为具身智能领域的里程碑事件。Figure 03 机器人搭载 Helix 视觉语言动作模型，已在 BMW 工厂完成真实生产任务部署。目前 Figure 已获得累计超 7.5 亿美元融资，估值达 26 亿美元——这场机器人取代人类劳动力的实验，已经从理论走入现实。"
featured_detail_url = f"featured-{TODAY}.html"
daily_url = f"daily-{TODAY}.html"
img_path = f"images/featured-{TODAY}-1.jpg"

# Find the featured-card section
old_featured_start = index_html.find('<div class="featured-card">')
old_featured_end = index_html.find('<div class="section-title" style="margin-top:12px">', old_featured_start)

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
      <img src="{img_path}" alt="Figure 03 人形机器人 | Figure AI" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''

if old_featured_start >= 0 and old_featured_end >= 0:
    index_html = index_html[:old_featured_start] + new_featured + '\n\n' + index_html[old_featured_end:]
    print("✅ Updated featured section")
else:
    print("❌ Could not find featured section")

# === Step 4: Add to prev-featured-list ===
# Find the prev-featured-list and add a new entry at the top
prev_list_start = index_html.find('<div class="prev-featured-list">')
prev_list_end = index_html.find('</div>', prev_list_start)

# Find the first entry
first_prev_entry = index_html.find('<a href="featured-', prev_list_start)

new_prev_entry = f'''    <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">Figure 机器人数首次超过人类员工：人形机器人工厂已经到来</span>
      <span class="prev-arrow">→</span>
    </a>
'''

if first_prev_entry >= 0:
    index_html = index_html[:first_prev_entry] + new_prev_entry + index_html[first_prev_entry:]
    print("✅ Added prev-featured entry")
else:
    print("❌ Could not find prev-featured-list")

# === Step 5: Update review card dates ===
# Replace all 📅 2026-06-20 with 📅 {TODAY}
index_html = index_html.replace('📅 2026-06-20</span>', f'📅 {TODAY}</span>')

# === Step 6: Write updated index.html ===
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("✅ Updated index.html")

# ========== Step 7: Update daily.html ==========
with open('daily.html', 'r', encoding='utf-8') as f:
    daily_html = f.read()

# Update banner
daily_html = daily_html.replace(
    f'href="daily-2026-06-20.html">📰 最新快报：2026-06-20',
    f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}'
)

# Update nav - add today's entry at top of nav
daily_nav_start = daily_html.find('<div class="daily-nav">')
# Find the first nav link
first_nav_link = daily_html.find('<a href="daily-', daily_nav_start)

new_nav_link = f'    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n'

if first_nav_link >= 0:
    daily_html = daily_html[:first_nav_link] + new_nav_link + daily_html[first_nav_link:]
    print("✅ Updated daily.html nav")
else:
    print("❌ Could not update daily.html nav")

# Update the subtitle text too
daily_html = daily_html.replace(
    'id="daily-subtitle">加载中...',
    'id="daily-subtitle">加载中...'
)

with open('daily.html', 'w', encoding='utf-8') as f:
    f.write(daily_html)
print("✅ Updated daily.html")

print(f"\n{'='*50}")
print(f"✅ All updates complete for {TODAY}")
print(f"{'='*50}")
