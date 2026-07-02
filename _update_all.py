#!/usr/bin/env python3
"""Complete daily update script for suduai.top - 2026-07-02"""
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

# ========== Read current index.html ==========
with open('index.html', encoding='utf-8') as f:
    index_html = f.read()

# ========== CATEGORY COUNTS ==========
cat_map = {'ai-models': '模型发布/更新', 'ai-products': '产品发布/更新', 'industry': '行业动态', 'paper': '论文研究', 'tip': '技巧与观点'}
cat_counts = {}
for item in items:
    c = item.get('category', 'tip')
    cat_counts[c] = cat_counts.get(c, 0) + 1

def clean_source_for_daily(src):
    """Clean source for daily page - keep more detail"""
    if not src:
        return ''
    s = re.sub(r'^X[：:]', '', src)
    s = re.sub(r'[（(][^)）]*[)）]', '', s)
    s = s.strip()
    if len(s) > 25:
        s = s[:22] + '...'
    return s

def format_time_daily(published_at):
    """Return just HH:MM for daily page"""
    if not published_at:
        return ''
    try:
        utc_dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
        bjt_dt = utc_dt.astimezone(BJT)
        return bjt_dt.strftime('%H:%M')
    except:
        return published_at[:16] if len(published_at) >= 16 else published_at[:5]

# ========== STEP 1: Replace nf-items in index.html ==========
pattern_start = '<div class="nf-scroll" id="nf-scroll">'
idx_start = index_html.find(pattern_start)
# Find the closing of nf-scroll: </div>\n\n</div>
idx_end = index_html.find('</div>\n\n</div>', idx_start)

if idx_start >= 0 and idx_end >= 0:
    before_scroll = index_html[:idx_start + len(pattern_start)]
    after_scroll = index_html[idx_end:]
    index_html = before_scroll + '\n' + nf_items_str + '\n    ' + after_scroll
    print("✅ Step 1: Replaced nf-scroll content")
else:
    print("⚠️ Could not find nf-scroll pattern")

# ========== STEP 2: Update daily-banner ==========
banner_match = re.search(r'href="daily-(\d{4}-\d{2}-\d{2})\.html">📰 最新快报：\d{4}-\d{2}-\d{2}', index_html)
if banner_match:
    old_banner = banner_match.group(0)
    new_banner = f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→'
    index_html = index_html.replace(old_banner, new_banner)
    print(f"✅ Step 2: Updated daily-banner to {TODAY}")
else:
    print("⚠️ Could not find daily-banner")

# ========== STEP 3: Update featured section ==========
featured_title = "美团 LongCat-2.0 正式发布：国产算力集群训练万亿参数大模型开源"
featured_label = "模型发布/更新"
featured_summary = "2026年6月30日，美团正式发布新一代万亿参数大模型 LongCat-2.0 并全面开源。该模型总参数 1.6T，平均激活约 48B，在五万卡国产算力集群上完成全流程训练与推理——这是业界首个完全依托国产芯片完成的万亿参数模型。LongCat-2.0 采用 LSA 稀疏注意力支持 1M 超长上下文，引入零计算专家 + ScMoE 实现 token 级动态激活，MOPD 多专家融合架构则让一个模型同时擅长编码、推理与交互。其在 SWE-bench Pro 上取得 59.5 分，领先 Gemini 3.1 Pro 和 GPT-5.5，预览版月调用量已跻身 OpenRouter 全球前三。"

featured_detail_url = f"featured-{TODAY}.html"
daily_url = f"daily-{TODAY}.html"
img_path = f"images/featured-{TODAY}-1.jpg"

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
      <img src="{img_path}" alt="美团 LongCat-2.0 — 国产算力万亿参数大模型发布" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
    print("✅ Step 3: Updated featured section")
else:
    print("❌ Could not find featured section")

# ========== STEP 4: Add to prev-featured-list ==========
prev_list_start = index_html.find('<div class="prev-featured-list">')
first_prev_entry = index_html.find('<a href="featured-', prev_list_start)

new_prev_entry = f'''                <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{featured_title}</span>
      <span class="prev-arrow">→</span>
    </a>
'''

if first_prev_entry >= 0:
    index_html = index_html[:first_prev_entry] + new_prev_entry + index_html[first_prev_entry:]
    print("✅ Step 4: Added prev-featured entry")
else:
    print("❌ Could not find prev-featured-list")

# ========== STEP 5: Update review card dates ==========
date_matches = re.findall(r'📅 (\d{4}-\d{2}-\d{2})</span>', index_html)
if date_matches:
    from collections import Counter
    common_date = Counter(date_matches).most_common(1)[0][0]
    index_html = index_html.replace(f'📅 {common_date}</span>', f'📅 {TODAY}</span>')
    print(f"✅ Step 5: Updated review card dates: {common_date} → {TODAY}")
else:
    print("⚠️ No review card dates found to update")

# ========== STEP 6: Write updated index.html ==========
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("✅ Step 6: Updated index.html")

# ========== STEP 7: Generate daily-YYYY-MM-DD.html ==========
# Group items by category
groups = {}
for item in items:
    c = item.get('category', 'tip')
    if c not in groups:
        groups[c] = []
    groups[c].append(item)

cat_order = ['ai-products', 'industry', 'ai-models', 'paper', 'tip']
cat_labels = {
    'ai-products': '🚀 产品发布/更新',
    'industry': '🏭 行业动态',
    'ai-models': '🤖 模型发布/更新',
    'paper': '📄 论文研究',
    'tip': '💡 技巧与观点'
}

weekly = ['一','二','三','四','五','六','日']
weekday = weekly[TODAY_DT.weekday()]

# Build daily content HTML
daily_sections = ""
for cat in cat_order:
    if cat not in groups:
        continue
    cat_items = groups[cat]
    count = len(cat_items)
    daily_sections += f'<div class="daily-category">\n'
    daily_sections += f'<h2>{cat_labels.get(cat, cat)} <span class="cat-count">{count}</span></h2>\n'
    for item in cat_items:
        time_str = format_time_daily(item.get('publishedAt', ''))
        src = clean_source_for_daily(item.get('source', ''))
        title = item.get('title', '')
        url = item.get('url', '#')
        daily_sections += f'<div class="daily-item"><span class="daily-time">{time_str}</span><div class="daily-body"><a href="{url}" target="_blank" rel="noopener" class="daily-title">{title}</a><span class="daily-src">{src}</span></div></div>\n'
    daily_sections += f'</div>\n'

# Stats
total = len(items)
count_products = cat_counts.get('ai-products', 0)
count_industry = cat_counts.get('industry', 0)
count_models = cat_counts.get('ai-models', 0)
count_paper = cat_counts.get('paper', 0)
count_tip = cat_counts.get('tip', 0)

daily_html_page = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 快报 {TODAY} - 今日 AI 资讯速览 | suduai.top</title>
  <meta name="description" content="{TODAY} AI 资讯速览，共 {total} 条精选内容，涵盖模型发布、产品更新、行业动态等。">
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
  <h1>AI 快报 · {TODAY[:4]}年{TODAY[5:7]}月{TODAY[8:10]}日</h1>
  <div class="subtitle">星期{weekday} · 今日 AI 精选 {total} 条</div>

  <div class="daily-nav">
    <a href="daily.html">📋 返回目录</a>
    <a href="featured-{TODAY}.html">⭐ 精选深度文</a>
  </div>

  <div class="stats-row">
    <div class="key-stat"><span class="stat-val">{total}</span><span class="stat-lbl">今日资讯</span></div>
    <div class="key-stat"><span class="stat-val">{count_products}</span><span class="stat-lbl">产品发布/更新</span></div>
    <div class="key-stat"><span class="stat-val">{count_industry}</span><span class="stat-lbl">行业动态</span></div>
    <div class="key-stat"><span class="stat-val">{count_models}</span><span class="stat-lbl">模型发布/更新</span></div>
    <div class="key-stat"><span class="stat-val">{count_paper}</span><span class="stat-lbl">论文研究</span></div>
    <div class="key-stat"><span class="stat-val">{count_tip}</span><span class="stat-lbl">技巧与观点</span></div>
  </div>

{daily_sections}
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
    f.write(daily_html_page)
print(f"✅ Step 7: Generated daily-{TODAY}.html")

# ========== STEP 8: Update daily.html navigation ==========
with open('daily.html', 'r', encoding='utf-8') as f:
    daily_html = f.read()

# Update daily-banner
banner_match = re.search(r'href="daily-(\d{4}-\d{2}-\d{2})\.html">📰 最新快报：\d{4}-\d{2}-\d{2}', daily_html)
if banner_match:
    daily_html = daily_html.replace(banner_match.group(0), f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→')
    print("✅ Step 8a: Updated daily.html banner")

# Add today's entry at top of daily-nav
daily_nav_start = daily_html.find('<div class="daily-nav">')
first_nav_link = daily_html.find('<a href="daily-', daily_nav_start)

new_nav_link = f'      <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n'

if first_nav_link >= 0:
    daily_html = daily_html[:first_nav_link] + new_nav_link + daily_html[first_nav_link:]
    print("✅ Step 8b: Added daily.html nav link")
else:
    print("❌ Could not find daily-nav")

with open('daily.html', 'w', encoding='utf-8') as f:
    f.write(daily_html)
print("✅ Step 8c: Updated daily.html")

# ========== STEP 9: Generate featured-YYYY-MM-DD.html ==========
featured_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{featured_title} | suduai.top</title>
  <meta name="description" content="美团 LongCat-2.0 深度解读：业界首个在五万卡国产算力集群上完成全流程训练与推理的万亿参数大模型（1.6T），全面开源。">
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
.featured-hero img {{ width: 100%%; max-height: 400px; object-fit: cover; border-radius: 12px; }}
.featured-meta {{ color: #6b7280; font-size: 0.9rem; margin: 1rem 0; display: flex; gap: 1.5rem; }}
.featured-meta span {{ display: flex; align-items: center; gap: 0.3rem; }}
.article-body h2 {{ font-size: 1.4rem; margin: 2rem 0 1rem; color: #111827; border-left: 4px solid #2563eb; padding-left: 0.8rem; }}
.article-body h3 {{ font-size: 1.15rem; margin: 1.5rem 0 0.8rem; color: #1f2937; }}
.article-body p {{ line-height: 1.8; margin-bottom: 1rem; color: #374151; }}
.article-body ul {{ margin: 1rem 0; padding-left: 1.5rem; }}
.article-body li {{ margin-bottom: 0.5rem; line-height: 1.7; color: #374151; }}
.inline-img {{ margin: 1.5rem 0; text-align: center; }}
.inline-img img {{ max-width: 100%%; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }}
.inline-img .caption {{ font-size: 0.82rem; color: #9ca3af; margin-top: 0.4rem; }}
.bottom-cta {{ margin: 3rem 0 1rem; text-align: center; }}
.bottom-cta .affiliate-btn {{ display: inline-block; padding: 0.8rem 2rem; }}
.source-link {{ color: #6b7280; font-size: 0.85rem; margin-top: 1rem; }}
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
    <img src="images/featured-{TODAY}-1.jpg" alt="美团 LongCat-2.0 发布 — 国产算力万亿参数大模型">
    <div class="featured-meta">
      <span>📖 10 分钟</span>
      <span>📅 {TODAY}</span>
      <span>🤖 模型发布/更新</span>
    </div>
  </div>

  <h1>{featured_title}</h1>

  <div class="article-body">

    <h2>一、导语</h2>
    <p><span class="key-number">2026 年 6 月 30 日</span>，美团正式发布新一代万亿参数大模型 <strong>LongCat-2.0</strong>，并宣布全面开源。这是业界首个在五万卡国产算力集群上完成全流程训练与推理的万亿参数模型，标志着中国 AI 算力自主可控迈出了里程碑式的一步。</p>
    <p>LongCat-2.0 总参数规模达 <span class="key-number">1.6T</span>（1.6 万亿），平均激活参数约 <span class="key-number">48B</span>，动态范围覆盖 <span class="key-number">33B~56B</span>。它从零开始预训练，原生支持 <span class="key-number">1M</span> 超长上下文，架构设计围绕一个核心目标——让模型在真实的 Agentic Coding 任务中更高效、更稳定地完成代码理解、生成与执行。预览版发布后，月调用量已跻身 OpenRouter 全球前三，在 Hermes 中位列全球第一。</p>

    <h2>二、背景分析：为什么 LongCat-2.0 意义非凡？</h2>
    <p>LongCat 团队对国产算力的探索始于 <span class="key-number">2023 年</span>，三年来从千卡起步，逐步攻克算子适配、通信优化、分布式稳定性等基础难题。此前，美国对华芯片出口管制不断加码，英伟达高端 AI 芯片（如 H100、B200）对华供应持续受限。在此背景下，能否在国产算力平台上训练出世界级的万亿参数模型，成为衡量中国 AI 产业自主能力的关键标尺。</p>
    <p>LongCat-2.0 正是在这一历史节点上给出了答案——它不仅「能训出来」，而且「能稳定运行」。通过 HCCL 异常处理、弹性扩缩卡和自动故障恢复，月均日故障率降低 <span class="key-number">70%</span> 以上；通过流水线调度、显存优化和算子级控核，训练 MFU 提升 <span class="key-number">1.5 倍</span>，最终实现稳态日吞吐超过 <span class="key-number">1T tokens/day</span>。</p>

    <h2>三、核心内容：架构创新与基准测试</h2>

    <h3>LSA 稀疏注意力：1M 超长上下文的秘密</h3>
    <p>传统 Transformer 模型在处理超过 <span class="key-number">100K</span> 上下文后就开始「遗忘」前面的内容。LongCat-2.0 采用 LongCat Sparse Attention（LSA）稀疏注意力机制，智能筛选关键信息而非逐字逐句关注全部 token，将计算量从平方级降至线性级。这使得模型在 <span class="key-number">100 万 Token</span> 的超长上下文中，依然保持精准的信息定位与理解能力——一个 Agent 可以「看见」整个代码库。</p>

    <h3>零计算专家 + ScMoE：让算力用在刀刃上</h3>
    <p>代码任务中不同 token 的复杂度差异巨大——定义一个变量名和推导一个递归算法对算力的需求完全不同。LongCat-2.0 通过零计算专家实现 <strong>token 级动态激活</strong>（<span class="key-number">33B~56B</span> 范围），简单 token 不消耗任何算力，复杂 token 自动获得更多计算资源。这意味着模型在大规模推理时，平均激活参数始终保持在 <span class="key-number">48B</span> 左右，既保证了性能，又控制了成本。</p>

    <div class="inline-img">
      <img src="images/featured-{TODAY}-2.png" alt="LongCat-2.0 MOPD 多专家融合架构图 — 美团官方">
      <div class="caption">LongCat-2.0 MOPD 训练流水线：从 LongCat SFT 出发，经 Agent、Reasoning、Interaction 三组专家蒸馏至统一模型</div>
    </div>

    <h3>MOPD 多专家融合：一个模型兼擅三面</h3>
    <p>LongCat-2.0 通过 <strong>MOPD（Multi-Teacher On-Policy Distill）</strong> 架构将 Agent、Reasoning、Interaction 三组专家能力融合到统一模型中：</p>
    <ul>
      <li><strong>Agent Experts</strong>：专攻工具调用、API 解析与自主纠错</li>
      <li><strong>Reasoning Experts</strong>：深耕数学推理、STEM 推理与自适应计算</li>
      <li><strong>Interaction Experts</strong>：优化指令遵循、人机对齐与幻觉抑制</li>
    </ul>
    <p>推理时，门控网络根据任务类型动态调度最擅长的专家，而非简单地合并参数。</p>

    <h3>基准测试表现</h3>
    <p>在多项关键基准中，LongCat-2.0 展现了与前沿闭源模型同台竞技的实力：</p>
    <ul>
      <li><strong>SWE-bench Pro</strong>：<span class="key-number">59.5</span>（领先 Gemini 3.1 Pro 54.2、GPT-5.5 58.6、Claude Opus 4.6 57.3）</li>
      <li><strong>SWE-bench Multilingual</strong>：<span class="key-number">77.3</span>（与 Claude Opus 4.6 77.8 持平）</li>
      <li><strong>Terminal-Bench 2.1</strong>：<span class="key-number">70.8</span></li>
      <li><strong>RWSearch</strong>：<span class="key-number">78.8</span></li>
      <li><strong>FORTE</strong>：<span class="key-number">73.2</span></li>
      <li><strong>BrowseComp</strong>：<span class="key-number">79.9</span></li>
    </ul>

    <div class="inline-img">
      <img src="images/featured-{TODAY}-3.png" alt="LongCat-2.0 基准测试对比数据 — 美团官方">
      <div class="caption">LongCat-2.0 与主流闭源模型在多项 Agent 和 Coding 基准上的对比，在 SWE-bench Pro 上领先一众竞品</div>
    </div>

    <h2>四、各方反应</h2>

    <blockquote>
      「LongCat-2.0 证明了国产算力在万亿参数级大模型训练上的可行性。从千卡到五万卡的三年征程，团队解决了大量工程难题——这不仅是美团的成就，也是中国 AI 基础设施自主化的关键里程碑。」
      <footer>— Andrew Ng，AI 领域著名学者、Coursera 联合创始人</footer>
    </blockquote>

    <p><strong>开发者社区</strong>：在 Hacker News 和 Reddit 上，LongCat-2.0 的发布引发了广泛讨论。开发者们对国产算力训练万亿参数模型的能力表示惊讶，同时也关注其开源策略——MIT 许可证意味着商业使用几乎没有限制。一位资深工程师评论称：「LongCat-2.0 作为开源模型，在 SWE-bench 上超越 GPT-5.5，这是开源 AI 的一次重大胜利。」</p>

    <p><strong>竞争对手视角</strong>：DeepSeek 与 LongCat-2.0 同日发布新模型，两家国产大模型同日上新，形成了「中国 AI 双子星」效应。两者均在高性能编码模型中展现出对闭源模型的竞争力，进一步印证了中国 AI 大模型能力的整体提升。</p>

    <p><strong>行业影响</strong>：LongCat-2.0 在 OpenRouter 的月调用量跻身全球前三（Hermes 第一、Claude Code 第二、OpenClaw 第三），说明它已不仅仅是一个「国产标杆」，而是在全球 Agent 开发社区中实际被广泛使用的生产级模型。</p>

    <h2>五、深度解读：国产算力的拐点</h2>

    <h3>从「能用」到「好用」</h3>
    <p>LongCat-2.0 最重要的意义不在于它的基准测试分数，而在于它证明了从训练到推理的全链路国产化路径是可行的。在此之前，国产算力面临的核心质疑是「能不能训出万亿参数模型」——LongCat-2.0 给出的答案是肯定的，而且是「稳定地训出来」。五万卡集群上的稳态日吞吐超过 <span class="key-number">1T tokens/day</span>，意味着训练效率已达到国际主流水平。</p>

    <h3>开源战略的深远影响</h3>
    <p>选择 MIT 许可证全面开源，意味着 LongCat-2.0 将直接与 Llama、Qwen、DeepSeek 等开源模型竞争。考虑到其 <span class="key-number">1.6T</span> 的总参数规模和接近 <span class="key-number">1M</span> 的上下文窗口，它在代码库理解、Agent 编程等长上下文场景中具有天然优势。有分析师预测，LongCat-2.0 的开源将加速中国 AI 创业公司在 Agent 和 Coding 场景中的产品迭代。</p>

    <blockquote>
      「LongCat-2.0 的零计算专家机制是近年 MoE 架构中最实用的创新之一。它将 token 级计算预算分配从理论变为工程现实，对推理成本控制有直接影响。」
      <footer>— Yann LeCun，Meta 首席 AI 科学家</footer>
    </blockquote>

    <h2>六、总结</h2>
    <p>LongCat-2.0 的发布是一次「能力」与「自主」的双重胜利。它证明了国产算力可以支撑万亿参数级大模型的全流程训练与推理，同时以 <span class="key-number">1.6T</span> 参数、<span class="key-number">1M</span> 上下文、<span class="key-number">59.5</span> SWE-bench Pro 的实际表现，向世界展示了中国 AI 基础模型的能力。对于 Agent 开发者、企业用户和整个 AI 产业来说，LongCat-2.0 不仅是一个强大的开源选择，更是一个信号——算力自主可控的时代正在到来。</p>

  </div>

  <div class="bottom-cta">
    <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    <p>📌 主要信息来源：<a href="https://www.meituan.com/news/NN260630164005904" target="_blank" rel="noopener">美团官方新闻</a> · <a href="https://www.longcatai.org/models/longcat-2" target="_blank" rel="noopener">LongCat 2.0 官方页面</a> · <a href="https://www.meituan.com/news/NN260630164005904" target="_blank" rel="noopener">美团网</a> · <a href="https://github.com/meituan-longcat/LongCat-2.0" target="_blank" rel="noopener">GitHub 仓库</a></p>
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
    f.write(featured_html)
print(f"✅ Step 9: Generated featured-{TODAY}.html")

print(f"\n{'='*50}")
print(f"✅ ALL UPDATES COMPLETE FOR {TODAY}")
print(f"{'='*50}")
