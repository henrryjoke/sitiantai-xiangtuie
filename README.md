# 解卦 | Hexagram Interpreter

**以代码演绎象数，用推演替代断言**  
**A divergent symbolic deduction system — unfolding possibilities instead of delivering verdicts.**

---

## 中文版

### 这是什么？

**象推演（Xiang Tuiye）** 是一个以中国传统术数为基础、以"展开可能性"为核心理念的符号推演系统。

传统解卦是**收敛式**的：无穷现实 → 压缩为一个吉凶结论。  
象推演是**发散式**的：有限符号 → 展开为丰富可能性 → 启发你自主判断。

> 不做吉凶断言，不做"宜/忌"指令。用"可能""或许""含有…之象"展开卦象。

### 快速开始

```bash
openclaw skills install sitiantai-xiangtuie
```

在对话中直接说：
- "帮我推演一下这个合作项目"
- "算一卦，看看最近运势"

### 架构

```
Layer 0: 干支历法 (calendar.py)      — 八字、节气、旬空
Layer 1: 梅花易数 (meihua.py)         — 主体起卦
Layer 2: 六爻纳甲 (liuyao.py)         — 主体排盘
Layer 3: 大六壬   (liuren.py)         — 用户触发辅助
Layer 4: 奇门遁甲 (qimen.py)          — 用户触发辅助
Layer 5: 象展开   (xiang_query.py)    — 28 JSON 类象知识库
Layer 6: 综合推演                    — 四象合参 + 启发提问
```

**特色**：梅花易数 + 六爻纳甲双主体，六壬/奇门按需触发，类象 SDK 五维度展开。

---

## English Version

### What is this?

**Hexagram Interpreter (Xiang Tuiye)** is a symbolic deduction system rooted in traditional Chinese metaphysics, with "unfolding possibilities" as its core philosophy.

Traditional hexagram reading is **convergent**: infinite realities → compressed into a single fortune-telling verdict.  
Xiang Tuiye is **divergent**: limited symbols → unfolded into rich possibilities → empowering you to make your own decisions.

> Makes no fortune-telling assertions, no "auspicious/inauspicious" instructions. Uses "possibly", "perhaps", "contains the image of..." to unfold hexagram meanings.

### Quick Start

```bash
openclaw skills install sitiantai-xiangtuie
```

In conversation, simply say:
- "Help me deduce this cooperation project"
- "Do a divination, see how my recent fortune is"

### Architecture

```
Layer 0: Ganzhi Calendar (calendar.py)      — Bazi, solar terms, empty branches
Layer 1: Plum Blossom Numerology (meihua.py)   — Primary hexagram casting
Layer 2: Six Lines NaJia (liuyao.py)         — Primary line arrangement
Layer 3: Da Liu Ren   (liuren.py)         — User-triggered supplement
Layer 4: Qi Men Dun Jia (qimen.py)          — User-triggered supplement
Layer 5: Symbol Expansion (xiang_query.py)    — 28 JSON symbol knowledge base
Layer 6: Comprehensive Deduction                    — Four-Symbol Synthesis + inspiring questions
```

**Features**: Plum Blossom + Six Lines dual-core, Liu Ren/Qi Men on-demand, Symbol SDK five-dimension expansion.

---

## Project Structure / 项目结构

```
sitiantai-xiangtuie/
├── scripts/                  # 6 core algorithm scripts / 6 核心算法脚本
│   ├── calendar.py           #   Ganzhi calendar (Swiss Ephemeris)
│   ├── meihua.py             #   Plum Blossom Numerology
│   ├── liuyao.py             #   Six Lines NaJia
│   ├── liuren.py             #   Da Liu Ren (9 gates)
│   ├── qimen.py              #   Qi Men Dun Jia (5-layer)
│   └── xiang_query.py        #   Symbol query SDK
├── data/xiang/               # 28 symbol JSON knowledge base / 28 类象 JSON 知识库
│   ├── bagua/   (8)          #   Eight Trigrams symbols
│   ├── liuqin/  (5)          #   Six Kin symbols
│   ├── liushen/ (6)          #   Six Spirits symbols
│   ├── ganzhi/  (2)          #   Heavenly Stems & Earthly Branches
│   ├── wuxing/  (1)          #   Five Elements interactions
│   └── guayao/  (6)          #   Hexagram line patterns
├── skill/
│   └── SKILL.MD              #   OpenClaw Skill orchestration file
├── LICENSE                   #   MIT (scripts/)
├── LICENSE-DATA              #   CC BY-NC-SA 4.0 (data/xiang/)
└── README.md
```

---

## Technical Highlights / 技术亮点

| EN | ZH |
|---|---|
| **Month-Branch Strength**: Judged entirely by Wang-Xiang-Xiu-Qiu-Si, not mixing birth/restraint | **月建旺衰**：完全通过旺相休囚死判断，不混用生克 |
| **Day-Branch Seven Effects**: Lin / Birth / Restraint / Clash (Scatter·Hidden Move) / Union / Punishment / Harm calculated independently | **日建七效应**：临/生/克/冲(散·暗动)/合/刑/害 独立计算 |
| **Empty-Branch Precision**: Based on 60 JiaZi cycle position precise lookup, not simplified formula | **旬空精算**：基于 60 甲子循环位置精确查找，非简化公式 |
| **NaJia Separation**: Upper trigram takes root palace NaJia, lower trigram takes trigram NaJia (Jing Fang rule) | **纳甲分离**：上卦取本宫纳甲，下卦取自卦纳甲（京房规则） |
| **Five-Hexagram Synthesis**: Root + Intern + Changing + Reverse + Inverted comprehensive deduction | **五卦合参**：本卦+互卦+变卦+错卦+综卦 综合推演 |
| **Five-Dimension Symbol**: Person / Object / Time / Space / State × 5 contexts | **类象五维**：人/物/时/空/态 × 5 语境 |

---

## License / 许可证

| Part | License | Description |
|---|---|---|
| `scripts/` (algorithm code) | [MIT](LICENSE) | Free use, modification, commercial use |
| `data/xiang/` (symbol knowledge base) | [CC BY-NC-SA 4.0](LICENSE-DATA) | Attribution-NonCommercial-ShareAlike |
| `skill/SKILL.MD` (inference rules) | [CC BY-NC-SA 4.0](LICENSE-DATA) | Attribution-NonCommercial-ShareAlike |

---

## Contributing / 贡献

Welcome to submit Issues and Pull Requests!  
欢迎提交 Issue 和 Pull Request！

For symbol knowledge base contributions, please ensure:  
类象知识库贡献请确保：

- Follow 5 dimensions × 5 contexts JSON structure / 遵循 5 维度 × 5 语境 JSON 结构
- Cite classical sources (Shuo Gua Zhuan / Mei Hua Yi Shu / Bu Ci Zheng Zong, etc.) / 标注古籍来源（《说卦传》/《梅花易数》/《卜筮正宗》等）
- Naming consistency (avoid using synonyms interchangeably) / 命名一致性（避免混用同义词）

---

## Acknowledgments / 致谢

- [Swiss Ephemeris](https://www.astro.com/swisseph/) — High-precision astronomical calculation / 高精度天文计算
- 《说卦传》《梅花易数》《卜筮正宗》《增删卜易》— Symbol knowledge base source classics / 类象来源古籍

---

**观天之道，执天之行**  
**Observe the way of Heaven, act in accordance with its course.**
