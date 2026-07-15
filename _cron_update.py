#!/usr/bin/env python3
"""Cron update script: generate daily, featured, update index.html and daily.html"""
import json, re, os
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
NOW = datetime.now(BJT)

with open('aihot_selected.json', encoding='utf-8') as f:
    data = json.load(f)
items = data['items']

CAT_MAP_ATTR = {'ai-models':'ai-models','ai-products':'ai-products','industry':'industry','paper':'paper','tip':'tip'}
CATEGORY_LABELS = {
    'ai-models': ('模型发布/更新', '🤖'),
    'ai-products': ('产品发布/更新', '🚀'),
    'industry': ('行业动态', '🏭'),
    'paper': ('论文研究', '📄'),
    'tip': ('技巧与观点', '💡'),
}
CATEGORY_ORDER = ['ai-products', 'industry', 'ai-models', 'paper', 'tip']
WEEKDAY_CN = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
WEEKDAY = WEEKDAY_CN[NOW.weekday()]

def fmt_time(iso_str):
    if not iso_str: return ''
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z','+00:00')).astimezone(BJT)
        d = dt.date()
        today = NOW.date()
        if d == today: return f"今天 {dt.strftime('%H:%M')}"
        if (today - d).days == 1: return f"昨天 {dt.strftime('%H:%M')}"
        return dt.strftime('%m/%d %H:%M')
    except: return iso_str[:16]

def clean_source(src):
    if not src: return ''
    s = re.sub(r'^[Xx][：:]', '', src)
    s = re.sub(r'[（(][^)）]*[)）]', '', s).strip()
    if len(s) > 18: s = s[:15] + '...'
    return s

def clean_src_daily(src):
    if not src: return ''
    return re.sub(r'^[Xx][：:]', '', src).strip()

def esc(t):
    return t.replace('"','&quot;').replace("'",'&#39;')

# ── 1. Generate nf-items HTML ──
nf_lines = []
for it in items:
    cat = CAT_MAP_ATTR.get(it.get('category',''), 'tip')
    title = esc(it.get('title',''))
    url = esc(it.get('url','#'))
    ts = fmt_time(it.get('publishedAt',''))
    src = clean_source(it.get('source',''))
    nf_lines.append(f'''      <a href="{url}" target="_blank" rel="noopener" class="nf-item" data-category="{cat}">
        <span class="nf-time">{ts}</span>
        <span class="nf-title">{title}</span>
        <span class="nf-src">{src}</span>
      </a>''')
nf_html = '\n'.join(nf_lines)
print(f"✅ {len(nf_lines)} nf-items")

# ── 2. Generate daily-YYYY-MM-DD.html ──
cat_groups = {}
for it in items:
    cat_groups.setdefault(it.get('category','uncategorized'), []).append(it)
cat_counts = {c: len(v) for c,v in cat_groups.items()}

daily_sections = []
for cat in CATEGORY_ORDER:
    if cat not in cat_groups: continue
    its = cat_groups[cat]
    label, icon = CATEGORY_LABELS.get(cat, (cat,''))
    items_html = []
    for it in its:
        t = datetime.fromisoformat(it.get('publishedAt','').replace('Z','+00:00')).astimezone(BJT).strftime('%H:%M')
        title = esc(it.get('title',''))
        url = esc(it.get('url','#'))
        src = clean_src_daily(it.get('source',''))
        items_html.append(f'<div class="daily-item"><span class="daily-time">{t}</span><div class="daily-body"><a href="{url}" target="_blank" rel="noopener" class="daily-title">{title}</a><span class="daily-src">{src}</span></div></div>')
    daily_sections.append(f'''<div class="daily-category">
<h2>{icon} {label} <span class="cat-count">{len(its)}</span></h2>
{chr(10).join(items_html)}
</div>''')

stats_lines = []
for cat in CATEGORY_ORDER:
    if cat in cat_counts:
        lbl, _ = CATEGORY_LABELS.get(cat, (cat,''))
        stats_lines.append(f'    <div class="key-stat"><span class="stat-val">{cat_counts[cat]}</span><span class="stat-lbl">{lbl}</span></div>')

daily_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 快报 {TODAY} - 今日 AI 资讯速览 | suduai.top</title>
  <meta name="description" content="{TODAY} AI 资讯速览，共 50 条精选内容，涵盖模型发布、产品更新、行业动态等。">
  <link rel="stylesheet" href="css/style.css">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="favicon.png">
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
  <div class="subtitle">{WEEKDAY} · 今日 AI 精选 50 条</div>

  <div class="daily-nav">
    <a href="daily.html">📋 返回目录</a>
    <a href="featured-{TODAY}.html">⭐ 精选深度文</a>
  </div>

  <div class="stats-row">
    <div class="key-stat"><span class="stat-val">50</span><span class="stat-lbl">今日资讯</span></div>
{chr(10).join(stats_lines)}
  </div>

{chr(10).join(daily_sections)}

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
    f.write(daily_html)
print(f"✅ daily-{TODAY}.html ({len(daily_html)} chars)")

# ── 3. Update index.html ──
with open('index.html', encoding='utf-8') as f:
    idx = f.read()

# 3a. daily-banner
idx = re.sub(
    r'<div class="daily-banner">\s*<a href="daily-\d{4}-\d{2}-\d{2}\.html">📰 最新快报：[^<]+→</a>\s*</div>',
    f'<div class="daily-banner">\n  <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    idx
)

# 3b. nf-items
idx = re.sub(
    r'<div class="nf-scroll"[^>]*>.*?</div>',
    f'        <div class="nf-scroll" id="nf-scroll">\n{nf_html}\n    </div>',
    idx, flags=re.DOTALL
)

# 3c. review card dates
idx = re.sub(r'<span>📅 \d{4}-\d{2}-\d{2}</span>', f'<span>📅 {TODAY}</span>', idx)

# 3d. featured card
featured_title = 'Qwen-Audio-3.0-Realtime：阿里通义语音 AI 登顶全球，超越 OpenAI GPT-Realtime-2'
featured_desc = '阿里通义实验室发布 Qwen-Audio-3.0-Realtime 实时语音交互模型，在 Artificial Analysis 的 Speech Reasoning 子项中综合排名第一，超越 OpenAI GPT-Realtime-2。该模型采用 Thinker-Talker 架构，端到端延迟约 300ms，语音识别支持 113 种语言，价格仅为 GPT-Realtime-2 的 30-40%。这是中国 AI 模型首次在语音推理这一关键赛道登顶全球。'

featured_block = f'''                                                                <div class="featured-card">
    <div class="featured-badge">模型发布</div>
    <div class="featured-content">
      <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="{featured_title}" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
      <div class="featured-label">模型发布/更新</div>
      <h2><a href="featured-{TODAY}.html">{featured_title}</a></h2>
      <p>{featured_desc}</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 {TODAY}</span><span>模型发布</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
  </div>'''

idx = re.sub(
    r'<div class="featured-card">.*?</div>\s*</div>',
    featured_block,
    idx, flags=re.DOTALL
)

# 3e. prev-featured-list - insert at top
new_prev = f'''                                                            <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{featured_title}</span>
      <span class="prev-arrow">→</span>
    </a>'''

idx = idx.replace(
    '  <div class="prev-featured-list">\n',
    f'  <div class="prev-featured-list">\n\n{new_prev}\n'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print("✅ index.html updated")

# ── 4. Update daily.html ──
with open('daily.html', encoding='utf-8') as f:
    daily_idx = f.read()

daily_idx = re.sub(
    r'<a href="daily-\d{4}-\d{2}-\d{2}\.html">📰 最新快报：[^<]+→</a>',
    f'<a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>',
    daily_idx
)

daily_link = f'    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报 🔥</a>'
daily_idx = daily_idx.replace(
    '  <div class="daily-nav">\n',
    f'  <div class="daily-nav">\n{daily_link}\n'
)

with open('daily.html', 'w', encoding='utf-8') as f:
    f.write(daily_idx)
print("✅ daily.html updated")
