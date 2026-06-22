# Changelog

All notable changes to the AI Intelligence Briefing Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-06-12

基于 skill-eval 评测结果（综合分 72，详见 eval-runs/ai-briefing-20260612）的修复版本。

### Fixed
- 修复 Phase 4 数据依赖断裂：Signal Radar 和信号公式只使用实际采集的三个数据源（GitHub热度×0.4 + 新闻热度×0.2 + 论文增长率×0.3 + 持续时间×0.1），移除无数据来源的「社区讨论度」「KOL提及率」输入
- 新增缺失输入规则：输入缺失时权重重新归一化，并在报告中标注「基于 N/3 项数据源输入」，禁止为缺失输入估值
- 修复 description 与实际数据源不一致（移除 HN/Reddit 表述，与 v1.1.0 移除决定对齐）
- 修复 scoring-weights.json 阈值歧义：`{delete:40, brief_analysis:60, deep_analysis:60}` → `{delete_below:40, brief_min:40, deep_min:60}`
- 移除 Arxiv 搜索词中硬编码的年份 2026，改为 `{current_year}` 占位符

### Added
- description 增加负向触发边界（不适用于股市/金融AI概念分析、单篇论文精读、特定公司研究）
- SKILL.md 增加 focus/depth 参数说明表，明确参数语义和未知参数处理
- scoring-system.md 增加五个评分维度的 0/5/10 分打分锚点，保证跨运行评分一致性

### Changed
- 报告文件名改为按日期命名 `output/report-YYYY-MM-DD.html`，历史报告保留

## [1.1.0] - 2026-06-04

### Changed
- 移除不可访问的数据源（Hacker News、Reddit、Twitter/X）
- 保留可访问的数据源（GitHub Trending、猫猫新闻、Arxiv）
- 移除JSON输出，仅保留HTML报告
- 修改输出路径为通用路径（相对于技能目录）

## [1.0.0] - 2026-06-04

### Added
- 多源数据采集（GitHub、猫猫新闻、Hacker News、Reddit、Arxiv、Twitter/X）
- 智能分析系统（重要性评分、深度分析、Developer ROI Engine）
- Signal Radar（信号雷达）系统
- 趋势地图（萌芽→成长→爆发→成熟）
- 学习建议生成
- 实验项目推荐
- 工具推荐
- 行动清单（P0/P1/P2分级）
- HTML报告输出（暗色主题、响应式设计）
- JSON摘要输出（结构化数据，供其他Agent消费）

### Changed
- 按照技能标准目录结构重组项目文件
- 优化README文档，使其更清晰精简
- 拆分SKILL.md，将详细说明移至reference目录
- 创建配置文件目录（scripts、data、assets）