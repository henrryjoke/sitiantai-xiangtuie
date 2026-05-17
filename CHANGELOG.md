# Changelog | 更新日志

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 规范。

---

## [v0.4.1] - 2026-05-17

### 🔥 Hotfix：修复 ClawHub 发布版本无法使用的问题

#### Fixed / 修复

- **`scripts/qigua.py` 编码映射错误**：
  - `TRIGRAM_BINARY` 中 `巽` 的二进制值从错误的 `[0,0,1]` 修正为 `[0,1,1]`
  - `_gua_name_to_encoding()` 中移除了对 `TRIGRAM_BINARY` 的 `reversed()` 调用（二进制已经是初→上顺序，不应反转）
  - **以上两处 bug 导致梅花起卦的卦象编码全部偏移，六爻排盘结果错误**
- **删除 `skill/SKILL.MD`（文件名大写错误）**：该文件导致 ClawHub 安装时 skill 加载失败，已删除整个 `skill/` 目录
- **`_meta.json` 版本号（0.2.3）与 `config.json`（0.3.0）不一致**：统一修正为 0.4.1

#### Changed / 变更

- **ClawHub 发布包结构修正**：移除冗余的 `skill/` 目录，确保 `SKILL.md` 在根目录且大小写正确

---

## [v0.2.6] - 2026-05-17

### 🎯 文档优化 + 多平台兼容声明

#### Added / 新增

- **config.json**: triggers 改为 array 格式（兼容 ClawHub 解析器）；新增 description_fr、description_es
- **README.md**: 全面重写，面向多平台非专业用户
- **SKILL.md**: 新增 §14 新人引导与起卦方式说明
- **SKILL.md frontmatter**: 更新多语言 triggers 和描述

#### Changed / 变更

- **README.md** 重构结构：
  - 🎯 适用范围：明确列出 WorkBuddy/OpenClaw/Hermes/QClaw/ArcLaw 及自媒体平台 AI Agent
  - ⚡ 30 秒快速安装：ClawHub 链接安装 + CLI 命令
  - 🗣️ 使用示例：完整对话流程
  - ⚠️ 起卦方式说明：日期起卦 vs 人工起卦差异（进阶功能支持范围）
  - 🖥️ 专业用户配置：环境要求、本地安装、项目结构
- **SKILL.md** 新增：
  - §14.1 新人引导规则：首次使用自动引导话术
  - §14.2 起卦推演规则：两种方式支持的功能范围
  - §14.3 输入检测逻辑：自动判断起卦方式
  - §14.4 多平台兼容说明

---

## [v0.2.0] - 2026-05-16

### 🎉 重大更新：Phase 1 全部完成

#### Added / 新增

**核心算法脚本（6 个，全部完成）**

- **`scripts/calendar.py`** — 干支历法精算模块
  - 基于 Swiss Ephemeris 的高精度天文计算
  - 输出：年柱/月柱/日柱/时柱（八字）、节气信息、旬空、月建
  - 时区：默认 Asia/Shanghai

- **`scripts/meihua.py`** — 梅花易数起卦模块
  - 函数 `compute_meihua(year, month, day, hour)`
  - 输出：本卦/上卦/下卦/体卦/用卦/变爻/变卦/互卦/错卦/综卦
  - 辅助函数 `gua_to_lines()` 将卦名转为六爻数字编码，供六爻模块使用

- **`scripts/liuyao.py`** — 六爻纳甲排盘模块
  - 函数 `arrange_hexagram(六爻, datetime, 事项)`
  - 输出：本卦（宫位/世应爻/六亲/地支/五行/六兽）、变卦、旬空、月建
  - 纳甲规则：上卦取本宫纳甲，下卦取自卦纳甲（京房规则）
  - 旺衰算法：月建用旺相休囚死（季节旺衰），日建用七效应（临/生/克/冲/合/刑/害）

- **`scripts/liuren.py`** — 大六壬排盘模块
  - 天地盘/四课/三传/贵人计算
  - 用户触发模式（基础推演完成后询问是否展开）

- **`scripts/qimen.py`** — 奇门遁甲排盘模块
  - 地盘/天盘/八门/九星/八神五层排盘
  - 用户触发模式

- **`scripts/xiang_query.py`** — 类象查询 SDK（★ 核心新增）
  - `query(symbol, context?, dimension?)` — 精确查询，支持语境 fallback 到 general
  - `expand_full(symbol, context?)` — 人类可读的多行展开文本
  - `multi_query(symbols[], context?)` — 批量符号查询
  - `expand_for_context(symbols[], context)` — 批量合并展开
  - `get_wuxing_combo(symbols[])` — 多符号五行组合查询
  - `available_symbols()` / `available_categories()` — 元数据查询

**类象知识库（28 个 JSON 文件，6 大类别，全部完成）**

路径：`data/xiang/`

| 类别 | 文件数 | 包含符号 |
|------|--------|----------|
| `bagua/` | 8 | qian / kun / zhen / xun / kan / li / gen / dui |
| `liuqin/` | 5 | fumu / xiongdi / qicai / guangui / zisun |
| `liushen/` | 6 | qinglong / zhuque / gouchen / tengshe / baihu / xuanwu |
| `ganzhi/` | 2 | tiangan / dizhi |
| `wuxing/` | 1 | shengke |
| `guayao/` | 6 | liuhe / liuchong / sanhe / sanxing / liuhai / gong_guayao |

每个 JSON 文件结构（同构）：
```json
{
  "symbol": "乾",
  "category": "bagua",
  "trigram": "☰",
  "core_properties": ["健","阳","刚","上","圆","创始"],
  "wu_xing": "金",
  "contexts": {
    "general":      {"person":[...],"object":[...],"time":[...],"space":[...],"state":[...]},
    "career":       {"person":[...],"object":[...],"state":[...]},
    "health":       {"person":[...],"state":[...]},
    "relationship": {"person":[...],"state":[...]},
    "finance":      {"object":[...],"state":[...]}
  }
}
```

**★ 新增机制（SKILL.md v0.2.0）**

- **反馈引导系统**（§4）
  - 推演完成后主动询问用户帮助程度
  - 反馈以 JSONL 格式存入 `feedback/local_feedback.jsonl`
  - 每收到 5 条有效反馈自动触发 Prompt 优化

- **风格记忆系统**（§5）
  - 每次对话结束，若用户有反馈或偏好表达，写入 `MEMORY.md`
  - 连续 3 次同类型纠正 → 永久注册为偏好
  - 单次纠正 → 标记为"待验证"
  - 每 10 次推演后回顾风格记忆一致性

- **验证闭环**（§6）
  - 推演前：时间解析/卦象计算/事项语境 三检查
  - 象展开时：类象层次/关键象覆盖/象间一致性 三检查
  - 推演后：可能性覆盖/禁用语检查/启发提问/结束语 四检查

- **自我评估与修正**（§7）
  - 输出前对 5 个维度打分（准确性/丰富性/相关性/启发性/开放性，各 1-5 分）
  - 任一维度 < 3 分 → 重新生成该部分
  - 总分 < 18 分 → 回到 Layer 5 重新展开

#### Fixed / 修复

- **纳甲归属错误**：修复上卦/下卦纳甲混用问题，上卦取本宫纳甲，下卦取自卦纳甲（京房规则）
- **旺衰算法混淆**：修复月建旺衰混用日建生克的问题，月建完全通过旺相休囚死判断，日建独立计算七效应
- **旬空计算公式错误**：修复简化公式导致的偏差，改为基于 60 甲子循环位置的精确查找
- **五卦合参逻辑**：修复本卦/互卦/变卦/错卦/综卦在推演中的权重分配

#### Changed / 变更

- 更新 SKILL.md §3 工作流，Step 2-4 包含具体函数调用和 SDK API 说明
- 更新 SKILL.md §9 知识库结构，从占位描述更新为实际 28-JSON/6-类别布局
- 更新 SKILL.md §10 技术架构，标记全部脚本为 ✅ 完成
- 更新 README.md 安装命令：`gamma skill install sitiantai-xiangtuie`（待确认 CLI 命令正确性）

#### Technical Highlights / 技术亮点

- 月建旺衰：完全通过旺相休囚死判断，不混用生克
- 日建七效应：临 / 生 / 克 / 冲（散·暗动）/ 合 / 刑 / 害 独立计算
- 旬空精算：基于 60 甲子循环位置精确查找，非简化公式
- 京房纳甲：上卦/下卦纳甲分离，符合京房八宫规则
- 五卦合参：本卦 + 互卦 + 变卦 + 错卦 + 综卦 综合推演
- 类象五维：人(person) / 物(object) / 时(time) / 空(space) / 态(state) × 5 语境

---

## [v0.1.0] - 2026-05-14

### Added / 新增

**初始 Skill 框架**

- 四象合参（Four-Elephant Synthesis）架构设计
- 象推演（Xiang Tuiye）方法论：发散式符号推演 vs 收敛式吉凶判断
- Layer 分层架构设计（Layer 0-6）

**Layer 0-2 自动执行层**

- Layer 0：干支历法（自动执行）— 八字、节气、旬空、月建
- Layer 1：梅花易数（自动执行）— 时间起卦、体用判定、错综卦生成
- Layer 2：六爻纳甲（自动执行）— 本变卦、世应爻、六亲、六神、旺衰

**Layer 5-6 推演层**

- Layer 5：象展开（核心）— 对关键符号进行五维度语义展开
- Layer 6a：基础综合推演 — 按三传时间线组织 3~7 个可能性叙述

**辅助系统**

- 六壬/奇门改为用户触发模式（基础推演完成后询问）
- 最终输出结构化报告：卦象总览 / 象展开 / 可能性推演 / 补充视角 / 启发提问
- 结束语强制要求："以上是根据卦象展开的可能性推演，并非确定性结论……"

**禁用语与鼓励语规则（§8）**

- 🚫 严禁：一定、必然、大吉、大凶、宜、忌、应该、必须
- ✅ 鼓励：可能、或许、含有…之象、与…相呼应、启发式提问

**待完成（TODO）**

- 推理链与推理示例（后续深入讨论）
- 类象知识库建设计划执行

---

## [Unreleased] / 待发布

### Phase 2 规划（Skill + MCP）

- 将 Python 脚本升级为 MCP 工具，标准化接口
- 支持 OpenClaw MCP 直接调用（无需 Python 子进程）
- 推理链（Reasoning Chain）可视化输出
- 推理示例库（5 个典型场景）
- 类象知识库持续扩充（更多符号 + 更多语境）

---

## 许可证说明

| 部分 | 许可证 |
|------|----------|
| `scripts/`（算法代码） | MIT |
| `data/xiang/`（类象知识库） | CC BY-NC-SA 4.0 |
| `SKILL.md`（推理规则） | CC BY-NC-SA 4.0 |
