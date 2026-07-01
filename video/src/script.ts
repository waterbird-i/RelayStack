export const scenes = [
  {
    kicker: 'RelayStack',
    title: '让 AI 编程工作可交接、可追溯、可验证',
    body: '仓库本地 skill set + handoff protocol，把聊天上下文、Git 证据、项目文档和 Agent 记录整理成交接快照。',
    voice: 'RelayStack 让 AI 编程工作可交接、可追溯、可验证。',
  },
  {
    kicker: 'handoff breaks first',
    title: '真正容易断的不是实现，是交接',
    body: '决策留在聊天里，diff 解释不了为什么改，下一个 owner 看不到风险、阻塞和验证状态。',
    voice:
      'AI agent 很能实现，真正容易断的是交接。决策留在聊天里，diff 解释不了为什么改。',
  },
  {
    kicker: 'snapshot',
    title: '一份 snapshot 回答 7 个继续工作的问题',
    body: 'current goal / what changed / why / risks / blockers / next action / validation plan',
    voice:
      'RelayStack 把聊天上下文、Git 证据、项目文档和 agent 记录整理成 handoff snapshot。这份 snapshot 说明目标、改动、原因、风险、下一步和验证方式。',
  },
  {
    kicker: 'benchmark',
    title: '当前 benchmark：接手成本明显下降',
    body: '灰色完整圆环代表 baseline，彩色圆环代表 RelayStack 剩余成本：耗时 75.9%，报告 token 77.0%，重复探索 0 次，盲评 53/60 胜场。',
    voice:
      '这张接手成本图里，灰色圆环是 baseline，彩色圆环是 RelayStack。二十五题合并口径下，总耗时只剩 baseline 的百分之七十五点九，报告 token 只剩百分之七十七。',
  },
  {
    kicker: 'repeat exploration',
    title: '重复探索从 4 次降到 0 次',
    body: 'handoff 把已知事实和来源放进 Evidence Map，减少下一个 owner 重新翻旧账。',
    voice:
      '扩展二十题盲评中，rs handoff 获得五十三个 reviewer 胜场，重复探索从四次降到零次。',
  },
  {
    kicker: 'smoke test',
    title: '第三方公开题源烟测：协议链路跑通',
    body: 'Multi-SWE-bench flash：两组都 resolved 1/1；RelayStack project skills 把 token 降到 34.1%，命令数减半，patch 也更小。',
    voice:
      '第三方公开题源烟测里，两组都 resolved 一题一题。RelayStack project skills 的 token 只剩 baseline 的百分之三十四点一，启动命令从三十二个降到十六个。',
  },
  {
    kicker: 'scope',
    title: '小而专注：只解决交接',
    body: '不是 agent 编排器，不是任务跟踪器，不是工作流平台。只有 snapshot 不够用时，再加平台能力。',
    voice:
      'RelayStack 不是 agent 编排器，不是任务系统。它只先解决交接。',
  },
  {
    kicker: 'next owner',
    title: '让下一个接手者更快继续',
    body: '安装 repo-local skills，运行 rs-handoff，把有证据、有风险、有下一步的交接留在仓库里。',
    voice:
      '安装 repo local skills，运行 rs handoff，把有证据、有风险、有下一步的交接留在仓库里。',
  },
] as const;

export const voiceoverScript = scenes.map((scene) => scene.voice).join('\n');

export const hasVoiceover = true;
