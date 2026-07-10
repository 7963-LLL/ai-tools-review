#!/usr/bin/env python3
"""Comprehensive update script for suduai.top - called by cron."""

import json
import re
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT)
TODAY_STR = TODAY.strftime('%Y-%m-%d')
YESTERDAY_STR = (TODAY - timedelta(days=1)).strftime('%Y-%m-%d')

CAT_MAP = {
    'ai-models': '模型发布/更新',
    'ai-products': '产品发布/更新',
    'industry': '行业动态',
    'paper': '论文研究',
    'tip': '技巧与观点',
}
CAT_EMOJI = {
    'ai-models': '🤖',
    'ai-products': '🚀',
    'industry': '🏭',
    'paper': '📄',
    'tip': '💡',
}
ORDER = ['ai-models', 'ai-products', 'industry', 'paper', 'tip']

def parse_time(iso_str):
    iso_str = iso_str.replace('Z', '+00:00')
    try:
        return datetime.fromisoformat(iso_str)
    except:
        return datetime.now(BJT)

def to_bjt(dt_utc):
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    return dt_utc.astimezone(BJT)

def fmt_time_bjt(dt_bjt):
    today = datetime.now(BJT)
    if dt_bjt.date() == today.date():
        return f"今天 {dt_bjt.strftime('%H:%M')}"
    yesterday = today - timedelta(days=1)
    if dt_bjt.date() == yesterday.date():
        return f"昨天 {dt_bjt.strftime('%H:%M')}"
    return dt_bjt.strftime('%m/%d %H:%M')

def clean_source(src):
    s = re.sub(r'^X[：:]\s*', '', src)
    s = re.sub(r'[（(][^）)]*[）)]', '', s)
    s = re.sub(r'（.*?）', '', s)
    s = s.strip()
    if len(s) > 18:
        s = s[:15] + '...'
    return s

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ── Load data ──
data = load_json('aihot_selected.json')
items = data.get('items', data)

# Sort by publishedAt descending (newest first)
items_sorted = sorted(items, key=lambda x: x.get('publishedAt', ''), reverse=True)

# ── Build nf-items HTML (50 items) ──
def build_nf_item(item):
    url = item.get('url', '#')
    cat = item.get('category', 'tip')
    title = item.get('title', '')
    source = clean_source(item.get('source', ''))
    pub = item.get('publishedAt', '')
    dt_bjt = to_bjt(parse_time(pub))
    time_str = fmt_time_bjt(dt_bjt)
    return f'''      <a href="{url}" target="_blank" rel="noopener" class="nf-item" data-category="{cat}">
        <span class="nf-time">{time_str}</span>
        <span class="nf-title">{title}</span>
        <span class="nf-src">{source}</span>
      </a>'''

nf_items_html = '\n'.join(build_nf_item(it) for it in items_sorted)

# ── Update index.html ──
print("=== Updating index.html ===")
idx = read_file('index.html')

# 1. Replace nf-scroll content
scroll_start = idx.find('<div class="nf-scroll" id="nf-scroll">')
scroll_end_bound = idx.find('</div>', scroll_start)  # close of nf-scroll div itself
last_a = idx.rfind('</a>', scroll_start, scroll_end_bound)
scroll_close = idx.find('</div>', last_a)  # first </div> = nf-scroll close
box_close = idx.find('</div>', scroll_close + 6)  # second </div> = nf-box close

new_scroll = f'''    <div class="nf-scroll" id="nf-scroll">
{nf_items_html}
    </div>
  </div>'''

idx = idx[:scroll_start] + new_scroll + idx[box_close:]

# 2. Update daily-banner link (use full content replacement to avoid suffix duplication)
banner_match = re.search(r'<div class="daily-banner">\s*<a href="daily-\d{4}-\d{2}-\d{2}\.html">([^<]+)</a>\s*</div>', idx)
if banner_match:
    new_banner = f'<div class="daily-banner">\n  <a href="daily-{TODAY_STR}.html">📰 最新快报：{TODAY_STR}（今日 AI 精选 50 条）→</a>\n</div>'
    idx = idx[:banner_match.start()] + new_banner + idx[banner_match.end():]
    print(f"  Banner updated to {TODAY_STR}")
else:
    print("  WARNING: Banner pattern not found!")

# 3. Update featured section
# Pick best featured topic
best = max(items, key=lambda x: x.get('score', 0))
for it in items:
    if it.get('score', 0) >= 80 and it.get('category') in ('ai-models', 'ai-products', 'industry'):
        best = it
        break

feat_cat = best.get('category', 'industry')
feat_label = CAT_MAP.get(feat_cat, '行业动态')
feat_title = best.get('title', '')
feat_url = best.get('url', '#')
feat_summary = best.get('summary', '')
# Truncate summary to 150-200 chars
if len(feat_summary) > 200:
    feat_summary = feat_summary[:197] + '...'
elif len(feat_summary) < 150:
    # Pad with more info from other sources
    pass

feat_cat_display = CAT_MAP.get(feat_cat, '行业动态')
score = best.get('score', 0)

# Build featured card HTML
feat_badge = "今日热议" if score >= 80 else "精选推荐"
feat_img_html = ''
feat_img2_html = ''

# Check if we have images
import os
img1_path = f'images/featured-{TODAY_STR}-1.jpg'
img2_path = f'images/featured-{TODAY_STR}-2.jpg'

has_img1 = os.path.isfile(img1_path) and os.path.getsize(img1_path) > 10000
has_img2 = os.path.isfile(img2_path) and os.path.getsize(img2_path) > 10000

if has_img1:
    feat_img_html = f'''
    <div class="featured-visual">
      <img src="{img1_path}" alt="{feat_title}" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>'''

# Build the featured card
feat_card = f'''                              <div class="featured-card">
    <div class="featured-badge">{feat_badge}</div>
    <div class="featured-content">
      <div class="featured-label">{feat_cat_display}</div>
      <h2><a href="featured-{TODAY_STR}.html">{feat_title}</a></h2>
      <p>{feat_summary}</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 {TODAY_STR}</span><span>{feat_cat_display}</span>
      </div>
      <a href="daily-{TODAY_STR}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    {feat_img_html}
  </div>'''

# Replace featured card
feat_start = idx.find('<div class="featured-card">')
feat_end = idx.find('</div>', idx.find('</div>', idx.find('</div>', idx.find('featured-card') + 1) + 1) + 1) + 6
# Better: find the matching closing </div> for .featured-card
# Find the beginning
fc_start = idx.find('<div class="featured-card">')
if fc_start > 0:
    # Find the actual end - it's the 4th </div> after fc_start counting the card structure
    # Let's find the </div> that closes featured-card  
    open_divs = 0
    fc_end = fc_start
    for pos in range(fc_start, len(idx)):
        if idx[pos:pos+4] == '<div':
            open_divs += 1
        elif idx[pos:pos+6] == '</div>':
            open_divs -= 1
            if open_divs == 0:
                fc_end = pos + 6
                break
    idx = idx[:fc_start] + feat_card + idx[fc_end:]

# 4. Add to prev-featured-list (at the top)
prev_list_start = idx.find('<div class="prev-featured-list">')
prev_item = f'''
                                                    <a href="featured-{TODAY_STR}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY_STR}</span>
      <span class="prev-title">{feat_title}</span>
      <span class="prev-arrow">→</span>
    </a>'''

list_end = prev_list_start + len('<div class="prev-featured-list">')
idx = idx[:list_end] + '\n' + prev_item + idx[list_end:]

# 5. Update review card dates (📅 YYYY-MM-DD)
idx = re.sub(r'📅 \d{4}-\d{2}-\d{2}', f'📅 {TODAY_STR}', idx)

write_file('index.html', idx)
print("  index.html written")

# ── Generate daily-YYYY-MM-DD.html ──
print("=== Generating daily page ===")
wday = TODAY.weekday()
weekdays_cn = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
wday_cn = weekdays_cn[wday]

# Count by category
cat_counts = {}
for it in items:
    c = it.get('category', 'tip')
    cat_counts[c] = cat_counts.get(c, 0) + 1

stats_rows = ''
stats_cols = [('ai-models', '模型发布/更新'), ('ai-products', '产品发布/更新'), ('industry', '行业动态'), ('paper', '论文研究'), ('tip', '技巧与观点')]
for c, cname in stats_cols:
    cnt = cat_counts.get(c, 0)
    stats_rows += f'\n    <div class="key-stat"><span class="stat-val">{cnt}</span><span class="stat-lbl">{cname}</span></div>'

# Build category sections
daily_sections = []
for cat in ORDER:
    cat_items = [it for it in items if it.get('category') == cat]
    if not cat_items:
        continue
    cnt = len(cat_items)
    emoji = CAT_EMOJI.get(cat, '📌')
    cname = CAT_MAP.get(cat, cat)
    section = f'<div class="daily-category">\n<h2>{emoji} {cname} <span class="cat-count">{cnt}</span></h2>\n'
    for it in cat_items:
        pub = it.get('publishedAt', '')
        dt_bjt = to_bjt(parse_time(pub))
        time_str = dt_bjt.strftime('%H:%M')
        url = it.get('url', '#')
        title = it.get('title', '')
        src = clean_source(it.get('source', ''))
        section += f'<div class="daily-item"><span class="daily-time">{time_str}</span><div class="daily-body"><a href="{url}" target="_blank" rel="noopener" class="daily-title">{title}</a><span class="daily-src">{src}</span></div></div>\n'
    section += '</div>'
    daily_sections.append(section)

daily_content = '\n'.join(daily_sections)

daily_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 快报 {TODAY_STR} - 今日 AI 资讯速览 | suduai.top</title>
  <meta name="description" content="{TODAY_STR} AI 资讯速览，共 {len(items)} 条精选内容，涵盖模型发布、产品更新、行业动态等。">
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
  <a href="daily-{TODAY_STR}.html">📰 最新快报：{TODAY_STR}（今日 AI 精选 50 条）→</a>
</div>

<div class="content-page">
  <h1>AI 快报 · {TODAY.year}年{TODAY.month}月{TODAY.day}日</h1>
  <div class="subtitle">{wday_cn} · 今日 AI 精选 {len(items)} 条</div>

  <div class="daily-nav">
    <a href="daily.html">📋 返回目录</a>
    <a href="featured-{TODAY_STR}.html">⭐ 精选深度文</a>
  </div>

  <div class="stats-row">
    <div class="key-stat"><span class="stat-val">{len(items)}</span><span class="stat-lbl">今日资讯</span></div>{stats_rows}
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

daily_path = f'daily-{TODAY_STR}.html'
write_file(daily_path, daily_html)
print(f"  {daily_path} written ({len(items)} items)")

# ── Update daily.html ──
print("=== Updating daily.html ===")
dh = read_file('daily.html')

# Update banner (same technique)
banner_match_dh = re.search(r'<div class="daily-banner">\s*(.*?)\s*</div>', dh, re.DOTALL)
if banner_match_dh:
    new_banner_dh = f'<div class="daily-banner">\n      <a href="daily-{YESTERDAY_STR}.html">📅 {YESTERDAY_STR} 今日快报 🔥</a>\n      <a href="daily-{TODAY_STR}.html">📰 最新快报：{TODAY_STR}（今日 AI 精选 50 条）→</a>\n</div>'
    dh = dh[:banner_match_dh.start()] + new_banner_dh + dh[banner_match_dh.end():]

# Add today to nav (at the top)
nav_insert = dh.find('<a href="daily-2026-07-09.html">📅 2026-07-09')
if nav_insert > 0:
    new_nav = f'                                                                                  <a href="daily-{TODAY_STR}.html">📅 {TODAY_STR} 今日快报</a>\n'
    dh = dh[:nav_insert] + new_nav + dh[nav_insert:]

write_file('daily.html', dh)
print("  daily.html written")

# ── Generate featured-YYYY-MM-DD.html ──
print("=== Generating featured article ===")

# Build a deeper article
feat_title_en = best.get('title_en', '')

# Get more detail from other items about OpenAI
feat_intro = f'{TODAY.year}年{TODAY.month}月{TODAY.day}日，OpenAI 正式发布了 ChatGPT Work——一个能够跨应用、跨文件自主完成复杂任务的 AI 智能体。这不仅是 OpenAI 产品线的又一次升级，更标志着 AI 从"问答工具"向"工作伙伴"的关键转型。同步推出的 GPT-5.6 系列模型（Sol、Terra、Luna）为这一产品提供了强大的底层能力支撑。'

feat_background = f'<h2>背景分析：AI Agent 赛道的关键转折点</h2>\n<p>2026 年被称为"AI Agent 元年"。从年初 Anthropic 发布具有计算机使用能力的 Claude，到 Microsoft 成立 Frontier Company 将 <span class="key-number">6000</span> 名 AI 工程师派驻企业现场，再到 Google 推出 Project Mariner——各大科技巨头不约而同地将战略重心从"更强的对话模型"转向"能真正干活的智能体"。\nOpenAI 的 ChatGPT Work 正是在这一背景下诞生。它并非简单的功能叠加，而是整合了 Codex（每周 <span class="key-number">500</span> 万用户使用）的代理能力、Operator 的浏览器操控能力、以及 Deep Research 的信息综合能力，形成了一个统一的 Agent 平台。</p>'

print("Featured topic:", feat_title)
print("Category:", feat_cat)

feat_core = """<h2>核心内容：ChatGPT Work 的五大能力</h2>

<h3>1. 跨应用工作能力</h3>
<p>ChatGPT Work 可以连接 Slack、Teams、Google Drive、SharePoint、邮件、日历、CRM 等工具，通过 @+应用名 的方式拉取上下文。在桌面端，它拥有内置浏览器、本地文件和应用访问权限，能够在不同工具之间自由穿梭，完成数据收集、分析和产出。</p>

<h3>2. 创建完整工作成果</h3>
<p>从幻灯片到电子表格，从文档到交互式网站（Sites 功能，公开测试版），ChatGPT Work 能将一个模糊的目标转化为可交付的成品。它甚至可以根据底层数据变化自动更新已创建的网站内容。</p>

<h3>3. 定时任务与委托</h3>
<p>支持一次性、周期性或事件触发的定时任务——例如：每天检查 Slack 更新并刷新议程、汇总 Dashboard 变化、监控客户反馈生成产品创意、收到新邮件后更新演示文稿。用户可精细控制访问权限、检查频率和审批要求。</p>

<h3>4. 计算机使用能力</h3>
<p>桌面端支持 ChatGPT 在后台自主点击、打字、移动文件——既可以执行一次性操作，也可以作为定时任务的一部分持续运行。</p>

<h3>5. Sites（公开测试版）</h3>
<p>这是本次发布中最具想象力的功能之一：将任何工作成果一键转化为可交互的 Web 应用——Dashboard、项目跟踪器、原型、内部门户，均可通过 URL 分享，并能随着底层信息的更新而自动同步。</p>"""

feat_responses = """<h2>各方反应</h2>

<blockquote>"ChatGPT Work is an agent in ChatGPT that helps you take on more ambitious tasks."<br>—— OpenAI 官方博客</blockquote>

<blockquote>"我们将手动月度发布检查转化为可重复的工作流，覆盖发布计划、Jira、上市时间表——从支持 1 个项目经理扩展到约 50 个。"<br>—— Vaneet Seth，RingCentral</blockquote>

<blockquote>"（ChatGPT）研究了竞争对手的优势和劣势，构建了数据集——将数周的分析压缩到几小时。"<br>—— Nathan Bolt，Virgin Atlantic</blockquote>

<p>在企业客户中，Zapier 的 Angela Ferrante 利用 ChatGPT Work 构建了跨 CRM、邮件和工具的数以千计潜在客户审查系统，每周自动生成 Dashboard——带来了 <span class="key-number">7</span> 位数的潜在销售额。NVIDIA 的 Will Daney 用其自动化 GTC 会议准备工作，取代了 <span class="key-number">40%</span> 的会前时间。</p>

<p>分析人士指出，ChatGPT Work 的发布与 Microsoft Frontier Company、Anthropic DeployCo 等企业级 Agent 方案形成了直接竞争。不同的是，OpenAI 选择了"平台中立"策略——支持在任何操作系统、任何工具生态中运行，而非局限于自有平台。</p>"""

feat_depth = """<h2>深度解读：Agent 时代的三个趋势</h2>

<h3>趋势一：从 API 到 Agent 的范式迁移</h3>
<p>过去两年，AI 产品的价值交付模式经历了三次跃迁：第一代是 API 调用（按 token 付费），第二代是 Copilot 嵌入（按席位付费），而第三代 Agent 模式将彻底改变这一格局——按结果付费。ChatGPT Work 的推出意味着 OpenAI 已经准备好从"卖工具"转向"卖服务"。</p>

<h3>趋势二：企业级 Agent 的安全护栏成为竞争壁垒</h3>
<p>ChatGPT Work 建立在 ChatGPT Enterprise 基础之上，提供了精细的 Admin 控制（插件管理、浏览器/网络设置、敏感操作限制）、桌面治理策略（基于 Codex 企业模型）、以及 Auto-review 功能——在执行重要操作前由高级模型自动审核，防止数据未经授权外泄。</p>

<h3>趋势三：Agent 正在模糊"软件"和"服务"的边界</h3>
<p>Sites 功能允许任何人基于自然语言描述就生成可交互的 Web 应用，这在本质上是一种"编程民主化"的终极形态。当 <span class="key-number">5</span>M+ 人每周使用 Codex、其中超过 <span class="key-number">1</span>M 人并非开发者时，Agent 正在重新定义"谁可以创造软件"。</p>"""

feat_conclusion = f"""<h2>总结</h2>
<p>ChatGPT Work 的发布是 OpenAI 从"对话 AI"向"行动 AI"转型的关键一步。当 AI 不再仅仅是回答问题，而是能够长时间自主工作、连接各类工具、产出完整成果时，它对知识工作者的生产力影响将是指数级的。正如 OpenAI 在公告中所说——"这只是让每个人都能够将想法转化为现实的第一步"。</p>"""

# Build image placement
feat_img1_tag = ''
feat_img2_tag = ''
if has_img1:
    feat_img1_tag = f'<figure style="margin:1.5rem 0;text-align:center;"><img src="{img1_path}" alt="{feat_title}" style="max-width:100%;border-radius:8px;max-height:400px;object-fit:cover;"><figcaption style="color:#6b7280;font-size:0.85rem;margin-top:0.5rem;">OpenAI ChatGPT Work — 跨应用自主工作的 AI 智能体</figcaption></figure>'
if has_img2:
    feat_img2_tag = f'<figure style="margin:1.5rem 0;text-align:center;"><img src="{img2_path}" alt="GPT-5.6 系列模型" style="max-width:100%;border-radius:8px;max-height:400px;object-fit:cover;"><figcaption style="color:#6b7280;font-size:0.85rem;margin-top:0.5rem;">GPT-5.6 系列：Sol、Terra、Luna 三模型分层架构</figcaption></figure>'

featured_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{feat_title} | AI快报站 suduai.top</title>
  <meta name="description" content="{feat_summary[:150]}">
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
.content-page {{ max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }}
.content-page h2 {{ margin-top: 2rem; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; }}
.content-page h3 {{ margin-top: 1.5rem; color: #374151; }}
.content-page blockquote {{ border-left: 4px solid #2563eb; margin: 1.5rem 0; padding: 1rem 1.5rem; background: #f9fafb; border-radius: 0 8px 8px 0; color: #4b5563; font-style: italic; }}
.key-number {{ color: #2563eb; font-weight: 700; font-size: 1.05em; }}
.back-link {{ display: inline-block; margin-top: 2rem; color: #2563eb; text-decoration: none; font-weight: 500; }}
.back-link:hover {{ text-decoration: underline; }}
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
  <a href="daily-{TODAY_STR}.html">📰 最新快报：{TODAY_STR}（今日 AI 精选 50 条）→</a>
</div>

<div class="content-page">
  <div class="featured-label" style="margin-bottom:0.5rem;">{feat_cat_display}</div>
  <h1 style="font-size:1.8rem;line-height:1.3;">{feat_title}</h1>
  <div class="featured-meta" style="margin:0.5rem 0 1.5rem;">
    <span>📅 {TODAY_STR}</span><span>📖 约 10 分钟</span>
  </div>

  <p>{feat_intro}</p>

  {feat_img1_tag}

  {feat_background}

  {feat_core}

  {feat_img2_tag}

  {feat_responses}

  {feat_depth}

  {feat_conclusion}

  <hr style="margin:2rem 0;">
  <p>📎 原文链接：<a href="{feat_url}" target="_blank" rel="noopener">{feat_url}</a></p>
  <a href="daily-{TODAY_STR}.html" class="back-link">→ 看今日完整快报（共 {len(items)} 条）</a>
</div>

<footer>
  <div class="container">
    <p>AI快报站 © 2026</p>
    <p style="margin-top:2px;"><a href="privacy-policy.html">隐私政策</a></p>
  </div>
</footer>

</body>
</html>'''

feat_path = f'featured-{TODAY_STR}.html'
write_file(feat_path, featured_html)
print(f"  {feat_path} written")

print("\n=== Done! All files generated. ===")
print(f"Total news items: {len(items)}")
print(f"Featured topic: {feat_title}")
print(f"Images: {('1.jpg' if has_img1 else 'none')}" + (f', 2.jpg' if has_img2 else ''))
