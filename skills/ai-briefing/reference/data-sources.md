# 数据源详细说明

## 1. GitHub Trending

**采集方式**: WebFetch

**目标URL**:
- `https://github.com/trending?since=daily`
- `https://github.com/trending?since=weekly`

**筛选条件**: AI/Agent/MCP/Coding Agent 相关项目

**记录字段**:
- 项目名
- Star数
- 描述
- 编程语言

---

## 2. 猫猫新闻

**采集方式**: WebFetch

**目标URL**: `https://maomu.com/news`

**筛选条件**: AI、编程、开源、Agent、大模型 相关条目

**记录字段**:
- 标题
- 摘要
- 时间

---

## 3. Arxiv

**采集方式**: WebSearch

**搜索关键词**（`{current_year}` 在执行时替换为当天日期所在年份，不要写死年份）:
- `site:arxiv.org AI agent multi-agent coding {current_year}`
- `arxiv new paper LLM agent software engineering this week`

**记录字段**:
- 论文标题
- 摘要要点
- 链接

---

## 失败处理

如某数据源抓取失败：
1. 跳过该源，继续其他数据源采集
2. 在HTML报告中注明失败的数据源
3. 不要因单个源失败而中断整个流程