#!/usr/bin/env python3
"""Generate featured-2026-10-07.html (Anthropic S-1 $518B compute bet) reusing the 10-06 shell/CSS."""
import re

TODAY = '2026-10-07'
tpl = open('featured-2026-10-06.html', encoding='utf-8').read()

head_part = tpl[:tpl.index('  <div class="featured-hero">')]
tail_part = tpl[tpl.rindex('<footer>'):]

TITLE = 'Anthropic S-1 曝光：5180 亿美元算力承诺、约八成不可撤销，冲刺近 2 万亿美元 IPO'
DESC = ('Anthropic 招股书首次披露：未来 7-10 年将在云与算力上投入至少 5180 亿美元，约八成不可撤销、'
        '用不用都要付，受体为 Google、Amazon、Broadcom、Microsoft；2025 年营收 45.9 亿美元、净亏约 420 亿，'
        'IPO 估值瞄向近 2 万亿美元，路演最早 11 月 9 日当周启动。')

head_part = re.sub(r'<title>.*?</title>', f'<title>{TITLE} | suduai.top</title>', head_part, count=1, flags=re.S)
head_part = re.sub(r'(<meta name="description" content=").*?(">)', lambda m: m.group(1) + DESC + m.group(2),
                   head_part, count=1, flags=re.S)

BODY = f'''
  <div class="featured-hero">
    <img src="images/featured-{TODAY}-1.jpg" alt="Anthropic 官方品牌标识（字标）| anthropic.com">
    <div class="featured-meta">
      <span>📖 9 分钟</span>
      <span>📅 {TODAY}</span>
      <span>🏭 行业动态</span>
    </div>
  </div>

  <h1>{TITLE}</h1>

<div class="article-body">

    <h2>一、导语：把账本摊开的这一天</h2>
    <p>Anthropic 的 S-1 招股书第一次把一家头部 AI 公司的家底完整摊开：未来 <span class="key-number">7 到 10 年</span>，它要在云计算、算力和基础设施上投入至少 <span class="key-number">5180 亿美元</span>；其中约 <span class="key-number">八成</span>属于不可撤销承诺——容量用不用、账都得付。按 Reuters 的整理，这相当于公司在 2025 年每挣 1 美元，就为未来的算力背上了约 <span class="key-number">113 美元</span>的账单。而它要冲刺的 IPO 估值，是接近 <span class="key-number">2 万亿美元</span>。</p>

    <h2>二、背景分析：为什么一份招股书成了行业风向标</h2>
    <p>2026 年的 AI 行业，竞争早已从"谁的模型更强"转到"谁先把算力锁死"。GPU、TPU、Trainium 这些长期合同的排队周期以年计，谁能提前把未来几年的产能订下来，谁才有资格继续训练下一个前沿模型。Anthropic 过去一年接连与 Amazon、Google、Broadcom、Microsoft 签下多年期大单，S-1 只是把这些散落的动作第一次用财务语言写清楚。</p>
    <p>更关键的是时点。招股书披露，Anthropic 已邀请机构投资者在 IPO 前质询高管，<span class="key-number">10 月 14 日</span>开会，最早 <span class="key-number">11 月 9 日</span>当周启动正式路演，力争感恩节前上市；按美国 SEC 规则，S-1 须在 10 月下旬公开。这不是一份普通的财务报表，而是市场对"AI 到底值多少钱"的一次公开定价。</p>

    <h2>三、核心内容：数字、供应商与时间线</h2>
    <p>先把金额拆开。5180 亿美元的算力承诺里，约 80% 为不可撤销、或"无论是否使用都需支付"（take-or-pay）性质，平均每年约 <span class="key-number">410 亿美元</span>。受体主要是四家：<span class="key-number">Broadcom</span> 约 <span class="key-number">1612 亿美元</span>、<span class="key-number">Google</span> 约 <span class="key-number">1111 亿美元</span>、<span class="key-number">Amazon</span> 约 <span class="key-number">1100 亿美元</span>、Microsoft 约 <span class="key-number">314 亿美元</span>，四家合计约 <span class="key-number">4137 亿美元</span>，其余分散在另外两家伙伴。</p>
    <p>再把代价摆齐：2025 年 Anthropic 营收约 <span class="key-number">45.9 亿美元</span>，净亏损约 <span class="key-number">420 亿美元</span>——但其中约 <span class="key-number">340 亿美元</span>是会计处理上的非现金费用（反映可转换为股份的融资估值上升），并非真金白银的运营支出。算力与基础设施支出则从 2024 年增长约三倍至 <span class="key-number">73.3 亿美元</span>，占 126.5 亿美元总运营费用的一半以上。截至年末，公司手上的现金及短期投资约 <span class="key-number">202.8 亿美元</span>。</p>
    <p>但增长的斜率同样惊人。Anthropic 自述其"运行率营收"已从 2025 年底约 90 亿美元升破 <span class="key-number">300 亿美元</span>；企业付费客户中，年支出超 100 万美元者已从 500 多家翻倍至 <span class="key-number">1000 家以上</span>。一边是天文数字的承诺，一边是陡峭的曲线——这正是招股书想同时讲给投资者听的两件事。</p>

    <div class="inline-img">
      <img src="images/featured-{TODAY}-2.jpg" alt="Anthropic 官方品牌插画：拾级而上的增长意象（Object Growth）| anthropic.com">
      <div class="caption">Anthropic 官方品牌插画"Object Growth"：阶梯式上行，用于对标算力与营收的陡峭增长（来源：anthropic.com）</div>
    </div>

    <h2>四、各方反应：投资人冷热交织</h2>
    <p>乐观的一方盯着需求。Anthropic 透露，2026 年企业与开发者需求加速，免费、Pro、Max 各档消费者用量都在攀升；同期它还推出 Opus 5.5，正面回应 OpenAI 的 GPT-6 系列。Amazon 在此前协议里已投资约 80 亿美元，并追加 50 亿美元、保留最多再投 200 亿美元的空间——云厂商既是供应商，也是股东，利益深度绑定。</p>
    <p>谨慎的一方盯着风险。招股书自己就把"客户集中"列为风险：近四分之一的营收来自两家客户，且许多大客户并未锁定长期合约，随时可能削减或停止支出。同时，<span class="key-number">80%</span> 的算力账单"用不用都要付"，一旦模型迭代或商业化节奏不及预期，现金流会立刻承压。</p>
    <blockquote>
      「我们在打造服务指数级增长所需的产能，同时让 Claude 定义 AI 开发的前沿——这是我们迄今最大的一笔算力承诺。」
      <footer>— Krishna Rao，Anthropic 首席财务官（据 Anthropic 官方公告）</footer>
    </blockquote>
    <p>竞争维度上，对手打法截然不同。Bloomberg 报道，OpenAI 以安全担忧为由排除了 2026 年上市，转而以约 <span class="key-number">1.4 万亿美元</span>估值私下寻求至少 300 亿美元融资。一个抢着上市，一个暂缓上市，两条路线在同一个赛道上正面对撞。</p>

    <h2>五、深度解读：AI 进入"重资产"定价时刻</h2>
    <p>第一层是商业模式的变化。Anthropic 的承诺不是"租算力"，而是把未来十年的产能提前买断——本质上是把自己变成一家"重资产公司"。这在软件时代罕见，却符合大模型训练的现实：算力是入场券，晚一步就可能出局。</p>
    <p>第二层是资本市场的定价逻辑。近 2 万亿美元的估值目标，是公司今年 5 月约 9650 亿美元估值估算的两倍以上，也紧追 SpaceX 近期 1.77 万亿美元的 IPO 估值。若成真，它会把"AI 基础设施"锚定成与航天、半导体同级的主权级资产类别。</p>
    <p>第三层是风险的集中度。当 80% 的支出不可撤销、近四分之一营收来自两个客户、而账上现金仅约 200 亿美元时，容错空间其实很窄。整个行业的隐忧也在这里：过去两年靠"预期"驱动的估值扩张，如今必须用真实的付费和留存来兑现。</p>
    <p>可以确定的是，"算力承诺"已经取代"模型参数"，成了 2026 年 AI 公司最重的筹码。谁锁定得早，谁就拿到下一轮竞赛的入场券；而账单的兑付，将从 IPO 那一刻开始计时。</p>

    <h2>六、总结</h2>
    <p>一句话：Anthropic 用一份 S-1 告诉市场——它愿意为算力押上 5180 亿美元、其中约八成不可撤销，去换一个近 2 万亿美元的 IPO 定价；这不只是一次上市，而是 AI 行业从"轻资产叙事"转向"重资产豪赌"的标志性一幕。</p>

  </div>

  <div class="bottom-cta">
    <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    <p>📌 主要信息来源：<a href="https://live.euronext.com/en/financial-news/anthropics-ipo-prospectus-shows-sweeping-ai-vision-surging-costs" target="_blank" rel="noopener">Reuters/Euronext：Anthropic IPO 招股书披露 5180 亿美元算力承诺</a> · <a href="https://www.anthropic.com/news/google-broadcom-partnership-compute" target="_blank" rel="noopener">Anthropic 官方：Google 与 Broadcom 算力合作</a> · <a href="https://www.anthropic.com/news/anthropic-amazon-compute" target="_blank" rel="noopener">Anthropic 官方：与亚马逊扩容算力合作</a> · <a href="https://aihot.news/items" target="_blank" rel="noopener">AIHOT 精选</a></p>
  </div>

'''

out = head_part + BODY + tail_part
open(f'featured-{TODAY}.html', 'w', encoding='utf-8').write(out)

html = open(f'featured-{TODAY}.html', encoding='utf-8').read()
start = html.find('<div class="article-body">')
end = html.find('<div class="bottom-cta">', start)
cn = len(re.findall(r'[\u4e00-\u9fff]', html[start:end]))
print(f'✅ featured-{TODAY}.html written | article-body Chinese chars: {cn}')
assert 1000 < cn < 1500, cn
assert html.count(f'featured-{TODAY}-1.jpg') == 1
assert html.count(f'featured-{TODAY}-2.jpg') == 1
print('✅ asserts passed')
