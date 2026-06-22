# AI Intelligence Briefing Skill 目录结构

```
ai-briefing/
├── SKILL.md                    # 主技能定义文件（核心执行流程）
├── README.md                   # 说明文档（使用指南）
├── CHANGELOG.md                # 版本变更记录
├── LICENSE                     # MIT版权文件
├── .gitignore                  # Git忽略文件配置
│
├── assets/                     # 静态资源目录
│   └── templates/              # 模板文件
│       └── html-template.html  # HTML报告模板（暗色主题）
│
├── scripts/                    # 脚本文件目录
│   └── data-sources.json       # 数据源配置（3个数据源）
│
├── data/                       # 数据文件目录
│   └── scoring-weights.json    # 评分权重配置
│
├── reference/                  # 参考文档目录
│   ├── data-sources.md         # 数据源详细说明
│   ├── scoring-system.md       # 评分体系详细说明
│   └── output-format.md        # 输出格式详细说明
│
└── output/                     # 输出目录（运行时生成）
    └── report-YYYY-MM-DD.html  # HTML报告（按日期命名，历史报告保留）
```

## 文件说明

### 核心文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 主技能定义文件，包含核心执行流程和质量规则 |
| `README.md` | 用户使用指南，包含安装、使用方法、功能说明 |

### 配置文件

| 文件 | 说明 |
|------|------|
| `scripts/data-sources.json` | 3个数据源的详细配置（URL、筛选条件、记录字段）|
| `data/scoring-weights.json` | 评分体系权重配置（重要性、信号、ROI评分）|

### 模板文件

| 文件 | 说明 |
|------|------|
| `assets/templates/html-template.html` | HTML报告模板，包含完整的CSS样式 |

### 参考文档

| 文件 | 说明 |
|------|------|
| `reference/data-sources.md` | 各数据源的采集方式、URL、筛选条件详细说明 |
| `reference/scoring-system.md` | 评分体系详细说明（重要性、信号、ROI评分）|
| `reference/output-format.md` | 输出格式详细说明（HTML）|

### 版本管理

| 文件 | 说明 |
|------|------|
| `CHANGELOG.md` | 版本变更记录，遵循Keep a Changelog格式 |
| `LICENSE` | MIT版权文件 |
| `.gitignore` | Git忽略配置，排除output目录等 |

## 设计原则

1. **模块化**: 将不同功能拆分到独立文件，便于维护
2. **可配置**: 评分权重、数据源等通过JSON配置文件管理
3. **可扩展**: 新增数据源或评分维度只需修改配置文件
4. **文档化**: 每个模块都有详细的参考文档说明

## 数据源

当前支持的数据源：
- **GitHub Trending** - AI/Agent/MCP/Coding Agent相关项目
- **猫猫新闻** - AI/编程/开源/Agent/大模型相关条目
- **Arxiv** - Agent/多智能体/Coding Agent/SE相关论文