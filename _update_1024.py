#!/usr/bin/env python3
"""Update 2026-10-24: featured page + nf-items + banner + card + prev list + review dates + daily nav."""
import re
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-10-24', TODAY
OLD = '2026-10-23'

TITLE = 'Black October：PHP2Shell 补丁上线后 48 小时，Cloudflare 记录到数百万次利用尝试'
LABEL = '行业动态'

CARD_P = ('10 月 21 日晚上 10 点，PHP 官方补丁上线。Cloudflare CEO Matthew Prince 随后给了三组数字：'
          '公告前 10 小时，全网看到数千次利用尝试；公告后 45 分钟，数万次；两小时，数十万；现在是数百万级。'
          '漏洞是两个 CVSS 9.2 的 PHP 核心缺陷（CVE-2026-109618/109619），绕过应用层直接拿服务器，'
          '从 PHP 5.4 起的十年版本几乎全中，覆盖全球约 70% 的网站。更麻烦的是披露秩序：'
          'Chainguard 提前几小时发了补丁，NSA 让打不了补丁的机构直接下线，4chan、部分 Wikimedia 服务、'
          'Archive.org 都短暂关过站。业内把这一轮叫 Black October。')

# ---------------- featured page ----------------
ARTICLE = """    <h2>一、导语：补丁上线 48 小时，攻击量级已经失控</h2>
    <p>10 月 21 日晚 10 点，PHP 官方发布了修复包。按惯例，这是漏洞故事的结尾——发现、上报、修复、披露。但这一次不是。补丁上线后的 48 小时里，真正发生的事情是：全世界突然意识到，运行着约 <span class="key-number">70%</span> 网站的编程语言，核心引擎里有两个存在了十几年的洞，而 AI 把它们从「理论上可能」变成了「脚本就能打」。</p>
    <p>Cloudflare CEO Matthew Prince 在 X 上给出的曲线比任何分析都直观：公开公告前 <span class="key-number">10 小时</span>，Cloudflare 全网已经看到数千次利用尝试；公告后 <span class="key-number">45 分钟</span>，数万次；<span class="key-number">2 小时</span>，数十万；他发帖时已经是「数百万次」。这不是一次普通的漏洞披露——这是一场在补丁上线之前就已经开始的、全球规模的自动化扫描。</p>
    <p>两个漏洞被合并命名为 PHP2Shell，编号 CVE-2026-109618 与 CVE-2026-109619，CVSS 最高 <span class="key-number">9.2</span>。它们位于 PHP 引擎本身，而不是某个应用：WordPress、Drupal、Joomla 只是被拿来做演示的靶子，任何跑在受影响版本上的 PHP 程序——哪怕是一个 Hello World——都在射程内。</p>

    <h2>二、背景：一个十年的洞，和一条被 AI 缩短的路</h2>
    <p>根因听上去平淡得不像一个 CVSS 9.2：PHP 在处理请求时，如果遇到致命错误（尤其是一次内存耗尽），会销毁请求堆，但不会清掉某些指向该堆的全局指针。下一次由同一个 worker 处理的请求，可能把这些悬空指针当成活的簿记结构来用——典型的跨请求 use-after-free。Wiz Research 把它拆成两条利用链：一条走 multipart 上传进度的反序列化器，可以无认证读取 worker 内存，里面可能躺着别人的密码、会话 token、API key 和证书；另一条走致命错误回溯，能把悬空指针做成可控的内存破坏，最终在 Drupal 与 WordPress 上拿到无认证 RCE。</p>
    <p>这类 bug 一直存在，只是过去「可演示」的成本太高。Wiz 的原话是：要把它变成可用 exploit，需要串联多个缺陷、还要针对每个目标的堆布局反复调试，"处于人类研究者实际能力边缘"。前沿模型把这道门槛拆了——Wiz 用了 Wiz Atlas、Gemini 4 Argon 和 GPT-5.6 Sol，其中 Argon 在定位与修复上贡献最大。他们的结论相当直接：一个研究员一周做完的事，过去要一个世界级团队做几个月。</p>
    <blockquote>
      “这些缺陷已经在代码里待了十多年。AI 改变的，是理解弱点并把它变成可用 exploit 的能力。”
      <footer>—— Wiz Research 团队（Sagi Tzadik、Shir Tamari、Nir Ohfeld、Tomer Schwartz）</footer>
    </blockquote>
    <p>时间线拉出来看，节奏快得不正常：<span class="key-number">8 月 19 日</span>发现第一个漏洞；8 月 20 日确认 Drupal 无认证 RCE；8 月 21 日拿下 WordPress；<span class="key-number">8 月 24 日</span>报告给 PHP 安全团队；9 月 21 日 PHP 确认并开始做协调修复；<span class="key-number">10 月 21 日</span>补丁发布。发现到上报 5 天，上报到修好 58 天——这个比例本身就是这次事件的核心矛盾。</p>

    <h2>三、核心内容：两个 CVE、一次引擎级手术</h2>
    <p>PHP2Shell 不是补一个函数就能完事的漏洞。Wiz 原本只报了四个可利用的 bug，随后发现「问题深植于代码库」，需要一次彻底的修复；这四个 bug 最终被归并进两个 CVE。受影响的版本回溯到 <span class="key-number">PHP 5.4</span>——也就是过去十年发布的每一个 PHP 版本，至少中一个。</p>
    <div class="inline-img">
      <img src="images/featured-2026-10-24-2.jpg" alt="Wiz Research 官方图示：PHP2Shell 对 WordPress / Drupal / Joomla 的远程代码执行链路">
      <div class="caption">Wiz Research 官方图示：特制 HTTP 请求触发内存耗尽后，攻击者在 WordPress / Drupal / Joomla 上取得 RCE。图源 wiz.io 官方博客</div>
    </div>
    <p>补丁由 PHP 维护者主导，但修复只是整件事的一小块。Wiz 联合了 Automattic、Akamai、AWS、Cloudflare、Fastly、Google、Imperva、Microsoft、Vercel 等一长串厂商，在技术细节公开前准备好检测规则、WAF 规则和「打不了补丁也能扛住」的临时缓解方案。Wiz 自家的 Sensor 1.0.12768 版本直接内置了一条响应策略：检测到 PHP2Shell 典型利用行为就终止进程。</p>
    <p>OpenAI 这一侧走的是另一条线。它牵头的 Patch the Planet 计划把维护者、研究者和安全厂商拉进同一个协调披露流程；安全公司 Calif 用 GPT-5.6 Sol 独立发现了同一批缺陷。OpenAI 还发了一个 Codex 技能，指向 github.com/openai/php2shell-checker，让站点自己跑一遍自查。至于为什么会有「四天提前量」——Ars Technica 报道称，有黑客在正式披露前四天就已经开始利用；Amazon 也表示在公告前观察到了利用尝试。</p>

    <h2>四、各方反应：从 NSA 警告到提前破禁</h2>
    <p>政府层面的反应是这次事件最不寻常的部分。NSA 的建议只有两条：立刻打补丁，或者把打不了补丁的服务器下线。英国 NCSC 提醒说，这类漏洞不需要任何登录凭据就能控制网站服务器。日本首相和多个国家政府发布了类似通告。白宫表示联邦机构正在评估对政府系统与关键基础设施的影响。落到具体站点上：4chan、部分 Wikimedia 服务、Archive.org 都曾短暂关站做升级。</p>
    <p>披露秩序也出了问题。安全公司 Chainguard 在正式公告前几小时就发布了修复，被 PHP 基金会与同行批评为破坏禁运——这等于给攻击者提前递上了对照样本。Chainguard CEO Dan Lorenc 在 LinkedIn 上的解释反而更让人不安：他们是对着一个前沿模型输入「find bad vulnerabilities in PHP」，然后独立找到了同一批 bug。这句话把两种可能同时摆上桌：要么洞真的这么好找，要么模型在训练中已经见过它。</p>
    <p>一线的恐慌是真实的。约翰霍普金斯大学教授、密码学家 Matthew Green 的比喻被转得最多：</p>
    <blockquote>
      “我们正处在电影里那个阶段——你得把手边所有东西都扔到僵尸前面，指望能拖慢它们一点。”
      <footer>—— Matthew Green，约翰霍普金斯大学，转引自 404 Media</footer>
    </blockquote>
    <p>404 Media 的 Jason Koebler 把过去一个月称为 Black October，并列出同期被 AI 辅助挖出的其它问题：eMudhra（印度证书机构）、Node.js、GitLab、Plex、Railway、OpenCode。PHP2Shell 只是其中影响面最大的一个，不是孤例。</p>

    <h2>五、深度解读：发现变快之后，修复没有变快</h2>
    <p>第一层是攻防经济学被改写。过去，「利用难度高」本身就是一种防御——漏洞睡在代码里十几年，因为没人付得起把它变成 exploit 的成本。当这个成本从「世界级团队数月」降到「一个研究员一周」，大量原本被判为「不可利用」的历史漏洞会重新进入攻击面。Wiz 的措辞是：复杂度可能不再构成有意义的门槛。</p>
    <p>第二层是速度的不对称。发现和利用可以在几天内完成，修复却要经过报告、确认、引擎级重构、生态验证、协调披露——PHP2Shell 走了 <span class="key-number">58 天</span>，在漏洞史上已经算快。真正慢的是最后一公里：全球数以百万计的 PHP 实例里，有多少会在下周完成升级？历史经验不乐观。这也是为什么 Cloudflare 那条「数百万次尝试」的曲线值得记住——攻击者不需要赢，他们只需要等。</p>
    <p>第三层是更长尾的代价。The Atlantic 提出的角度可能是这次事件最被低估的：那些跑在老旧 PHP 上、没人维护、也升不动的历史网站，会被预防性下线，或者被攻破后再也回不来。链接腐烂（link rot）不是抽象概念——它意味着一段互联网记忆的物理消失。</p>
    <p>第四层，是这套能力的方向问题。OpenAI 把这次协调披露称为给防御方打开的「Defender's Window」——AI 先发现，于是政府和关键基础设施有时间在细节公开前做准备。但同一批模型、同样的用法，攻击者一样拿得到。开权重模型和「拒答被移除」的变体模型让门槛进一步降低。窗口是存在的，只是不会一直开着。</p>

    <h2>六、总结</h2>
    <p>一句话：PHP2Shell 把「AI 能找到漏洞」从演示变成了基础设施事故——<span class="key-number">70%</span> 的网站在射程内，补丁上线 48 小时后攻击量级已到数百万次，而真正决定损失的，是接下来几周有多少台服务器真的完成了升级。</p>"""

SOURCES = ('<p>📌 主要信息来源：'
           '<a href="https://www.wiz.io/blog/php2shell-php-rce" target="_blank" rel="noopener">Wiz Research：PHP2Shell 技术分析（时间线、CVE、利用链）</a> · '
           '<a href="https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/" target="_blank" rel="noopener">OpenAI：关键漏洞的协调披露（Patch the Planet）</a> · '
           '<a href="https://www.404media.co/php2shell-black-october-ai-is-changing-everything-about-hacking-no-one-knows-what-happens-next/" target="_blank" rel="noopener">404 Media：Black October 与 Cloudflare 数据</a> · '
           '<a href="https://arstechnica.com/security/2026/10/hackers-got-a-four-day-head-start-on-epic-php2shell-vulnerability/" target="_blank" rel="noopener">Ars Technica：披露前四天已被利用</a> · '
           '<a href="https://aihot.news/items" target="_blank" rel="noopener">AIHOT 精选</a></p>')

DESC = ('PHP2Shell（CVE-2026-109618 / 109619，CVSS 9.2）补丁 10 月 21 日上线后，Cloudflare 记录到公告前 10 小时数千次、'
        '公告后 2 小时数十万、目前数百万次利用尝试；影响回溯到 PHP 5.4、覆盖约 70% 网站；NSA 建议无法修补的服务器下线，'
        'Chainguard 提前破禁发布修复。')

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
    <img src="images/featured-__TODAY__-1.jpg" alt="Wiz Research 官方 PHP2Shell 封面图（wiz.io 官方博客素材）">
    <div class="featured-meta">
      <span>📖 8 分钟</span>
      <span>📅 __TODAY__</span>
      <span>🏭 行业动态</span>
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
        <span>📖 8 分钟</span><span>📅 {TODAY}</span><span>{LABEL}</span>
      </div>
      <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
    </div>
    <div class="featured-visual">
      <img src="images/featured-{TODAY}-1.jpg" alt="Wiz Research 官方 PHP2Shell 封面图（wiz.io 官方博客素材）" style="width:180px;border-radius:8px;object-fit:cover;height:100px;">
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
