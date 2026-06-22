# AI Intelligence Briefing Skill

AI研发情报分析 Skill - 从多源采集AI资讯，深度分析趋势和弱信号，生成可执行的情报报告。

## ✨ 功能特性

- **多源数据采集**: GitHub Trending、猫猫新闻、Arxiv
- **智能分析**: 重要性评分、深度分析、Developer ROI Engine
- **Signal Radar**: 发现未来3-12个月可能爆发的弱信号和新兴趋势
- **趋势地图**: 萌芽→成长→爆发→成熟 四阶段趋势可视化
- **学习建议**: 本周/本月最值得学习的内容
- **实验项目**: 周末可完成的Side Project推荐
- **工具推荐**: 最值得尝试的新工具
- **行动清单**: P0/P1/P2分级行动建议

## 🚀 使用方法

### 基本用法

```
/ai-briefing
```

### 指定关注方向

```
/ai-briefing {"focus":["agent","mcp","coding-agent"]}
```

### 深度分析模式

```
/ai-briefing {"depth":"deep"}
```

### 完整参数

```json
{
  "focus": ["agent", "coding-agent", "mcp", "ai-engineering"],
  "depth": "deep"
}
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `focus` | 不限定 | 限定关注方向，覆盖数据源 filters，过滤和 ROI 评分向该方向倾斜 |
| `depth` | `"deep"` | `quick` 仅简要分析；`deep` 完整执行全部 Phase |

## 📊 输出

执行完成后，在技能目录下的 `output/` 目录生成:

| 文件                       | 说明                    |
|--------------------------|-----------------------|
| `report-YYYY-MM-DD.html` | 自包含HTML报告（暗色主题，响应式设计），按日期命名，历史报告保留 |

## 📋 报告结构

| Section   | 内容                 |
|-----------|--------------------|
| 首页        | 日期 + 一句话总结         |
| Section 1 | 今日Top10动态          |
| Section 2 | GitHub高价值项目        |
| Section 3 | Signal Radar（信号雷达） |
| Section 4 | 趋势地图               |
| Section 5 | 学习建议               |
| Section 6 | 实验项目推荐             |
| Section 7 | 工具推荐               |
| Section 8 | 行动清单               |

## 🎯 评分体系

### 重要性评分 (0-100)

```
importance_score = (技术价值 + 创新性 + 实用价值 + 对研发工程师影响 + 半年影响力) * 2
```

### Signal Score (0-100)

```
Signal Score = GitHub热度 * 0.4 + 新闻热度 * 0.2 + 论文增长率 * 0.3 + 持续时间 * 0.1
```

输入与三个实际采集源一一对应（GitHub Trending / 猫猫新闻 / Arxiv）；某项输入缺失时重新归一化权重并在报告中标注「基于 N/3 项数据源输入」。

### 信号等级

| 分数    | 等级    |
|-------|-------|
| 0-30  | 噪音    |
| 30-50 | 弱信号   |
| 50-70 | 值得关注  |
| 70-90 | 高价值趋势 |
| 90+   | 下一代方向 |

## 📁 目录结构

```
ai-briefing/
├── SKILL.md                    # 主技能定义文件
├── README.md                   # 说明文档
├── CHANGELOG.md                # 版本变更记录
├── LICENSE                     # 版权文件
├── .gitignore                  # Git忽略文件
├── assets/                     # 静态资源目录
│   └── templates/              # 模板文件
│       └── html-template.html  # HTML报告模板
├── scripts/                    # 脚本文件目录
│   └── data-sources.json       # 数据源配置
├── data/                       # 数据文件目录
│   └── scoring-weights.json    # 评分权重配置
├── reference/                  # 参考文档目录
│   ├── data-sources.md         # 数据源详细说明
│   ├── scoring-system.md       # 评分体系详细说明
│   └── output-format.md        # 输出格式详细说明
└── output/                     # 输出目录
    └── report-YYYY-MM-DD.html  # HTML报告（按日期命名）
```

## 📚 参考文档

- [数据源详细说明](reference/data-sources.md)
- [评分体系详细说明](reference/scoring-system.md)
- [输出格式详细说明](reference/output-format.md)

## 📄 License

MIT