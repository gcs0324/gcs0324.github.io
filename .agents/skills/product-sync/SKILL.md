---
name: product-sync
description: |
  同步 WorkBuddy 和 AI-Briefing 产物到 gcs0324.github.io 项目。
  触发场景：用户说"同步产物"、"sync products"、"导入产物"、"更新产物"、
  "把 WorkBuddy 产物加进来"、"更新 AI 情报"、引用 WorkBuddy 目录中的文件路径、
  或任何涉及将 Codex 生成的 HTML/MD 报告导入到静态站点的工作。
  也适用于新增 AI-Briefing 报告后需要更新索引页和首页卡片的场景。
---

# 产物同步 Skill

将 WorkBuddy 和 AI-Briefing 生成的 HTML/MD 产物同步到 gcs0324.github.io 项目中，自动更新索引页和首页卡片。

## 项目结构速览

```
项目根目录/
├── workbuddy/           # WorkBuddy 产物目录（含 index.html）
│   ├── index.html       # 产物汇总页（需保持最新）
│   ├── *.html           # 独立 HTML 长文
│   └── *.md             # Markdown 报告
├── ai-briefing/         # AI 研发情报目录（含 index.html）
│   ├── index.html       # 情报汇总页（需保持最新）
│   └── report-*.html    # 各期报告
├── index.html           # 首页 Dashboard（含卡片和侧栏）
└── shared/
    ├── theme.css        # 统一主题变量
    └── theme.js         # 主题切换脚本
```

源目录：
- WorkBuddy 源：`/Users/cs_beike/WorkBuddy/` 下各时间戳子目录
- AI-Briefing 报告源：由 ai-briefing skill 直接生成到 `ai-briefing/` 目录

## 执行流程

### 第一步：扫描增量

**WorkBuddy：**
1. `find /Users/cs_beike/WorkBuddy -name "*.html" -type f` 获取所有源 HTML
2. 对比 `workbuddy/` 目录中已有的文件，找出未导入的新文件
3. 同样检查 `*.md` 文件（如调研报告、速查手册）

**AI-Briefing：**
1. `ls ai-briefing/report-*.html` 获取已有报告
2. 对比 `ai-briefing/index.html` 中已列出的报告，找出新增的

### 第二步：导入新文件

```bash
# WorkBuddy HTML
cp /Users/cs_beike/WorkBuddy/<session-dir>/<file>.html workbuddy/

# WorkBuddy MD
cp /Users/cs_beike/WorkBuddy/<session-dir>/<file>.md workbuddy/
```

### 第三步：提取元数据

对每个新文件，提取标题和描述：

```bash
# HTML 文件标题
grep -i "<title>" <file> | head -1 | sed 's/<[^>]*>//g' | xargs

# MD 文件标题（第一个 # 开头行）
head -3 <file> | grep "^#" | head -1 | sed 's/^#* *//'
```

从文件名中推断日期：
- WorkBuddy 文件：看所在 session 目录名 `YYYY-MM-DD-HH-MM-SS`
- AI-Briefing 报告：文件名中的日期 `report-YYYY-MM-DD.html`

### 第四步：更新 workbuddy/index.html

在 `<main>` 区域的合适 `<div class="sec">` 下添加新的 card：

```html
<div class="card">
  <div class="card-icon"><emoji></div>
  <div class="card-body">
    <div class="card-title"><a href="<filename>"><title></a></div>
    <div class="card-meta"><span class="tag html">HTML</span> <date> · <category></div>
    <div class="card-desc"><description></div>
  </div>
</div>
```

**分类规则：**
- AI/技术深度研究 → 放在 `AI & 技术深度研究` section 下
- Agent/记忆系统 → 放在 `Agent & 记忆系统` section 下
- 实用工具/生活 → 放在 `实用工具` section 下

**图标选择：**
- 技术架构类：🔬 🦌 🖥️
- AI/Agent 类：🧠 📋
- 学习路径类：🧭 📖
- 商业报告类：💼
- 实用工具类：🏠

根据文件内容选择合适的 emoji 和 section。

同时更新页面顶部的统计数据 `"<strong>N</strong> 篇产物"`。

### 第五步：更新 ai-briefing/index.html

在"最新报告" section 最前面插入新卡片：

```html
<div class="card">
  <div class="card-icon">📡</div>
  <div class="card-body">
    <div class="card-title"><a href="<filename>">AI Intelligence Briefing · <date></a></div>
    <div class="card-meta"><date> · 第N期</div>
    <div class="card-desc"><description></div>
  </div>
</div>
```

更新概览区的期数统计。

### 第六步：更新 index.html（首页 Dashboard）

**更新 DEFAULT_CARDS 中的卡片链接：**

1. **AI 研发情报卡片**（`icon: '📡'`）：在 links 数组最前面插入新报告的链接，保持日期倒序
2. **WorkBuddy 产物卡片**（`icon: '🤖'`）：在 links 数组最前面插入新产物的链接
3. 如果卡片不存在，创建新卡片

**更新 CARDS_VERSION：**
```javascript
var CARDS_VERSION = <当前版本 + 1>;
```
递增版本号会触发浏览器重置为新的 DEFAULT_CARDS。

### 第七步：更新侧栏链接

如果侧栏中还没有 workbuddy 或 ai-briefing 的链接，在"AI 工具"子分类下添加：
```html
<li><a href="workbuddy/index.html" target="_blank">WorkBuddy · AI 深度研究产物</a></li>
<li><a href="ai-briefing/index.html" target="_blank">AI 研发情报 · 趋势简报</a></li>
```

### 第八步：提交

```bash
git add workbuddy/ ai-briefing/ index.html
git commit -m "feat(product-sync): sync WorkBuddy & AI-Briefing products (<date>)

- Import <N> new WorkBuddy files
- Update AI-Briefing report list
- Bump CARDS_VERSION to <version>"
```

## 注意事项

- **不要重复导入**：对比文件名确认文件是否已存在，已存在则跳过
- **保持格式一致**：新卡片必须与现有卡片使用相同的 HTML 结构和 CSS 类
- **日期格式**：WorkBuddy 使用 `YYYY-MM-DD`，AI-Briefing 使用 `YYYY年M月D日`
- **MD 文件处理**：Markdown 文件在卡片中使用 `.md` 扩展名链接，GitHub Pages 会渲染或下载
- **index.html 的 CARDS_VERSION**：每次修改 DEFAULT_CARDS 都必须递增，否则已访问过的用户看到的仍是旧版（localStorage 缓存）
- **检查 AI-Briefing 是否需要创建 index.html**：如果 `ai-briefing/index.html` 不存在（首次使用），需要从模板创建完整的汇总页
- **检查 WorkBuddy 是否需要创建 index.html**：同理，如果 `workbuddy/index.html` 不存在，需要从模板创建

## 产出物说明

执行完毕后，向用户报告：
- 新增了哪些文件
- 更新了哪些索引页
- CARDS_VERSION 从 X 变为 Y
- commit hash
