"""
xiang_query.py — 类象知识库查询引擎（司天监象推演系统）

Phase 1.5 SDK — 符号→现实语义 展开查询
支持：数据中心化加载 / 符号查询 / 语境过滤 / 维度筛选 / 批量查询 / 可读展开
"""

import json, os
from typing import Dict, List, Optional, Any


class XiangQuery:
    """类象知识库查询引擎"""

    def __init__(self, data_dir: str = None):
        """data_dir: 类象JSON根目录，默认 workspace/data/xiang"""
        if data_dir is None:
            # 自动定位：从此脚本所在目录推断 workspace
            script_dir = os.path.dirname(os.path.abspath(__file__))
            workspace = os.path.dirname(os.path.dirname(script_dir))
            data_dir = os.path.join(workspace, "data", "xiang")
            if not os.path.isdir(data_dir):
                # 备用：绝对路径
                data_dir = r"E:\qclaw\workspace-sitiantai\data\xiang"
        self.data_dir = data_dir
        self._cache: Dict[str, dict] = {}
        self._index: Dict[str, str] = {}  # symbol → category
        self._load_all()

    # ── 数据加载 ──────────────────────────────

    def _load_all(self):
        """递归加载 data_dir 下所有 JSON"""
        if not os.path.isdir(self.data_dir):
            return
        for root, dirs, files in os.walk(self.data_dir):
            for fn in files:
                if fn.endswith(".json"):
                    path = os.path.join(root, fn)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        symbol = data.get("symbol", "")
                        category = data.get("category", "")
                        self._cache[symbol] = data
                        self._index[symbol] = category
                    except Exception:
                        pass

    def available_symbols(self) -> List[str]:
        """列出所有已加载的符号"""
        return sorted(self._index.keys())

    def available_categories(self) -> List[str]:
        """列出所有已加载的类别"""
        cats = set(v for v in self._index.values())
        return sorted(cats)

    # ── 查询接口 ──────────────────────────────

    def query(self, symbol: str, context: Optional[str] = None,
              dimension: Optional[str] = None) -> Optional[Dict]:
        """
        查询一个符号的类象数据

        Args:
            symbol:   符号名，如 "乾"、"妻财"、"青龙"
            context:  语境过滤，如 "career"、"health"，None=全部语境
            dimension: 维度过滤，如 "person"、"state"，None=全部维度

        Returns:
            {"symbol":..., "category":..., "context":..., "result":...}
            或 None
        """
        data = self._cache.get(symbol)
        if data is None:
            return None

        contexts = data.get("contexts", {})

        # 构建结果
        if context and context in contexts:
            ctx_data = contexts[context]
            result = self._filter_dimension(ctx_data, dimension)
            return {
                "symbol": symbol,
                "category": data.get("category"),
                "wu_xing": data.get("wu_xing"),
                "core_properties": data.get("core_properties", []),
                "context": context,
                "result": result,
            }
        elif context:
            # 指定语境不存在→fallback到general
            ctx_data = contexts.get("general", {})
            result = self._filter_dimension(ctx_data, dimension)
            return {
                "symbol": symbol,
                "category": data.get("category"),
                "wu_xing": data.get("wu_xing"),
                "core_properties": data.get("core_properties", []),
                "context": "general",
                "fallback": True,
                "result": result,
            }
        else:
            # 返回所有语境
            all_ctx = {}
            for ctx_name, ctx_data in contexts.items():
                all_ctx[ctx_name] = self._filter_dimension(ctx_data, dimension)
            return {
                "symbol": symbol,
                "category": data.get("category"),
                "wu_xing": data.get("wu_xing"),
                "core_properties": data.get("core_properties", []),
                "context": None,
                "result": all_ctx,
            }

    def _filter_dimension(self, ctx_data: dict, dimension: Optional[str]) -> dict:
        """按维度过滤语境数据"""
        if dimension:
            return {dimension: ctx_data.get(dimension, [])}
        return dict(ctx_data)

    def expand_full(self, symbol: str, context: Optional[str] = None) -> str:
        """
        展开为人类可读的段落文字

        Args:
            symbol: 符号名
            context: 语境，如"career"

        Returns:
            人类可读的多行文本
        """
        result = self.query(symbol, context=context)
        if result is None:
            return f"【{symbol}】未找到对应的类象数据。"

        lines = []
        props = result.get("core_properties", [])
        wuxing = result.get("wu_xing", "")
        lines.append(f"【{symbol}】")
        lines.append(f"五行: {wuxing}　核心属性: {'、'.join(props)}")
        lines.append("")

        if context and result.get("context"):
            # 单语境展开
            ctx_name = result["context"]
            data = result.get("result", {})
            lines.append(f"语境: {ctx_name}")
            lines.append(self._format_dimensions(data))
        else:
            # 多语境展开
            all_ctx = result.get("result", {})
            for ctx_name in ["general", "career", "health", "relationship", "finance"]:
                if ctx_name in all_ctx:
                    lines.append(f"语境: {ctx_name}")
                    lines.append(self._format_dimensions(all_ctx[ctx_name]))
                    lines.append("")

        return "\n".join(lines).strip()

    def _format_dimensions(self, data: dict) -> str:
        """格式化维度数据为文字"""
        dim_names = {
            "person": "人物", "object": "物品", "time": "时间",
            "space": "空间", "state": "状态",
        }
        lines = []
        for dim, items in data.items():
            if items and dim != "core_properties":
                name = dim_names.get(dim, dim)
                lines.append(f"  {name}: {'、'.join(items)}")
        return "\n".join(lines)

    def multi_query(self, symbols: List[str], context: Optional[str] = None) -> List[Dict]:
        """批量查询多个符号"""
        results = []
        for sym in symbols:
            r = self.query(sym, context=context)
            if r:
                results.append(r)
        return results

    # ── 便捷方法 ──────────────────────────────

    def expand_for_context(self, symbols: List[str], context: str) -> str:
        """为指定语境批量展开多个符号，合并输出"""
        all_text = []
        for sym in symbols:
            text = self.expand_full(sym, context=context)
            all_text.append(text)
        return "\n\n".join(all_text)

    def get_wuxing_combo(self, symbols: List[str]) -> Dict[str, str]:
        """获取多个符号的五行组合"""
        result = {}
        for sym in symbols:
            data = self._cache.get(sym, {})
            result[sym] = data.get("wu_xing", "未知")
        return result


# ══════════════════════════════════════════════
# 测试入口
# ══════════════════════════════════════════════

if __name__ == "__main__":
    q = XiangQuery()

    print("=== 已加载符号 ===")
    print(q.available_symbols())
    print()

    # 测试：乾卦 career语境 person维度
    r = q.query("乾", context="career", dimension="person")
    print("【query('乾', 'career', 'person')】")
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print()

    # 测试：展开全文
    print("【expand_full('乾', 'health')】")
    print(q.expand_full("乾", context="health"))
    print()

    # 测试：批量查询
    m = q.multi_query(["乾", "坤", "震"], context="general")
    print(f"【multi_query】 返回 {len(m)} 个结果")

    print("\n=== 完成 ===")