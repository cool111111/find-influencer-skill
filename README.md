<div align="center">

# 🔍 find-influencer Skill

**一个让 AI Agent 帮你跨平台找达人的 Skill**

支持小红书、抖音、B 站、YouTube 等多平台。从"我想找 XXX 类型的博主"到"完整的达人评估报告"，全流程自动化。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skill: Claude Code](https://img.shields.io/badge/Skill-Claude%20Code-8A2BE2)](https://github.com/anthropics/claude-code)
[![Platforms](https://img.shields.io/badge/Platforms-小红书%20·%20抖音%20·%20B站%20·%20YouTube-FF2741)]()
[![Stars](https://img.shields.io/github/stars/cool111111/find-influencer-skill?style=social)](https://github.com/cool111111/find-influencer-skill/stargazers)

</div>

> 做内容运营的人都知道：找达人这件事 80% 的时间花在了**翻平台、看主页、评估内容质量**上。
> 这个 Skill 把这 80% 自动化了。

<!-- TODO 在此处插入一张 demo GIF 或截图（达人发现 + 评估报告产出过程） -->

## 解决什么问题

传统做法：
- 打开小红书，搜关键词，一个个点开主页看
- 翻 50 个主页 + 看 200 条内容，挑出 5 个值得对接的
- 整理成 Excel，写评估笔记
- **耗时：3-5 小时**

用这个 Skill：
- 描述需求："**帮我找 10 个小红书上做 AI 教程的中腰部博主**"
- Agent 自动跨平台搜索 → 数据筛选 → 深度内容分析 → 输出结构化评估报告
- **耗时：15-20 分钟**

## 工作流

```
1. 收集需求（领域 / 平台 / 粉丝量级 / 内容类型 / 商业化偏好）
   ↓
2. 跨平台搜索（opencli / Playwright 自动化）
   ↓
3. 数据筛选（粉丝量 / 互动率 / 更新频率）
   ↓
4. 深度内容分析（抽样视频转写 + 内容质量评估）
   ↓
5. 结构化报告（达人画像 + 优劣势 + 合作建议）
```

## Quick Start

```bash
# 1. Clone Skill
git clone https://github.com/cool111111/find-influencer-skill.git \
  ~/.your-agent/skills/find-influencer

# 2. Check dependencies
bash ~/.your-agent/skills/find-influencer/scripts/setup_check.sh

# 3. 在 Agent 里说：
#    "帮我找 10 个小红书上做 XXX 的博主"
```

## 依赖项

### 必需

| 依赖 | 用途 | 安装 |
|------|------|------|
| Python 3 | 视频转写脚本 | `brew install python` / `apt install python3` |
| ffmpeg | 视频音频抽取 | `brew install ffmpeg` / `apt install ffmpeg` |
| openai-whisper | 语音转文字 | `pip install openai-whisper` |

### 可选

| 依赖 | 用途 | 兜底方案 |
|------|------|---------|
| opencli | CLI 搜索小红书 / B 站 / YouTube | Playwright 浏览器自动化 |

### Agent 环境

| 要求 | 用途 |
|------|------|
| Claude Code（或兼容的 Skill runtime） | Skill 运行环境 |
| Playwright MCP Server | 抖音 / 主页访问 / 内容分析的浏览器自动化 |

## 一键安装（macOS）

```bash
brew install python ffmpeg
pip install openai-whisper
```

## 实战数据

这个 Skill 在我自己工作中跑过，覆盖 **5000+ 创作者** 的初筛 + 评估，用过的项目反馈：从"找达人 → 输出对接清单"的总时长压缩了 **80%+**。

## 注意事项

- **首次运行会下载 Whisper `base` 模型**（约 140MB）
- **平台访问需要登录态** — 小红书、B 站等需要在 Chrome 提前登录，opencli/Playwright 会复用浏览器登录态
- **转写自动跳过** — 如果帖子已有文字稿，会跳过视频转写步骤

## 配套 Skill

- 长文写作 → [Writer Skill](https://github.com/cool111111/writer-skill)
- 小红书短图文 → [XHS Content Skill](https://github.com/cool111111/xhs-content-skill)

## License

MIT — 觉得有用就 **star 一下** ⭐

---

<details>
<summary>📷 怎么贴 demo 图/GIF？</summary>

1. 在 GitHub 网页打开这个 README，点编辑
2. **直接把图片或 GIF 拖到编辑框**，GitHub 自动上传
3. 把生成的标记剪切到上面 `<!-- TODO -->` 那一行
4. 保存

</details>
