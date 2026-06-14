#!/usr/bin/env python3
"""Generate daily-YYYY-MM-DD.html and nf-items from aihot_selected.json"""
import json
from datetime import datetime, timezone, timedelta
import os

BJT = timezone(timedelta(hours=8))

def parse_utc(iso_str):
    """Parse ISO8601 UTC string to datetime"""
    if not iso_str:
        return None
    s = iso_str.replace('Z', '+00:00')
    return datetime.fromisoformat(s)

def to_bjt_str(utc_str):
    """Convert UTC ISO string to BJT display string"""
    dt = parse_utc(utc_str)
    if not dt:
        return ''
    bjt = dt.astimezone(BJT)
    now = datetime.now(BJT)
    today = now.date()
    bjt_date = bjt.date()
    
    if bjt_date == today:
        return f"今天 {bjt.strftime('%H:%M')}"
    elif (today - bjt_date).days == 1:
        return f"昨天 {bjt.strftime('%H:%M')}"
    else:
        return bjt.strftime('%m/%d %H:%M')

def to_bjt_time(utc_str):
    """Just return HH:MM part in BJT"""
    dt = parse_utc(utc_str)
    if not dt:
        return ''
    bjt = dt.astimezone(BJT)
    return bjt.strftime('%H:%M')

def clean_source(source):
    """Clean source name: remove X prefix, paren comments, truncate"""
    if not source:
        return ''
    # Remove X： prefix (both full and half width colon)
    import re
    s = re.sub(r'^[Xx][：:]\s*', '', source)
    # Remove parenthetical comments
    s = re.sub(r'\s*\([^)]*\)', '', s)
    s = re.sub(r'\s*（[^）]*）', '', s)
    # Trim
    if len(s) > 18:
        s = s[:15] + '...'
    return s.strip()

def clean_source_daily(source):
    """Keep original source for daily page (no truncation)"""
    if not source:
        return ''
    import re
    s = re.sub(r'^[Xx][：:]\s*', '', source)
    return s.strip()

CATEGORY_LABELS = {
    'ai-models': ('模型发布/更新', '🤖'),
    'ai-products': ('产品发布/更新', '🚀'),
    'industry': ('行业动态', '🏭'),
    'paper': ('论文研究', '📄'),
    'tip': ('技巧与观点', '💡'),
}

CATEGORY_ORDER = ['ai-products', 'industry', 'ai-models', 'paper', 'tip']

data = json.load(open('aihot_selected.json'))
items = data['items']

# Today's date
today = datetime.now(BJT).strftime('%Y-%m-%d')

# Weekday in Chinese
weekday_map = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
weekday = weekday_map[datetime.now(BJT).weekday()]

# Build category counts
cat_counts = {}
for item in items:
    cat = item.get('category') or 'uncategorized'
    cat_counts[cat] = cat_counts.get(cat, 0) + 1

# ======== 1. Generate nf-item HTML snippets ========
nf_items_html = []
for item in items:
    cat = item.get('category') or ''
    time_str = to_bjt_str(item.get('publishedAt'))
    title = item.get('title', '')
    url = item.get('url', '')
    src = clean_source(item.get('source', ''))
    
    nf_items_html.append(f'''      <a href="{url}" target="_blank" rel="noopener" class="nf-item" data-category="{cat}">
        <span class="nf-time">{time_str}</span>
        <span class="nf-title">{title}</span>
        <span class="nf-src">{src}</span>
      </a>''')

nf_items_str = '\n'.join(nf_items_html)

# ======== 2. Generate daily page content ========
daily_categories = {}
for item in items:
    cat = item.get('category') or 'uncategorized'
    if cat not in daily_categories:
        daily_categories[cat] = []
    daily_categories[cat].append(item)

daily_sections = []
for cat in CATEGORY_ORDER:
    if cat not in daily_categories:
        continue
    cat_items = daily_categories[cat]
    label, icon = CATEGORY_LABELS.get(cat, (cat, ''))
    count = len(cat_items)
    
    items_html = []
    for item in cat_items:
        t = to_bjt_time(item.get('publishedAt'))
        title = item.get('title', '')
        url = item.get('url', '')
        src = clean_source_daily(item.get('source', ''))
        items_html.append(f'''<div class="daily-item"><span class="daily-time">{t}</span><div class="daily-body"><a href="{url}" target="_blank" rel="noopener" class="daily-title">{title}</a><span class="daily-src">{src}</span></div></div>''')
    
    daily_sections.append(f'''<div class="daily-category">
<h2>{icon} {label} <span class="cat-count">{count}</span></h2>
{chr(10).join(items_html)}
</div>''')

daily_body = '\n'.join(daily_sections)

# Calculate stats
stats = []
for cat in CATEGORY_ORDER:
    if cat in cat_counts:
        label, _ = CATEGORY_LABELS.get(cat, (cat, ''))
        stats.append(f'    <div class="key-stat"><span class="stat-val">{cat_counts[cat]}</span><span class="stat-lbl">{label}</span></div>')
stats_str = '\n'.join(stats)

# Category count stats (first 4 only)
count_keys = [c for c in CATEGORY_ORDER if c in cat_counts][:4]

# Generate daily-YYYY-MM-DD.html
daily_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 快报 {today} - 今日 AI 资讯速览 | suduai.top</title>
  <meta name="description" content="{today} AI 资讯速览，共 50 条精选内容，涵盖模型发布、产品更新、行业动态等。">
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
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8469472392292447" crossorigin="anonymous"></script>
<style>
.daily-category {{ margin-bottom: 2.5rem; }}
.daily-category h2 {{ font-size: 1.5rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 3px solid #2563eb; display: inline-block; }}
.cat-count {{ display: inline-block; background: #2563eb; color: #fff; font-size: 0.8rem; padding: 0.15rem 0.6rem; border-radius: 999px; vertical-align: middle; margin-left: 0.3rem; }}
.daily-item {{ display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.6rem 0; border-bottom: 1px solid rgba(0,0,0,0.06); }}
.daily-item:last-child {{ border-bottom: none; }}
.daily-time {{ color: #6b7280; font-size: 0.85rem; min-width: 3.5rem; margin-top: 0.1rem; }}
.daily-body {{ flex: 1; }}
.daily-title {{ color: #1f2937; text-decoration: none; font-weight: 500; display: block; margin-bottom: 0.15rem; }}
.daily-title:hover {{ color: #2563eb; text-decoration: underline; }}
.daily-src {{ color: #9ca3af; font-size: 0.78rem; }}
.content-page {{ max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }}
.stats-row {{ display: flex; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap; }}
.key-stat {{ flex: 1; min-width: 100px; background: #f9fafb; border-radius: 12px; padding: 1rem; text-align: center; }}
.stat-val {{ font-size: 2rem; font-weight: 700; color: #2563eb; display: block; }}
.stat-lbl {{ font-size: 0.85rem; color: #6b7280; margin-top: 0.25rem; display: block; }}
.daily-nav {{ margin: 1rem 0; display: flex; gap: 0.5rem; flex-wrap: wrap; }}
.daily-nav a {{ background: #f3f4f6; padding: 0.4rem 1rem; border-radius: 6px; text-decoration: none; color: #374151; font-size: 0.9rem; }}
.daily-nav a:hover {{ background: #e5e7eb; }}
</style>
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
  <a href="daily-{today}.html">📰 最新快报：{today}（今日 AI 精选 50 条）→</a>
</div>

<div class="content-page">
  <h1>AI 快报 · {today[:4]}年{today[5:7]}月{today[8:10]}日</h1>
  <div class="subtitle">{weekday} · 今日 AI 精选 50 条</div>

  <div class="daily-nav">
    <a href="daily.html">📋 返回目录</a>
    <a href="featured-{today}.html">⭐ 精选深度文</a>
  </div>

  <div class="stats-row">
    <div class="key-stat"><span class="stat-val">50</span><span class="stat-lbl">今日资讯</span></div>
{stats_str}
  </div>

{daily_body}

</div>

<footer>
  <div class="container">
    <p>AI快报站 © 2026</p>
    <p style="margin-top:2px;"><a href="privacy-policy.html">隐私政策</a></p>
  </div>
</footer>

</body>
</html>"""

# Write daily file
daily_filename = f'daily-{today}.html'
with open(daily_filename, 'w', encoding='utf-8') as f:
    f.write(daily_html)

# Write nf_items to a file for manual insertion
with open('_nf_items_output.txt', 'w', encoding='utf-8') as f:
    f.write(nf_items_str)

print(f"✅ Generated {daily_filename}")
print(f"✅ Generated _nf_items_output.txt with {len(nf_items_html)} nf-items")
print(f"✅ Stats: {json.dumps(cat_counts, ensure_ascii=False)}")
print(f"✅ Date: {today} ({weekday})")

# Also output summary info
print("\n--- Category breakdown ---")
for cat in CATEGORY_ORDER:
    if cat in cat_counts:
        label, icon = CATEGORY_LABELS.get(cat, (cat, ''))
        print(f"  {icon} {label}: {cat_counts[cat]}")
