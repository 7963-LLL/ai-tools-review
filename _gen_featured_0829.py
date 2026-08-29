#!/usr/bin/env python3
"""Generate featured-2026-08-29.html — Qwen3.8-Flash-Next / Qwen4 architecture preview."""
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
assert TODAY == '2026-08-29'

TITLE = 'Qwen3.8-Flash-Next 开源：125B 主模型激活仅 6B，训练成本压到 Qwen3.7-Plus 的 1/9，Qwen4 架构提前亮相'

hero_img = f'images/featured-{TODAY}-1.jpg'
arch_img = f'images/featured-{TODAY}-2.jpg'
work_img = f'images/featured-{TODAY}-3.jpg'

body = f'''
<div class="article-body">

    <h2>一、导语</h2>
    <p><span class="key-number">2026 年 8 月 26 日晚 23:00</span>，通义千问按 ModelScope 倒计时页面的预告时间准点开源 <strong>Qwen3.8-Flash-Next</strong>。这不是一次普通的版本迭代：这是一款 <span class="key-number">125B</span> 总参数、每 token 仅激活 <span class="key-number">6B</span> 参数的多模态 MoE 模型，官方明确定位为 <strong>Qwen4 所用模型结构的「先导预览」</strong>——承担的角色，与当年 Qwen3-Next 之于 Qwen3.5 完全一致。相比 Qwen3.7-Plus，它的训练开销只有约 <span class="key-number">1/9</span>，编码与办公智能体能力却更强：SWE-bench Pro 拿下 <span class="key-number">62.5</span> 分反超 Claude Opus 4.6，CoWorkBench <span class="key-number">73.9</span> 分领跑同组对比。生产版本 Qwen3.8-Flash 同步上线千问 AI 平台，输入价格压到每百万 tokens <span class="key-number">0.8 元</span>。</p>

    <h2>二、背景分析：为什么提前开源一套架构？</h2>
    <p>Qwen 团队的逻辑很直白：Qwen3-Next 当年引入的 <strong>Gated DeltaNet + Gated Attention</strong> 混合结构，此后被 Qwen3.5、3.6、3.7、3.8 全系列沿用——「先放架构、再建家族」的路径已经被验证过一次。这次他们把 Attention、Residual、Embedding、Optimization 四个方向的结构改动同样提前释出，让社区在 Qwen4 完整模型家族构建之前先行检验。</p>
    <p>更大的背景是，开源模型竞争已进入「效率战」阶段：智谱 GLM-5.3 用后训练 Scaling 把编程能力提升 50%，蚂蚁 Ling-3.0-flash 以 <span class="key-number">5.1B</span> 激活参数对标 1T 旗舰，腾讯混元 Hy4 preview（<span class="key-number">770B</span> 总参、1M 上下文）也在同一周开源上线。<strong>「每 token 激活参数」正在取代「总参数」成为新的军备竞赛指标</strong>——谁用更少的算力办同样的事，谁就能在价格战里活到最后。</p>

    <h2>三、核心内容：四大架构升级与真实数据</h2>
    <h3>1. 参数结构：小而锐利的 MoE</h3>
    <p>Qwen3.8-Flash-Next 由 <span class="key-number">125B</span> 主模型 + <span class="key-number">51B</span> N-gram Embedding + 4B MTP（多 token 预测）层构成，共 <span class="key-number">512</span> 个专家，每 token 只路由 <span class="key-number">10</span> 个专家并配 1 个共享专家，共 48 层。原生支持 <span class="key-number">262,144</span> token 上下文，通过 YaRN 可扩展至 <span class="key-number">1,000,000</span> token，并内置视觉编码器，是标准的图文多模态模型。</p>

    <div class="inline-img">
      <img src="{arch_img}" alt="Qwen3.8-Flash-Next 架构总览：QSA 稀疏注意力、Gated Residual、N-gram Embedding 与 Muon 优化 | 通义千问官方博客">
      <div class="caption">官方架构图：四个升级方向共同指向「长上下文智能体场景的成本极限压缩」</div>
    </div>

    <h3>2. Attention：QSA 稀疏注意力 + Gated DeltaNet</h3>
    <p>核心改动是 <strong>Qwen Sparse Attention（QSA）</strong>：Gated DeltaNet（GDN）负责高效压缩历史信息，一个压缩式轻量 Indexer 在 micro-block 粒度上筛选重要上下文，显著降低长序列 Attention 开销——不再对每个 token 都做全量注意力，这正是长上下文场景下延迟与显存的大头。</p>

    <h3>3. Residual 与 Embedding：容量与显存解耦</h3>
    <p>Gated Residual 把 Residual Stream 扩展为 <span class="key-number">4</span> 条分支，通过动态 Gate 控制信息读写，Residual State 还支持 FP8 存储。Embedding 层面借鉴 Gemma 3n 的 Per-Layer Embedding 与 DeepSeek Engram 思路引入 <strong>N-gram Embedding</strong>：结合当前 token 与前几个 token 组成的局部上下文查表，<span class="key-number">51B</span> 参数可以存放在 Host Memory 中，通过异步 Prefetch 与模型计算重叠，<strong>不长期占用 GPU 显存</strong>——模型容量与推理显存首次被拆开。</p>

    <h3>4. Optimization：Muon 优化器与「去掉 Batch Size Warmup」</h3>
    <p>训练端使用 Muon 优化器，并围绕正交化精度、Muon 与 AdamW 的参数分工、融合参数矩阵拆分做工程优化；针对新结构重新拟合 Scaling Law 后，模型可以稳定使用更大的学习率与 Batch Size。实验还发现过去常见的 Batch Size Warmup 已无必要——它只会额外消耗 <span class="key-number">18.8%</span> 的 optimizer steps，最终训练配置直接从目标 Batch Size 开始。</p>

    <h3>5. 基准与定价：反超闭源旗舰的性价比</h3>
    <p>Agentic 编程上，DeepSWE 1.1 得分 <span class="key-number">58.7</span>（Qwen3.7-Plus 仅 16.5、DeepSeek-V4-Flash-0731 为 54.4）；SWE-bench Pro <span class="key-number">62.5</span>，高于 Claude Opus 4.6 的 <span class="key-number">53.4</span>；SWE-bench Multilingual <span class="key-number">81.0</span>。办公智能体方面 CoWorkBench <span class="key-number">73.9</span>、JobBench <span class="key-number">55.7</span>（Qwen3.8-27B 仅 33.4）。Base 模型在 <span class="key-number">14</span> 个 benchmark 的 <span class="key-number">8</span> 个上取得最优。定价上，生产版 Qwen3.8-Flash 默认 1M 上下文并内置工具，每百万 tokens 输入 <span class="key-number">0.8 元</span>、输出 <span class="key-number">2.7 元</span>。</p>

    <blockquote>
      「我们此次发布 Qwen3.8-Flash-Next 的开源权重……提前释出结构上的改动，以便在其上构建 Qwen4 完整模型家族之前，先让社区对其进行检验。」
      <footer>— Qwen 官方博客《Qwen3.8-Flash-Next：全新架构，迈向极致性价比》（2026-08-26）</footer>
    </blockquote>

    <h2>四、各方反应</h2>
    <p><strong>中文社区</strong>：知乎作者将这次发布称为「一份架构金丝雀」——ModelScope 当天下午先挂出倒计时页面，晚间 23:00 准点开源，围观与讨论集中在「6B 激活参数能否撑起旗舰级 Agent 表现」上；GitHub 仓库（QwenLM/Qwen3.8-Flash-Next）上线两天即收获 <span class="key-number">229</span> 颗 star。</p>
    <p><strong>生态联动</strong>：千问办公的全新「标准」模式直接接入该模型，主打 Agent 智能水平、推理效率、成本控制三位一体；API 同时兼容 OpenAI 与 Anthropic 协议，可直连 Claude Code 与 Codex 使用，等于把最流行的两个编程 Agent 入口都打通了。</p>

    <div class="inline-img">
      <img src="{work_img}" alt="千问办公「标准」模式接入 Qwen3.8-Flash-Next | 通义千问官方博客">
      <div class="caption">千问办公新「标准」模式由 Qwen3.8-Flash-Next 驱动</div>
    </div>
    <p><strong>谨慎声音</strong>：海外评测媒体提醒，这些仍是厂商自报基准、未经独立验证；且本地部署门槛不低——社区构建的 GGUF 即便是 1-bit 量化仍需约 <span class="key-number">123GB</span> 存储，普通开发者大概率只能走 API。</p>

    <h2>五、深度解读：这意味着什么？</h2>
    <h3>1. 效率本身就是下一代架构的竞争力</h3>
    <p>6B 激活参数 + 1/9 训练成本意味着「更强的模型」和「更低的价格」可以同时成立。当输入价压到每百万 tokens 0.8 元，长上下文 Agent 的 token 账单会指数级下降——这会直接挤压闭源厂商的定价空间，重演 2025 年 DeepSeek 引发的价格战。</p>
    <h3>2. 开源社区成为架构检验场</h3>
    <p>Qwen 选择在 Qwen4 之前把核心结构开源，本质是把全球社区变成免费的架构测试、性能验证与生态预热渠道。Qwen3-Next 模式已被证明有效：提前放出结构，让社区用一年时间打磨，再以完整家族收割成果。</p>
    <h3>3. 长上下文智能体成本正在「解耦」</h3>
    <p>QSA 稀疏注意力 + 可卸载到 Host Memory 的 51B 查表 Embedding，指向同一个目标：把长上下文 Agent 场景中「记忆」和「计算」的成本拆开。这可能是下一轮模型架构竞争的真正主战场。</p>

    <h2>六、总结</h2>
    <p>Qwen3.8-Flash-Next 用 6B 激活参数和 1/9 训练成本证明：效率本身就是下一代架构的竞争力——Qwen4 的底牌，已经提前翻给了整个行业。</p>

  </div>
'''

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TITLE} | suduai.top</title>
  <meta name="description" content="2026年8月26日，通义千问开源 Qwen3.8-Flash-Next：125B 主模型激活仅 6B，训练成本约为 Qwen3.7-Plus 的 1/9，作为 Qwen4 架构先导预览引入 QSA 稀疏注意力、N-gram Embedding 与 Muon 优化四大升级。">
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
    <img src="{hero_img}" alt="Qwen3.8-Flash-Next 官方发布横幅：Qwen4 架构先导预览 | 通义千问">
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
    <p>📌 主要信息来源：<a href="https://qwen.ai/blog?id=qwen3.8-flash-next" target="_blank" rel="noopener">Qwen 官方博客：Qwen3.8-Flash-Next，全新架构，迈向极致性价比</a> · <a href="https://github.com/QwenLM/Qwen3.8-Flash-Next" target="_blank" rel="noopener">GitHub：QwenLM/Qwen3.8-Flash-Next（含技术报告）</a> · <a href="https://huggingface.co/Qwen/Qwen3.8-Flash-Next" target="_blank" rel="noopener">Hugging Face 模型卡</a></p>
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
