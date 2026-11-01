#!/usr/bin/env python3
"""One-off: patch index.html + daily.html for 2026-11-01. ponytail: throwaway, same shape as the last hundred."""
import re

TODAY = '2026-11-01'
PREV = '2026-10-30'
TITLE = '一年之后，Weave 长入了画布：Figma 把 AI 创作从「抽卡」改成「流水线」'
html = open('index.html', encoding='utf-8').read()

# ---------- 1. nf-items ----------
new_items = open('_nf_items_output.txt', encoding='utf-8').read().replace('\r\n', '\n')
start_marker = '<div class="nf-scroll" id="nf-scroll">'
end_marker = '\n\n<script>\n// AI 热点分类过滤'
i = html.index(start_marker) + len(start_marker)
j = html.index(end_marker)
assert j > i, 'nf-scroll markers not found'
html = html[:i] + '\n' + new_items + '\n' + html[j:]

# ---------- 2. banner ----------
html = re.sub(
    r'<div class="daily-banner">\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*</div>',
    f'<div class="daily-banner">\n  <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    html, count=1)

# ---------- 3. featured card ----------
new_card = '''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">产品动态</div>
      <h2><a href="featured-2026-11-01.html">一年之后，Weave 长入了画布：Figma 把 AI 创作从「抽卡」改成「流水线」</a></h2>
      <p>10 月 31 日 Figma 宣布 Weave 工作流与 Figma 画框打通：Figma 的 frame 变成 Weave 里的节点，改动双向推送，原始文件不被覆盖。加上 10 月 26 日把 Seedance、Kling、Nano Banana 等全部图像视频模型开放给 Figma MCP，10 月 30 日放开 Organization 与 Enterprise 的内网 Weave tools 发布——AI 生成从「一个输入框」变成了能存下来、给同事复跑的流水线。代价是账单位置：一方 Weave tool 每次 <span class="key-number">19~55 credits</span>，而 Weave 自己还有一套订阅（Free 到 Max <span class="key-number">$0~$100/月</span>、Team <span class="key-number">$42/人/月</span>），Figma 计划<strong>不含</strong> Weave，两个额度池互不相通。设计师的反馈倒是统一：真正在意的不是生成多快，而是「随时能回来改」。</p>
      <div class="featured-meta">
        <span>📖 9 分钟</span><span>📅 2026-11-01</span><span>产品动态</span>
      </div>
      <a href="daily-2026-11-01.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-2026-11-01-1.jpg" alt="Figma Design 画框与 Weave 节点画布双向连接示意（Figma 官方博客配图）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''
m = re.search(r'<div class="featured-card">.*?\n  </div>\n<div class="section-title" style="margin-top:12px">', html, re.S)
assert m, 'featured card not found'
html = html[:m.start()] + new_card + '\n<div class="section-title" style="margin-top:12px">' + html[m.end():]

# ---------- 4. prev-featured prepend ----------
prev_marker = '<div class="prev-featured-list">\n'
k = html.index(prev_marker) + len(prev_marker)
if f'prev-date">{TODAY}' not in html:
    html = html[:k] + f'''            <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{TITLE}</span>
      <span class="prev-arrow">→</span>
    </a>
''' + html[k:]

# ---------- 5. review card dates ----------
html = html.replace(f'<div class="meta"><span>📅 {PREV}</span>', f'<div class="meta"><span>📅 {TODAY}</span>')

open('index.html', 'w', encoding='utf-8', newline='\n').write(html)

# ---------- 6. daily.html nav ----------
d = open('daily.html', encoding='utf-8').read()
d = d.replace(f'<a href="daily-{PREV}.html">📰 最新快报：{PREV}（今日 AI 精选 50 条）→</a>',
              f'<a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>')
if f'daily-{TODAY}.html">📅' not in d:
    d = d.replace(f'<a href="daily-{PREV}.html">📅 {PREV} 今日快报</a>',
                  f'<a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n    ' +
                  f'<a href="daily-{PREV}.html">📅 {PREV} 今日快报</a>')
open('daily.html', 'w', encoding='utf-8', newline='\n').write(d)

# ---------- verify ----------
h = open('index.html', encoding='utf-8').read()
print('nf-items:', h.count('class="nf-item"'))
print('tabs:', h.count('class="nf-tab"'))
print('filter js:', 'AI 热点分类过滤' in h)
print('banner:', f'daily-{TODAY}.html">📰' in h)
print('featured h2:', f'featured-{TODAY}.html">' in h)
print('featured btn -> daily:', f'<a href="daily-{TODAY}.html" class="affiliate-btn">' in h)
print('prev first:', f'prev-date">{TODAY}' in h, '| total:', h.count('prev-featured-item">'))
print('review dates today:', h.count(f'📅 {TODAY}'), '| leftovers:', h.count(f'📅 {PREV}'))
print('daily.html new link:', f'daily-{TODAY}.html' in open('daily.html', encoding='utf-8').read())
