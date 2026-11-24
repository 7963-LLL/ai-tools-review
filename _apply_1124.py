#!/usr/bin/env python3
"""Apply 2026-11-24 update: nf items, featured block, prev list, banner, dates, daily nav."""
import re, io

D = '2026-11-24'
idx = io.open('index.html', encoding='utf-8').read()

# 1. nf items: replace everything between nf-scroll open and the script block
items = io.open('_nf_items_output.txt', encoding='utf-8').read().strip()
start = idx.index('<div class="nf-scroll" id="nf-scroll">') + len('<div class="nf-scroll" id="nf-scroll">')
end = idx.index('\n\n\n<script>\n// AI 热点分类过滤')
idx = idx[:start] + '\n' + items + idx[end:]
print('nf items:', idx.count('class="nf-item"'))

# 2. featured block
fm = re.search(r'<div class="featured-card">.*?\n  </div>\n', idx, re.S)
new_feat = '''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">前沿研究 / 数学</div>
      <h2><a href="featured-2026-11-24.html">1700 万行 Lean 代码、25 万页纸：Claude 和阿尔珀格把黎曼猜想写成了可编译的定理</a></h2>
      <p>11 月 20 日，Anthropic 数学家 Levent Alpöge 在个人主页贴出一份 4 页手记，宣布与 Claude 一起证明了黎曼猜想，连带广义黎曼猜想。证明没有写成论文，而是 <span class="key-number">1700 万行</span> Lean 代码，打印出来超过 <span class="key-number">25 万页</span>，拆成 14 个数据包。第二天 Lean 与 Mathlib 社区发声明：核验通过，数十人独立复现。Metaculus 上的预测中位数原本是 2035 年 5 月。几小时后，斯坦福端出一份全人类、无 AI 的竞争草稿。</p>
      <div class="featured-meta">
        <span>📖 9 分钟</span><span>📅 2026-11-24</span><span>前沿研究 / 数学</span>
      </div>
      <a href="daily-2026-11-24.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-2026-11-24-1.png" alt="阿尔珀格与 Claude 的证明手记首页（来源：alpo.ge 原文 PDF）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>
'''
idx = idx[:fm.start()] + new_feat + idx[fm.end():]

# 3. prev-featured: newest on top
idx = idx.replace('  <div class="prev-featured-list">\n',
'''  <div class="prev-featured-list">
            <a href="featured-2026-11-24.html" class="prev-featured-item">
      <span class="prev-date">2026-11-24</span>
      <span class="prev-title">1700 万行 Lean 代码、25 万页纸：Claude 和阿尔珀格把黎曼猜想写成了可编译的定理</span>
      <span class="prev-arrow">→</span>
    </a>
''', 1)

# 4. daily banner
idx = idx.replace('<a href="daily-2026-11-19.html">📰 最新快报：2026-11-19（今日 AI 精选 50 条）→</a>',
                  '<a href="daily-2026-11-24.html">📰 最新快报：2026-11-24（今日 AI 精选 50 条）→</a>')

# 5. review card dates
n = len(re.findall(r'<span>📅 2026-11-19</span><span>📖', idx))
idx = idx.replace('<span>📅 2026-11-19</span><span>📖', '<span>📅 2026-11-24</span><span>📖')
print('review dates updated:', n)

io.open('index.html', 'w', encoding='utf-8').write(idx)

# 6. daily.html nav
dl = io.open('daily.html', encoding='utf-8').read()
dl = dl.replace('<a href="daily-2026-11-19.html">📰 最新快报：2026-11-19（今日 AI 精选 50 条）→</a>',
                '<a href="daily-2026-11-24.html">📰 最新快报：2026-11-24（今日 AI 精选 50 条）→</a>')
dl = dl.replace('  <div class="daily-nav">\n',
                '  <div class="daily-nav">\n    <a href="daily-2026-11-24.html">📅 2026-11-24 今日快报</a>\n', 1)
io.open('daily.html', 'w', encoding='utf-8').write(dl)
print('daily.html updated')
