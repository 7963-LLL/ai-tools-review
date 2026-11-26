#!/usr/bin/env python3
"""Apply 2026-11-26 update: nf items, featured block, prev list, banner, review dates, daily nav."""
import re, io

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
      <div class="featured-label">产品 / 软件开发</div>
      <h2><a href="featured-2026-11-26.html">AI 给自己发了合并权限：Claude Ship 让 Agent 审 PR、修 CI、按策略自己批准</a></h2>
      <p>11 月 23 日，Anthropic 上线 Claude Ship 测试版，把三个 Agent 串成一条流水线：Code Review 审出问题并<em>对抗性自证</em>，PR Steward 负责修 CI、解冲突、改反馈但<strong>被禁止批准合并</strong>，Claude Approvals 读一份写进仓库的策略文件，符合条件就自己点通过。Claude Code 团队自己的数字是：6 月到 9 月合并 PR 数<span class="key-number">翻倍以上</span>，被回滚的变更占比<span class="key-number">下降 40%</span>。真正的新东西不是 Agent 会写代码，而是审批权第一次变成仓库里可 diff、可回滚的一份文件。</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 2026-11-26</span><span>产品 / 软件开发</span>
      </div>
      <a href="daily-2026-11-26.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-2026-11-26-1.png" alt="Claude Ship 三步流程：Code Review 审查、PR Steward 修复、Claude Approvals 按策略批准（来源：Claude 官方博客）" style="width:180px;border-radius:8px;object-fit:contain;background:#fff;height:100px;">
    </div>
  </div>
'''
idx = idx[:fm.start()] + new_feat + idx[fm.end():]

# 3. prev-featured: newest on top
idx = idx.replace('  <div class="prev-featured-list">\n',
'''  <div class="prev-featured-list">
            <a href="featured-2026-11-26.html" class="prev-featured-item">
      <span class="prev-date">2026-11-26</span>
      <span class="prev-title">AI 给自己发了合并权限：Claude Ship 让 Agent 审 PR、修 CI、按策略自己批准</span>
      <span class="prev-arrow">→</span>
    </a>
''', 1)

# 4. daily banner
idx = idx.replace('<a href="daily-2026-11-25.html">📰 最新快报：2026-11-25（今日 AI 精选 50 条）→</a>',
                  '<a href="daily-2026-11-26.html">📰 最新快报：2026-11-26（今日 AI 精选 50 条）→</a>')

# 5. review card dates
n = idx.count('<span>📅 2026-11-25</span><span>📖')
idx = idx.replace('<span>📅 2026-11-25</span><span>📖', '<span>📅 2026-11-26</span><span>📖')
print('review dates updated:', n)

io.open('index.html', 'w', encoding='utf-8').write(idx)

# 6. daily.html nav + banner
dl = io.open('daily.html', encoding='utf-8').read()
dl = dl.replace('<a href="daily-2026-11-25.html">📰 最新快报：2026-11-25（今日 AI 精选 50 条）→</a>',
                '<a href="daily-2026-11-26.html">📰 最新快报：2026-11-26（今日 AI 精选 50 条）→</a>')
dl = dl.replace('  <div class="daily-nav">\n',
                '  <div class="daily-nav">\n    <a href="daily-2026-11-26.html">📅 2026-11-26 今日快报</a>\n', 1)
io.open('daily.html', 'w', encoding='utf-8').write(dl)
print('daily.html updated')
