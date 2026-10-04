#!/usr/bin/env python3
"""Generate featured-2026-10-04.html (Google Project Suncatcher) reusing the 10-03 shell/CSS."""
import re

TODAY = '2026-10-04'
tpl = open('featured-2026-10-03.html', encoding='utf-8').read()

head_part = tpl[:tpl.index('  <div class="featured-hero">')]
tail_part = tpl[tpl.rindex('<footer>'):]

TITLE = 'Google 把 TPU 送进轨道：Project Suncatcher 原型卫星上天，太空数据中心迈出第一步'
DESC = ('Google 10 月 1 日用 SpaceX Transporter-18 拼车任务把 Project Suncatcher 原型卫星送入低地球轨道，'
        '卫星由 Planet 合造、内装 4 颗 TPU、运行开源模型 Gemma；低轨可获最多 8 倍地面太阳能，'
        '2027 年计划双星激光互联。')

head_part = re.sub(r'<title>.*?</title>', f'<title>{TITLE} | suduai.top</title>', head_part, count=1, flags=re.S)
head_part = re.sub(r'(<meta name="description" content=").*?(">)', lambda m: m.group(1) + DESC + m.group(2),
                   head_part, count=1, flags=re.S)

BODY = f'''
  <div class="featured-hero">
    <img src="images/featured-{TODAY}-1.jpg" alt="Google Project Suncatcher 官方主视觉：低轨太阳能卫星集群构想 | blog.google">
    <div class="featured-meta">
      <span>📖 8 分钟</span>
      <span>📅 {TODAY}</span>
      <span>🛰️ 前沿探索</span>
    </div>
  </div>

  <h1>{TITLE}</h1>

<div class="article-body">

    <h2>一、导语：一颗冰箱大小的卫星，和四颗 TPU</h2>
    <p>10 月 1 日，Google 的 Project Suncatcher 原型卫星搭着 SpaceX 的 Transporter-18 拼车任务进入低地球轨道。这颗卫星由 Google 与行星影像公司 Planet 合作建造，内部装了 <span class="key-number">4 颗</span> Google 自研的 TPU 芯片，跑的是开源模型 Gemma。Google 研究团队当天确认已与卫星建立联系、状态正常。体量不大，但方向很清楚：把机器学习里最耗电的那部分，先从地面搬到全天都能晒到太阳的地方。</p>

    <h2>二、背景分析：AI 的瓶颈，正在从算法变成「电」</h2>
    <p>站在 2026 年看，AI 数据中心最大的对手不是同行，而是电和地。训练一个前沿模型动辄要几万千瓦的供电，而欧美多地的电网和社区对新建数据中心的抵触越来越强。Google 自己算过一笔账：在低地球轨道上，卫星几乎全程处在日照中，能发出的太阳能最多是地面的 <span class="key-number">8 倍</span>；散热也只需面对真空里的辐射问题，不必和城市争水争地。</p>
    <p>所以 Project Suncatcher 不是突发奇想，而是一场「从终点往回推」的长线研究——先在 Joule 上发同行评审论文，再把第一颗原型送上天，用真实数据替换纸面假设。文章作者 Travis Beals 是 Google「Paradigms of Intelligence」团队的高级总监。</p>

    <h2>三、核心内容：上天要过哪三关</h2>
    <p>Google 在官方博客里把难点拆成了三块。</p>
    <p>第一关，硬件能不能活下来。火箭从地面到低轨只要约 <span class="key-number">10 分钟</span>，飞行器要承受最高 <span class="key-number">10 倍</span>重力加速度，单个芯片承受的力可达 <span class="key-number">50 到 100 倍</span>重力。为此团队在三个轴向都做了振动测试。更难的是辐射：他们把 TPU 送进加州大学戴维斯分校 Crocker 核实验室的质子束设备，一边跑真实负载一边监测位翻转等错误，结论是 Trillium 代 TPU 能扛住「超过一次 <span class="key-number">5 年</span>太空任务」的总电离剂量。</p>
    <p>第二关，散热。太空没有空气，热量只能靠辐射器散掉，Google 的方案是热管加辐射器，并在地面的热真空舱里反复验证。也正因为散热受限，原型卫星上那颗 Gemma 每次只能连续运行 <span class="key-number">15 分钟</span>。</p>

    <div class="inline-img">
      <img src="images/featured-{TODAY}-2.jpg" alt="Transporter-18 发射时现场观众用手机拍摄火箭升空 | blog.google">
      <div class="caption">Google 原型卫星搭乘 SpaceX Transporter-18 拼车任务发射，现场观众拍摄火箭升空（来源：blog.google）</div>
    </div>

    <p>第三关，连通。未来设想是每颗卫星携带数十颗 TPU，多颗卫星用激光互联。难点在于：现有空间激光技术擅长「远距离、低带宽」，而 Project Suncatcher 要的是「极短距离、极高带宽」——精度要求被形容为「像在两处都高速运动的情况下，从数英里外打中一枚硬币」。这一步要等 <span class="key-number">2027 年</span>两颗卫星同时在轨时才能验证。</p>

    <h2>四、各方反应：一次「先拿数据」的务实下注</h2>
    <p>这是 Google 第一次把 TPU 真正送上轨道，此前项目只停留在论文和地面实验。对航天界来说，Google 的入场让「轨道数据中心」这条赛道更热了。外界最直接的疑问有两个：一是性价比——把芯片送上天的发射成本，能不能被 8 倍太阳能和免地租省回来；二是在辐射和温差夹击下，芯片的寿命与良率会被打掉多少。Google 给出的回应是务实路线：先收集在轨数据，再谈规模化。</p>

    <blockquote>
      「就像早期对自动驾驶和量子计算的研究，需要多年的实验才能走到实用系统一样，探索太空计算，也要从谨慎、克制的第一步开始。」
      <footer>— Travis Beals，Google「Paradigms of Intelligence」高级总监（译）</footer>
    </blockquote>

    <h2>五、深度解读：算力开始「离开地面」</h2>
    <p>第一层，是能源逻辑。当地面电力成为 AI 扩张的硬约束，「把算力搬到有近乎无限阳光的地方」就不再是科幻，而是一种工程选择。</p>
    <p>第二层，是竞争格局。Google 手里同时握着 TPU、Gemma 开源模型和 Planet 的卫星资源，这条链只有极少数公司能拼齐。太空算力一旦跑通，标准的定义权会落在先把芯片送上去的一方。</p>
    <p>第三层，是节奏。Google 反复强调这是「长线 moonshot」，2027 年的双星只是验证激光互联，距离真正规模化还有很长。但方向已经不再含糊：AI 的算力边界，可能要从地球的电力账本上解绑。</p>

    <h2>六、总结</h2>
    <p>一句话：Google 用一颗装了 4 颗 TPU 的原型卫星，把「太空数据中心」从论文推到了轨道上——AI 算力的下一个边界，也许不在沙漠里，而在头顶。</p>

  </div>

  <div class="bottom-cta">
    <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    <p>📌 主要信息来源：<a href="https://blog.google/innovation-and-ai/models-and-research/google-research/project-suncatcher-prototype/" target="_blank" rel="noopener">Google 官方博客：Our Project Suncatcher prototype satellite is in orbit.</a> · <a href="https://blog.google/innovation-and-ai/models-and-research/google-research/google-project-suncatcher-facts/" target="_blank" rel="noopener">Behind Project Suncatcher: Google's Moonshot to Put AI in Space</a> · <a href="https://aihot.news/items/ljyywltag6vvryw193ryz7lgd" target="_blank" rel="noopener">AIHOT 精选</a></p>
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
