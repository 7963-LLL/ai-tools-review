#!/usr/bin/env python3
"""Generate featured-2026-10-06.html (DeepSeek 800亿 financing) reusing the 10-05 shell/CSS."""
import re

TODAY = '2026-10-06'
tpl = open('featured-2026-10-05.html', encoding='utf-8').read()

head_part = tpl[:tpl.index('  <div class="featured-hero">')]
tail_part = tpl[tpl.rindex('<footer>'):]

TITLE = 'DeepSeek 敲定至少 800 亿元融资：腾讯、宁德时代重金押注，为 2027 年 IPO 铺路'
DESC = ('据彭博社，DeepSeek 新一轮融资接近敲定，规模至少 800 亿元人民币、可能逼近 1000 亿元，'
        '腾讯与宁德时代为最大出资方；公司同时在内蒙古建设部署至少 16 万枚华为 AI 芯片的数据中心，'
        '并计划 2027 年初启动 IPO。')

head_part = re.sub(r'<title>.*?</title>', f'<title>{TITLE} | suduai.top</title>', head_part, count=1, flags=re.S)
head_part = re.sub(r'(<meta name="description" content=").*?(">)', lambda m: m.group(1) + DESC + m.group(2),
                   head_part, count=1, flags=re.S)

BODY = f'''
  <div class="featured-hero">
    <img src="images/featured-{TODAY}-1.jpg" alt="DeepSeek 官方品牌标识（鲸鱼 Logo 与字标）| deepseek">
    <div class="featured-meta">
      <span>📖 9 分钟</span>
      <span>📅 {TODAY}</span>
      <span>🏭 行业动态</span>
    </div>
  </div>

  <h1>{TITLE}</h1>

<div class="article-body">

    <h2>一、导语：一笔可能刷新纪录的融资</h2>
    <p>10 月 6 日，彭博社消息——DeepSeek 新一轮融资已接近敲定，募资规模至少 <span class="key-number">800 亿元</span>人民币，大幅超出其自身原定约 500 亿元的目标。知情人士称，按照已签署的投资条款书，本轮最终总额有可能逼近 <span class="key-number">1000 亿元</span>，而<span class="key-number">腾讯</span>与<span class="key-number">宁德时代</span>是出资规模最大的几家投资方，交易很快就会完成交割。这笔钱，将直接为该公司计划在 2027 年初启动的里程碑式 IPO 铺路。</p>

    <h2>二、背景分析：为什么这轮融资值得单拎出来看</h2>
    <p>第一，体量。DeepSeek 最初的募资目标约为 500 亿元，而实际认购远超预期；据报，公司原本希望对应的估值约为 <span class="key-number">5000 亿元</span>。在上一轮（今年夏天，规模 500 亿元）里，DeepSeek 的估值约为 <span class="key-number">3500 亿元</span>，创始人梁文锋也继续出资——也就是说，短短几个月，市场愿意给它更高一级的定价。</p>
    <p>第二，触发点。这轮认购情绪的转折，来自最新模型的成功。自 <span class="key-number">V4-Flash</span> 推出后，公司发展势头明显加快，该模型重塑了业界对"性价比"的认知，被认为已经可以同 Anthropic、OpenAI 等海外头部厂商展开竞争。技术叙事变成资本叙事，这是 2026 年 AI 行业反复上演的戏码。</p>

    <h2>三、核心内容：金额、算力与时间线</h2>
    <p>先把数字摆齐。本轮目标由约 500 亿元上调，落定规模至少 <span class="key-number">800 亿元</span>，上限可能逼近 1000 亿元；IPO 目标时间点为 <span class="key-number">2027 年初</span>。</p>
    <p>算力是这笔钱最主要的去处。DeepSeek 正在内蒙古建设一座大型数据中心，计划在这里部署至少 <span class="key-number">16 万枚</span>华为高端 AI 加速芯片，有望建成目前规模数一数二的华为 AI 芯片算力集群。它同时还发布了与华为联合开发、用于 AI 芯片编程的软件，借此与这家硬件厂商深度协作，正式踏入一块全新的业务领域——从"租算力"转向"造算力"，是这轮扩张最值得注意的信号。</p>
    <p>资本层面，老股东的加注意图也很清晰。腾讯在上一轮融资中就已经是这家初创公司的最大投资方，出资 <span class="key-number">100 亿元</span>，它希望把 AI 能力整合进旗下各个产品平台；宁德时代则可能看好面向数据中心等场景的算力零部件赛道，希望布局这块日渐景气的市场。</p>
    <p>创始人个人财富同步水涨船高：今年夏天 DeepSeek 完成首轮外部融资之后，梁文锋的个人净资产翻了一倍以上，大约达到 <span class="key-number">360 亿美元</span>。这家公司脱胎于他创办的对冲基金幻方量化，早期发展的大部分资源也来自幻方。</p>

    <div class="inline-img">
      <img src="images/featured-{TODAY}-2.jpg" alt="DeepSeek 官方公布的 V4 基准测试：DeepSeek-V4-Pro-Max 与 Claude Opus 4.6 Max、GPT-5.4 xHigh、Gemini 3.1 Pro High 对比 | deepseek.com">
      <div class="caption">DeepSeek 官方公布的 V4 基准对比：V4-Pro-Max 在 Codeforces 拿到 3206 分、SWE Verified 80.6%，直接对标 Claude、GPT 与 Gemini 的旗舰档（来源：deepseek.com）</div>
    </div>

    <h2>四、各方反应：投资人抢筹，同行抢跑</h2>
    <p>认购热情最直接的证据，就是"超额"。据报道，DeepSeek 最初的募资目标约 500 亿元，但随着最新模型发布取得成功，市场投资者的认购热情远超预期，最终规模被推高。腾讯与宁德时代的角色分工也耐人寻味：一个要模型能力，一个要算力硬件，两家押注的是同一条产业链的不同环节。</p>
    <p>创始人本人的态度则给这笔钱定了调——据彭博社，梁文锋今年至少在一场投资者会议上表态：在向着实现通用人工智能这一长远目标迈进的同时，他会持续坚持开源 AI 模型的开发；这位对冲基金出身的管理者明确表示，自己首要目标是不断拓展技术的边界，而非优先追求商业化变现。</p>
    <blockquote>
      「在向着实现通用人工智能这一长远目标迈进的同时，他会持续坚持开源 AI 模型的开发……首要目标是不断拓展技术的边界，而非优先追求商业化变现。」
      <footer>— 梁文锋，DeepSeek 创始人（据彭博社报道，整理转述）</footer>
    </blockquote>
    <p>竞争对手也没闲着。月之暗面（Moonshot）在完成一轮估值 <span class="key-number">500 亿美元</span>的融资之后，同样把 IPO 目标定在了 2027 年初。两家中国头部 AI 公司，几乎踩着同一个时间表冲向公开市场。</p>

    <h2>五、深度解读：这是一场"算力 + 开源 + 上市"的三重竞速</h2>
    <p>第一层是算力自主。16 万枚华为芯片的集群，把 DeepSeek 与国产硬件生态绑在了一起。当外部先进算力获取不确定时，"自建 + 国产芯片"既是成本选择，也是供应链安全的必需项。</p>
    <p>第二层是开源策略的商业化路径。坚持开源、把技术边界放在商业化之前，短期看是放弃了一部分直接收入，但配合 IPO，它换来的是开发者生态、行业心智和更高的资本溢价。</p>
    <p>第三层是上市节奏。DeepSeek 与月之暗面同时把时间点瞄向 2027 年初，意味着中国 AI 公司正集体从"烧钱研发"切换到"资本兑现"阶段。谁先上市、拿到多少估值，会直接影响下一轮人才与算力的争夺。</p>
    <p>当然，风险也在：知情人士提醒，谈判虽近收尾，最后阶段仍可能改动部分交易细节；而大额算力投入一旦碰上模型迭代不及预期，现金流压力会迅速显现。</p>

    <h2>六、总结</h2>
    <p>一句话：DeepSeek 用至少 800 亿元、可能逼近 1000 亿元的融资，把"开源模型 + 国产算力 + 2027 年 IPO"绑成一条完整路径——这不只是一次融资，而是中国 AI 头部玩家从技术竞赛转向资本竞赛的发令枪。</p>

  </div>

  <div class="bottom-cta">
    <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    <p>📌 主要信息来源：<a href="https://www.ithome.com/1/009/990.htm" target="_blank" rel="noopener">IT之家：消息称 DeepSeek 接近完成至少 800 亿元融资（据彭博社）</a> · <a href="https://www.deepseek.com/news/v4-preview" target="_blank" rel="noopener">DeepSeek 官方：DeepSeek-V4 发布</a> · <a href="https://aihot.news/items" target="_blank" rel="noopener">AIHOT 精选</a></p>
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
