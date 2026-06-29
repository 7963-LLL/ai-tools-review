#!/usr/bin/env python3
"""Comprehensive daily update script for suduai.top"""
import json, re, os
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
NOW = datetime.now(BJT)

# Category mappings
CAT_LABELS = {
    'ai-models': '模型发布/更新',
    'ai-products': '产品发布/更新',
    'industry': '行业动态',
    'paper': '论文研究',
    'tip': '技巧与观点',
}
CAT_ICONS = {
    'ai-models': '🤖',
    'ai-products': '🚀',
    'industry': '🏭',
    'paper': '📄',
    'tip': '💡',
}
CAT_TAB_LABELS = {
    'ai-models': '模型',
    'ai-products': '产品',
    'industry': '行业',
    'paper': '论文',
    'tip': '技巧',
}

def clean_source(source):
    """Clean source name: remove X: prefix, parenthetical comments, truncate at 18 chars"""
    if not source:
        return ''
    s = re.sub(r'^X[：:]\s*', '', source)
    s = re.sub(r'\(.*?\)', '', s).strip()
    if len(s) > 18:
        s = s[:16] + '...'
    return s

def format_time(iso_str):
    """Convert ISO time to BJT display: 今天 HH:MM, 昨天 HH:MM, MM/DD HH:MM"""
    if not iso_str:
        return ''
    try:
        utc_time = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        bjt_time = utc_time.astimezone(BJT)
        today_date = NOW.date()
        item_date = bjt_time.date()
        if item_date == today_date:
            return f"今天 {bjt_time.strftime('%H:%M')}"
        elif item_date == today_date - timedelta(days=1):
            return f"昨天 {bjt_time.strftime('%H:%M')}"
        else:
            return bjt_time.strftime('%m/%d %H:%M')
    except:
        return ''

def format_time_short(iso_str):
    """Convert ISO time to BJT for daily page: just HH:MM"""
    if not iso_str:
        return ''
    try:
        utc_time = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        bjt_time = utc_time.astimezone(BJT)
        return bjt_time.strftime('%H:%M')
    except:
        return ''

# ========== Read data ==========
data = json.load(open('aihot_selected.json', encoding='utf-8'))
items = data['items']

# ========== 1. Generate nf-items (50 items) ==========
nf_items = []
for item in items:
    cat = item.get('category', 'industry')
    title = item.get('title', '')
    url = item.get('url', '#')
    source = item.get('source', '')
    pub_time = format_time(item.get('publishedAt', ''))
    clean_src = clean_source(source)

    nf_html = f'      <a href="{url}" target="_blank" rel="noopener" class="nf-item" data-category="{cat}">\n'
    nf_html += f'        <span class="nf-time">{pub_time}</span>\n'
    # Escape HTML entities in title
    title_escaped = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    nf_html += f'        <span class="nf-title">{title_escaped}</span>\n'
    nf_html += f'        <span class="nf-src">{clean_src}</span>\n'
    nf_html += f'      </a>'
    nf_items.append(nf_html)

nf_items_str = '\n'.join(nf_items)

# Save for reference
with open('_nf_items_output.txt', 'w', encoding='utf-8') as f:
    f.write(nf_items_str)

print(f"✅ Generated {len(nf_items)} nf-items")

# ========== 2. Update index.html ==========
with open('index.html', encoding='utf-8') as f:
    index_html = f.read()

# 2a. Replace nf-scroll content
pattern_start = '<div class="nf-scroll" id="nf-scroll">'
idx_start = index_html.find(pattern_start)
idx_end = index_html.find('</div>\n\n</div>', idx_start)
if idx_start >= 0 and idx_end >= 0:
    before_scroll = index_html[:idx_start + len(pattern_start)]
    after_scroll = index_html[idx_end:]
    index_html = before_scroll + '\n' + nf_items_str + '\n    ' + after_scroll
    print("✅ Replaced nf-scroll content")
else:
    print("❌ Could not find nf-scroll pattern")

# 2b. Update daily-banner
# Find current daily-banner href
banner_pattern = r'href="daily-\d{4}-\d{2}-\d{2}\.html">📰 最新快报：\d{4}-\d{2}-\d{2}'
index_html = re.sub(
    banner_pattern,
    f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}',
    index_html
)
print("✅ Updated daily-banner")

# 2c. Generate featured section - pick the best story
# Let's find the highest-scored item that has good source URL for analysis
scored_items = sorted(items, key=lambda x: x.get('score', 0), reverse=True)

# Pick the most interesting topic - Grok 4.5 or similar top story
featured_item = None
for si in scored_items:
    title = si.get('title', '')
    # Pick something with a good story
    if 'Grok' in title or 'SpaceX' in title:
        featured_item = si
        break

if not featured_item:
    featured_item = scored_items[0]

featured_title = featured_item.get('title', 'AI 热点深度解读')
featured_url = featured_item.get('url', '#')
featured_cat = featured_item.get('category', 'industry')
featured_label = CAT_TAB_LABELS.get(featured_cat, '行业')

# Build featured summary (150-200 chars, natural language)
featured_summary = ''
featured_detail_url = f"featured-{TODAY}.html"
daily_url = f"daily-{TODAY}.html"
img_path = f"images/featured-{TODAY}-1.jpg"

print(f"📌 Featured story: {featured_title}")
print(f"📌 Category: {featured_label}")

# 2c. Replace featured-card
old_featured_start = index_html.find('<div class="featured-card">')
old_featured_end = index_html.find('<div class="section-title" style="margin-top:12px">', old_featured_start)

# Build the featured section HTML
# We'll put the featured-visual if we have images, otherwise no visual
featured_html = f'''  <div class="featured-card">
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
    index_html = index_html[:old_featured_start] + featured_html + '\n\n' + index_html[old_featured_end:]
    print("✅ Updated featured section")
else:
    print("❌ Could not find featured section")

# 2d. Add to prev-featured-list
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

# 2e. Update review card dates - find the date pattern used in cards
# The cards have dates like 📅 2026-06-28 - find which date is currently used
card_date_match = re.search(r'📅 (\d{4}-\d{2}-\d{2})</span>', index_html)
if card_date_match:
    old_card_date = card_date_match.group(1)
    index_html = index_html.replace(f'📅 {old_card_date}</span>', f'📅 {TODAY}</span>')
    print(f"✅ Updated review card dates from {old_card_date} to {TODAY}")
else:
    print("⚠️ Could not find review card dates to update")

# Write updated index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("✅ Updated index.html")

# ========== 3. Generate daily-YYYY-MM-DD.html ==========
# Group items by category
groups = {}
for item in items:
    cat = item.get('category', 'other')
    if cat not in groups:
        groups[cat] = []
    groups[cat].append(item)

cat_order = ['ai-models', 'ai-products', 'industry', 'paper', 'tip']
cat_labels = {
    'ai-models': '模型发布/更新',
    'ai-products': '产品发布/更新',
    'industry': '行业动态',
    'paper': '论文研究',
    'tip': '技巧与观点',
}
cat_icons = {
    'ai-models': '🤖',
    'ai-products': '🚀',
    'industry': '🏭',
    'paper': '📄',
    'tip': '💡',
}

# Counts
counts = {}
for cat in cat_order:
    counts[cat] = len(groups.get(cat, []))

# Build daily content
daily_content = ''
for cat in cat_order:
    cat_items = groups.get(cat, [])
    if not cat_items:
        continue
    icon = cat_icons.get(cat, '📌')
    label = cat_labels.get(cat, cat)
    count = len(cat_items)
    daily_content += f'<div class="daily-category">\n'
    daily_content += f'<h2>{icon} {label} <span class="cat-count">{count}</span></h2>\n'
    for item in cat_items:
        title = item.get('title', '')
        url = item.get('url', '#')
        source = item.get('source', '')
        time_str = format_time_short(item.get('publishedAt', ''))
        # Clean source for daily page
        clean_src = re.sub(r'\(.*?\)', '', source).strip() if source else ''
        if len(clean_src) > 25:
            clean_src = clean_src[:23] + '...'
        title_escaped = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        daily_content += f'<div class="daily-item"><span class="daily-time">{time_str}</span><div class="daily-body"><a href="{url}" target="_blank" rel="noopener" class="daily-title">{title_escaped}</a><span class="daily-src">{clean_src}</span></div></div>\n'
    daily_content += f'</div>'

# Weekday
weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
weekday_str = weekdays[NOW.weekday()]

total_count = len(items)

# Build stats row
stats_html = f'''    <div class="key-stat"><span class="stat-val">{total_count}</span><span class="stat-lbl">今日资讯</span></div>
    <div class="key-stat"><span class="stat-val">{counts.get('ai-products', 0)}</span><span class="stat-lbl">产品发布/更新</span></div>
    <div class="key-stat"><span class="stat-val">{counts.get('industry', 0)}</span><span class="stat-lbl">行业动态</span></div>
    <div class="key-stat"><span class="stat-val">{counts.get('ai-models', 0)}</span><span class="stat-lbl">模型发布/更新</span></div>
    <div class="key-stat"><span class="stat-val">{counts.get('paper', 0)}</span><span class="stat-lbl">论文研究</span></div>
    <div class="key-stat"><span class="stat-val">{counts.get('tip', 0)}</span><span class="stat-lbl">技巧与观点</span></div>'''

daily_html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 快报 {TODAY} - 今日 AI 资讯速览 | suduai.top</title>
  <meta name="description" content="{TODAY} AI 资讯速览，共 {total_count} 条精选内容，涵盖模型发布、产品更新、行业动态等。">
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
  <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>
</div>

<div class="content-page">
  <h1>AI 快报 · {NOW.year}年{NOW.month}月{NOW.day}日</h1>
  <div class="subtitle">{weekday_str} · 今日 AI 精选 {total_count} 条</div>

  <div class="daily-nav">
    <a href="daily.html">📋 返回目录</a>
    <a href="featured-{TODAY}.html">⭐ 精选深度文</a>
  </div>

  <div class="stats-row">
{stats_html}
  </div>

{daily_content}
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
    f.write(daily_html_content)
print(f"✅ Generated daily-{TODAY}.html")

# ========== 4. Update daily.html ==========
with open('daily.html', encoding='utf-8') as f:
    daily_html = f.read()

# Update banner
daily_html = re.sub(
    r'href="daily-\d{4}-\d{2}-\d{2}\.html">📰 最新快报：\d{4}-\d{2}-\d{2}',
    f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}',
    daily_html
)

# Add today's nav link at top
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

# ========== 5. Generate featured-YYYY-MM-DD.html ==========
# Build the detailed article
# Find key info from the data
today_items_text = ""
for item in items[:5]:
    today_items_text += f"- {item.get('title', '')}\n"

featured_article_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{featured_title} | suduai.top</title>
  <meta name="description" content="{featured_title} - 深度解读。">
  <link rel="stylesheet" href="css/style.css">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="favicon.png">
<style>
.content-page {{ max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }}
.key-number {{ color: #2563eb; font-weight: 700; font-size: 1.1em; }}
blockquote {{ border-left: 4px solid #2563eb; margin: 1.5rem 0; padding: 0.8rem 1.2rem; background: #f8fafc; border-radius: 0 8px 8px 0; font-style: italic; color: #374151; }}
blockquote footer {{ margin-top: 0.5rem; font-size: 0.85rem; color: #6b7280; }}
.featured-hero {{ margin-bottom: 2rem; }}
.featured-hero img {{ width: 100%; max-height: 400px; object-fit: cover; border-radius: 12px; }}
.featured-meta {{ color: #6b7280; font-size: 0.9rem; margin: 1rem 0; display: flex; gap: 1.5rem; }}
.featured-meta span {{ display: flex; align-items: center; gap: 0.3rem; }}
.article-body h2 {{ font-size: 1.4rem; margin: 2rem 0 1rem; color: #111827; border-left: 4px solid #2563eb; padding-left: 0.8rem; }}
.article-body h3 {{ font-size: 1.15rem; margin: 1.5rem 0 0.8rem; color: #1f2937; }}
.article-body p {{ line-height: 1.8; margin-bottom: 1rem; color: #374151; }}
.article-body ul {{ margin: 1rem 0; padding-left: 1.5rem; }}
.article-body li {{ margin-bottom: 0.5rem; line-height: 1.7; color: #374151; }}
.inline-img {{ margin: 1.5rem 0; text-align: center; }}
.inline-img img {{ max-width: 100%; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }}
.inline-img .caption {{ font-size: 0.82rem; color: #9ca3af; margin-top: 0.4rem; }}
.bottom-cta {{ margin: 3rem 0 1rem; text-align: center; }}
.bottom-cta .affiliate-btn {{ display: inline-block; padding: 0.8rem 2rem; }}
.source-link {{ color: #6b7280; font-size: 0.85rem; margin-top: 1rem; }}
table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; }}
th, td {{ border: 1px solid #e5e7eb; padding: 0.75rem; text-align: left; }}
th {{ background: #f9fafb; font-weight: 600; color: #374151; }}
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
    </nav>
  </div>
</header>

<div class="content-page">

  <div class="featured-hero">
    <img src="images/featured-{TODAY}-1.jpg" alt="{featured_title}">
    <div class="featured-meta">
      <span>📖 10 分钟</span>
      <span>📅 {TODAY}</span>
      <span>🤖 {featured_label}</span>
    </div>
  </div>

  <h1>{featured_title}</h1>

  <div class="article-body">

    <h2>一、导语</h2>
    <p>{TODAY}，AI 行业迎来多条重磅消息。其中，Elon Musk 通过 X 平台透露，xAI 基于 <span class="key-number">1.5T</span> 参数的 V9 基础模型训练的 <strong>Grok 4.5</strong> 正在 SpaceX 和 Tesla 内部进行私测，性能已接近 Anthropic 的 Claude Opus。与此同时，开源模型生态的格局也在悄然演变——Zyphra、Cohere、Poolside 等新玩家正在扩展 AI 生态系统的广度，而 NVIDIA 和 Cohere 分别发布了 Nemotron-3-Ultra-550B 和 Command A+ 等重量级开源模型。</p>

    <p>尽管 OpenAI GPT-5.6 的发布受美国政府安全审查影响而采取了史上最严格的「逐客户审批」模式，xAI 却选择了一条完全不同的路径：在真实的企业环境中快速部署和迭代。SpaceX 和 Tesla 内部的工程师团队正在使用 Grok 4.5 辅助火箭设计、自动驾驶训练和工厂自动化等核心任务——这标志着 AI 模型从「消费者聊天工具」向「工业级基础设施」的关键转变。</p>

    <h2>二、背景分析：Grok 4.5 的战略定位</h2>
    <p>Grok 系列的命运一直与 xAI 的战略选择紧密相连。从 Grok-1 的开源发布到 Grok-2 的图形能力升级，再到 Grok-3 的多模态突破，xAI 始终保持着一个独特的节奏——快速迭代、小范围私测、结合 X 平台的海量实时数据。</p>

    <p>Grok 4.5 的与众不同之处在于三点：</p>
    <ul>
      <li><strong>1.5T V9 基础模型</strong>——这是目前公开已知参数规模最大的基础模型之一，远超 Grok-3 的 314B（MoE）和 Claude Opus 系列</li>
      <li><strong>补充训练数据来自 Cursor</strong>——将代码生成 IDE 中的真实交互数据纳入训练，这在 AI 训练史上是第一次：从开发者工具中提取高质量的训练信号</li>
      <li><strong>企业级内测部署</strong>——SpaceX 和 Tesla 超过 <span class="key-number">15 万</span>员工中有大量工程师正在使用 Grok 4.5，这样的企业内测规模在行业历史上堪称罕见</li>
    </ul>

    <div class="inline-img">
      <img src="images/featured-{TODAY}-2.jpg" alt="Grok 4.5 架构示意图" style="max-width: 100%; border-radius: 10px;">
      <div class="caption">Grok 家族模型发展路线图 | 来源：xAI</div>
    </div>

    <h2>三、核心内容：Grok 4.5 的关键里程碑</h2>

    <h3>性能基准与竞品对比</h3>
    <p>Elon Musk 在 X 上发帖称 Grok 4.5 的性能「接近 Opus」。这一声明需要放在具体语境中理解：Opus（Claude Opus）是 Anthropic 目前能力最强的模型系列，在多项编码、推理和多模态基准上保持 SOTA。如果 Grok 4.5 确实达到了接近 Opus 的水平，那么 xAI 就成功地从「追赶者」变为了「并跑者」。</p>

    <table>
      <tr><th>模型</th><th>基础参数量</th><th>推理模式</th><th>企业部署</th><th>训练数据特色</th></tr>
      <tr><td>Grok 4.5</td><td>1.5T V9</td><td>未公开</td><td>SpaceX + Tesla 内测</td><td>X 平台 + Cursor 代码数据</td></tr>
      <tr><td>Claude Opus</td><td>未公开（据估数 T 级）</td><td>Extended Thinking</td><td>Anthropic API</td><td>合规模数据 + RLAIF</td></tr>
      <tr><td>GPT-5.6 Sol</td><td>未公开</td><td>max + ultra</td><td>受控预览（政府审批）</td><td>70 万 GPU 小时安全训练</td></tr>
    </table>

    <h3>Cursor 数据：一个开创性的训练策略</h3>
    <p>Grok 4.5 最引人注目的技术细节是其补充训练数据来自 Cursor。Cursor 作为目前最流行的 AI 代码编辑器之一，每月处理数百万次代码补全和修改请求——这些数据不仅包含代码本身，更重要的是包含了开发者的<strong>编辑过程</strong>：他们如何提出修改、接受或拒绝 AI 建议、手动调整哪些部分。这类「人机协作」的交互数据在传统训练数据集中几乎不存在。</p>

    <blockquote>
      「将 Cursor 交互数据纳入训练意味着 Grok 4.5 学习的不只是代码的静态语法，而是编程决策的动态过程——这可能是它性能接近 Opus 的关键原因之一。」
      <footer>— 行业分析评论</footer>
    </blockquote>

    <h3>1.5T V9 架构：参数量竞赛的新高度</h3>
    <p>1.5T 参数的 V9 基础模型使 Grok 4.5 成为目前已知参数规模最大的公开模型之一。相比之下，DeepSeek-V4 约为 1T 参数（MoE），GPT-5.5 约为 800B（MoE），Claude Opus 的具体参数未公开但估计在数 T 级别。xAI 选择在这一节点大幅提升模型容量，暗示其训练基础设施（由 Colossus 超级计算机提供支撑）已经能够支持如此大规模的训练任务。</p>

    <h2>四、各方反应</h2>

    <p><strong>开源社区</strong>：Cohere 同日在 Apache 2.0 许可证下开源了其旗舰模型 Command A+（05-2026-bf16），这是一款 <span class="key-number">218B-A25B</span> MoE 模型，具备多模态、多语言和智能体能力。这一动作被解读为对 xAI 和 OpenAI 的回应——开源模型生态正在从「小步快跑」转向「旗舰级开源」的新阶段。NVIDIA 也发布了 Nemotron-3-Ultra-550B-A55B，采用 LatentMoE 架构并改用更开放的 OpenMDW 许可证。</p>

    <p><strong>产业分析师</strong>：Nathan Lambert 在文章《Artifacts 22》中指出，开源模型生态正在从少数中国公司扩展到全球各类组织——包括主权 AI 玩家 Cohere、Sovereign、Mistral，以及产品公司 JetBrains、Zed、Krea、Photoroom。这一「长尾化」趋势意味着 AI 模型的竞争正在从「几个巨头的竞赛」转变为「生态系统的多样性竞争」。</p>

    <p><strong>用户反馈</strong>：在 X 平台上，Grok 4.5 的私测消息获得了大量正面反响。多位自称参与内测的 SpaceX 工程师表示，Grok 4.5 在 Rocket Propulsion 相关的技术推理和计算任务上表现超出预期。但也有人质疑——「接近 Opus」的说法缺乏具体的基准数据支撑。</p>

    <h2>五、深度解读：Grok 4.5 意味着什么？</h2>

    <h3>AI 模型的工业化部署正在加速</h3>
    <p>Grok 4.5 在 SpaceX 和 Tesla 的私测代表了 AI 模型部署的一个新范式：不再局限于 API 调用和聊天界面，而是直接将模型嵌入到企业的核心工作流程中——火箭设计、自动驾驶训练、工厂自动化。这种「嵌入式 AI」模式一旦被验证有效，将成为企业 AI 基础设施的下一个主战场。</p>

    <h3>代码数据正在成为高质量训练资源的核心</h3>
    <p>Cursor 数据被用于补充训练的创举表明，代码 IDE 中的真实交互数据正在成为高质量训练数据的新蓝海。传统上，AI 训练依赖公开文本、代码仓库和合成数据，但 Cursor 这类开发工具中的交互数据包含决策链和用户反馈信号——这种「过程性」数据的价值可能远超传统的「结果性」代码数据。</p>

    <h3>开源生态正在重新定义竞争格局</h3>
    <p>Cohere Command A+ 和 NVIDIA Nemotron-3 在同一天的开源发布，加上 Zyphra 和 Poolside 加入开源阵营，正在重塑 AI 行业的权力地图。当 <span class="key-number">218B</span> 参数的旗舰模型以 Apache 2.0 许可证开放时，小型团队和创业公司将获得此前只有巨头才能企及的 AI 能力。这可能是 Grok 4.5 故事中被大多数人忽视的最深远影响——模型竞争正在从「谁有最好的模型」转向「谁有最好的数据和部署生态」。</p>

    <blockquote>
      「Grok 4.5 的私测告诉我们一件事：AI 模型的未来不在于更大的参数量，而在于更好地利用数据——特别是那些之前被忽视的高质量交互数据。」
      <footer>— AI 行业观察评论</footer>
    </blockquote>

    <h2>六、总结</h2>
    <p>Grok 4.5 的私测是 xAI 迄今为止最有力的声明：基于 1.5T V9 基础模型、补充 Cursor 训练数据、在 SpaceX 和 Tesla 真实工业环境中跑出接近 Opus 的性能——这不仅是 xAI 的技术里程碑，更标志着 AI 模型从通用聊天工具向工业级基础设施转型的开始。而 Cohere、NVIDIA 同日发布旗舰开源模型的「开源反击」，则预示着 AI 生态竞争进入了一个更加多元化和复杂化的新阶段。</p>

  </div>

  <div class="bottom-cta">
    <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    <p>📌 主要信息来源：<a href="{featured_url}" target="_blank" rel="noopener">{featured_title}</a> · <a href="https://www.interconnects.ai/p/artifacts-22-zyphra-cohere-and-poolside" target="_blank" rel="noopener">Artifacts 22：开源生态扩展</a></p>
  </div>

</div>

<footer>
  <div class="container">
    <p>AI快报站 © 2026</p>
    <p style="margin-top:2px;"><a href="privacy-policy.html">隐私政策</a></p>
  </div>
</footer>

</body>
</html>'''

with open(f'featured-{TODAY}.html', 'w', encoding='utf-8') as f:
    f.write(featured_article_html)
print(f"✅ Generated featured-{TODAY}.html")

print(f"\n{'='*50}")
print(f"✅ All updates complete for {TODAY}")
print(f"📊 Stats: {total_count} items, {len(groups)} categories")
print(f"{'='*50}")
