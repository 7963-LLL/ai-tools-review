#!/usr/bin/env python3
"""Generate featured-2026-09-16.html: Anthropic September 2026 threat intelligence report."""
import re

TODAY = '2026-09-16'
SRC_REPORT = 'https://www.anthropic.com/threat-intelligence-report-september-2026'

BODY = '''
    <h2>一、导语</h2>
    <p>9 月 16 日，Anthropic 发布 9 月威胁情报报告，把 2025 年 12 月至 2026 年 8 月间被中断的 <span class="key-number">七</span> 类滥用一次摊开。最刺眼的是常规武器：一个被评估极可能关联胡塞武装的也门小组，用 Claude Code 替代人类工程师写完制导、导航与控制（GNC）软件，涉及射程目标 <span class="key-number">2,000</span> 公里以上的多级弹道导弹，以及代号 <span class="key-number">R2000</span>、含高超声速滑翔载具的导弹家族。</p>

    <h2>二、背景分析：攻击链不再需要「高手」</h2>
    <p>报告用 GTG 编号标记滥用 AI 的团伙，用「能力增量」衡量同一场攻击在有 AI 与没 AI 之间的差距。前置条件已经成熟：2025 年 11 月观察到的国家级自主攻击模式，如今扩散到所有类型攻击者。PentAGI 这类公开可下载的攻击型智能体框架复制了大部分脚手架，把攻击链每一步自动化。后果是「技术水平」不再是判断攻击者身份的可信信号——用偷来的 API Key 的黑客、图利者、国家级间谍，都能维持多目标的持续行动。</p>

    <h2>三、核心内容：三份档案与一组数字</h2>
    <h3>1. 也门：用 Claude Code 写导弹制导</h3>
    <p>GTG-87001 并行推进三个项目：手机级飞控计算机加末段寻的制导的战术火箭、射程目标逾 2,000 公里的多级弹道导弹、R2000 多型导弹家族。他们用 Claude 把开源自动驾驶整合进手机级飞控计算机，写控制与位置估计代码、调参、跑固件构建与飞行仿真，并试射过一枚制导火箭——但外场试验看起来失败了，几小时后这群人回到 Claude 排查原因。账号已被封禁，但对方已搭好不依赖 Claude 的离线仿真工具链。</p>
    <div class="inline-img">
      <img src="images/featured-2026-09-16-2.jpg" alt="Anthropic 9 月威胁报告官方流程图：也门制导武器工程小组的系统开发生命周期，蓝色为多级弹道导弹、橙色为战术制导火箭 | Anthropic 官方">
      <div class="caption">Anthropic 官方图：也门制导武器小组在系统开发生命周期上的推进程度（来源：Anthropic 威胁情报报告 2026 年 9 月）</div>
    </div>
    <h3>2. 俄语间谍组织：把「被发现」变成一次自动重编译</h3>
    <p>GTG-20006 被评估与 Midnight Blizzard 一致，用 AI 工作流覆盖从开发、钓鱼到数据外泄：植入物一旦被安全产品检出，监控用智能体就自动改写重编译，迭代到不被检出为止，再从一次性服务器投放。其行动覆盖 <span class="key-number">20</span> 多个组织，多在乌克兰与欧洲；另一起入侵中窃走 <span class="key-number">30</span> 万条国民身份记录与 <span class="key-number">50</span> 万家企业的商业登记数据，并借三家酒店 WiFi 供应商做 DNS 劫持。</p>
    <h3>3. 自由职业团队：无人人在环的 FPV 蜂群</h3>
    <p>GTG-27005 自称 DronDoc 或 Serafim：自主 FPV 自杀式无人机蜂群，机载小模型决定攻击、观察与返航，末端制导用摄像头引向目标并给出引爆指令，目标类别含「人」；Anthropic 关联到 <span class="key-number">九</span> 个账号。</p>
    <h3>4. 蒸馏：峰值一天 300 万次交换</h3>
    <p>商业侧数字更具体：自 2026 年 2 月起，Anthropic 已中断 <span class="key-number">七</span> 家中国实验室的蒸馏攻击——借代理服务批量注册假账号、伪造支付。阿里规模最大——峰值一天近 <span class="key-number">300</span> 万次交换、动用逾 <span class="key-number">3,500</span> 个欺诈账号，5 至 7 月累计超 <span class="key-number">1.51</span> 亿次，CoT 数据被用于训练 Qwen 3.5/3.6/3.7；Moonshot 用 <span class="key-number">5,380</span> 个账号归集 2,300 万次以上；DeepSeek 在 7 月的 <span class="key-number">14</span> 天里产生 1,210 万次以上；智谱以 <span class="key-number">273</span> 个账号在 10 天内跑了 <span class="key-number">770,609</span> 次推理清洗。TechCrunch 汇总：累计近 <span class="key-number">2 亿</span> 次交互、五个活动。</p>
    <div class="inline-img">
      <img src="images/featured-2026-09-16-3.jpg" alt="Anthropic 官方示意图：蒸馏流程——教师模型接收数百万提示词、输出数百万回答，经训练集得到模仿教师的学生模型 | Anthropic 官方">
      <div class="caption">Anthropic 官方图：蒸馏的通用流程——合法训练方法与「未经授权的工业化抽取」只差授权与规模（来源：Anthropic 威胁情报报告 2026 年 9 月）</div>
    </div>

    <h2>四、各方反应：安全披露，也是商业修辞</h2>
    <p>「我们发布这项工作，是因为我们认为有责任披露对我们服务的恶意滥用。」Anthropic 称每个案例都做了封号、加固护栏、按需与执法及行业伙伴共享情报。</p>
    <p>质疑同样真实。同一周 The Verge 报道，奥尔特曼、阿莫迪、哈萨比斯与马斯克「粗略同意放慢 AI 开发」，批评者把这读作压制竞争者的「卡特尔」。而 Anthropic 一边主张行业自律，一边筹备纳斯达克上市、洽谈英伟达以基石投资者身份投入最多 <span class="key-number">100</span> 亿美元——「谁定义滥用」同时也是一门生意。</p>

    <h2>五、深度解读：成本被反转给了防御方</h2>
    <p>过去防御方靠发布新检测特征抬高攻击成本，报告的结论是这套循环正在失效：攻击方用 AI 监控自家植入物是否被检出，一旦被识别就自动改写重编译直到绕过——Anthropic 把这称作「把成本反转给防御方」。</p>
    <p>第二层变化是执法主体。封号、封 API、发 IOC、跨境共享情报，这些动作事实上由前沿模型厂商执行——它们既是技术守门人，也起草嫌疑人名单，而「防止 Claude 被滥用的护栏并不会随蒸馏迁移」。报告还提到，DeepSeek、小米与 Moonshot 把自家模型与用户的对话送进 Claude 当训练数据，涉及十几个语种与数百名终端用户——蒸馏由此从版权问题变成隐私与合规问题。</p>

    <h2>六、总结</h2>
    <p>值得记住的不是导弹，而是那条被自动化抹平的曲线：当写恶意软件、调制导参数、抽推理轨迹都变成按 Token 计费的调用，国家安全、隐私与竞争格局就被压进同一张成本表——而填表的是模型厂商自己。</p>
'''

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Anthropic 9 月威胁报告：也门小组用 Claude Code 写导弹制导，AI 在攻击链上从助手变成编排者 | suduai.top</title>
  <meta name="description" content="Anthropic 发布 2026 年 9 月威胁情报报告：2025 年 12 月至 2026 年 8 月间中断七类滥用，含也门小组用 Claude Code 开发射程 2000 公里以上弹道导弹制导软件、俄语间谍组织自动化改写恶意软件、FPV 无人机蜂群，以及七家中国实验室的蒸馏活动（峰值一天 300 万次交换）。">
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
    <img src="images/featured-2026-09-16-1.jpg" alt="Anthropic 2026 年 9 月威胁情报报告官方封面《Detecting and countering misuse of AI》 | Anthropic 官方">
    <div class="featured-meta">
      <span>📖 10 分钟</span>
      <span>📅 {TODAY}</span>
      <span>🏭 行业动态</span>
    </div>
  </div>

  <h1>Anthropic 9 月威胁报告：也门小组用 Claude Code 写导弹制导，AI 在攻击链上从助手变成编排者</h1>

<div class="article-body">
{BODY}
  <blockquote>
    「随着模型能力不断增强，除非 AI 开发者与社会防御者采取行动让它们更安全，风险将会上升。」
    <footer>— Anthropic《Detecting and countering misuse of AI: September 2026》</footer>
  </blockquote>

  </div>

  <div class="bottom-cta">
    <a href="daily-{TODAY}.html" class="affiliate-btn">看今日完整快报 →</a>
  </div>

  <div class="source-link">
    <p>📌 主要信息来源：<a href="{SRC_REPORT}" target="_blank" rel="noopener">Anthropic 官方：Detecting and countering misuse of AI — September 2026</a> · <a href="https://the-decoder.com/how-hackers-used-claude-for-missiles-drone-swarms-and-surveillance-while-chinese-labs-mined-it-for-training-data" target="_blank" rel="noopener">The Decoder：Claude 被用于导弹、无人机蜂群与监控，中国实验室抽取训练数据</a> · <a href="https://techcrunch.com/2026/09/10/anthropic-details-distillation-campaigns-from-alibaba-moonshot-ai-and-deepseek" target="_blank" rel="noopener">TechCrunch：Anthropic 详述来自阿里、月之暗面与 DeepSeek 的蒸馏活动</a> · <a href="https://www.theverge.com/ai-artificial-intelligence/995186/is-big-techs-ai-slowdown-a-safety-pact-or-a-cartel" target="_blank" rel="noopener">The Verge：巨头放缓 AI 开发是安全共识还是卡特尔</a> · <a href="https://the-decoder.com/anthropic-eyes-nasdaq-listing-as-a-second-profitable-quarter-aims-to-win-over-investors-ahead-of-a-mega-ipo" target="_blank" rel="noopener">The Decoder：Anthropic 瞄准纳斯达克上市</a></p>
  </div>

</div>

<footer>
  <div class="container">
    <p>AI快报站 © 2026</p>
    <p style="margin-top:2px;"><a href="privacy-policy.html">隐私政策</a></p>
  </div>
</footer>

</body>
</html>
'''

open(f'featured-{TODAY}.html', 'w', encoding='utf-8').write(html)

# verify
h = open(f'featured-{TODAY}.html', encoding='utf-8').read()
start = h.find('<div class="article-body">')
end = h.find('<div class="bottom-cta">', start)
cn = len(re.findall(r'[\u4e00-\u9fff]', h[start:end]))
print(f'Chinese chars in article-body: {cn}')
assert 1000 <= cn <= 1500, cn
print('OK')
