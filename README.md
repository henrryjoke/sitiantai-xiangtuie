# 解卦 | Hexagram Interpreter

**以代码演绎象数，用推演替代断言**  
**展开可能性，而非给出结论。**

---

## 📢 这是什么？

**「解卦·象推演」** 是一个基于中国传统易学（梅花易数 + 六爻纳甲）的符号推演系统。它不是一个"算命工具"，而是一个**启发式思考助手**——帮你从卦象符号中展开多种可能性，让你自己判断。

> 不做吉凶断言，不替你做决定。只展开"可能""或许""含有…之象"。

---

## 🎯 谁可以用？在哪些平台可以用？

**任何支持 OpenClaw Skill 格式的 AI Agent 都可以使用本技能。**

包括但不限于：

| 平台/工具 | 是否兼容 | 说明 |
|-----------|---------|------|
| **WorkBuddy**（腾讯小龙虾） | ✅ | 直接安装使用 |
| **OpenClaw** | ✅ | 标准兼容 |
| **Hermes Agent** | ✅ | 支持 OpenClaw 格式 |
| **QClaw** | ✅ | 支持 OpenClaw 格式 |
| **ArcLaw** | ✅ | 支持 OpenClaw 格式 |
| **微信**（接入 AI Agent 的工具） | ✅ | 若使用的 AI 支持 OpenClaw Skill 则可安装 |
| **小红书**（AI 助手类工具） | ✅ | 同上 |
| **X / Twitter**（AI Bot 工具） | ✅ | 同上 |
| **TikTok**（AI 创作助手） | ✅ | 同上 |
| **其他 OpenClaw 兼容 Agent** | ✅ | 只要支持 OpenClaw Skill 格式均可 |

简而言之：**如果你用的 AI 助手支持安装 Skill/技能，并且兼容 OpenClaw 标准，就能用这个。**

---

## ⚡ 30 秒快速安装

### 方式一：通过 ClawHub（推荐，最简单）

1. 打开你的 AI Agent 工具的 Skill/技能 管理页面
2. 搜索 **"sitiantai-xiangtuie"** 或 **"解卦"**
3. 点击安装
4. 或者直接访问链接：https://clawhub.ai/skills/sitiantai-xiangtuie
5. 点击 **Install** 按钮

### 方式二：CLI 命令（技术用户）

```bash
# 使用 OpenClaw CLI 安装
openclaw skills install sitiantai-xiangtuie

# 或使用 ClawHub CLI
clawhub skill install sitiantai-xiangtuie
```

---

## 🗣️ 怎么用？直接跟 AI 说这些话

安装后，在对话中直接说以下**触发词**，AI 就能自动启动解卦推演：

**中文触发词：**
> 解卦、算一卦、问卦、卜问、分析这事、推演一下、象推演、四象合参

**英文/其他语言触发词：**
> divination, iching, hexagram reading, symbolic deduction, lecture d'hexagramme, adivinación, lectura de hexagramas

### 完整对话示例

> **你：** 算一卦，帮我看一下最近的事业发展
>
> **AI（推演师）：**
> 📅 时间确认：2026年5月17日 12:44（当前时间）
> 🔍 事项确认：事业发展
> 👁 外应：无
>
> [开始推演…]
> 📋 **卦象总览**
> 本卦：风天小畜（巽上乾下）
> 变爻：第3爻
> ...
>
> 💡 **启发提问：**
> - 在工作中有没有遇到需要耐心积累的瓶颈？
> - 当前最大的阻力来自外部环境还是内部团队？

---

## ⚠️ 重要：起卦方式说明

本 Skill 支持两种起卦方式，但**进阶功能有差异**，请按你的实际情况选择：

### 🔵 方式一：日期起卦（推荐，支持进阶）

由 AI 根据当前日期自动计算卦象，无需你提供任何卦象信息。

```text
你只需说：算一卦，看看我和这个合作项目的发展
```

**支持进阶功能 ✅**：
- ✅ 可使用大六壬（时空脉络分析）
- ✅ 可使用奇门遁甲（空间方位分析）

基础推演完成后，AI 会主动询问是否启动进阶推演：
> 📊 基础推演已生成。需要更多角度吗？
>   → 想了解发展脉络？ [触发大六壬]
>   → 想了解空间方位？ [触发奇门遁甲]
>   → 已经够了

### 🟢 方式二：人工起卦（不支持进阶）

如果你已经通过其他方式得到了卦象（如掷铜钱、数字起卦、外应取卦等），可以手动输入：

```text
我掷铜钱得到了风天小畜卦，第3爻动，帮我推演一下最近的财运
```

或

```text
用数字3和8起卦，看看这次出行怎么样
```

**不支持进阶功能 ❌**：
- ❌ 无法使用大六壬
- ❌ 无法使用奇门遁甲
- 仅进行基础推演（梅花 + 六爻 + 类象展开）

> 💡 **为什么？** 六壬和奇门需要精确的日期/时间/空间数据才能计算，人工起卦时缺乏这些基础信息，无法进行准确计算。

---

## 🖥️ 专业用户配置说明

如果你希望在本地运行或进行二次开发，以下是技术配置说明。

### 前置条件

| 依赖 | 版本要求 | 说明 |
|------|---------|------|
| Python | 3.8+ | 核心算法脚本 |
| Swiss Ephemeris | 2.10+ | 天文历法计算 |
| lunar-python | 1.0.4+ | 农历/节气计算 |

### 本地安装

```bash
# 克隆仓库
git clone https://github.com/henrryjoke/sitiantai-xiangtuie.git
cd sitiantai-xiangtuie

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Swiss Ephemeris（Windows）
# 下载 sweph.dll 放入 scripts/ 目录
```

### 项目结构

```
sitiantai-xiangtuie/
├── scripts/                  # 6 个核心算法脚本
│   ├── calendar.py           #   干支历法（Swiss Ephemeris）
│   ├── meihua.py             #   梅花易数（时间起卦）
│   ├── liuyao.py             #   六爻纳甲
│   ├── liuren.py             #   大六壬（9 门）
│   ├── qimen.py              #   奇门遁甲（5 层）
│   └── xiang_query.py        #   类象查询 SDK
├── data/xiang/               # 28 个类象知识库 JSON
├── skill/
│   └── SKILL.MD              #   AI Skill 编排文件
├── config.json               #   技能元数据
├── SKILL.md                  #   根目录 Skill 文件
├── CHANGELOG.md              #   更新日志
├── LICENSE                   #   MIT（脚本）
└── LICENSE-DATA              #   CC BY-NC-SA 4.0（数据）
```

### 技术架构（可选阅读）

```
Layer 0: 干支历法 (calendar.py)      → 八字·节气·旬空
Layer 1: 梅花易数 (meihua.py)        → 主体起卦
Layer 2: 六爻纳甲 (liuyao.py)        → 主体排盘
Layer 3: 大六壬   (liuren.py)        → ⚡日期起卦可触发
Layer 4: 奇门遁甲 (qimen.py)         → ⚡日期起卦可触发
Layer 5: 象展开   (xiang_query.py)   → 28 JSON 类象知识库
Layer 6: 综合推演                    → 四象合参 + 启发提问
```

---

## 📜 许可证

| 部分 | 许可证 | 说明 |
|------|--------|------|
| `scripts/`（算法代码） | MIT | 自由使用、修改、商用 |
| `data/xiang/`（类象知识库） | CC BY-NC-SA 4.0 | 署名-非商业-相同方式共享 |
| `skill/SKILL.MD`（推理规则） | CC BY-NC-SA 4.0 | 同上 |

---

## 📚 了解更多

- **GitHub 仓库**: https://github.com/henrryjoke/sitiantai-xiangtuie
- **ClawHub 页面**: https://clawhub.ai/skills/sitiantai-xiangtuie
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)

---

**观天之道，执天之行**

---

## English Version

### What is this?

**Hexagram Interpreter (Xiang Tuiye)** is a symbolic deduction system based on traditional Chinese metaphysics (Plum Blossom Numerology + Six Lines). Instead of making fortune-telling verdicts, it unfolds multiple possibilities to inspire your own judgment.

### Where can I use it?

Any AI Agent that supports the **OpenClaw Skill format**, including:

| Platform | Compatible |
|----------|-----------|
| WorkBuddy | ✅ |
| OpenClaw | ✅ |
| Hermes Agent | ✅ |
| QClaw | ✅ |
| ArcLaw | ✅ |
| WeChat AI tools | ✅ (if OpenClaw compatible) |
| Xiaohongshu AI tools | ✅ |
| X / Twitter AI Bots | ✅ |
| TikTok AI tools | ✅ |
| Other OpenClaw agents | ✅ |

### Quick Install

```bash
# Via ClawHub CLI
openclaw skills install sitiantai-xiangtuie

# Or visit: https://clawhub.ai/skills/sitiantai-xiangtuie
```

### How to Use

Say these trigger words in your conversation:

> divination, iching, hexagram reading, symbolic deduction, I Ching, lecture d'hexagramme, adivinación, lectura de hexagramas

### Important: Two Casting Methods

1. **Date-based casting (recommended)** — Just tell AI your query, it auto-computes the hexagram from current date. **Supports advanced features** (Da Liu Ren, Qi Men Dun Jia).

2. **Manual casting** — If you already have a hexagram (coin toss, numbers, external signs), describe it to AI. **No advanced features** (Liu Ren / Qi Men not supported due to missing temporal data).

### For Developers

```bash
git clone https://github.com/henrryjoke/sitiantai-xiangtuie.git
cd sitiantai-xiangtuie
pip install -r requirements.txt
```

**License**: MIT (scripts) | CC BY-NC-SA 4.0 (data & SKILL.md)
