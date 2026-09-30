#!/usr/bin/env python3
"""Generate featured-2026-09-30.html (Anthropic x SpaceX compute deal)
reusing the 09-29 shell/CSS."""
import re

TODAY = '2026-09-30'
tpl = open('featured-2026-09-29.html', encoding='utf-8').read()

head_part = tpl[:tpl.index('  <div class="featured-hero">')]
tail_part = tpl[tpl.rindex('<footer>'):]

TITLE = 'Anthropic 与 SpaceX 签下最高 845 亿美元算力协议：每月付 12.5 亿，90 天通知即可解约'
DESC = ('SpaceX S-1 与 Anthropic IPO 文件披露：2026 年 5 月签署的算力协议覆盖 Colossus 一号、二号数据中心，'
        'Anthropic 每月支付 12.5 亿美元至 2029 年 5 月，合同金额上限 845 亿美元（剔除爬坡月约 425 亿），'
        '且只需提前 90 天通知即可解约。')

head_part = re.sub(r'<title>.*?</title>', f'<title>{TITLE} | suduai.top</title>', head_part, count=1, flags=re.S)
head_part = re.sub(r'(<meta name="description" content=").*?(">)', lambda m: m.group(1) + DESC + m.group(2),
                   head_part, count=1, flags=re.S)

BODY = f'''
  <div class="featured-hero">
    <img src="images/featured-{TODAY}-1.jpg" alt="Anthropic 官方公告配图：节点相连的地球插画 | anthropic.com">
    <div class="featured-meta">
      <span>📖 8 分钟</span>
      <span>📅 {TODAY}</span>
      <span>🏭 行业动态</span>
    </div>
  </div>

  <h1>{TITLE}</h1>

<div class="article-body">

    <h2>一、导语：一份 IPO 文件里翻出的算力大单</h2>
    <p>9 月 30 日，随着 Anthropic 筹备上市，路透社查阅的申报文件把一笔此前只闻其声的算力交易摊开：Anthropic 与 SpaceX 签署的合作，最高价值 <span class="key-number">845 亿美元</span>。SpaceX 在 S-1 申报文件里写明了细节，Anthropic 自己招股书里的口径还要更高。核心数字很直白——每月 <span class="key-number">12.5 亿美元</span>，付款一直持续到 2029 年 5 月，而解约只需要提前 <span class="key-number">90 天</span>发通知。</p>

    <h2>二、背景分析：两个都在赶上市窗口的玩家</h2>
    <p>协议签于 2026 年 5 月。当时 Anthropic 正为 IPO 冲刺，收入一年翻 12 倍、账面亏损约 420 亿美元，它最缺的不是客户而是算力；另一头，马斯克一边推进 SpaceX 上市，一边把 Colossus 数据中心扩到惊人的规模，目标年底前上线 <span class="key-number">超过 100 万张 GPU</span>。一个要电，一个要订单，协议就落在中间。</p>
    <p>这也不是 Anthropic 唯一的算力来源。它同时握有 Amazon 最高 5 GW 的协议、Google 与 Broadcom 的 5 GW（2027 年上线）、Microsoft 与 NVIDIA 约 300 亿美元的 Azure 容量，以及 Fluidstack 的 500 亿美元美国基础设施投资。SpaceX 只是这套组合里最新、也最“非典型”的一块——一家火箭公司，来给一家 AI 公司供电。</p>

    <h2>三、核心内容：每月 12.5 亿，怎么算到 845 亿</h2>
    <h3>三个数字锁定这笔交易</h3>
    <p>SpaceX 披露：协议覆盖 Colossus 一号与二号的算力资源，Anthropic 每月支付 12.5 亿美元（约合 83.97 亿元人民币），持续到 2029 年 5 月；2026 年 5、6 两个月处于算力爬坡期，执行优惠费率。剔除这两个月，按 SpaceX 的口径测算，Anthropic 至少付出 <span class="key-number">425 亿美元</span>。而路透从 Anthropic 招股书看到的最新数字更高——合同金额上限达到 <span class="key-number">845 亿美元</span>。两份文件对解约通知期的表述完全一致：<span class="key-number">90 天</span>。</p>
    <p>SpaceX 给出的理由是把自己用不完的产能变现，即“盘活自身基础设施当中闲置的算力资源”。对 Anthropic 而言，这是一个月内就能拿到的增量：超过 <span class="key-number">300 兆瓦</span>、逾 <span class="key-number">22 万张</span> NVIDIA GPU，直接补给 Claude Pro 与 Max 订阅用户。同一时间，Anthropic 上调了 Claude Code 的五小时速率上限、取消了 Pro/Max 账户的峰时降速，并大幅提高 Opus 模型的 API 速率上限。</p>

    <div class="inline-img">
      <img src="images/featured-{TODAY}-2.jpg" alt="Anthropic 官方公布的 API 速率上限调整表：Tier 1 每分钟输入 3 万→50 万 token | anthropic.com">
      <div class="caption">Anthropic 官方公布的 API 速率上限调整（来源：anthropic.com/news/higher-limits-spacex）——算力一到手，最直接的落点就是用户看得到的额度</div>
    </div>

    <h3>马斯克那边的账</h3>
    <p>站在 SpaceX 一侧，这是把重资产变成经常性收入。Colossus 二号大量采用英伟达最新的 Blackwell GPU，全部 <span class="key-number">10 吉瓦</span>算力上线之后，公司预计 AI 基础设施业务的年营收可达 <span class="key-number">3000 亿至 5000 亿美元</span>。换句话说，Anthropic 的月付只是这张更大算力账单上的一行。</p>

    <h2>四、各方反应：把风险写进了条款</h2>
    <p>路透的报道把重点放在那条“90 天可解约”上——对一家正在冲击 <span class="key-number">2 万亿美元</span>估值的公司，这既是灵活性，也是不确定性的注脚：算力协议可以撤，收入承诺也就没看上去那么硬。</p>
    <p>Anthropic 在公告里另有一套说法：算力要落在“法律与监管框架支持这种规模投资、供应链安全”的民主国家，用来满足金融、医疗、政府等受监管行业的数据驻留需求；它还承诺覆盖自有美国数据中心带来的居民电价上涨，并把这套承诺向海外延伸。</p>

    <blockquote>
      「SpaceX 借此可以盘活自身基础设施当中闲置的算力资源，将闲置产能变现。」
      <footer>— SpaceX S-1 申报文件（经 IT之家 援引路透社，2026 年 9 月 30 日，译）</footer>
    </blockquote>

    <p>分析师的解读更冷静。Tomer Tunguz 指出，Anthropic 与 OpenAI 正在企业市场分层竞争，重定价与计费策略比模型本身更能决定输赢；而当供应商同时是投资方、客户和算力地主时，AI 基建的资金在几家巨头之间打转，循环成分本身就值得警惕。</p>

    <h2>五、深度解读：算力合同正在变成新的资产负债表</h2>
    <p>第一层含义是，AI 竞赛的入场券已经从“谁的模型强”换成了“谁签得到电”。Anthropic 规划未来十年至少投入 <span class="key-number">5180 亿美元</span>建自有 AI 基础设施，这不是研发预算，是基建预算。第二层含义是那个“90 天”——它把长期承诺切成短期选项，既让 Anthropic 保留退出权，也意味着 SpaceX 的收入没有表面那么稳。第三层是角色错位：火箭公司把算力租给 AI 公司，而这家 AI 公司同时被云厂商、芯片厂商和主权资本持有，生态边界已经模糊到旧框架解释不了。</p>

    <h2>六、总结</h2>
    <p>一句话：845 亿美元买的不只是 GPU，而是时间——在 IPO 敲钟之前，Anthropic 用一份可随时抽身的合同，换来模型继续往上跑所需要的电。</p>

  </div>

  <div class="bottom-cta">
    <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    <p>📌 主要信息来源：<a href="https://www.anthropic.com/news/higher-limits-spacex" target="_blank" rel="noopener">Anthropic 官方公告：Higher usage limits and a SpaceX compute deal</a> · <a href="https://www.ithome.com/1/008/589.htm" target="_blank" rel="noopener">IT之家（援引路透社）：Anthropic 与 SpaceX 签署最高 845 亿美元算力协议</a> · <a href="https://tomtunguz.com/anthropic-repriced-the-enterprise/" target="_blank" rel="noopener">Tomer Tunguz：Anthropic Repriced the Enterprise</a></p>
  </div>

'''

out = head_part + BODY + tail_part
open(f'featured-{TODAY}.html', 'w', encoding='utf-8').write(out)

html = open(f'featured-{TODAY}.html', encoding='utf-8').read()
start = html.find('<div class="article-body">')
end = html.find('<div class="bottom-cta">', start)
cn = len(re.findall(r'[\u4e00-\u9fff]', html[start:end]))
print(f'✅ featured-{TODAY}.html written | article-body Chinese chars: {cn}')
assert 900 < cn < 1700, cn
assert html.count(f'featured-{TODAY}-1.jpg') == 1
assert html.count(f'featured-{TODAY}-2.jpg') == 1
