"""
qigua.py — 起卦引擎（司天监象推演系统）

提供两种起卦方式：
1. 梅花易数日期起卦 — 基于年月日时自动起卦
2. 卜蓍正宗掷铜钱起卦 — 传统三硬币法

输出统一为 liuyao.py 的 [1,2,3,4]×6 编码格式，
可直接传入 arrange_hexagram() 进行六爻纳甲排盘。

编码约定：
  1 = 少阴（阴爻静）  ─ ─
  2 = 少阳（阳爻静）  ─────
  3 = 老阳/纯阳（阳爻动）  ───── ○
  4 = 老阴/纯阴（阴爻动）  ─ ─ ×
"""

from __future__ import annotations
import sys
import os
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# 确保项目根目录在 sys.path 中，方便相对导入
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# ═══════════════════════════════════════════
# 八卦 ↔ 数字映射（与 meihua.py 一致）
# ═══════════════════════════════════════════

BA_GUA = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 0: "坤"}

# 八卦 → 二进制三爻（1=阳, 0=阴），从下到上
GUA_TO_LINES = {
    "乾": (1, 1, 1),  # ☰
    "兑": (1, 1, 0),  # ☱
    "离": (1, 0, 1),  # ☲
    "震": (1, 0, 0),  # ☳
    "巽": (0, 1, 1),  # ☴
    "坎": (0, 1, 0),  # ☵
    "艮": (0, 0, 1),  # ☶
    "坤": (0, 0, 0),  # ☷
}

# 六十四卦查找表（用于卦名反查）
# 从 liuyao.py 的 HEXAGRAMS 表中提取卦名→二进制映射
# 此处直接内联，避免循环导入
_GUA_NAME_TO_BINARY: Dict[str, List[int]] = {
    "乾为天": [1,1,1,1,1,1], "天风姤": [0,1,1,1,1,1], "天山遁": [0,0,1,1,1,1],
    "天地否": [0,0,0,1,1,1], "风地观": [0,0,0,0,1,1], "山地剥": [0,0,0,0,0,1],
    "火地晋": [0,0,0,1,0,1], "火天大有": [1,1,1,1,0,1],
    "坤为地": [0,0,0,0,0,0], "地雷复": [1,0,0,0,0,0], "地泽临": [1,1,0,0,0,0],
    "地天泰": [1,1,1,0,0,0], "雷天大壮": [1,1,1,1,0,0], "泽天夬": [1,1,1,1,1,0],
    "水天需": [1,1,1,0,1,0], "水地比": [0,0,0,0,1,0],
    "震为雷": [1,0,0,1,0,0], "雷地豫": [0,0,0,1,0,0], "雷水解": [0,1,0,1,0,0],
    "雷风恒": [0,1,1,1,0,0], "地风升": [0,1,1,0,0,0], "水风井": [0,1,1,0,1,0],
    "泽风大过": [0,1,1,1,1,0], "泽雷随": [1,0,0,1,1,0],
    "巽为风": [0,1,1,0,1,1], "风天小畜": [1,1,1,0,1,1], "风火家人": [1,0,1,0,1,1],
    "风雷益": [1,0,0,0,1,1], "天雷无妄": [1,0,0,1,1,1], "火雷噬嗑": [1,0,0,1,0,1],
    "山雷颐": [1,0,0,0,0,1], "山风蛊": [0,1,1,0,0,1],
    "坎为水": [0,1,0,0,1,0], "水泽节": [1,1,0,0,1,0], "水雷屯": [1,0,0,0,1,0],
    "水火既济": [1,0,1,0,1,0], "泽火革": [1,0,1,1,1,0], "雷火丰": [1,0,1,1,0,0],
    "地火明夷": [1,0,1,0,0,0], "地水师": [0,1,0,0,0,0],
    "离为火": [1,0,1,1,0,1], "火山旅": [0,0,1,1,0,1], "火风鼎": [0,1,1,1,0,1],
    "火水未济": [0,1,0,1,0,1], "山水蒙": [0,1,0,0,0,1], "风水涣": [0,1,0,0,1,1],
    "天水讼": [0,1,0,1,1,1], "天火同人": [1,0,1,1,1,1],
    "艮为山": [0,0,1,0,0,1], "山火贲": [1,0,1,0,0,1], "山天大畜": [1,1,1,0,0,1],
    "山泽损": [1,1,0,0,0,1], "火泽睽": [1,1,0,1,0,1], "天泽履": [1,1,0,1,1,1],
    "风泽中孚": [1,1,0,0,1,1], "风山渐": [0,0,1,0,1,1],
    "兑为泽": [1,1,0,1,1,0], "泽水困": [0,1,0,1,1,0], "泽地萃": [0,0,0,1,1,0],
    "泽山咸": [0,0,1,1,1,0], "水山蹇": [0,0,1,0,1,0], "地山谦": [0,0,1,0,0,0],
    "雷山小过": [0,0,1,1,0,0], "雷泽归妹": [1,1,0,1,0,0],
}


# ═══════════════════════════════════════════
# 1. 梅花易数日期起卦
# ═══════════════════════════════════════════

def meihua_date_qigua(year: int, month: int, day: int, hour: int) -> Dict:
    """
    梅花易数年月日时起卦。

    调用 meihua.py::compute_meihua 获取卦象，
    然后转换为 liuyao.py 的 [1,2,3,4]×6 编码。

    Returns:
        {
            "method": "meihua_date",
            "时间": "YYYY-MM-DD HH:MM",
            "上卦": "巽", "下卦": "乾",
            "卦名": "风天小畜",
            "动爻": 3,  # 1-6
            "体卦": "巽", "用卦": "乾",
            "变卦": {"上卦":"巽", "下卦":"兑", "卦名":"风泽中孚"},
            "互卦": {...},
            "错卦": {...},
            "综卦": {...},
            "hexagram_encoding": [1,2,2,1,2,3],  # 供 liuyao.py 使用
            "变卦_encoding": [1,2,2,1,2,1],        # 供参考
        }
    """
    from scripts.meihua import compute_meihua

    result = compute_meihua(year, month, day, hour)

    # 梅花结果 → 六爻编码
    encoding = meihua_to_hexagram_encoding(
        result["上卦"], result["下卦"], result["变爻"]
    )

    # 变卦编码（仅动爻变化）
    bian_encoding = list(encoding)
    moving_idx = result["变爻"] - 1  # 0-based
    if encoding[moving_idx] == 3:
        bian_encoding[moving_idx] = 2  # 老阳动→少阳
    elif encoding[moving_idx] == 4:
        bian_encoding[moving_idx] = 1  # 老阴动→少阴

    result["method"] = "meihua_date"
    result["hexagram_encoding"] = encoding
    result["变卦_encoding"] = bian_encoding

    return result


def meihua_to_hexagram_encoding(up_gua: str, down_gua: str, change_line: int) -> List[int]:
    """
    梅花起卦结果 → [1,2,3,4]×6 六爻编码。

    参数：
        up_gua: 上卦名（如"巽"）
        down_gua: 下卦名（如"乾"）
        change_line: 动爻序号 1-6（1=初爻, 6=上爻）

    算法：
        1. 从八卦→三爻二进制映射获取上下卦各爻
        2. 二进制 0→编码1(少阴) 或 4(老阴动)，1→编码2(少阳) 或 3(老阳动)
        3. 动爻位置标记为 3 或 4
    """
    up_lines = GUA_TO_LINES.get(up_gua)
    down_lines = GUA_TO_LINES.get(down_gua)

    if up_lines is None or down_lines is None:
        raise ValueError(f"无法识别的卦名：上卦={up_gua}, 下卦={down_gua}")

    # 下卦三爻 (初爻,二爻,三爻) + 上卦三爻 (四爻,五爻,上爻)
    all_binary = list(down_lines) + list(up_lines)

    encoding = []
    for i, bit in enumerate(all_binary):
        line_num = i + 1  # 1-based 爻序
        if bit == 1:  # 阳爻
            if line_num == change_line:
                encoding.append(3)  # 老阳动
            else:
                encoding.append(2)  # 少阳静
        else:  # 阴爻
            if line_num == change_line:
                encoding.append(4)  # 老阴动
            else:
                encoding.append(1)  # 少阴静

    return encoding


# ═══════════════════════════════════════════
# 2. 卜蓍正宗掷铜钱起卦
# ═══════════════════════════════════════════

# 铜钱面值定义
COIN_FRONT = "字"   # 正面（有字）
COIN_BACK = "背"    # 反面（无字）


def coin_toss_result_to_encoding(coins: List[str]) -> int:
    """
    3枚铜钱结果 → 编码。

    传统规则（卜蓍正宗·三硬币法）：
      3背(老阳) → 3（纯阳动）  ○
      2背1字(少阴) → 1（阴爻静）  ─ ─
      1背2字(少阳) → 2（阳爻静）  ─────
      3字(老阴) → 4（纯阴动）  ×

    参数：
        coins: 3枚铜钱结果，如 ["背","背","背"] 或 ["字","字","背"]
    """
    back_count = sum(1 for c in coins if c == COIN_BACK)
    # front_count = 3 - back_count

    if back_count == 3:
        return 3  # 老阳（纯阳动）
    elif back_count == 2:
        return 1  # 少阴（阴爻静）
    elif back_count == 1:
        return 2  # 少阳（阳爻静）
    else:  # back_count == 0
        return 4  # 老阴（纯阴动）


def coin_toss_qigua(tosses: List[List[str]]) -> Dict:
    """
    掷铜钱起卦。

    参数：
        tosses: 六次摇的结果，每次3枚铜钱，
                从初爻到上爻（索引0=初爻，索引5=上爻）
                如 [["背","背","背"], ["字","字","背"], ...]

    Returns:
        {
            "method": "coin_toss",
            "tosses": [...],                     # 原始掷币记录
            "toss_summary": [                    # 每次汇总
                {"coins": ["背","背","背"], "背数": 3, "结果": "老阳", "爻象": "----- ○"},
                ...
            ],
            "hexagram_encoding": [3,1,2,...],    # [1,2,3,4]×6
            "卦名": "xxx",
            "动爻": [0,3],                       # 动爻索引(0-based)
        }
    """
    if len(tosses) != 6:
        raise ValueError(f"掷铜钱需要6次，当前提供了{len(tosses)}次")

    encoding = []
    toss_summary = []
    moving_lines = []

    line_names = {1: "少阴", 2: "少阳", 3: "老阳", 4: "老阴"}
    line_symbols = {1: "─ ─", 2: "─────", 3: "───── ○", 4: "─ ─ ×"}

    for i, coins in enumerate(tosses):
        if len(coins) != 3:
            raise ValueError(f"第{i+1}次摇铜钱需要3枚，当前提供了{len(coins)}枚")

        code = coin_toss_result_to_encoding(coins)
        encoding.append(code)

        back_count = sum(1 for c in coins if c == COIN_BACK)

        toss_summary.append({
            "爻位": f"{'初二三四五上'[i]}爻",
            "coins": coins,
            "背数": back_count,
            "字数": 3 - back_count,
            "结果": line_names[code],
            "爻象": line_symbols[code],
        })

        if code in (3, 4):
            moving_lines.append(i)

    # 查卦名
    gua_name = _encoding_to_gua_name(encoding)

    return {
        "method": "coin_toss",
        "tosses": tosses,
        "toss_summary": toss_summary,
        "hexagram_encoding": encoding,
        "卦名": gua_name,
        "动爻": moving_lines,
    }


def coin_toss_random() -> Dict:
    """
    随机模拟掷铜钱（6次×3枚）。
    自动生成 tosses 并调用 coin_toss_qigua。

    Returns: 同 coin_toss_qigua 返回结构
    """
    tosses = []
    for _ in range(6):
        coins = [random.choice([COIN_FRONT, COIN_BACK]) for _ in range(3)]
        tosses.append(coins)
    return coin_toss_qigua(tosses)


def coin_toss_interactive_input(results: List[str]) -> Dict:
    """
    用户以简化格式输入铜钱结果。

    参数：
        results: 6个字符串，每个表示一次摇的"背"数。
                 格式支持：
                   "3背" / "2背1字" / "1背2字" / "3字"
                   或简写："3" / "2" / "1" / "0"（背的数量）
                 从初爻到上爻。

    Returns: 同 coin_toss_qigua 返回结构
    """
    if len(results) != 6:
        raise ValueError(f"需要6次摇铜钱的结果，当前提供了{len(results)}次")

    tosses = []
    for r in results:
        r = r.strip()
        # 解析背的数量
        back_count = _parse_back_count(r)
        # 构造 coins 列表
        coins = [COIN_BACK] * back_count + [COIN_FRONT] * (3 - back_count)
        tosses.append(coins)

    return coin_toss_qigua(tosses)


def _parse_back_count(s: str) -> int:
    """解析用户输入的铜钱结果字符串，返回背的数量。"""
    s = s.strip()

    # 纯数字
    if s in ("0", "1", "2", "3"):
        return int(s)

    # "3背" / "2背1字" 等格式
    if "背" in s:
        # 取"背"前面的数字
        idx = s.index("背")
        prefix = s[:idx].strip()
        if prefix.isdigit():
            return int(prefix)

    # "3字" → 0背
    if "字" in s and "背" not in s:
        # 纯字，提取数字作为字数
        idx = s.index("字")
        prefix = s[:idx].strip()
        if prefix.isdigit():
            return 3 - int(prefix)  # 字数 → 背数 = 3 - 字数

    # "三背" / "两背" 等中文
    cn_map = {"三背": 3, "两背": 2, "二背": 2, "一背": 1, "零背": 0, "全背": 3, "全字": 0,
              "三字": 0, "两字": 1, "二字": 1, "一字": 2, "零字": 3}
    for cn, num in cn_map.items():
        if cn in s:
            return num

    # "老阳"/"少阴"/"少阳"/"老阴"
    name_map = {"老阳": 3, "少阴": 2, "少阳": 1, "老阴": 0}
    for name, num in name_map.items():
        if name in s:
            return num

    raise ValueError(f"无法解析铜钱结果：'{s}'。请使用'3背'/'2背1字'/'1背2字'/'3字'或数字0-3")


# ═══════════════════════════════════════════
# 3. 桥接与工具函数
# ═══════════════════════════════════════════

def _encoding_to_gua_name(encoding: List[int]) -> str:
    """从 [1,2,3,4]×6 编码查找卦名。"""
    from scripts.liuyao import _hex_to_binary, HEXAGRAMS

    binary = _hex_to_binary(encoding)
    key = ",".join(str(x) for x in binary)
    info = HEXAGRAMS.get(key, {})
    return info.get("卦名", "未知卦")


def encoding_to_display(encoding: List[int]) -> List[str]:
    """
    将 [1,2,3,4]×6 编码转为可显示的爻象字符串。
    从上爻到初爻（传统排盘方向）。

    返回如 ["─ ─ ×", "─────", "───── ○", "─ ─", "─────", "─ ─"]
    """
    line_symbols = {
        1: "─ ─",       # 少阴
        2: "─────",     # 少阳
        3: "───── ○",   # 老阳动
        4: "─ ─ ×",    # 老阴动
    }
    # 从上爻(index 5)到初爻(index 0)输出
    return [line_symbols.get(e, "???") for e in reversed(encoding)]


def qigua_full_pailian(encoding: List[int], dt: datetime, reason: str = "") -> Dict:
    """
    起卦结果 → 完整六爻纳甲排盘（一站式调用）。

    参数：
        encoding: [1,2,3,4]×6 编码
        dt: 起卦时间
        reason: 占问事项

    Returns:
        liuyao.arrange_hexagram() 的完整输出
    """
    from scripts.liuyao import arrange_hexagram
    return arrange_hexagram(encoding, dt, reason)


# ═══════════════════════════════════════════
# 4. 外应辅助（预留接口）
# ═══════════════════════════════════════════

def waiying_to_trigram(waiying: str) -> Optional[str]:
    """
    外应感知 → 八卦映射（预留，用于梅花易数外应起卦）。

    传统外应规则（梅花易数·万物类象）：
      天/父/君/金 → 乾    地/母/布/土 → 坤
      雷/龙/足/木 → 震    风/长女/股/木 → 巽
      水/雨/豕/水 → 坎    火/日/雉/火 → 离
      山/少男/手/土 → 艮   泽/少女/口/金 → 兑

    当前返回 None，待后续实现完整映射表。
    """
    # TODO: 实现完整的外应→八卦映射
    return None


# ═══════════════════════════════════════════
# 5. CLI 测试入口
# ═══════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 50)
    print("起卦引擎测试")
    print("=" * 50)

    # ─── 测试1：梅花日期起卦 ───
    print("\n【测试1：梅花易数日期起卦】")
    print("时间：2026-05-17 13:00")
    mh = meihua_date_qigua(2026, 5, 17, 13)
    print(f"  卦名：{mh['卦名']}")
    print(f"  上卦：{mh['上卦']}  下卦：{mh['下卦']}")
    print(f"  动爻：第{mh['变爻']}爻")
    print(f"  体卦：{mh['体卦']}  用卦：{mh['用卦']}")
    print(f"  变卦：{mh['变卦']['卦名']}")
    print(f"  六爻编码：{mh['hexagram_encoding']}")
    print(f"  爻象展示：")
    for line in encoding_to_display(mh['hexagram_encoding']):
        print(f"    {line}")

    # ─── 测试2：随机掷铜钱 ───
    print("\n【测试2：随机掷铜钱起卦】")
    ct = coin_toss_random()
    print(f"  卦名：{ct['卦名']}")
    print(f"  动爻：{ct['动爻']}")
    print(f"  六爻编码：{ct['hexagram_encoding']}")
    print(f"  详细记录：")
    for s in ct['toss_summary']:
        print(f"    {s['爻位']}: {s['coins']} → {s['背数']}背{s['字数']}字 → {s['结果']} {s['爻象']}")

    # ─── 测试3：手动铜钱输入 ───
    print("\n【测试3：手动铜钱输入】")
    manual = coin_toss_interactive_input(["3背", "2背1字", "1背2字", "3字", "2背1字", "1背2字"])
    print(f"  卦名：{manual['卦名']}")
    print(f"  动爻：{manual['动爻']}")
    print(f"  六爻编码：{manual['hexagram_encoding']}")

    # ─── 测试4：桥接到六爻排盘 ───
    print("\n【测试4：起卦→六爻纳甲排盘】")
    dt = datetime(2026, 5, 17, 13, 0)
    result = qigua_full_pailian(mh['hexagram_encoding'], dt, "测试起卦")
    print(f"  本卦：{result['本卦']['名']} ({result['本卦']['宫']})")
    print(f"  世爻：{result['本卦']['世爻']}  应爻：{result['本卦']['应爻']}")
    print(f"  旬空：{result['旬空']}")
