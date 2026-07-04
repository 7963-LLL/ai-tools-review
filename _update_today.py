#!/usr/bin/env python3
"""Update index.html and daily.html for 2026-07-04"""
import json, re, os
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
TODAY_DT = datetime.now(BJT)

print(f"Running update for {TODAY}")

# ========== Read data ==========
data = json.load(open('aihot_selected.json', encoding='utf-8'))
items = data['items']

# ========== Read generated nf-items ==========
with open('_nf_items_output.txt', encoding='utf-8') as f:
    nf_items_str = f.read()

# ========== Count items by category ==========
cat_counts = {}
for item in items:
    c = item.get('category', 'other')
    cat_counts[c] = cat_counts.get(c, 0) + 1
print(f"Items by category: {cat_counts}")

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
    new_banner = f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}'
    index_html = index_html.replace(old_banner, new_banner)
    print(f"✅ Updated daily-banner to {TODAY}")
else:
    print("⚠️ Could not find daily-banner")

# === Step 3: Update featured section ===
# Pick the most interesting topic for today
# Let's make this data-driven - pick highest score industry/item
featured_items = sorted(items, key=lambda x: x.get('score', 0), reverse=True)
top = featured_items[0]
print(f"\nTop scored item: [{top.get('category')}] score={top.get('score')} | {top.get('title')}")

# Let's pick something with depth - check top items for a good topic
# Item 4: 全球首例AI Agent勒索攻击 (industry, score 76)
# Item 8: 国家网信办AI管理办法 (industry, score 79)
# Item 13: 阿里达摩院超导材料AI (paper, score 80)
# Item 19: Microsoft Frontier Company (industry, score 78)
# Item 1: pxpipe (tip, score 83)

# I'll pick the AI Agent勒索攻击 since it's a very timely and impactful topic
featured_title = "全球首例 AI Agent 勒索攻击曝光：从漏洞利用到数据库加密全程自主完成"
featured_label = "行业安全"
featured_summary = "2026年7月，安全研究人员披露了全球首例由 AI Agent 完全自主发起的勒索攻击事件。攻击者利用一个未打补丁的漏洞，AI Agent 独立完成了情报收集、漏洞利用、横向移动、权限提升和数据加密的全链条攻击。这起事件标志着网络安全的根本性转变——攻击者不再仅仅是工具的使用者，AI可以独立规划并执行复杂的多阶段攻击。各安全厂商紧急升级防护策略。"
featured_detail_url = f"featured-{TODAY}.html"
daily_url = f"daily-{TODAY}.html"
img_path = f"images/featured-{TODAY}-1.jpg"

# Find featured-card section
old_featured_start = index_html.find('<div class="featured-card">')
old_featured_end = index_html.find('<div class="section-title" style="margin-top:12px">', old_featured_start)

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
      <img src="{img_path}" alt="AI Agent 勒索攻击 — 全球首例" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
      <span class="prev-title">{featured_title}</span>
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
    daily_html = daily_html.replace(banner_match.group(0), f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}')
    print("✅ Updated daily.html banner")

# Add today's entry at top of daily-nav
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

# ========== Step 8: Generate daily-YYYY-MM-DD.html ==========
def fmt_time_bjt(published_at):
    """Format time to BJT"""
    if not published_at:
        return ''
    try:
        utc_dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
        bjt_dt = utc_dt.astimezone(BJT)
        return bjt_dt.strftime('%H:%M')
    except:
        return published_at[:16] if len(published_at) >= 16 else published_at

def clean_src(source):
    if not source:
        return ''
    s = re.sub(r'^X[：:]', '', source)
    s = re.sub(r'[（(][^)）]*[)）]', '', s)
    s = s.strip()
    if len(s) > 25:
        s = s[:22] + '...'
    return s

CAT_LABELS = {
    'ai-models': '模型发布/更新',
    'ai-products': '产品发布/更新',
    'industry': '行业动态',
    'paper': '论文研究',
    'tip': '技巧与观点'
}
CAT_ORDER = ['ai-models', 'ai-products', 'industry', 'paper', 'tip']

groups = {}
for item in items:
    c = item.get('category', 'other')
    if c not in groups:
        groups[c] = []
    groups[c].append(item)

weekday_names = ['日','一','二','三','四','五','六']
date_display = TODAY + ' 星期' + weekday_names[TODAY_DT.weekday()]

# Stats
total = len(items)
m_count = sum(1 for i in items if i.get('category') == 'ai-models')
p_count = sum(1 for i in items if i.get('category') == 'ai-products')
i_count = sum(1 for i in items if i.get('category') == 'industry')

daily_content_html = ''
for cat in CAT_ORDER:
    if cat not in groups or len(groups[cat]) == 0:
        continue
    label = CAT_LABELS.get(cat, cat)
    daily_content_html += f'    <h2>{label}</h2>\n    <div class="daily-section">\n'
    for item in groups[cat]:
        time_str = fmt_time_bjt(item.get('publishedAt', ''))
        src_clean = clean_src(item.get('source', ''))
        title = item.get('title', '')
        url = item.get('url', '#')
        summary = item.get('summary', '')
        daily_content_html += f'''    <div class="daily-item">
      <span class="daily-time">{time_str}</span>
      <div class="daily-body">
        <a href="{url}" target="_blank" rel="noopener" class="daily-title">{title}</a>
        <span class="daily-src">{src_clean}</span>
      </div>
    </div>
'''
    daily_content_html += '    </div>\n'

daily_page = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 快报 - {TODAY} 每日 AI 资讯速览 | suduai.top</title>
  <meta name="description" content="{TODAY} 的 AI 资讯速览，涵盖模型发布、产品更新、行业动态、论文研究等 {total} 条最新 AI 热点。">
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
  <style>
    .daily-item .daily-body .daily-title {{ font-size: 0.95em; line-height: 1.5; }}
    .daily-item .daily-body .daily-src {{ font-size: 0.8em; opacity: 0.7; margin-top: 2px; }}
    .daily-section {{ margin-bottom: 28px; }}
    .daily-section h2:first-child {{ margin-top: 0; }}
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
  <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 {total} 条）→</a>
</div>

<div class="content-page">
  <h1>AI 快报 · {date_display}</h1>
  <div class="subtitle">共 {total} 条 AI 热点资讯</div>

  <div class="daily-nav">
    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>
  </div>

  <!-- Quick Stats -->
  <div class="stats-row" id="daily-stats">
    <div class="key-stat"><span class="stat-val">{total}</span><span class="stat-lbl">今日资讯</span></div>
    <div class="key-stat"><span class="stat-val">{m_count}</span><span class="stat-lbl">模型发布</span></div>
    <div class="key-stat"><span class="stat-val">{p_count}</span><span class="stat-lbl">产品更新</span></div>
    <div class="key-stat"><span class="stat-val">{i_count}</span><span class="stat-lbl">行业动态</span></div>
  </div>

  <div id="daily-content">
{daily_content_html}  </div>

  <!-- Methodology -->
  <h2>关于本简报</h2>
  <p>本页面由 AI 自动生成，数据来源 <a href="https://aihot.virxact.com" target="_blank" rel="noopener">aihot.virxact.com</a>，每天自动更新。涵盖模型发布、产品更新、行业动态、论文研究、技巧观点五大类 AI 资讯。</p>
  <p>所有条目标注了来源和发布时间，点击标题可查看原文。</p>
</div>

<footer>
  <div class="container">
    <p>AI快报站 © 2026</p>
    <p style="margin-top:2px;"><a href="privacy-policy.html">隐私政策</a></p>
  </div>
</footer>

</body>
</html>'''

with open(f'daily-{TODAY}.html', 'w', encoding='utf-8') as f:
    f.write(daily_page)
print(f"✅ Generated daily-{TODAY}.html with {total} items")

print(f"\n{'='*50}")
print(f"✅ All updates complete for {TODAY}")
print(f"{'='*50}")
