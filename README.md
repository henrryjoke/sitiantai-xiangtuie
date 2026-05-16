# 解卦 | Xiang Tuiye

**以代码演绎象数，用推演替代断言**

*A divergent symbolic deduction system — unfolding possibilities instead of delivering verdicts.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/Data-CC_BY--NC--SA_4.0-lightgrey.svg)](LICENSE-DATA)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)

---

## 这是什么？ / What is this?

**象推演（Xiang Tuiye）** 是一个以中国传统术数为基础、以"展开可能性"为核心理念的符号推演系统。

传统解卦是**收敛式**的：无穷现实 → 压缩为一个吉凶结论。
象推演是**发散式**的：有限符号 → 展开为丰富可能性 → 启发你自主判断。

> 不做吉凶断言，不做"宜/忌"指令。用"可能""或许""含有…之象"展开卦象。

**Xiang Tuiye** is a symbolic deduction engine rooted in traditional Chinese metaphysics.
Instead of converging infinite realities into a single fortune-telling verdict,
it diverges limited symbols into rich possibilities — empowering you to make your own decisions.

---

## 架构 / Architecture

```
Layer 0: 干支历法 (calendar.py)      — 八字、节气、旬空
Layer 1: 梅花易数 (meihua.py)         — 主体起卦
Layer 2: 六爻纳甲 (liuyao.py)         — 主体排盘
Layer 3: 大六壬   (liuren.py)         — 用户触发辅助
Layer 4: 奇门遁甲 (qimen.py)          — 用户触发辅助
Layer 5: 象展开   (xiang_query.py)    — 28 JSON 类象知识库
Layer 6: 综合推演                    — 五卦合参 + 启发提问
```

**特色**：梅花易数 + 六爻纳甲双主体，六壬/奇门按需触发，类象 SDK 五维度展开。

---

## 快速开始 / Quick Start

### 作为 OpenClaw Skill 使用（推荐）

```bash
openclaw skills install sitiantai-xiangtuie
```

在对话中直接说：
- "帮我推演一下这个合作项目"
- "算一卦，看看最近运势"

### 作为 Python 库使用

```bash
git clone https://github.com/henrryjoke/sitiantai-xiangtuie.git
cd sitiantai-xiangtuie
pip install -r requirements.txt
python scripts/meihua.py
python scripts/liuyao.py
```

### 类象查询 SDK

```python
from scripts.xiang_query import XiangQuery

xq = XiangQuery("data/xiang")
# 精确查询：乾卦 + 事业语境
result = xq.query("qian", context="career")
# 全维度展开
text = xq.expand_full("qian", context="career")
print(text)
```

---

## 项目结构 / Project Structure

```
sitiantai-xiangtuie/
├── scripts/                  # 6 核心算法脚本
│   ├── calendar.py           #   干支历法（swisseph 精算）
│   ├── meihua.py             #   梅花易数起卦
│   ├── liuyao.py             #   六爻纳甲排盘
│   ├── liuren.py             #   大六壬（九宗门）
│   ├── qimen.py              #   奇门遁甲（五层排盘）
│   └── xiang_query.py        #   类象查询 SDK
├── data/xiang/               # 28 类象 JSON 知识库
│   ├── bagua/   (8)          #   八卦类象
│   ├── liuqin/  (5)          #   六亲类象
│   ├── liushen/ (6)          #   六种类象
│   ├── ganzhi/  (2)          #   干支类象
│   ├── wuxing/  (1)          #   五行生克
│   └── guayao/  (6)          #   卦爻格局
├── skill/
│   └── SKILL.MD              #   OpenClaw Skill 编排文件
├── LICENSE                   #   MIT (scripts/)
├── LICENSE-DATA              #   CC BY-NC-SA 4.0 (data/xiang/)
└── README.md
```

---

## 许可证 / License

| 部分 | 许可证 | 说明 |
|---|---|---|
| `scripts/` (算法代码) | [MIT](LICENSE) | 自由使用、修改、商用 |
| `data/xiang/` (类象知识库) | [CC BY-NC-SA 4.0](LICENSE-DATA) | 署名-非商业-相同方式共享 |
| `skill/SKILL.MD` (推理规则) | [CC BY-NC-SA 4.0](LICENSE-DATA) | 署名-非商业-相同方式共享 |

---

## 技术亮点 / Technical Highlights

- **月建旺衰**：完全通过旺相休囚死判断，不混用生克
- **日建七效应**：临 / 生 / 克 / 冲(散·暗动) / 合 / 刑 / 害 独立计算
- **旬空精算**：基于 60 甲子循环位置精确查找，非简化公式
- **纳甲分离**：上卦取本宫纳甲，下卦取自卦纳甲（京房规则）
- **五卦合参**：本卦 + 互卦 + 变卦 + 错卦 + 综卦 综合推演
- **类象五维**：人(person) / 物(object) / 时(time) / 空(space) / 态(state) x 5 语境

---

## 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

类象知识库贡献请确保：
- 遵循 5 维度 x 5 语境 JSON 结构
- 标注古籍来源（说卦传 / 梅花易数 / 卜筮正宗 等）
- 命名一致性（避免混用同义词）

---

## 致谢 / Acknowledgments

- [Swiss Ephemeris](https://www.astro.com/swisseph/) — 高精度天文计算
- 《说卦传》《梅花易数》《卜筮正宗》《增删卜易》— 类象来源古籍

---

**观天之道，执天之行** — *Observe the way of Heaven, act in accordance with its course.*
