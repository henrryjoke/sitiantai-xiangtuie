"""
xiang_query.py — 类象知识库查询引擎（开源层）

注：核心实现已移至 protected/xiang_engine.py（保护层）
此文件仅作为公开接口包装器。
"""
from .protected.xiang_engine import XiangQuery

__all__ = ["XiangQuery"]
