# 408 数据链路层学习页 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增一篇面向 408 总分 110 分目标的数据链路层考点页，包含必要 SVG 图解、学习取舍与首页入口。

**Architecture:** 页面保持单文件 HTML，与物理层文章共用主题脚本和样式变量；文章内局部 CSS 负责卡片、公式、优先级和 SVG 图解。首页只新增两处静态入口，不引入构建工具或外部运行时。

**Tech Stack:** HTML5、CSS、内嵌 SVG、现有 `shared/theme.css` 与 `shared/theme.js`

## Global Constraints

- 页面文件固定为 `doc/kaoyan-408-network-datalink.html`。
- 同步维护 `index.html` 的侧栏入口与 `defaultCards` 搜索数据入口。
- 内容按 2026 大纲组织，不把未明列的 HDLC 作为正文学习章节。
- 页面必须说明 408 满分 150、计网约 25 分、数据链路层经验分值与题型。
- 每个考点标 A 必学、B 会辨析、C 时间紧可跳过，不写虚假的精确命题概率。
- 必须包含滑动窗口、CSMA/CD、以太网帧格式、交换机自学习四张内嵌 SVG 图解。
- 不修改 `shared/theme.css` 或 `shared/theme.js`，不依赖外部图片。

---

### Task 1: 创建数据链路层学习页

**Files:**
- Create: `doc/kaoyan-408-network-datalink.html`

**Interfaces:**
- Consumes: `../shared/theme.css` 的颜色变量与 `../shared/theme.js` 的主题切换。
- Produces: 可直接从静态站点打开、锚点完整的独立知识页。

- [ ] **Step 1: 建立静态验收命令并确认页面尚不存在**

Run:

```bash
test ! -e doc/kaoyan-408-network-datalink.html
```

Expected: exit code 0。

- [ ] **Step 2: 编写完整 HTML**

实现页头、粘性导航、考情与 110 分策略、考纲正文、四张 SVG、速记表和典型例题。重点公式必须包括：

```text
CRC：发送码字 = 数据后补 r 个 0，再除以生成多项式得到 r 位余数
海明码：2^r >= k + r + 1
停止-等待：U = Tt / (Tt + 2Tp + Tack)
GBN：Wt <= 2^n - 1
SR：Wt = Wr，且 Wt <= 2^(n-1)
CSMA/CD：最短帧长 = 2τ × 数据率
```

- [ ] **Step 3: 校验 HTML 结构、锚点和内容约束**

Run:

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import re

p = Path("doc/kaoyan-408-network-datalink.html")
s = p.read_text()
HTMLParser().feed(s)
ids = set(re.findall(r'id="([^"]+)"', s))
hrefs = re.findall(r'href="#([^"]+)"', s)
assert hrefs and all(x in ids for x in hrefs)
assert len(ids) == len(re.findall(r'id="([^"]+)"', s))
for text in ["110 分", "A 必学", "B 会辨析", "C 时间紧可跳过",
             "CRC", "GBN", "CSMA/CD", "以太网帧", "交换机自学习"]:
    assert text in s, text
assert s.count("<svg") >= 4
assert "HDLC</h" not in s
print("page structure OK")
PY
```

Expected: 输出 `page structure OK`。

### Task 2: 注册首页入口

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: Task 1 产生的 `doc/kaoyan-408-network-datalink.html`。
- Produces: 侧栏与客户端搜索卡片均可访问新页面。

- [ ] **Step 1: 添加两处相邻入口**

在物理层链接后分别加入：

```html
<li><a href="doc/kaoyan-408-network-datalink.html" target="_blank">📖 408计网 · 数据链路层考点全解</a></li>
```

```javascript
{ text: '📖 408计网 · 数据链路层考点全解', url: 'doc/kaoyan-408-network-datalink.html' },
```

- [ ] **Step 2: 验证入口数量和目标文件**

Run:

```bash
test "$(rg -o 'doc/kaoyan-408-network-datalink.html' index.html | wc -l | tr -d ' ')" = "2"
test -f doc/kaoyan-408-network-datalink.html
```

Expected: 两条命令均返回 exit code 0。

### Task 3: 浏览器与内容验收

**Files:**
- Verify: `doc/kaoyan-408-network-datalink.html`
- Verify: `index.html`

**Interfaces:**
- Consumes: Tasks 1–2 的静态文件。
- Produces: 可交付的视觉与内容验证记录。

- [ ] **Step 1: 启动本地静态服务器**

Run:

```bash
python3 -m http.server 8080
```

Expected: 服务监听 `http://localhost:8080`。

- [ ] **Step 2: 在浏览器检查桌面端和移动端**

检查：

- 页头、粘性导航和主题切换正常。
- 四张 SVG 的文字不截断、不依赖颜色才能理解。
- 375px 宽度下正文无不可控横向溢出。
- 所有锚点点击后定位到对应小节。
- 首页两处入口指向新页面。

- [ ] **Step 3: 执行最终静态检查**

Run:

```bash
git diff --check
rg -n "TODO|TBD|lorem ipsum" doc/kaoyan-408-network-datalink.html
```

Expected: `git diff --check` 无输出，内容扫描无匹配。

- [ ] **Step 4: 提交实现**

```bash
git add doc/kaoyan-408-network-datalink.html index.html
git commit -m "feat: add 408 data link study guide"
```
