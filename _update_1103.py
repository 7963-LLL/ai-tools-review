#!/usr/bin/env python3
"""One-off: patch index.html for 2026-11-03. ponytail: throwaway, same shape as the last hundred."""
import re

TODAY = '2026-11-03'
PREV = '2026-11-02'
TITLE = '营收涨 12 倍，亏 233 亿：Anthropic 的 S-1 把「AI 是不是泡沫」摊上了牌桌'
html = open('index.html', encoding='utf-8').read()

# ---------- 1. nf-items ----------
new_items = open('_nf_items_output.txt', encoding='utf-8').read().replace('\r\n', '\n')
start_marker = '<div class="nf-scroll" id="nf-scroll">'
end_marker = '\n\n<script>\n// AI 热点分类过滤'
i = html.index(start_marker) + len(start_marker)
j = html.index(end_marker)
assert j > i, 'nf-scroll markers not found'
assert html.count('class="nf-item"') == 50, html.count('class="nf-item"')
html = html[:i] + '\n' + new_items + '\n' + html[j:]

# ---------- 2. banner ----------
html, n = re.subn(
    r'<div class="daily-banner">\s*<a href="daily-[\d-]+\.html">[^<]*</a>\s*</div>',
    f'<div class="daily-banner">\n  <a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>\n</div>',
    html, count=1)
assert n == 1, 'banner not patched'

# ---------- 3. featured card ----------
new_card = '''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">行业动态</div>
      <h2><a href="featured-2026-11-03.html">营收涨 12 倍，亏 233 亿：Anthropic 的 S-1 把「AI 是不是泡沫」摊上了牌桌</a></h2>
      <p>11 月 2 日 Anthropic 公开 S-1。第三季度营收 <span class="key-number">168 亿美元</span>，是去年同期的 12 倍；运营成本 <span class="key-number">175 亿</span>，收入被吃穿，单季净亏 <span class="key-number">233 亿美元</span>（去年同期 121 亿）。真正压在文件后面的是承诺：算力与数据中心租赁合计约 <span class="key-number">8954 亿美元</span>，其中 <span class="key-number">4475 亿</span>须在 2031 年前付清，只有 <span class="key-number">2138 亿</span>可取消。账上现金 1120 亿、负债 1175 亿，现金储备在美国非银行企业里排第三，前面只有 Google 和伯克希尔。白宫科技顾问萨克斯读完说这可能是"资本主义史上最伟大的企业"；黑石却在 IPO 前改口，称其未必拿得到投资级评级。收入曲线没问题，问题是它得跑多快才追得上已经签下的产能。</p>
      <div class="featured-meta">
        <span>📖 11 分钟</span><span>📅 2026-11-03</span><span>行业动态</span>
      </div>
      <a href="daily-2026-11-03.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-2026-11-03-1.jpg" alt="Anthropic 官方品牌标识（anthropic.com 官网图）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
print('prev featured date 11-02 still present:', 'prev-date">2026-11-02' in html)
