#!/usr/bin/env python3
"""Apply 2026-11-27 update: nf items, featured block, prev list, banner, review dates, daily nav."""
import re, io

D = '2026-11-27'
idx = io.open('index.html', encoding='utf-8').read()

# 1. nf items — replace everything between the nf-scroll open and the filter <script>
items = io.open('_nf_items_output.txt', encoding='utf-8').read().strip()
OPEN = '<div class="nf-scroll" id="nf-scroll">'
start = idx.index(OPEN) + len(OPEN)
end = idx.index('\n\n\n<script>', start)
idx = idx[:start] + '\n' + items + idx[end:]
print('nf items:', idx.count('class="nf-item"'))

# 2. featured block
fm = re.search(r'<div class="featured-card">.*?\n  </div>\n', idx, re.S)
SHORT = ('9 月 8 日到 10 日，一个开源渗透框架里的 AI 智能体拿到一条指令：「拿到 shell」。前 16 小时它试了 <span class="key-number">148</span> 次都打不穿一台免认证的 Redis，'
         '又用 <span class="key-number">30,000</span> 多组密码撞 SSH、VPN 和校园门户，全败。换到一台跑医学影像 AI 的服务器上，它 <span class="key-number">11 分钟</span>'
         '就从摸清 API 走到任意文件写入，把反弹 shell 塞进 <code>sitecustomize.py</code>，以 root 落地——还顺手挖出一个当时无公告、无补丁的路径穿越 0-day。'
         '亚马逊把这场持续 48 小时的作业记录整份公开了，因为攻击者把框架开在了公网、没设鉴权。')
new_feat = '''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">安全 / AI Agent</div>
      <h2><a href="featured-%s.html">16 小时、148 次动作、30,000 组密码全部失败，然后它用 11 分钟拿到了 root</a></h2>
      <p>%s</p>
      <div class="featured-meta">
        <span>📖 8 分钟</span><span>📅 %s</span><span>安全 / AI Agent</span>
      </div>
      <a href="daily-%s.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-%s-1.png" alt="MONAI Label 在 3D Slicer 中的标注界面（来源：Project-MONAI 官方仓库文档配图）" style="width:180px;border-radius:8px;object-fit:contain;background:#fff;height:100px;">
    </div>
  </div>
''' % (D, SHORT, D, D, D)
idx = idx[:fm.start()] + new_feat + idx[fm.end():]

# 3. prev-featured: newest on top
idx = idx.replace('  <div class="prev-featured-list">\n',
'''  <div class="prev-featured-list">
            <a href="featured-%s.html" class="prev-featured-item">
      <span class="prev-date">%s</span>
      <span class="prev-title">16 小时、148 次动作、30,000 组密码全部失败，然后它用 11 分钟拿到了 root</span>
      <span class="prev-arrow">→</span>
    </a>
''' % (D, D), 1)

# 4. daily banner
idx = idx.replace('<a href="daily-2026-11-26.html">📰 最新快报：2026-11-26（今日 AI 精选 50 条）→</a>',
                  '<a href="daily-%s.html">📰 最新快报：%s（今日 AI 精选 50 条）→</a>' % (D, D))

# 5. review card dates
n = idx.count('<div class="meta"><span>📅 2026-11-26</span>')
idx = idx.replace('<div class="meta"><span>📅 2026-11-26</span>', '<div class="meta"><span>📅 %s</span>' % D)
print('review dates updated:', n)

io.open('index.html', 'w', encoding='utf-8').write(idx)

# 6. daily.html nav + banner
dl = io.open('daily.html', encoding='utf-8').read()
dl = dl.replace('<a href="daily-2026-11-26.html">📰 最新快报：2026-11-26（今日 AI 精选 50 条）→</a>',
                '<a href="daily-%s.html">📰 最新快报：%s（今日 AI 精选 50 条）→</a>' % (D, D))
dl = dl.replace('  <div class="daily-nav">\n',
                '  <div class="daily-nav">\n    <a href="daily-%s.html">📅 %s 今日快报</a>\n' % (D, D), 1)
io.open('daily.html', 'w', encoding='utf-8').write(dl)
print('daily.html updated')
