#!/usr/bin/env python3
import re
TODAY = '2026-11-19'
TITLE = '每股 $83、9.8 亿股、代码 ANT：Anthropic 把史上最大 IPO 定在了今天'
html = open('index.html', encoding='utf-8').read()

block = f'''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">行业 / 资本市场</div>
      <h2><a href="featured-{TODAY}.html">{TITLE}</a></h2>
      <p>11 月 18 日盘后，Anthropic 把发行价定在每股 <span class="key-number">$83.00</span>、发行 <span class="key-number">9.8 亿股</span>，今天以代码 <strong>ANT</strong> 登陆纳斯达克，募资约 <span class="key-number">$813 亿</span>——超过沙特阿美，成为史上最大 IPO 之一。一周前价格区间还挂在 $70–78。Vanda 预计首日散户净买入 <span class="key-number">$2.5 亿</span>，是 SpaceX 纪录的两倍多；但 StockTwits 上 1.8 万人投票，<span class="key-number">67%</span> 说不会在发行价买入，Orbis 干脆弃购，理由是 1.4 万亿估值"对一家尚未得到市场验证的公司实在太高"。同一笔交易，散户在抢配售，机构在算分母。</p>
      <div class="featured-meta">
        <span>📖 10 分钟</span><span>📅 {TODAY}</span><span>行业 / 资本市场</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="Anthropic 官方品牌图（来源：anthropic.com 官方新闻稿）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>

  '''

start = html.index('<div class="featured-card">')
end = html.index('<div class="section-title" style="margin-top:12px">')
html = html[:start] + block + html[end:]

# prepend prev-featured item
anchor = '<div class="prev-featured-list">\n'
item = f'''            <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{TITLE}</span>
      <span class="prev-arrow">→</span>
    </a>
'''
i = html.index(anchor) + len(anchor)
html = html[:i] + item + html[i:]

open('index.html', 'w', encoding='utf-8').write(html)
print('featured block replaced; prev items:', html.count('prev-featured-item'))
