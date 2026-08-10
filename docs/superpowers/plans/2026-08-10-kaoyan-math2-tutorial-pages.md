# 数学二 110 分专题教程页 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有数学二总纲扩展为九页、面向 110 分目标的教程体系。

**Architecture:** 保留总纲作为学习入口，新增五张高数页和三张线代页。每页为独立静态 HTML，沿用共享主题文件，并采用统一决策矩阵、教程例题和前后章导航。

**Tech Stack:** HTML5、页面内 CSS、内嵌 SVG、`shared/theme.css`、`shared/theme.js`、Python 标准库静态检查。

## Global Constraints

- A/B/C 标签依次使用红、蓝、灰。
- 考频极高用红，高和中高用橙，中用蓝，低用灰。
- A 类例题必须包含规则来源、具体数字、关键中间值、结果检查和易错点。
- B 类只展开标准考法，C 类不添加长例题。
- 经验分值不能相加，考频不是命题概率。
- 不覆盖、暂存或提交无关并行改动。

---

### Task 1: 建立页面结构验收

**Files:**
- Create: `tests/verify_math2_tutorial_pages.py`

**Interfaces:**
- Consumes: 九个约定的数学页面路径。
- Produces: 可重复运行的结构、标签、锚点、互链和首页入口检查。

- [ ] 写检查：九页存在；专题页含七列矩阵、A/B/C 与四级考频标签、至少三道例题、有效锚点和前后章链接。
- [ ] 运行检查，确认因八页尚未创建而失败。

### Task 2: 生成五张高等数学专题页

**Files:**
- Create: `doc/kaoyan-math2-limit.html`
- Create: `doc/kaoyan-math2-derivative.html`
- Create: `doc/kaoyan-math2-integral.html`
- Create: `doc/kaoyan-math2-multivariable.html`
- Create: `doc/kaoyan-math2-ode.html`

**Interfaces:**
- Consumes: `shared/theme.css`、`shared/theme.js` 与设计规范。
- Produces: 五张可独立学习且前后互链的高数教程页。

- [ ] 极限页覆盖方法选择、等价无穷小、洛必达/Taylor、数列极限和连续间断。
- [ ] 微分页覆盖导数定义、复合/隐函数、高阶导数、中值定理、性态和曲率边界。
- [ ] 积分页覆盖换元/分部、定积分性质、变限积分、反常积分和几何应用。
- [ ] 多元页覆盖偏导/全微分、复合/隐函数、极值、直角与极坐标二重积分。
- [ ] 微分方程页覆盖类型识别、一阶方程、降阶、二阶常系数和简单建模。
- [ ] 运行结构检查，确认五张高数页通过且线代页仍按预期缺失。

### Task 3: 生成三张线性代数专题页

**Files:**
- Create: `doc/kaoyan-math2-matrix.html`
- Create: `doc/kaoyan-math2-vector-equations.html`
- Create: `doc/kaoyan-math2-eigen-quadratic.html`

**Interfaces:**
- Consumes: 高数页的统一页面结构和导航约定。
- Produces: 三张可独立学习且与高数链路连续的线代教程页。

- [ ] 矩阵页覆盖行列式、矩阵运算、逆、初等变换、秩和矩阵方程。
- [ ] 向量方程页覆盖线性相关、极大无关组、齐次/非齐次方程组和参数分类。
- [ ] 特征二次型页覆盖特征值、相似对角化、正交对角化、二次型与正定性。
- [ ] 运行结构检查，确认八张专题页全部通过。

### Task 4: 改造总纲并更新首页

**Files:**
- Modify: `doc/kaoyan-math2-110.html`
- Modify: `index.html`

**Interfaces:**
- Consumes: 八张专题页路径。
- Produces: 总纲章节入口、首页九页入口和一致的彩色标签。

- [ ] 将总纲七列表头统一为“要不要学、考频、经验分值、考察题型、学到什么程度”。
- [ ] 为 H01～H05、L01～L03 添加对应专题入口。
- [ ] 在首页侧栏和卡片数据中添加八张专题页，并更新卡片缓存版本。
- [ ] 运行结构检查，确认首页每个入口出现两次且路径存在。

### Task 5: 全量静态与浏览器验收

**Files:**
- Verify: `doc/kaoyan-math2-*.html`
- Verify: `index.html`

**Interfaces:**
- Consumes: 九张数学页面和首页入口。
- Produces: 桌面、移动端与内容规范验收结果。

- [ ] 运行 `python3 tests/verify_math2_tutorial_pages.py`，预期全部通过。
- [ ] 运行 `git diff --check`，预期无空白错误。
- [ ] 浏览器检查 1440×900 与 375×844：无页面级横向溢出、矩阵内部可滚动、控制台无错误。
- [ ] 抽查所有 A 类教程例题的步骤、结果验证和易错说明。
- [ ] 检查 Git 状态，只报告本次文件，不暂存、不提交。

### Task 6: 增加第一轮高收益解题步骤卡

**Files:**
- Modify: `scripts/generate_math2_topics.py`
- Modify: `shared/math2-topic.css`
- Modify: `tests/verify_math2_tutorial_pages.py`
- Regenerate: `doc/kaoyan-math2-limit.html`
- Regenerate: `doc/kaoyan-math2-derivative.html`
- Regenerate: `doc/kaoyan-math2-integral.html`
- Regenerate: `doc/kaoyan-math2-multivariable.html`
- Regenerate: `doc/kaoyan-math2-ode.html`
- Regenerate: `doc/kaoyan-math2-vector-equations.html`
- Regenerate: `doc/kaoyan-math2-eigen-quadratic.html`

**Interfaces:**
- Consumes: 每页已有的知识矩阵、方法主线和教程例题。
- Produces: 12 张可迁移的步骤卡，每张包含识别信号、至少四步、结果检查和易错点。

- [ ] 先扩展静态检查，要求 12 张卡按 2/3/3/1/1/1/1 分布在七个专题页。
- [ ] 运行检查，确认因步骤卡尚不存在而失败。
- [ ] 在生成器中增加结构化 `procedures` 数据和统一渲染函数。
- [ ] 补充步骤卡样式和移动端单列布局，重新生成八张专题页。
- [ ] 运行静态检查与浏览器验收，确认锚点、内容字段和移动端布局通过。

### Task 7: 将剩余十张步骤卡升级为完整图文教程

**Files:**
- Modify: `scripts/generate_math2_topics.py`
- Modify: `tests/verify_math2_tutorial_pages.py`
- Regenerate: `doc/kaoyan-math2-{limit,derivative,integral,multivariable,ode,vector-equations,eigen-quadratic}.html`

**Interfaces:**
- Consumes: Task 6 的 12 张步骤卡，以及间断点、不可导点已落地的正文型模板。
- Produces: 12 张统一的详细教程卡；每张包含目标、流程图、至少四步、完整例题、结果检查、易错点和考试速记。

- [ ] 把结构校验中的详细卡数量从 `1/1` 扩展为 `2/3/3/1/1/1/1`，运行并确认因剩余十张仍为简卡而失败。
- [ ] 为十张卡补充结构化教程数据，沿用统一渲染器，不复制十套页面骨架。
- [ ] 每张卡选择一个能覆盖核心分支的数字例题，写清方法依据、中间计算和反向检查。
- [ ] 重新生成八张专题页并运行结构校验，确认 12 张卡全部满足详细模板。
- [ ] 浏览器检查七张含步骤卡的页面：桌面双列/全宽布局正确，375×844 下正文无横向溢出，流程图仅在自身容器滚动。
- [ ] 检查暂存范围，提交并推送学习文档；排除技能安装文件。
