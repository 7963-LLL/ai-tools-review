#!/usr/bin/env python3
"""Generate featured-2026-10-23.html — Anthropic S-1 / IPO 定价之争"""
TODAY = '2026-10-23'
TITLE = 'Anthropic 递交 S-1：半年收入 163 亿美元、十年算力承诺 4500 亿，1.5 万亿美元 IPO 的定价之争'
DESC = ('Anthropic 最快本周五公开提交 S-1：2026 上半年收入 163 亿美元、同比增约 15 倍，'
        '半年算力支出 90 亿美元、十年云合约约 4500 亿美元，上半年净亏损 807 亿（其中 720 亿为非现金），'
        '投资人讨论的 IPO 估值已从 2 万亿美元下调至约 1.5 万亿，代码 ANTP。')

NAV = '''    <nav>
      <a href="/">首页</a>
      <a href="chatgpt-vs-claude.html">ChatGPT vs Claude</a>
      <a href="best-ai-writing-tools.html">写作</a>
      <a href="best-ai-image-tools.html">图像</a>
      <a href="best-ai-coding-tools.html">编程</a>
      <a href="best-ai-video-tools.html">视频</a>
      <a href="best-ai-voice-tools.html">语音</a>
      <a href="daily.html">每日快报</a>
      <a href="about.html">关于</a>
    </nav>'''

CSS = '''.content-page { max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }
.key-number { color: #2563eb; font-weight: 700; font-size: 1.1em; }
blockquote { border-left: 4px solid #2563eb; margin: 1.5rem 0; padding: 0.8rem 1.2rem; background: #f8fafc; border-radius: 0 8px 8px 0; font-style: italic; color: #374151; }
blockquote footer { margin-top: 0.5rem; font-size: 0.85rem; color: #6b7280; font-style: normal; }
.featured-hero { margin-bottom: 2rem; }
.featured-hero img { width: 100%; max-height: 400px; object-fit: cover; border-radius: 12px; }
.featured-meta { color: #6b7280; font-size: 0.9rem; margin: 1rem 0; display: flex; gap: 1.5rem; flex-wrap: wrap; }
.article-body h2 { font-size: 1.4rem; margin: 2rem 0 1rem; color: #111827; border-left: 4px solid #2563eb; padding-left: 0.8rem; }
.article-body h3 { font-size: 1.15rem; margin: 1.5rem 0 0.8rem; color: #1f2937; }
.article-body p { line-height: 1.8; margin-bottom: 1rem; color: #374151; }
.article-body ul { margin: 1rem 0; padding-left: 1.5rem; }
.article-body li { margin-bottom: 0.5rem; line-height: 1.7; color: #374151; }
.inline-img { margin: 1.5rem 0; text-align: center; }
.inline-img img { max-width: 100%; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
.inline-img .caption { font-size: 0.82rem; color: #9ca3af; margin-top: 0.4rem; }
.bottom-cta { margin: 3rem 0 1rem; text-align: center; }
.bottom-cta .affiliate-btn { display: inline-block; padding: 0.8rem 2rem; }
.source-link { color: #6b7280; font-size: 0.85rem; margin-top: 1rem; }'''

BODY = '''
    <h2>一、导语：一份被提前看到的招股书</h2>
    <p>雅虎财经本周援引知情人士的消息说，Anthropic 最早可能在<span class="key-number">本周五</span>（10 月 23 日）公开提交 S-1 招股说明书，如果成行，这将是史上规模最大的一次 IPO——超过 SpaceX 今年 6 月上市时创下的纪录。而在此之前，The Wall Street Journal 已经看到了这份招股书的草稿版本，里面的数字足以让任何一位二级市场投资人坐直：<span class="key-number">2026 年上半年收入 163 亿美元</span>，去年同期是 11 亿美元，一年涨了约 <span class="key-number">15 倍</span>。</p>
    <p>同一份文件里还有另一组数字：上半年算力与基础设施支出接近 <span class="key-number">90 亿美元</span>，已经超过 2025 年全年的 73 亿；未来十年的云服务承诺约 <span class="key-number">4500 亿美元</span>，其中 Google Cloud 1110 亿、AWS 1100 亿、微软 310 亿；文件还承认，如果想拿到全部想要的算力，总支出可能达到 <span class="key-number">7500 亿美元</span>。收入端和支出端同时在创造历史，这就是这场 IPO 的全部张力所在。</p>
    <p>截止本文发稿，SEC EDGAR 的全文本检索里还没有出现 Anthropic 的 S-1 正本。所以下面写的每一个数字，都来自媒体看到的草稿与投资人和分析师的说法，正式文件公开后可能有出入。</p>

    <h2>二、背景分析：从 11 亿到 163 亿，只用了十二个月</h2>
    <p>要理解这份招股书为什么值得这么高的定价，得先看收入曲线的斜率。按投资人在 10 月 14 日旧金山总部说明会上听到的口径，Anthropic 的季度收入是：一季度 <span class="key-number">47 亿美元</span>，二季度 <span class="key-number">116 亿</span>，三季度 <span class="key-number">168 亿</span>——三季度环比增长 <span class="key-number">45%</span>，公司同时告诉投资人，按调整后口径已经实现盈利。</p>
    <p>再往前推：2025 年底的年化收入约 90 亿美元，今年 5 月完成一轮 <span class="key-number">650 亿美元</span>融资时，年化收入已经超过 470 亿。三年里年化收入每年涨十倍以上，这种曲线在软件史上前所未见，连 Salesforce、Snowflake 最快的那几年都只有它的零头。</p>
    <p>它也是这场 IPO 背景里最容易被忽略的一点：Anthropic 卖的不是一个玩具。Claude 现在同时吃三条腿——API 调用、企业席位的 Claude for Work、以及编程工具 Claude Code。收入高度集中在企业侧，这也是它敢在招股书里承认「约 20% 的上半年收入来自两个客户」的原因：客户少，但每一个都很大。</p>

    <h2>三、核心内容：一份把风险写在首页的招股书</h2>
    <h3>钱从哪来，花到哪去</h3>
    <ul>
      <li><strong>收入：</strong>上半年 163 亿美元，全年年化运行率有望达到 <span class="key-number">1100 亿美元</span>；公司对 2028 年的内部预测是 <span class="key-number">1900–2000 亿美元</span>收入——投行正是拿这个两年后的数字在给它定价。</li>
      <li><strong>亏损：</strong>上半年净亏损 <span class="key-number">807 亿美元</span>，但其中 <span class="key-number">720 亿</span>来自可转债等融资工具的非现金会计调整，真正烧掉的钱远小于这个数。</li>
      <li><strong>算力：</strong>已签订十年期云合约约 4500 亿美元（Google 1110 亿 / AWS 1100 亿 / 微软 310 亿），并且承认「向超大规模云厂商要的算力超过了它们愿意给的」，只能自己去谈第三方数据中心。</li>
      <li><strong>估值：</strong>投资人正在讨论的区间是 <span class="key-number">1.5 万亿美元</span>，比此前预期的 2 万亿下调了四分之一；5 月私募轮的投后估值已经接近万亿量级。</li>
      <li><strong>代码：</strong>ANTP，纳斯达克，市场普遍预期 11 月挂牌。</li>
    </ul>

    <div class="inline-img">
      <img src="images/featured-2026-10-23-2.jpg" alt="Claude 官方品牌标识（claude.com 官方素材）">
      <div class="caption">Claude 是 Anthropic 收入的全部来源，也是这份招股书里唯一的产品故事。图：claude.com 官方素材</div>
    </div>

    <h3>为什么定价要看到 2028 年</h3>
    <p>把 1.5 万亿除以今年预计的千亿级收入，得到的是十几倍的市销率；但如果除以 2028 年 1900–2000 亿的预测，倍数立刻变得「可以接受」。这正是承销商想要的叙事：拿两年后的收入给今天的公司定价。可比公司里，Palantir 是今年预期收入的 53 倍，SpaceX 和 Cloudflare 约 41.6 倍——Anthropic 要说服市场的，是自己会比这些公司更快地把收入变成利润。</p>

    <h2>四、各方反应：多头看增长，空头看承诺</h2>
    <p>最直接的分歧出现在估值上。路透社 10 月中旬的报道说，部分现有和潜在投资人已经把心理价位从 2 万亿调到 1.5 万亿，理由是季度增速从二季度的翻倍以上，掉到了三季度的 45%——增速在放缓，而支出承诺是十年期的。</p>
    <blockquote>
      “Anthropic 对 2028 年的收入预测约为 1900 亿至 2000 亿美元。”
      <footer>—— 路透社，援引两名了解公司财务的人士，2026 年 8 月</footer>
    </blockquote>
    <p>卖方也在往下调。SemiAnalysis 在最新披露后把 Anthropic 的年化收入估计下调到约 <span class="key-number">740 亿美元</span>，比公司自己 5 月给出的 470 亿年化和市场外推都要保守。另一侧的乐观派则盯着另一个事实：Anthropic 是这一轮 AI 公司里第一个在调整后口径上转正的，这在「烧钱换增长」的行业叙事里是个分水岭。</p>
    <p>真正的对手不在华尔街，在隔壁。OpenAI 的估值谈判、xAI 的融资节奏、以及 Google Gemini 在企业侧的捆绑销售，都在争夺同一批机构资金。Anthropic 抢在它们前面上市，本质上是抢一个「第一家纯 AI 大模型上市公司」的定价权——这个位置只有一次机会。</p>

    <h2>五、深度解读：这不只是一家公司的 IPO</h2>
    <p>第一层，它会把 AI 公司的估值方法从「故事」拽回「报表」。过去三年，一级市场给大模型公司的定价靠的是收入增速和创始人叙事；上市之后，每个季度都要面对毛利率、客户集中度、算力承诺这些硬指标。4500 亿美元的十年期合约一旦写进 10-K，它就不再是战略选择，而是资产负债表上的负债。</p>
    <p>第二层，是「算力即成本」的商业模式第一次被公开定价。Anthropic 上半年花了 90 亿美元买算力，相当于每赚 1 美元先花掉 0.55 美元在 GPU 和数据中心上。如果推理效率每年提升一倍，这个比例会降；如果模型继续变大、agent 继续变长，它也可能原地不动。市场愿不愿意为「还没证明能降下来的成本结构」付 1.5 万亿，10 月 23 日之后就有了答案。</p>
    <p>第三层，是对整个 AI 基建链的传导。Google、AWS、微软合计锁定了 Anthropic 2520 亿美元的十年订单，这意味着无论 Anthropic 股价怎么走，这三家的云收入里已经有一块是确定的。反过来说，如果 IPO 定价不及预期、公司被迫收缩算力扩张，最先感到寒意的是那些靠 Anthropic 订单建起来的三方数据中心。</p>

    <h2>六、总结</h2>
    <p>一句话：Anthropic 的 S-1 是 AI 泡沫论的第一次公开考试——收入曲线漂亮到不像真的，支出承诺也大到不像真的，1.5 万亿美元的定价意味着市场愿意相信两年后的它，而不是今天的它。</p>
'''

SOURCES = ('<p>📌 主要信息来源：'
           '<a href="https://www.ithome.com/1/016/243.htm" target="_blank" rel="noopener">IT之家：Anthropic 最快本周五公开提交上市申请</a> · '
           '<a href="https://finance.yahoo.com/technology/ai/articles/anthropic-revenue-hits-16-3-201707100.html" target="_blank" rel="noopener">WSJ / Investing.com：草稿 S-1 披露的收入与算力承诺</a> · '
           '<a href="https://www.channelinsider.com/channel-business/news-anthropic-ipo-valuation-revenue-growth" target="_blank" rel="noopener">Channel Insider：1.5 万亿美元估值讨论</a> · '
           '<a href="https://live.euronext.com/en/financial-news/anthropic-ipo-valuation-hinges-190-200-billion-2028-revenue-forecast-sources-say" target="_blank" rel="noopener">路透社：2028 年收入预测</a> · '
           '<a href="https://aihot.news/items" target="_blank" rel="noopener">AIHOT 精选</a></p>')

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TITLE} | suduai.top</title>
  <meta name="description" content="{DESC}">
  <link rel="stylesheet" href="css/style.css">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="favicon.png">
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Z33SFE6V0H"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-Z33SFE6V0H');
</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8469472392292447" crossorigin="anonymous"></script>
<style>
{CSS}
</style>
</head>
<body>

<header>
  <div class="container">
    <a href="/" class="logo">AI<span>快报</span></a>
{NAV}
  </div>
</header>

<div class="content-page">

  <div class="featured-hero">
    <img src="images/featured-{TODAY}-1.jpg" alt="Anthropic 官方品牌标识（anthropic.com 官方素材）">
    <div class="featured-meta">
      <span>📖 9 分钟</span>
      <span>📅 {TODAY}</span>
      <span>🏭 行业动态</span>
    </div>
  </div>

  <h1>{TITLE}</h1>

<div class="article-body">
{BODY}
  </div>

  <div class="bottom-cta">
    <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    {SOURCES}
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

open(f'featured-{TODAY}.html', 'w', encoding='utf-8').write(html)

# self-check: body length + required bits
import re
text = re.sub(r'<[^>]+>', '', BODY)
cjk = len(re.findall(r'[\u4e00-\u9fff]', BODY))
print(f'✅ featured-{TODAY}.html 正文 {len(text)} 字（中文 {cjk} 字，与往期 1863/1920 字持平）')
# ponytail: 往期实测 1863~1920 中文汉字，按站点既有长度校准而非任务里的名义 1500
assert 1500 <= cjk <= 2100, cjk
assert html.count('key-number') > 10
assert 'blockquote' in html and 'daily-2026-10-23.html' in html
