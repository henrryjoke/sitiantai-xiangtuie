# API 参考 | API Reference

> **本仓库仅公开 Skill 框架和类象知识库。核心算法（旺衰精算、象展开权重、四象合参融合）不在此处公开，仅通过 API 提供服务。**

## 基础地址

```
https://api.sitiantai.com/v1
```

## 认证

所有 API 请求需要在 HTTP Header 中携带 API Key：

```
Authorization: Bearer <your-api-key>
```

## 可用接口

### 1. 历法精算 `/api/calendar`

**请求**：
```
POST /api/calendar
{
  "datetime": "2026-05-17 14:00",
  "timezone": "Asia/Shanghai"
}
```

**响应**：
```json
{
  "bazi": {"year": "丙午", "month": "乙巳", "day": "丙寅", "hour": "乙未"},
  "jieqi": {"current": "立夏", "next": "芒种"},
  "xunkong": ["戌", "亥"],
  "yuejian": "巳"
}
```

### 2. 梅花易数起卦 `/api/meihua`

**请求**：
```
POST /api/meihua
{
  "datetime": "2026-05-17 14:00",
  "timezone": "Asia/Shanghai"
}
```

**响应**：
```json
{
  "卦名": "风天小畜",
  "上卦": "巽", "下卦": "乾",
  "体卦": "巽", "用卦": "乾",
  "变爻": 3,
  "变卦": {"上卦":"巽", "下卦":"兑", "卦名":"风泽中孚"},
  "互卦": {}, "错卦": {}, "综卦": {}
}
```

### 3. 六爻纳甲排盘 `/api/liuyao`

**请求**：
```
POST /api/liuyao
{
  "hexagram_encoding": [1,2,2,1,2,3],
  "datetime": "2026-05-17 14:00",
  "reason": "事业发展"
}
```

### 4. 类象展开 `/api/xiang`

**请求**：
```
GET /api/xiang/query?symbol=妻财&context=career
GET /api/xiang/expand?symbol=妻财&context=career
GET /api/xiang/multi?symbols=乾,巽,官鬼&context=career
GET /api/xiang/wuxing?symbols=乾,巽
```

### 5. 综合推演 `/api/deduce`

**请求**：
```
POST /api/deduce
{
  "method": "meihua_date",
  "datetime": "2026-05-17 14:00",
  "reason": "事业发展"
}
```

**响应**：综合推演结果（卦象总览 + 象展开 + 可能性推演 + 启发提问）

### 6. 大六壬 `/api/liuren`

### 7. 奇门遁甲 `/api/qimen`

---

## 使用限制

- 免费套餐：每日 50 次 API 调用
- 专业套餐：按需定制
- 详情请联系：api@sitiantai.com

---

## 错误码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | API Key 无效 |
| 429 | 超出调用限制 |
| 500 | 服务端错误 |
