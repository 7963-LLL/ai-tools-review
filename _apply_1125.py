#!/usr/bin/env python3
"""Apply 2026-11-25 update: nf items, featured block, prev list, banner, review dates, daily nav."""
import re, io

D = '2026-11-25'
idx = io.open('index.html', encoding='utf-8').read()

# 1. nf items
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
      <div class="featured-label">行业 / 劳动力市场</div>
      <h2><a href="featured-2026-11-25.html">5,414 家公司、38% 的美国程序员：Copilot 把初级工程师招聘砍掉四成，资深岗毫发无损</a></h2>
      <p>11 月 6 日，MIT 的 Lindsey Raymond 和微软研究院的 Eleanor Dillon 把「AI 抢工作」从问卷讨论变成了后台数据：<span class="key-number">5,414</span> 家跨国公司、4,500 万雇员、覆盖 <span class="key-number">38%</span> 的美国编程劳动力。他们用企业软件合同审查的时点做自然实验，发现真正用上 Copilot 的公司，初级软件工程师的季度招聘下降约 <span class="key-number">40%</span>，资深工程师和系统/基础设施岗位几乎没动。更耐人寻味的是结构变化——初级技术招聘里进入代码密集岗的比例，从 72% 掉到 52%。AI 没有裁掉谁，它只是不再给新人开门。</p>
      <div class="featured-meta">
        <span>📖 11 分钟</span><span>📅 2026-11-25</span><span>行业 / 劳动力市场</span>
      </div>
      <a href="daily-2026-11-25.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-2026-11-25-1.jpg" alt="Copilot 采用前后技术岗位招聘率变化（来源：论文 Figure 2，MIT / 微软研究院）" style="width:180px;border-radius:8px;object-fit:contain;background:#fff;height:100px;">
    </div>
  </div>
'''
idx = idx[:fm.start()] + new_feat + idx[fm.end():]

# 3. prev-featured: newest on top
idx = idx.replace('  <div class="prev-featured-list">\n',
'''  <div class="prev-featured-list">
            <a href="featured-2026-11-25.html" class="prev-featured-item">
      <span class="prev-date">2026-11-25</span>
      <span class="prev-title">5,414 家公司、38% 的美国程序员：Copilot 把初级工程师招聘砍掉四成，资深岗毫发无损</span>
      <span class="prev-arrow">→</span>
    </a>
''', 1)

# 4. daily banner
idx = idx.replace('<a href="daily-2026-11-24.html">📰 最新快报：2026-11-24（今日 AI 精选 50 条）→</a>',
                  '<a href="daily-2026-11-25.html">📰 最新快报：2026-11-25（今日 AI 精选 50 条）→</a>')

# 5. review card dates
n = len(re.findall(r'<span>📅 2026-11-24</span><span>📖', idx))
idx = idx.replace('<span>📅 2026-11-24</span><span>📖', '<span>📅 2026-11-25</span><span>📖')
print('review dates updated:', n)

io.open('index.html', 'w', encoding='utf-8').write(idx)

# 6. daily.html nav
dl = io.open('daily.html', encoding='utf-8').read()
dl = dl.replace('<a href="daily-2026-11-24.html">📰 最新快报：2026-11-24（今日 AI 精选 50 条）→</a>',
                '<a href="daily-2026-11-25.html">📰 最新快报：2026-11-25（今日 AI 精选 50 条）→</a>')
dl = dl.replace('  <div class="daily-nav">\n',
                '  <div class="daily-nav">\n    <a href="daily-2026-11-25.html">📅 2026-11-25 今日快报</a>\n', 1)
io.open('daily.html', 'w', encoding='utf-8').write(dl)
print('daily.html updated')
