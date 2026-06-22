# 输出格式详细说明

## HTML报告

**输出路径**: `output/report-YYYY-MM-DD.html`（相对于技能目录，YYYY-MM-DD 为当天日期；同日多次运行覆盖当日文件，历史日期报告保留）

**特性**:

- 自包含HTML文件（所有CSS内联）
- 暗色主题
- 响应式设计（支持移动端）
- 使用语义化HTML标签
- 所有外部链接可点击
- 评分使用彩色标签显示

### 报告结构

| Section   | 内容                 |
|-----------|--------------------|
| 首页        | 日期 + 一句话总结         |
| Section 1 | 今日Top10动态          |
| Section 2 | GitHub高价值项目        |
| Section 3 | Signal Radar（信号雷达），信号分数有输入缺失时必须标注「基于 N/3 项数据源输入」 |
| Section 4 | 趋势地图               |
| Section 5 | 学习建议               |
| Section 6 | 实验项目推荐             |
| Section 7 | 工具推荐               |
| Section 8 | 行动清单               |

### HTML模板

详见 [assets/templates/html-template.html](../assets/templates/html-template.html)

---

## 输出位置

HTML报告存放在技能目录下的 `output/` 目录：

```
output/
├── report-2026-06-04.html    # 历史报告（保留）
└── report-2026-06-12.html    # 当日报告
```

---

## 完成提示

执行完成后，告知用户：

1. 报告已生成的位置
2. 一句话总结本次分析的主要发现