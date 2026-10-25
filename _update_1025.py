#!/usr/bin/env python3
"""Update 2026-10-25: featured page + nf-items + banner + card + prev list + review dates + daily nav."""
import re
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-10-25', TODAY
OLD = '2026-10-24'

TITLE = 'Kimi K3.1 Pro：3T 级开源权重、100 万上下文，Terminal-Bench 只差 Claude Opus 5.5 不到 1 分'
LABEL = '模型发布'

CARD_P = ('月之暗面 10 月 23 日发布 Kimi K3.1 Pro：3T 级开放权重、100 万 token 上下文，'
          '在 Terminal-Bench 4.0 拿到 65.7%，只比 Claude Opus 5.5 的 66.4% 低 0.7 分，把 GPT-6 Astra 的 58.2% 甩开 7.5 分。'
          'SWE Marathon 51.7%、Agents\' Last Exam 43.2%、Humanity\'s Last Exam 78.0 三项直接第一。'
          'API 价格从 K3 几乎砍半到每百万 token 输入 13 元、输出 68 元，完整权重承诺 11 月 4 日前释出——'
          '开源模型第一次在通用 agent 榜上贴住闭源旗舰。')

# ---------------- featured page ----------------
ARTICLE = """    <h2>一、导语：开源权重第一次贴住闭源旗舰</h2>
    <p>10 月 23 日，月之暗面发布 Kimi K3.1 Pro。三个数字放在一起就够说明问题：<span class="key-number">3T</span> 级参数规模、<span class="key-number">100 万</span> token 上下文、<span class="key-number">11 月 4 日</span>前释出完整权重。在 Terminal-Bench 4.0 上它拿到 <span class="key-number">65.7%</span>，Claude Opus 5.5 是 66.4%，GPT-6 Astra 是 58.2%。</p>
    <p>这不是「开源模型又进步了」那种进步。过去两年，开放权重模型的标准剧本是：榜单上落后半个身位，价格便宜一个数量级，靠性价比活在闭源旗舰的阴影里。K3.1 Pro 把这个剧本改了一半——价格仍然便宜，但在编码 agent、长程任务、含工具的知识问答上，它已经站在同一张桌子边上。</p>

    <h2>二、背景：不是新模型，是一次把后训练算力堆到底的重训</h2>
    <p>官方博客写得很直白：K3.1 Pro 是 Kimi K3 的后训练版本，但后训练算力「大幅增加」。为了让这套算力真的换成能力，月之暗面重做了整个栈——RL 框架、长上下文推理、训练效率、沙箱基础设施、rollout 调度，以及一套共享的环境质量校验平台，目标是让每一份 RL 算力都带来稳定可预测的回报。</p>
    <p>这条路线和 2026 年开源阵营的整体节奏对得上。DeepSeek 的 V4.1 Flash 系列、智谱 GLM-5.3 都在这几个月内密集迭代，方向一致：基座不动，把后训练和 agent 环境做到极致。差别在于 K3.1 Pro 把规模推到了 3T 级，并把上下文拉到 100 万 token——这两个指标过去是闭源模型的护城河。</p>
    <blockquote>
      “我们优化了栈的每一层，让 RL 算力的每一次增量都带来稳定、可预测的回报。结果是 K3.1 Pro 在每个领域都取得了一致的提升。”
      <footer>—— Moonshot AI 官方技术博客《Kimi K3.1 Pro: Advancing Open Intelligence》</footer>
    </blockquote>

    <h2>三、核心内容：榜单数据与定价</h2>
    <p>先看最硬的几组对比。Terminal-Bench 4.0 测的是编码 agent 在真实、资源受限的终端任务上能否通过严格的任务级测试，K3.1 Pro 65.7%，落后 Opus 5.5 仅 <span class="key-number">0.7</span> 个百分点，领先 GPT-6 Astra <span class="key-number">7.5</span> 分。SWE Marathon 上它以 <span class="key-number">51.7%</span> 直接排第一，Opus 5.5 是 46.3%。Agents' Last Exam 43.2%，同样第一。Humanity's Last Exam（含工具）78.0，Opus 5.5 67.7。</p>
    <div class="inline-img">
      <img src="images/featured-2026-10-25-2.jpg" alt="Kimi K3.1 Pro 官方基准测试汇总图：Terminal-Bench 4.0、SWE Marathon、BenchCAD、OfficeQA Pro v2 等 14 项对比">
      <div class="caption">官方基准汇总：蓝色为 K3.1 Pro。编码与 agent 类任务多为第一或逼近第一，Terminal-Bench-Science 仍明显落后。图源 kimi.com 官方技术博客</div>
    </div>
    <p>也有打不过的地方，博客没藏。Terminal-Bench-Science 0.1 上 K3.1 Pro 只有 <span class="key-number">38.1%</span>，GPT-6 Astra 是 68.1%，Opus 5.5 是 63.3%——差了近 30 分。ChartoGraphy 90.2 对 GPT-6 Astra 的 91.0，GDPval-AA 1846 对 Opus 5.5 的 1866，都是「接近但没赢」。BenchCAD（多视图渲染反推 CAD 代码）92.7%，Opus 5.5 96.2%。</p>
    <p>垂直场景的数据更值得看。财务方向，OfficeQA Pro v2 拿 <span class="key-number">64.4</span> 分称 SOTA，内部财务研究基准比 K3 提升 11.6 分，商业运营模拟提升约 <span class="key-number">4.2 倍</span>。幻觉率这块，官方内部压力测试 Kimi Hallu Bench Hard 上，claim 级幻觉率从 K3 的 <span class="key-number">23.4%</span> 降到 <span class="key-number">8.3%</span>。3D 方向则顺手把产品做了：3D Make 已在 kimi.com 和 App 上线，可直接预览编辑、导出 3D 打印文件或视频。</p>
    <div class="inline-img">
      <img src="images/featured-2026-10-25-3.jpg" alt="Kimi 3D Make 产品界面截图：自然语言生成 3D 模型，首页展示建筑、机械、珠宝等模板">
      <div class="caption">Kimi 3D Make 实际界面：输入一句话生成可编辑 3D 模型，支持导出 3D 打印与视频。图源 kimi.com 官方博客</div>
    </div>
    <p>价格是这次最直接的信号。API 每百万 token 输入 <span class="key-number">13 元</span>、输出 <span class="key-number">68 元</span>，相比 K3 基本砍半；OpenRouter 上的挂牌价是 $2 / $10。同时推出 K3.1 Pro Highspeed，速度约 2–3 倍、价格翻倍。上架渠道一次性铺满：kimi.com、Kimi App（iOS / Android / HarmonyOS）、Kimi Work 桌面端 3.1.0+、Kimi Code（<code>/model</code> 切换）、Kimi API，企业版默认关闭需管理员开启。</p>

    <h2>四、各方反应：第 4 名，和一个被主动砍掉的能力</h2>
    <p>第三方评测机构 Artificial Analysis 给出的 Intelligence Index 是 <span class="key-number">55</span> 分，排第 4，比 Kimi K3 高 11 分，前面只剩 Claude Opus 5.5、Claude Sonnet 5.5 和 Muse Wonder Full。对一个权重即将公开的模型来说，这个位置此前没有出现过。OpenRouter 当天就挂上了 1M 上下文的多模态版本，定位写的是「长程编码与 agent 任务」。</p>
    <p>真正有意思的是安全那一节的自曝。博客承认：随着后训练规模上去，模型的漏洞研究能力一路走高，追查后发现网络攻击相关内容混在中训练语料和 RL 环境里。于是他们在两个训练阶段都做了数据清洗，再拿内部基准 xdev-bench-hard 测——不清洗的 checkpoint 能解 <span class="key-number">90.5%</span> 的题目（pass@3），清洗后的正式版是 <span class="key-number">81.0%</span>。也就是说，他们主动砍掉了近 10 个百分点的攻击能力才敢开源。</p>
    <p>博客同时给了两条边界：不发布会推高网络攻击能力绝对前沿的权重；但会逐步提高开放权重里的这部分能力，理由是防御方需要能在自己控制的机器上审代码。这话在 Black October 刚过去的语境里，等于往火上又添了一点柴——同一个星期，AI 辅助挖出的 PHP 核心 RCE 正在被数百万次尝试利用。</p>

    <h2>五、深度解读：三个被改写的成本项</h2>
    <p>第一是部署成本。3T 级参数、开放权重，意味着有能力自建集群的团队第一次可以在前沿水平上做私有部署。对金融、医疗、政务这类数据不能出境的场景，这不是「便宜一点」，而是「能不能用」的问题。</p>
    <p>第二是上下文经济学。100 万 token 配上 agent 能力，改的是工作流的形状——不是把长文档塞进去做摘要，而是让模型在一个仓库、一份财报、一整套 CAD 工程里连续跑几十步。K3.1 Pro 在长程编码上的提升（内部 Kimi Code Bench 3.0 从 55.95% 到 61.2%）就来自这里。博客里那个「人形行走模拟器」的例子很典型：167 个任务、420 次独立评审，模型发现奖励塑形无效后没有继续调奖励，而是去跑开环探针，找出并修正了肩部肌肉力臂计算里的 <span class="key-number">36</span> 处错误，最终让人形连续行走 11.2 秒。</p>
    <p>第三是开源与安全的定价权之争。K3.1 Pro 把「开源模型能不能碰前沿」这个问题从能力层面挪到了治理层面：能力已经有了，剩下的是发布者愿意放出多少、监管愿意接受多少。月之暗面选了「先砍攻击能力再开源」这条路，这套做法会成为后续所有中国实验室的参照系。</p>

    <h2>六、总结</h2>
    <p>一句话：Kimi K3.1 Pro 用 <span class="key-number">65.7%</span> 的 Terminal-Bench 成绩和 11 月 4 日的权重日期证明，开放权重模型已经能站在闭源旗舰旁边——接下来决定格局的，不再是榜单差几分，而是有多少团队真的会把它部署到自己的机房里。</p>"""

SOURCES = ('<p>📌 主要信息来源：'
           '<a href="https://www.kimi.com/blog/kimi-k3-1-pro" target="_blank" rel="noopener">Moonshot AI：Kimi K3.1 Pro 官方技术博客（基准、定价、安全策略）</a> · '
           '<a href="https://artificialanalysis.ai/articles/kimi-k3-1-pro-launch-benchmarks" target="_blank" rel="noopener">Artificial Analysis：K3.1 Pro 评测（Intelligence Index 55）</a> · '
           '<a href="https://x.com/OpenRouter/status/2113699820124934334" target="_blank" rel="noopener">OpenRouter：K3.1 Pro 上架与定价</a> · '
           '<a href="https://aihot.news/items" target="_blank" rel="noopener">AIHOT 精选</a></p>')

DESC = ('月之暗面发布 Kimi K3.1 Pro：3T 级开放权重、100 万 token 上下文，Terminal-Bench 4.0 得 65.7%（Opus 5.5 为 66.4%、'
        'GPT-6 Astra 58.2%），SWE Marathon 51.7% 第一；API 每百万 token 输入 13 元、输出 68 元，完整权重 11 月 4 日前释出。')

HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITLE__ | suduai.top</title>
  <meta name="description" content="__DESC__">
  <link rel="stylesheet" href="css/style.css">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="favicon.png">
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Z33SFE6V0H"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-Z33SFE6V0H');
</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8469472392292447" crossorigin="anonymous"></script>
<style>
.content-page { max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }
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
.article-body code { background: #f3f4f6; padding: 0.1rem 0.35rem; border-radius: 4px; font-size: 0.9em; }
.inline-img { margin: 1.5rem 0; text-align: center; }
.inline-img img { max-width: 100%; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
.inline-img .caption { font-size: 0.82rem; color: #9ca3af; margin-top: 0.4rem; }
.bottom-cta { margin: 3rem 0 1rem; text-align: center; }
.bottom-cta .affiliate-btn { display: inline-block; padding: 0.8rem 2rem; }
.source-link { color: #6b7280; font-size: 0.85rem; margin-top: 1rem; }
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
    <img src="images/featured-__TODAY__-1.jpg" alt="Kimi K3.1 Pro 官方发布主视觉（kimi.com 官方技术博客素材）">
    <div class="featured-meta">
      <span>📖 9 分钟</span>
      <span>📅 __TODAY__</span>
      <span>🤖 模型发布</span>
    </div>
  </div>

  <h1>__TITLE__</h1>

<div class="article-body">

__ARTICLE__

  </div>

  <div class="bottom-cta">
    <a href="daily-__TODAY__.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    __SOURCES__
  </div>

</div>

<footer>
  <div class="container">
    <p>AI快报站 © 2026</p>
    <p style="margin-top:2px;"><a href="privacy-policy.html">隐私政策</a></p>
  </div>
</footer>

</body>
</html>"""

page = (HEAD.replace('__TITLE__', TITLE)
            .replace('__DESC__', DESC)
            .replace('__TODAY__', TODAY)
            .replace('__ARTICLE__', ARTICLE)
            .replace('__SOURCES__', SOURCES))
open(f'featured-{TODAY}.html', 'w', encoding='utf-8').write(page)

# ---------------- index.html ----------------
nf_items = open('_nf_items_output.txt', encoding='utf-8').read().strip()
assert nf_items.count('class="nf-item"') == 50, nf_items.count('class="nf-item"')

idx_path = 'index.html'
idx = open(idx_path, encoding='utf-8').read()

s = idx.find('id="nf-scroll"')
content_start = idx.find('>', s) + 1
script_marker = '<script>\n// AI 热点分类过滤'
script_start = idx.find(script_marker, content_start)
assert script_start > 0, 'JS filter marker not found'
tabs_kept = idx.count('<div class="nf-tabs"')
idx = idx[:content_start] + '\n' + nf_items + '\n\n' + idx[script_start:]


def swap_banner(html):
    m = re.search(r'<a href="daily-\d{4}-\d{2}-\d{2}\.html">📰 最新快报：[^<]*→</a>', html)
    assert m, 'banner not found'
    new = f'<a href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>'
    return html.replace(m.group(0), new)


idx = swap_banner(idx)

card_start = idx.index('<div class="featured-card">')
card_end = idx.index('<div class="section-title', card_start)

new_card = f'''<div class="featured-card">
    <div class="featured-badge">今日热议</div>
    <div class="featured-content">
      <div class="featured-label">{LABEL}</div>
      <h2><a href="featured-{TODAY}.html">{TITLE}</a></h2>
      <p>{CARD_P}</p>
      <div class="featured-meta">
        <span>📖 9 分钟</span><span>📅 {TODAY}</span><span>{LABEL}</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="Kimi K3.1 Pro 官方发布主视觉（kimi.com 官方博客素材）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
    </div>
  </div>'''

idx = idx[:card_start] + new_card + '\n' + idx[card_end:]

plist_anchor = '<div class="prev-featured-list">'
plist_pos = idx.index(plist_anchor) + len(plist_anchor)
prev_entry = f'''
            <a href="featured-{TODAY}.html" class="prev-featured-item">
      <span class="prev-date">{TODAY}</span>
      <span class="prev-title">{TITLE}</span>
      <span class="prev-arrow">→</span>
    </a>'''
idx = idx[:plist_pos] + prev_entry + idx[plist_pos:]

n_before = idx.count(f'📅 {OLD}')
idx = idx.replace(f'📅 {OLD}', f'📅 {TODAY}')
print(f'review dates replaced: {n_before}')

assert idx.count('<div class="nf-tabs"') == tabs_kept, 'nf-tabs changed!'
assert idx.count('class="nf-item"') == 50, idx.count('class="nf-item"')
assert 'AI 热点分类过滤' in idx, 'tab filter JS lost!'
assert idx.count('nf-scroll') == 2, idx.count('nf-scroll')
assert f'href="daily-{TODAY}.html">📰 最新快报：{TODAY}（今日 AI 精选 50 条）→</a>' in idx, 'banner mismatch'
assert idx.count(f'featured-{TODAY}.html') == 2, idx.count(f'featured-{TODAY}.html')
assert idx.count(f'📅 {TODAY}') == n_before + 1, idx.count(f'📅 {TODAY}')
open(idx_path, 'w', encoding='utf-8').write(idx)

# ---------------- daily.html ----------------
dl_path = 'daily.html'
dl = open(dl_path, encoding='utf-8').read()
dl = swap_banner(dl)

nav_anchor = '<div class="daily-nav">'
nav_pos = dl.index(nav_anchor) + len(nav_anchor)
nav_entry = f'\n    <a href="daily-{TODAY}.html">📅 {TODAY} 今日快报</a>'
dl = dl[:nav_pos] + nav_entry + dl[nav_pos:]
assert dl.count(f'daily-{TODAY}.html') == 2, dl.count(f'daily-{TODAY}.html')
open(dl_path, 'w', encoding='utf-8').write(dl)

print(f'✅ index.html + daily.html + featured-{TODAY}.html updated (review dates: {n_before})')
