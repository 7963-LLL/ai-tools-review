#!/usr/bin/env python3
"""Comprehensive daily update script for suduai.top"""
import json, re, os
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
now = datetime.now(BJT)
TODAY = now.strftime('%Y-%m-%d')
today_display = f"{now.year}年{now.month}月{now.day}日"
weekday = ['日','一','二','三','四','五','六'][now.weekday()]

# ========== Load data ==========
with open('aihot_selected.json', encoding='utf-8') as f:
    raw = json.load(f)
items = raw.get('items', raw.get('data', []))

print(f"Loaded {len(items)} items")

# Category mapping
CAT_MAP = {
    'ai-models': ('模型发布/更新', '🤖', '模型'),
    'ai-products': ('产品发布/更新', '🚀', '产品'),
    'industry': ('行业动态', '🏭', '行业'),
    'paper': ('论文研究', '📄', '论文'),
    'tip': ('技巧与观点', '💡', '技巧'),
}

CAT_ORDER = ['ai-models', 'ai-products', 'industry', 'paper', 'tip']

def parse_iso_time(ts):
    """Parse ISO 8601 time string to BJT datetime"""
    if not ts:
        return None, ''
    ts = ts.replace('Z', '+00:00')
    try:
        dt = datetime.fromisoformat(ts)
        bjt_dt = dt.astimezone(BJT)
        return bjt_dt, ''
    except:
        return None, ts

def format_time_bjt(bjt_dt, now):
    """Format datetime to BJT display string"""
    if bjt_dt is None:
        return ''
    today = now.date()
    dt_date = bjt_dt.date()
    if dt_date == today:
        return f"今天 {bjt_dt.strftime('%H:%M')}"
    elif dt_date == today - timedelta(days=1):
        return f"昨天 {bjt_dt.strftime('%H:%M')}"
    else:
        return bjt_dt.strftime('%m/%d %H:%M')

def clean_source(src):
    """Clean source name: remove X： prefix, parenthetical annotations, truncate"""
    if not src:
        return ''
    s = re.sub(r'^X[：:]\s*', '', src)
    s = re.sub(r'[（(][^）)]*[）)]', '', s)
    s = s.strip()
    if len(s) > 18:
        s = s[:15] + '...'
    return s

# ========== Generate nf-items HTML ==========
nf_items_lines = []
for item in items:
    cat = item.get('category', 'industry')
    title = item.get('title', '')
    url = item.get('url', '#')
    source = item.get('source', '')
    
    bjt_dt, _ = parse_iso_time(item.get('publishedAt', ''))
    time_str = format_time_bjt(bjt_dt, now)
    
    src_clean = clean_source(source)
    
    nf_items_lines.append(
        f'      <a href="{url}" target="_blank" rel="noopener" class="nf-item" data-category="{cat}">\n'
        f'        <span class="nf-time">{time_str}</span>\n'
        f'        <span class="nf-title">{title}</span>\n'
        f'        <span class="nf-src">{src_clean}</span>\n'
        f'      </a>'
    )

nf_items_str = '\n'.join(nf_items_lines)

# Print count for verification
print(f"Generated {len(nf_items_lines)} nf-items")

# ========== Update index.html ==========
with open('index.html', encoding='utf-8') as f:
    index_html = f.read()

# --- Step 1: Replace nf-scroll content ---
pattern_start = '<div class="nf-scroll" id="nf-scroll">'
# Find the nf-scroll opening
idx_start = index_html.find(pattern_start)
# Find the nf-scroll closing (the </div> that closes the nf-scroll div)
# After the last nf-item </a>, there's a closing </div>
content_start = idx_start + len(pattern_start)

# Find where nf-scroll closes: it's the </div> after all nf-items
# Before the </div>\n  </div>\n\n</div> (nf-box close, then another div)
search_from = content_start
nf_scroll_close = index_html.find('</div>', search_from)
# Find the close of nf-scroll - let's find it by looking for the pattern after all items
# The structure is: <div class="nf-scroll"...> ...items... </div>\n  </div>\n\n</div>
# So nf-scroll's </div> is the one right before the \n  </div> of nf-box

# Better approach: find the end marker
end_marker = '</div>\n  </div>\n\n</div>\n\n<script>'
end_idx = index_html.find(end_marker, idx_start)
if end_idx >= 0:
    # The nf-scroll closing </div> is at end_idx
    new_index = index_html[:content_start] + '\n' + nf_items_str + '\n    ' + index_html[end_idx:]
    print("✅ Replaced nf-scroll content (method 1)")
else:
    # Fallback: find the closing of nf-scroll which is the first </div> before </div><!-- end nf-box -->
    ss = content_start
    # Find the last </a> before close
    last_a = index_html.rfind('</a>', ss, index_html.find('</div>', ss))
    if last_a >= 0:
        close_div = index_html.find('</div>', last_a)
        # Also find the nf-box close right after
        new_index = index_html[:content_start] + '\n' + nf_items_str + '\n    ' + index_html[close_div:]
        print("✅ Replaced nf-scroll content (method 2)")
    else:
        print("❌ Could not find nf-scroll boundaries")
        new_index = index_html

index_html = new_index

# --- Step 2: Update daily-banner ---
# Find any daily-YYYY-MM-DD.html link in the banner
banner_pattern = r'href="daily-\d{4}-\d{2}-\d{2}\.html"[^>]*>📰 最新快报：\d{4}-\d{2}-\d{2}'
index_html = re.sub(
    banner_pattern,
    f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}',
    index_html
)
print("✅ Updated daily-banner")

# --- Step 3: Update featured section ---
# Determine featured topic - pick Oracle story or another good one
# Sort by score to find best topic
sorted_items = sorted(items, key=lambda x: x.get('score', 0), reverse=True)

# Find the best topic for featured article - pick industry or ai-products news with score >= 70
featured_item = None
for item in sorted_items:
    cat = item.get('category', '')
    score = item.get('score', 0)
    # Prefer industry or ai-products with good score
    if cat in ('industry', 'ai-products', 'ai-models') and score >= 70:
        featured_item = item
        break

if not featured_item:
    featured_item = sorted_items[0]

featured_cat = featured_item.get('category', 'industry')
featured_label = CAT_MAP.get(featured_cat, ('行业动态', '🏭', '行业'))[0]
featured_title = featured_item.get('title', '')
featured_url = featured_item.get('url', '#')
featured_summary = featured_item.get('summary', '')

# Generate a good summary
if len(featured_summary) > 200:
    featured_summary = featured_summary[:197] + '...'

featured_detail_url = f"featured-{TODAY}.html"
daily_url = f"daily-{TODAY}.html"

# Build featured card (without image for now - we'll add image after download)
# We'll add image if we can find one
img_path = f"images/featured-{TODAY}-1.jpg"
img_tag = f'<img src="{img_path}" alt="{featured_title} | 官方图" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">'

# Find and replace the featured card
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
      {img_tag}
    </div>
  </div>'''

if old_featured_start >= 0 and old_featured_end >= 0:
    index_html = index_html[:old_featured_start] + new_featured + '\n\n' + index_html[old_featured_end:]
    print(f"✅ Updated featured section: {featured_title[:50]}")
else:
    print("❌ Could not find featured section")

# --- Step 4: Add to prev-featured-list ---
prev_list_start = index_html.find('<div class="prev-featured-list">')
first_prev_entry = index_html.find('<a href="featured-', prev_list_start)

new_prev_entry = f'''    <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{featured_title}</span>
      <span class="prev-arrow">→</span>
    </a>
'''

if first_prev_entry >= 0:
    index_html = index_html[:first_prev_entry] + new_prev_entry + index_html[first_prev_entry:]
    print("✅ Added prev-featured entry")
else:
    print("❌ Could not find prev-featured-list")

# --- Step 5: Update review card dates ---
# Find and replace all review dates (like 📅 2026-06-24</span>)
index_html = re.sub(r'📅 \d{4}-\d{2}-\d{2}</span>', f'📅 {TODAY}</span>', index_html)
print("✅ Updated review card dates")

# ========== Write updated index.html ==========
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("✅ Written index.html")


# ========== Generate daily-YYYY-MM-DD.html ==========
# Load a template from an existing daily page
daily_template_path = f'daily-{TODAY}.html'
# Check if today's daily already exists (unlikely)
if os.path.exists(daily_template_path):
    print(f"⚠️ {daily_template_path} already exists, will overwrite")

# Read an existing daily for template
existing_daily = None
for d in sorted(os.listdir('.')):
    if d.startswith('daily-20') and d.endswith('.html') and d != daily_template_path:
        existing_daily = d
        break

# Use daily.html as base template structure
daily_html_new = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 快报 · {TODAY} - 每日 AI 资讯速览 | suduai.top</title>
  <meta name="description" content="{TODAY} AI资讯速览，涵盖模型发布、产品更新、行业动态、论文研究等最新AI热点，共{len(items)}条。">
  <link rel="stylesheet" href="css/style.css">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="favicon.png">
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Z33SFE6V0H"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-Z33SFE6V0H');
</script>
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8469472392292447" crossorigin="anonymous"></script>
</head>
<body>

<header>
  <div class="container">
    <a href="/" class="logo">AI<span>快报</span></a>
    <nav>
      <a href="/">首页</a>
      <a href="chatgpt-vs-claude.html">ChatGPT vs Claude</a>
      <a href="best-ai-writing-tools.html">写作</a>
      <a href="best-ai-image-tools.html">图像</a>
      <a href="best-ai-coding-tools.html">编程</a>
      <a href="best-ai-video-tools.html">视频</a>
      <a href="best-ai-voice-tools.html">语音</a>
      <a href="daily.html">每日快报</a>
      <a href="about.html">关于</a>
      <span class="lang-select">🌐</span>
      <div class="lang-menu" id="lang-menu">
        <a href="#" data-lang="en">English</a>
        <a href="#" data-lang="ja">日本語</a>
        <a href="#" data-lang="ko">한국어</a>
        <a href="#" data-lang="es">Español</a>
        <a href="#" data-lang="fr">Français</a>
        <a href="#" data-lang="de">Deutsch</a>
        <a href="#" data-lang="pt">Português</a>
      </div>
    </nav>
  </div>
</header>

<div class="daily-banner">
  <a href="featured-{TODAY}.html">⭐ 今日深度解读：{featured_title} →</a>
</div>

<div class="content-page">
  <h1>AI 快报 · {TODAY}</h1>
  <div class="subtitle">{today_display} 星期{weekday}</div>

  <div class="daily-nav">
    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报 🔥</a>
    <a href="featured-{TODAY}.html">⭐ {TODAY} 深度解读</a>
  </div>

  <!-- Quick Stats -->
  <div class="stats-row">
    <div class="key-stat"><span class="stat-val">{len(items)}</span><span class="stat-lbl">今日资讯</span></div>
'''

# Count per category
cat_counts = {}
for item in items:
    c = item.get('category', 'other')
    cat_counts[c] = cat_counts.get(c, 0) + 1

daily_html_new += f'    <div class="key-stat"><span class="stat-val">{cat_counts.get("ai-models", 0)}</span><span class="stat-lbl">模型发布</span></div>\n'
daily_html_new += f'    <div class="key-stat"><span class="stat-val">{cat_counts.get("ai-products", 0)}</span><span class="stat-lbl">产品更新</span></div>\n'
daily_html_new += f'    <div class="key-stat"><span class="stat-val">{cat_counts.get("industry", 0)}</span><span class="stat-lbl">行业动态</span></div>\n'
daily_html_new += '  </div>\n\n'

# Group by category
groups = {}
for item in items:
    c = item.get('category', 'other')
    if c not in groups:
        groups[c] = []
    groups[c].append(item)

# Render each category
for cat in CAT_ORDER:
    if cat not in groups or not groups[cat]:
        continue
    cat_display, cat_emoji, _ = CAT_MAP.get(cat, (cat, '', cat))
    daily_html_new += f'  <h2>{cat_emoji} {cat_display} <span class="cat-count">({len(groups[cat])}条)</span></h2>\n'
    daily_html_new += '  <div class="daily-section">\n'
    
    for item in groups[cat]:
        title = item.get('title', '')
        url = item.get('url', '#')
        source = item.get('source', '')
        bjt_dt, _ = parse_iso_time(item.get('publishedAt', ''))
        time_str = format_time_bjt(bjt_dt, now)
        src_clean = clean_source(source)
        
        daily_html_new += f'''    <div class="daily-item">
      <span class="daily-time">{time_str}</span>
      <div class="daily-body">
        <a href="{url}" target="_blank" rel="noopener" class="daily-title">{title}</a>
        <span class="daily-src">{src_clean}</span>
      </div>
    </div>
'''
    
    daily_html_new += '  </div>\n\n'

daily_html_new += '''  <!-- Methodology -->
  <h2>关于本简报</h2>
  <p>本页面由 AI 自动生成，数据来源 <a href="https://aihot.virxact.com" target="_blank" rel="noopener">aihot.virxact.com</a>，每天早上更新。涵盖模型发布、产品更新、行业动态、论文研究、技巧观点五大类 AI 资讯。</p>
  <p>所有条目标注了来源和发布时间，点击标题可查看原文。</p>
  <p style="margin-top:12px;"><a href="daily.html">← 返回每日快报目录</a></p>
</div>

<footer>
  <div class="container">
    <p>AI快报站 © 2026</p>
    <p style="margin-top:2px;"><a href="privacy-policy.html">隐私政策</a></p>
  </div>
</footer>

</body>
</html>'''

with open(daily_template_path, 'w', encoding='utf-8') as f:
    f.write(daily_html_new)
print(f"✅ Generated {daily_template_path}")

# ========== Update daily.html ==========
with open('daily.html', encoding='utf-8') as f:
    daily_html = f.read()

# Update banner
daily_html = re.sub(
    r'href="daily-\d{4}-\d{2}-\d{2}\.html"[^>]*>📰 最新快报：\d{4}-\d{2}-\d{2}',
    f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}',
    daily_html
)

# Update nav - add today's entry at top
daily_nav_start = daily_html.find('<div class="daily-nav">')
first_nav_link = daily_html.find('<a href="daily-', daily_nav_start)

new_nav_link = f'    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报 🔥</a>\n'

if first_nav_link >= 0:
    daily_html = daily_html[:first_nav_link] + new_nav_link + daily_html[first_nav_link:]
    print("✅ Updated daily.html nav")
else:
    print("❌ Could not update daily.html nav")

with open('daily.html', 'w', encoding='utf-8') as f:
    f.write(daily_html)
print("✅ Updated daily.html")

print(f"\n{'='*50}")
print(f"✅ All updates complete for {TODAY}")
print(f"  - {len(items)} nf-items generated")
print(f"  - index.html updated (nf-scroll, banner, featured, prev-featured, review dates)")
print(f"  - {daily_template_path} generated")
print(f"  - daily.html updated")
print(f"  - Featured topic: {featured_title[:60]}")
print(f"{'='*50}")
