#!/usr/bin/env python3
"""Generate featured-2026-08-18.html — Cursor Origin 代码托管 deep dive"""
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-08-18', TODAY

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cursor 推出 Origin 代码托管：被 SpaceX 收购后首张牌，AI 原生托管正面挑战 GitHub | suduai.top</title>
  <meta name="description" content="2026年8月17日，Cursor 推出 Origin 代码托管服务：仓库、Pull Request、代码浏览与 GitHub 双向同步四项基础能力先行，Agent 原生功能随后上线。三天前 Cursor 刚完成被 SpaceX 收购。深入分析 AI 原生代码托管对 GitHub 的挑战。">
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
    <img src="images/featured-{TODAY}-1.jpg" alt="Cursor Origin 代码托管官方发布图 | Cursor">
    <div class="featured-meta">
      <span>📖 10 分钟</span>
      <span>📅 {TODAY}</span>
      <span>🚀 产品发布</span>
    </div>
  </div>

  <h1>Cursor 推出 Origin 代码托管：被 SpaceX 收购后首张牌，AI 原生托管正面挑战 GitHub</h1>

  <div class="article-body">

    <h2>一、导语</h2>
    <p><span class="key-number">2026 年 8 月 17 日</span>，Cursor 官方变更日志宣布推出 Origin 代码托管服务，一句话定调：「Cursor can now host your code.」。这项以早期公测形式向全部付费计划用户开放的服务，首批包含仓库托管、Pull Request、代码浏览与 GitHub 双向同步四项基础能力，Agent 原生功能随后上线。而就在三天前（<span class="key-number">8 月 14 日</span>），Cursor 刚刚官宣完成被 SpaceX 收购的交易。一周之内连出两张牌，Anysphere 的平台野心已经不再遮掩——它要做的不是更好的编辑器，而是 AI 时代完整的开发基础设施。</p>

    <h2>二、背景分析：为什么这件事重要？</h2>
    <p>Cursor 起家于 AI 编辑器，但过去一年它已从「自动补全」一路扩张到 Composer、Cloud Agents、CLI、Code Review 与 Marketplace 的完整开发平台。代码托管是开发工作流最底层的基础设施——<strong>谁拥有仓库，谁就拥有 Agent 的默认执行环境</strong>。GitHub 在同一时间加速 AI 化，Copilot 已渗透进 Actions、Issues、Reviews 全流程；Cursor 推出 Origin，本质是把战场从「编辑器里的智能」延伸到「仓库里的智能」。</p>
    <p>关键前置条件早已埋下：<span class="key-number">2026 年 4 月</span>，Cursor 宣布与 SpaceXAI 合作加速模型训练；<span class="key-number">8 月 12 日</span>，双方合作的早期成果 Grok 4.6 发布；<span class="key-number">8 月 14 日</span>，收购流程正式走完。有了全球最大 GPU 机队，Cursor 得以做「模型 + 工具链」的垂直整合——这正是 Origin 敢于叫板 GitHub 的底气来源。</p>

    <h2>三、核心内容：Origin 的四个基础能力</h2>
    <h3>1. Origin Repos：把仓库搬进编辑器</h3>
    <p>新的 Codebase 标签页成为 Origin 仓库的入口。点击 +New 创建仓库并命名后，页面会给出 CLI 安装与推送指引，克隆、推送本地项目即可完成托管，仓库 URL 形如 <code>cursor.com/codebase/&lt;name&gt;</code>。</p>
    <h3>2. GitHub 双向同步：GitHub 仍是 source of truth</h3>
    <p>连接 GitHub 组织后可选择仓库同步，同步副本实时更新，推送到 GitHub 的代码仍以 GitHub 为准。Pull Request 双向打通：在 Cursor 里评论会回传 GitHub，GitHub 上的回复几秒内出现在 Cursor；被分配的 Review 可以直接在 Cursor 里审阅并合并。</p>
    <h3>3. Agents in every repo：代码、PR 与 Agent 同处一地</h3>
    <p>浏览代码时可以直接向 Cursor 提问，它可以回答、修改、更新 PR 甚至推送分支——仓库不再只是「存放代码的地方」，而是 Agent 的工作台。</p>

    <div class="inline-img">
      <img src="images/featured-{TODAY}-2.jpg" alt="Cursor Origin 应用生态集成界面 | Cursor">
      <div class="caption">Origin 的应用生态：Vercel、Depot、Buildkite 集成已上线</div>
    </div>

    <h3>4. 应用生态先行：Vercel / Depot / Buildkite</h3>
    <p>Origin 首日即接入 <span class="key-number">3</span> 个集成：连接 Vercel 后每个 PR 自动获得预览部署、合并即上线；CI 侧 Depot 与 Buildkite 可运行现有 GitHub Actions 工作流。官方明确表示更多集成在路上，一个围绕 Origin 的应用市场正在成型。</p>
    <blockquote>
      「Cursor can now host your code. Origin begins rolling out today in early beta on all paid plans.」
      <footer>— Cursor 官方变更日志（2026-08-17）</footer>
    </blockquote>

    <h2>四、各方反应</h2>
    <p><strong>收购公告的底气</strong>：8 月 14 日的 SpaceX 收购公告写道：「我们将获得全球最大的 GPU 机队，用来构建更强、运行成本更低的模型——这意味着我们能以更低价格向客户提供更强大的模型。」Grok 4.6 被官方视为双方合作成果的早期体现。</p>
    <p><strong>安全认证加持</strong>：8 月 13 日，Cursor 获得 <span class="key-number">AIUC-1</span> 认证（Agent 安全与可靠性）；<span class="key-number">2026 年 5 月</span>，入选 Gartner 企业级 AI 编码 Agent 魔力象限「领导者」象限。这些背书让 Origin 在面向企业客户时有了合规层面的说服力。</p>
    <p><strong>开发者社区</strong>：讨论集中在两处——一是「AI 原生托管」能否分流 GitHub 的社交网络效应；二是双向同步模式下「谁是真源」的信任问题。GitHub 用十年建立的分支、Fork、Issue 社交图谱，是 Origin 短期最难复制的部分，但 Agent 时代的托管粘性，正在从「人」转向「Agent」。</p>

    <h2>五、深度解读：这意味着什么？</h2>
    <h3>「模型-算力-工具链」闭环的最后一块拼图</h3>
    <p>SpaceX 提供算力 → 自家模型（Grok 系列）→ 编辑器 + Cloud Agents → Origin 托管，Anysphere 用一周时间把链条焊死。当 OpenAI 绑定 GitHub、Anthropic 主攻企业工作流时，Cursor 选择了第三条路：<strong>更便宜的模型 + 更深的工具链整合</strong>，把「换芯成本」压到最低，同时用托管把用户锁进自己的生态。</p>

    <div class="inline-img">
      <img src="images/featured-{TODAY}-3.jpg" alt="Origin 仓库设置与同步状态界面 | Cursor">
      <div class="caption">Origin 仓库设置：同步状态、访问权限与应用管理一目了然</div>
    </div>

    <h3>对 GitHub 的真正威胁</h3>
    <p>GitHub 的优势在社交网络与生态，Origin 的优势在 Agent 集成。当 PR 评论、代码浏览、CI 触发全部可由 Agent 完成时，开发者留在托管平台的理由会从「协作网络」转向「自动化深度」。早期公测的克制（先做基础能力）恰恰说明 Cursor 清楚：Agent-native 功能才是 Origin 的杀手锏，现在放出的只是入场券。</p>
    <h3>风险与未知</h3>
    <p>三项不确定性值得跟踪：企业客户对仓库数据离开 GitHub 的顾虑；SpaceX 关联带来的治理与舆论风险；以及 GitHub 若开放更深层的 Agent API 后 Origin 的差异化空间。无论哪条线先兑现，代码托管的竞争格局都已进入新阶段。</p>

    <h2>六、总结</h2>
    <p>从被 SpaceX 收购到 Origin 上线，Cursor 在一周内完成了「算力入袋」与「平台奠基」两件大事——当代码托管与 Agent 深度耦合，开发者工具的竞争正式从「编辑器」升级为「整个开发基础设施」。</p>

  </div>

  <div class="bottom-cta">
    <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    <p>📌 主要信息来源：<a href="https://cursor.com/changelog/origin-code-hosting" target="_blank" rel="noopener">Cursor 官方变更日志：Origin Code Hosting</a> · <a href="https://cursor.com/blog/joining-spacex" target="_blank" rel="noopener">Cursor 官方博客：Cursor is now a part of SpaceX</a> · <a href="https://x.ai/news/grok-4-6" target="_blank" rel="noopener">xAI：Grok 4.6 官方公告</a></p>
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

filename = f'featured-{TODAY}.html'
with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)

# body char count check (article-body section)
body = html.split('<div class="article-body">')[1].split('</div>')[0]
import re
text = re.sub(r'<[^>]+>', '', body)
print(f"✅ Generated {filename} ({len(html)} chars, body text {len(text)} chars)")
