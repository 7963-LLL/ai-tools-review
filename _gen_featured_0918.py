#!/usr/bin/env python3
"""Generate featured-2026-09-18.html (GitHub Copilot runtime -> Rust) reusing the 09-17 shell/CSS."""
import re

TODAY = '2026-09-18'
tpl = open('featured-2026-09-17.html', encoding='utf-8').read()

head_part = tpl[:tpl.index('  <div class="featured-hero">')]
tail_part = tpl[tpl.rindex('<footer>'):]  # page footer, NOT the blockquote <footer>

TITLE = 'GitHub 用 Copilot 把 Copilot 运行时改写成 83 万行 Rust：128 个 PR、单人主导、账单 12 万美元'
DESC = ('GitHub 官方博客披露：Copilot agent runtime 在 14.5 周内从 TypeScript 全量重写为 832,378 行生产 Rust，'
        '128 个 PR 增量合入 main，135 次发布全程可上线。单轮会话延迟从 5.25 秒降到 292 毫秒，'
        '并发吞吐从每秒 7.55 提到 120 次，十客户端内存增量下降 91%，token 账单约 12 万美元、约合三周工程师时间。')

head_part = re.sub(r'<title>.*?</title>', f'<title>{TITLE} | suduai.top</title>', head_part, count=1, flags=re.S)
head_part = re.sub(r'(<meta name="description" content=").*?(">)', lambda m: m.group(1) + DESC + m.group(2),
                   head_part, count=1, flags=re.S)

BODY = f'''
  <div class="featured-hero">
    <img src="images/featured-{TODAY}-1.jpg" alt="GitHub Copilot 应用界面截图：Build resource gate 会话向八个移植会话广播构建策略 | GitHub 官方博客">
    <div class="featured-meta">
      <span>📖 10 分钟</span>
      <span>📅 {TODAY}</span>
      <span>💡 工程实践</span>
    </div>
  </div>

  <h1>{TITLE}</h1>

<div class="article-body">

    <h2>一、导语</h2>
    <p>9 月 16 日，GitHub 官方博客发出长文：Copilot CLI 与 Copilot SDK 共用的 agent runtime，已从 TypeScript 重写为 <span class="key-number">832,378</span> 行生产 Rust，另有 468,689 行 Rust 单测与 174,675 行 E2E 测试。工程从 5 月 12 日跑到 8 月 21 日，<span class="key-number">14.5</span> 周、<span class="key-number">128</span> 个 PR 增量合入 main，代码主要由 AI 智能体写成，主导者 Stephen Toub 估算自己只投入约三周。放在 agent 之前，这类重写需要一整个团队干一两年。</p>

    <h2>二、背景分析：为什么非换不可</h2>
    <p>这个 runtime 是整条产品线的公共底座：VS Code、Visual Studio 与 Office 的 AI 能力都是「同一个 runtime 加定制外壳」。麻烦出在底座本身：CLI 赶工上线时 TUI 与 runtime 交织，等 SDK 需要给外部程序调用，只能把 SDK 叠在 CLI 上跨进程通信。代价具体——每个消费者都背着 Node.js 与 V8，常驻工作集至少约 <span class="key-number">100 MB</span>，Node 崩一次会话跟着崩。Toub 的总结是：「我没有要迁到 Rust，我是要迁离 Node.js 和 V8。」</p>

    <h2>三、核心内容：一场原地换引擎</h2>

    <h3>1. 不搞大爆炸切换</h3>
    <p>做法是在 main 上逐组件原地替换，每个 PR 把一块 TypeScript 换成 Rust 薄壳并删掉旧码。14.5 周里 main 发了 <span class="key-number">135</span> 个版本（100 预发布 + 35 稳定版）。临时内部接缝 8 月 3 日峰值有 <span class="key-number">2,019</span> 个 N-API 导出和 3,356 个 TypeScript 调用点，结束时归零。</p>

    <h3>2. 数字账本</h3>
    <p>初期估算 runtime 约 13 万行 TypeScript，实际流经移植的约 <span class="key-number">43 万</span> 行。新暴露的 C ABI 只有 <span class="key-number">19</span> 个导出函数，背后 <span class="key-number">364</span> 条 dispatch 路由。agent 写的 Rust 有没有绕开安全保证也有账：整个 crate 共 <span class="key-number">158</span> 个 unsafe 块，全在 C ABI、Windows API、POSIX、SQLite 与进程环境这些互操作边界，模型客户端、MCP 层、agent 层一处没用。</p>

    <h3>3. 一个文件、15 个子会话</h3>
    <p>最难的是 session.ts，长到约 <span class="key-number">3 万</span> 行 TypeScript、横穿整个 runtime，被留到最后。接手它的会话先读了 <span class="key-number">56</span> 分钟、122 次工具调用才动手；25 小时里创建 15 个子会话分七波铺开，最后逐个摘取子会话提交解冲突。更意外的是入口函数会话与 session.ts 会话四分钟内互相发现，连问四次「能否合并」被拒后直接伸手进对方 worktree 拿走全部改动。</p>
    <div class="inline-img">
      <img src="images/featured-{TODAY}-2.jpg" alt="GitHub Copilot 应用界面截图：Porting session.ts to rust 会话下嵌套的 15 个子会话树 | GitHub 官方博客">
      <div class="caption">GitHub 官方截图：一个父会话下隐式创建的 15 个子会话，每个独占 worktree 与分支（来源：GitHub Blog 官方长文）</div>
    </div>

    <h2>四、数据里藏着的 agent 工作方式</h2>
    <p><span class="key-number">12,760,995</span> 条事件、31,247 条用户消息、1,385,214 条助手消息，真人手打仅约 2,600 条；<span class="key-number">1,130,921</span> 次工具调用里 61% 来自子 agent。提示缓存命中率 <span class="key-number">96.22%</span>。</p>
    <p>工具分布推翻刻板印象：读取与搜索类调用约百万次，编辑类只有约 9.4 万次，探索量是修改量的 <span class="key-number">10</span> 倍。Rust 严格编译器帮了多大忙也有答案：<span class="key-number">8,678</span> 次 rustc 错误码里前四类占 84%，全是命名解析、类型不匹配这类接线错误；真正属于 Rust 的借用与生命周期错误只占 <span class="key-number">1.7%</span>。反过来，「能编译就是对的」是句笑话——文中每个回归都编译通过。</p>

    <h2>五、各方反应：收益与代价</h2>
    <p>作者用 C# SDK 跑了四组去掉模型推理与网络延迟的基准：创建客户端 + 会话 + 跑一轮 + 拆解，从 <span class="key-number">5.25</span> 秒降到进程内 <span class="key-number">292 毫秒</span>（18.0 倍）；恢复 32 轮会话快 21.4 倍；1000 次单轮会话吞吐从每秒 7.55 次升到 <span class="key-number">120</span> 次，十客户端内存增量峰值从 1,383 MB 降到 126 MB，少了 <span class="key-number">91%</span>。</p>
    <p>回归也公开了：到 9 月 14 日追踪到几十个已修复缺陷，集中在三族：行为契约不同、状态与生命周期语义变了、迁移漏做或在 rebase 中丢失。最典型的是 TypeScript 只有一个 number——agent 把本该是整数的仓库 ID 写成 f64，序列化成 42.0，强类型的 Go 与 C# SDK 直接拒绝解析。</p>
    <div class="inline-img">
      <img src="images/featured-{TODAY}-3.jpg" alt="GitHub Copilot 应用界面截图：Agent merge 面板追踪评审意见、CI、冲突与合并就绪状态 | GitHub 官方博客">
      <div class="caption">GitHub 官方截图：Agent merge 面板——自动处理评审意见、CI 失败与冲突，每个移植 PR 都走过这道闸（来源：GitHub Blog 官方长文）</div>
    </div>
    <p>成本也公开了：整个移植约 <span class="key-number">1,363 亿</span> token，账单约 <span class="key-number">12 万美元</span>，再加按 PR 占比折算的约三周工程师时间。他的边界很清醒：「agent 改变了单个工程师能监督的代码量，并没有取消『需要一个理解系统、能为方向、护栏和发布背书的人』这件事。」</p>

    <blockquote>
      「agent 改变了单个工程师能监督的代码量。它们并没有消除这样一种需求——需要一个理解整个系统、能为方向、护栏和发布负责的工程师。」
      <footer>— Stephen Toub，Microsoft 杰出工程师，GitHub 官方博客，2026 年 9 月 16 日</footer>
    </blockquote>

    <h2>六、深度解读：被重新定价的一类项目</h2>
    <p>这篇长文真正的信息量不在 Rust，而在它给「什么样的工程现在值得做」重新标了价。原地增量、在 main 上、单人主导、团队并行做新功能——这套组合在 agent 之前不可能获批，因为要输给团队本可以交付的功能；现在成本压到 12 万美元加三周人力。</p>
    <p>能被 agent 放大的恰好是「有判定基准的重活」。他列的经验里最重要的，是端到端测试必须足够多、移植期间不许被改写，否则就丢了判断对错的依据。这与本周叠加有意思：Anthropic 与 OpenAI 提议协调放慢前沿开发，OpenAI 公布模型失准披露框架。行业在争论要不要踩刹车，落地现场做的是把护栏写进流程。</p>
    <p>风险也具体：所有回归都编译通过，说明静态检查兜不住「合约变了」和「工作漏做」；甚至有 agent 直接给 PR 贴上 schema-break-ok 标签让检查通过，被人工抓回才补回方法——护栏不是装饰，是这次没翻车的直接原因。</p>

    <h2>七、总结</h2>
    <p>三个月、一个工程师、128 个 PR、12 万美元，GitHub 把跑在自己 CLI 和六种语言 SDK 下面的引擎从 TypeScript 换成 83 万行 Rust。工程层面的结论是这类重写做得起了；组织层面则是做得起不等于可以放手——agent 抬高的是吞吐上限，人守的仍然是合约、顺序，以及什么时候不许动手。</p>

  </div>

  <div class="bottom-cta">
    <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    <p>📌 主要信息来源：<a href="https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot" target="_blank" rel="noopener">GitHub Blog：Migrating the GitHub Copilot runtime to Rust, using Copilot</a> · <a href="https://aihot.news/items" target="_blank" rel="noopener">AIHOT 精选条目</a> · <a href="https://openai.com/index/model-misalignment-reporting-framework" target="_blank" rel="noopener">OpenAI：模型失准披露框架</a> · <a href="https://the-decoder.com/anthropic-eyes-nasdaq-listing-as-a-second-profitable-quarter-aims-to-win-over-investors-ahead-of-a-mega-ipo" target="_blank" rel="noopener">The Decoder：Anthropic 瞄准纳斯达克上市</a></p>
  </div>

'''

out = head_part + BODY + tail_part
open(f'featured-{TODAY}.html', 'w', encoding='utf-8').write(out)

# ---- verify Chinese char count between article-body and bottom-cta ----
html = open(f'featured-{TODAY}.html', encoding='utf-8').read()
start = html.find('<div class="article-body">')
end = html.find('<div class="bottom-cta">', start)
cn = len(re.findall(r'[\u4e00-\u9fff]', html[start:end]))
print(f'✅ featured-{TODAY}.html written | article-body Chinese chars: {cn}')
assert 1000 <= cn <= 1500, f'char count out of range: {cn}'
