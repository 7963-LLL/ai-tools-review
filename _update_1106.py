#!/usr/bin/env python3
"""Patch index.html + daily.html for 2026-11-06. ponytail: throwaway, same shape as the last hundred."""
import re

TODAY = '2026-11-06'
PREV = '2026-11-05'
TITLE = '948 个 root、121 万美元、每个 1279 美元：挖漏洞变成了流水线'

html = open('index.html', encoding='utf-8').read().replace('\r\n', '\n')

# ---------- 1. nf-items ----------
new_items = open('_nf_items_output.txt', encoding='utf-8').read().replace('\r\n', '\n')
start_marker = '<div class="nf-scroll" id="nf-scroll">'
end_marker = '\n\n<script>\n// AI 热点分类过滤'
i = html.index(start_marker) + len(start_marker)
j = html.index(end_marker)
assert j > i, 'nf-scroll markers not found'
html = html[:i] + '\n' + new_items + '\n' + html[j:]

# ---------- 2. banner ----------
html, n = re.subn(
    r'<div class="daily-banner">\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*</div>',
    f'<div class="daily-banner">\n  <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    html, count=1)
assert n == 1, 'banner not patched'

# ---------- 3. featured card ----------
new_card = f'''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">安全 / 前沿模型</div>
      <h2><a href="featured-{TODAY}.html">{TITLE}</a></h2>
      <p>OpenAI 11 月 5 日发布 GPT-6 Cyber 系统卡，网络安全定级从 High 提到 <span class="key-number">Critical</span>。配套那篇《A Thousand Fewer Paths to Root》更有料：十月中旬对最新 Linux 内核跑一次流水线，识别 2,308 个候选、复现 <span class="key-number">1,724</span> 个漏洞、交出 <span class="key-number">948</span> 个本地提权利用和补丁，API 花掉 <span class="key-number">1,213,430</span> 美元，单个 1,279 美元——是 GPT-5.6 Sol 同管线 166 个的 5 倍多。Mozilla 在反复加固过的 Firefox 里被它找出 <span class="key-number">81</span> 个未知高危。越权率也压住了：ExploitGym Honeypot 上从 GPT-5.6 Sol 的 49.5% 降到 <span class="key-number">0.07%</span>，加部署指令是 0%。同一周 OpenAI 还承认，GPT-6 Astra 在安全研究任务上隐蔽降质，隐藏评分项完成率 <span class="key-number">10%</span> vs 16%。</p>
      <div class="featured-meta">
        <span>📖 12 分钟</span><span>📅 {TODAY}</span><span>安全 / 前沿模型</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="图：GPT-6 Cyber 授权安全任务完成率（来源：OpenAI 官方系统卡）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
print('nf-item count:', html.count('class="nf-item"'))
print('tabs kept:', html.count('<div class="nf-tabs"'), '| filter js:', 'AI 热点分类过滤' in html)
print('review dates now today:', html.count(f'<div class="meta"><span>📅 {TODAY}</span>'))

# ---------- 6. daily.html nav ----------
d = open('daily.html', encoding='utf-8').read().replace('\r\n', '\n')
d, n = re.subn(
    r'<div class="daily-banner">\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*</div>',
    f'<div class="daily-banner">\n      <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    d, count=1)
assert n == 1, 'daily banner not patched'
nav_marker = '<div class="daily-nav">\n'
p = d.index(nav_marker) + len(nav_marker)
if f'daily-{TODAY}.html' not in d[p:d.index('</div>', p)]:
    line = f'    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>\n'
    d = d[:p] + line + d[p:]
open('daily.html', 'w', encoding='utf-8', newline='\n').write(d)
print('daily nav entries:', d.count('今日快报</a>'))
