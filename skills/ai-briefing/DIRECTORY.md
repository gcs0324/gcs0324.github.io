# AI Intelligence Briefing Skill 目录结构

```
ai-briefing/
├── SKILL.md                    # 主技能定义文件（核心执行流程）
├── README.md                   # 说明文档（使用指南）
├── CHANGELOG.md                # 版本变更记录
├── LICENSE                     # MIT版权文件
├── .gitignore                  # Git忽略文件配置
├── STRUCTURE.md                # 目录结构说明
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
    └── report-YYYY-MM-DD.html  # HTML报告（按日期命名）
```

## 文件统计

- **总文件数**: 12个文件
- **配置文件**: 2个JSON文件
- **模板文件**: 1个HTML文件
- **参考文档**: 3个Markdown文件
- **核心文件**: 6个文件（SKILL.md、README.md、CHANGELOG.md、LICENSE、.gitignore、STRUCTURE.md）