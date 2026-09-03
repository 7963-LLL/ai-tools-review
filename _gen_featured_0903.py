#!/usr/bin/env python3
"""Generate featured-2026-09-03.html — Anthropic Claude Fable 5.1 / Mythos 5.1 launch."""
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-09-03', TODAY

TITLE = 'Claude Fable 5.1 与 Mythos 5.1 同日发布：同一模型两种安全档，缓存读取降价 75%，编码与科学智能体双双破纪录'

hero_img = f'images/featured-{TODAY}-1.jpg'
sci_img = f'images/featured-{TODAY}-2.jpg'

body = f'''
<div class="article-body">

    <h2>一、导语</h2>
    <p><span class="key-number">2026 年 9 月 3 日</span>，Anthropic 一口气发布两款新旗舰：<strong>Claude Fable 5.1</strong> 与 <strong>Claude Mythos 5.1</strong>。严格说它们是<strong>同一个模型</strong>，只是安全护栏不同——Fable 5.1 即日全平台上线，Mythos 5.1 仅通过可信访问计划开放给网络安全与生命科学领域的受信机构。发布中最受关注的一组数字：缓存读取价格下调 <span class="key-number">75%</span> 至每百万 tokens <span class="key-number">0.25 美元</span>，典型负载成本比 Fable 5 低约 <span class="key-number">25%</span>，重度 Agent 场景最高可省 <span class="key-number">45%</span>；科研智能体基准 Terminal-Bench-Science 0.1 得分 <span class="key-number">52.6%</span>，是前代 Fable 5（24.7%）的<strong>两倍以上</strong>。</p>

    <h2>二、背景分析：为什么是「一个模型、两种档位」？</h2>
    <p>Anthropic 上一轮旗舰 Fable 5 发布于今年 8 月，但短短数周内，竞争格局已被彻底改写：OpenAI 的 GPT-5.6 在代码智能体上步步紧逼，DeepMind 同日放出 Gemini 3.8 Flash 系列，而安全层面，监管与客户对「越强越危险」的顾虑也在升温——OpenAI 刚把达到网络安全 Critical 阈值的 Astra 转为受限发布，说明前沿实验室正集体走向「能力越界即上锁」的路线。</p>
    <p>Fable 5.1 / Mythos 5.1 正是对这一压力的直接回应：<strong>把「能力」与「安全档位」解耦</strong>。Fable 5.1 面向大众市场走最强通用路线；Mythos 5.1 则在同一颗模型上放开部分护栏，只给通过审核的网络安全与生物研究机构使用。这样既保住商用竞争力，又让高危能力始终停留在可控人群内。</p>

    <h2>三、核心内容：价格、安全与企业级数据策略</h2>
    <h3>1. 定价：向「缓存读取」开刀，Agent 成本结构生变</h3>
    <p>Fable 5.1 的输入输出单价与 Fable 5 保持一致：每百万 tokens 输入 <span class="key-number">10 美元</span>、输出 <span class="key-number">50 美元</span>。真正的降价来自缓存读取——从每百万 tokens <span class="key-number">1 美元</span>直降到 <span class="key-number">0.25 美元</span>。由于多轮 Agent 任务里模型反复读取已处理过的上下文，缓存读取往往是账单大头，因此典型负载成本下降约 <span class="key-number">25%</span>，长程 Agent 场景最高省近 <span class="key-number">45%</span>。官方同时调整了默认档位：Claude Code 中默认 High effort，Claude Cowork 与 claude.ai 默认 Medium——用更低档位跑出旧旗舰同级结果，是这次性价比策略的核心。</p>

    <h3>2. 企业数据：Enterprise Frontier Safeguards（EFS）</h3>
    <p>针对企业客户最在意的数据留存问题，Anthropic 推出 <strong>EFS</strong>：模型运行数据存放在<strong>完全由客户掌控的云基础设施</strong>中，而非 Anthropic 的服务器上，等效于零数据留存（ZDR）策略。EFS 将于今年秋季开始分批向企业开放；在它落地前，合格客户可直接以零数据留存方式使用 Fable 5.1。</p>

    <h3>3. 安全：误报率大降，漏洞「可发现不可利用」</h3>
    <p>新护栏把网络安全场景的误报（把良性内容当威胁拦截）减少了 <span class="key-number">60%</span>。值得注意的是，Anthropic 明确承认 Fable 5.1 已能<strong>发现软件漏洞</strong>，但被设计为无法据此开发利用工具；在生物领域，配合美国政府的访问计划，Mythos 5.1 的高级生物能力只向受信科学家开放，报名即将启动。官方评估认为 Mythos 5.1 仍未触及负责任扩展政策（RSP）中的下一风险等级，因此沿用 Mythos 5 的安全部署方案。</p>

    <div class="inline-img">
      <img src="{sci_img}" alt="Magellan 雷达图像：金星火山亮锥与放射状熔岩流 | Anthropic 官方">
      <div class="caption">官方展示的科学应用之一：基于雷达与 DEM 数据的行星测绘研究</div>
    </div>

    <h3>4. 基准：科学、编码、办公全面刷新</h3>
    <p>对照表（Fable 5.1 / Fable 5 / Opus 5 / GPT-5.6）：科研智能体 Terminal-Bench-Science 0.1 为 <span class="key-number">52.6% / 24.7% / 29.0% / 22.4%</span>；编码 Terminal-Bench 4.0 为 <span class="key-number">55.8%</span>（放开护栏的 Mythos 5.1 达 <span class="key-number">60.9%</span>），Fable 5 仅 42.0%、Opus 5 为 52.3%；知识工作 GDPval-AA v2 得分 <span class="key-number">1853</span>，高于 Fable 5 的 1723；Humanity's Last Exam 无工具 <span class="key-number">60.9%</span>、带工具 <span class="key-number">65.0%</span>；自动化办公 AutomationBench <span class="key-number">31.4%</span>，接近 Fable 5（17.1%）的两倍。</p>

    <blockquote>
      「Claude Fable 5.1 将比 Fable 5 便宜约 25%（按 token 计费的典型负载）；在高度 Agentic 的工作中，节省往往更大——最高约 45%。」
      <footer>— Anthropic 官方发布《Introducing Claude Fable 5.1 and Claude Mythos 5.1》（2026-09-03）</footer>
    </blockquote>

    <h2>四、各方反应</h2>
    <p><strong>量化交易巨头 Jane Street</strong>（量化研究主管 Craig Falls）：「内部基准里 Fable 5.1 解决的编码问题比 Fable 5 和 Opus 5 都多，交易直觉上达到 SOTA；以前模型跑久了会变得难以跟踪，Fable 5.1 在长任务中始终可读。」</p>
    <p><strong>Cognition（Devin 团队）</strong>：「我们将在发布当天把 Devin 里的 Opus 5 流量切到 Claude Fable 5.1——它在我们测试中与 Fable 5 打平或略胜。」<strong>MongoDB</strong> 工程师则总结为「Fable 级智能、Opus 级定价、Sonnet 级速度，测试中约为 Opus 5 的两倍速、一半 token」。</p>
    <p><strong>第三方榜单快速跟进</strong>：同一批 50 条热点显示，Artificial Analysis 智能指数已将 Claude Fable 5.1 列为榜首，但同时指出其<strong>每任务成本高于 Fable 5 的特定档位</strong>——性价比叙事仍有待独立验证；Fable 5.1 系统卡同步披露了隐蔽任务识别与监控难度上升等安全发现，提醒社区「更强的模型 = 更难的监管」。</p>

    <h2>五、深度解读：这件事意味着什么？</h2>
    <h3>1. 「缓存读取」成为价格战新战场</h3>
    <p>当各家在输入输出单价上已经卷无可卷，长上下文 Agent 的成本大头——缓存读取——成了下一个主战场。降价 75% 等于把「让模型反复读同一段代码库」的代价打对折，直接利好 Cursor 类、Devin 类深度 Agent 的商业模式，也会倒逼 OpenAI、Google 跟进。</p>
    <h3>2. 安全分级正在成为旗舰发布的标准动作</h3>
    <p>OpenAI 对 Astra 的 Critical 阈值受限发布、Anthropic 的 Mythos 可信访问计划，两条新闻同日出现并非巧合：前沿模型的能力已触及「双用」红线区，实验室们正在用「同一模型 + 分级护栏 + 受信白名单」的方式，把监管风险转化为可控的产品分层。</p>
    <h3>3. 科研智能体或成下一轮竞争叙事</h3>
    <p>Terminal-Bench-Science 的翻倍提升与生命科学访问计划，暗示 Anthropic 认为「AI 科学家」是比「AI 程序员」更大的市场。当模型能自主设计实验、解释数年未解的故障（如 Millennium 内部那个被 Fable 5.1 定位到根因的罕见崩溃），企业级信任的建立方式也会随之改变。</p>

    <h2>六、总结</h2>
    <p>Claude Fable 5.1 与 Mythos 5.1 用「一套模型、两档安全、三线降价」证明：前沿 AI 的竞争，已经从单纯刷分转向能力、成本与可控性的三维博弈。</p>

  </div>
'''

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TITLE} | suduai.top</title>
  <meta name="description" content="2026年9月3日，Anthropic 发布 Claude Fable 5.1 与 Claude Mythos 5.1：同一模型两种安全档位，缓存读取降价75%至每百万tokens 0.25美元，科研智能体 Terminal-Bench-Science 得分52.6%较前代翻倍，Mythos 5.1 仅向网络安全与生命科学可信访问计划开放。">
  <link rel="stylesheet" href="css/style.css">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="favicon.png">
<style>
.content-page {{ max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }}
.key-number {{ color: #2563eb; font-weight: 700; font-size: 1.1em; }}
blockquote {{ border-left: 4px solid #2563eb; margin: 1.5rem 0; padding: 0.8rem 1.2rem; background: #f8fafc; border-radius: 0 8px 8px 0; font-style: italic; color: #374151; }}
blockquote footer {{ margin-top: 0.5rem; font-size: 0.85rem; color: #6b7280; }}
.featured-hero {{ margin-bottom: 2rem; }}
.featured-hero img {{ width: 100%; max-height: 400px; object-fit: cover; border-radius: 12px; }}
.featured-meta {{ color: #6b7280; font-size: 0.9rem; margin: 1rem 0; display: flex; gap: 1.5rem; }}
.featured-meta span {{ display: flex; align-items: center; gap: 0.3rem; }}
.article-body h2 {{ font-size: 1.4rem; margin: 2rem 0 1rem; color: #111827; border-left: 4px solid #2563eb; padding-left: 0.8rem; }}
.article-body h3 {{ font-size: 1.15rem; margin: 1.5rem 0 0.8rem; color: #1f2937; }}
.article-body p {{ line-height: 1.8; margin-bottom: 1rem; color: #374151; }}
.article-body ul {{ margin: 1rem 0; padding-left: 1.5rem; }}
.article-body li {{ margin-bottom: 0.5rem; line-height: 1.7; color: #374151; }}
.inline-img {{ margin: 1.5rem 0; text-align: center; }}
.inline-img img {{ max-width: 100%; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }}
.inline-img .caption {{ font-size: 0.82rem; color: #9ca3af; margin-top: 0.4rem; }}
.bottom-cta {{ margin: 3rem 0 1rem; text-align: center; }}
.bottom-cta .affiliate-btn {{ display: inline-block; padding: 0.8rem 2rem; }}
.source-link {{ color: #6b7280; font-size: 0.85rem; margin-top: 1rem; }}
</style>
</head>
<body>

<header>
  <div class="container">
    <a href="/" class="logo">AI<span>快报</span></a>
    <nav>
      <a href="/">首页</a>
      <a href="chatgpt-vs-claude.html">ChatGPT vs Claude</a>
      <a href="best-ai-writing-tools.html">写作</a>
      <a href="best-ai-image-tools.html">图像</a>
      <a href="best-ai-coding-tools.html">编程</a>
      <a href="best-ai-video-tools.html">视频</a>
      <a href="best-ai-voice-tools.html">语音</a>
      <a href="daily.html">每日快报</a>
      <a href="about.html">关于</a>
    </nav>
  </div>
</header>

<div class="content-page">

  <div class="featured-hero">
    <img src="{hero_img}" alt="Claude Fable 5.1 与 Claude Mythos 5.1 官方发布横幅 | Anthropic">
    <div class="featured-meta">
      <span>📖 10 分钟</span>
      <span>📅 {TODAY}</span>
      <span>🤖 模型发布/更新</span>
    </div>
  </div>

  <h1>{TITLE}</h1>

{body}

  <div class="bottom-cta">
    <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    <p>📌 主要信息来源：<a href="https://www.anthropic.com/claude-fable-and-mythos-5-1" target="_blank" rel="noopener">Anthropic 官方发布：Introducing Claude Fable 5.1 and Claude Mythos 5.1</a> · <a href="https://x.com/rohanpaul_ai/status/2094873718237565197" target="_blank" rel="noopener">Fable 5.1 系统卡要点（X 线程）</a> · <a href="https://x.com/ArtificialAnlys/status/2094881171066978525" target="_blank" rel="noopener">Artificial Analysis 智能指数评测（X）</a></p>
  </div>

</div>

<footer>
  <div class="container">
    <p>AI快报站 © 2026</p>
    <p style="margin-top:2px;"><a href="privacy-policy.html">隐私政策</a></p>
  </div>
</footer>

</body>
</html>'''

fname = f'featured-{TODAY}.html'
open(fname, 'w', encoding='utf-8').write(html)
print(f'✅ Generated {fname}')
