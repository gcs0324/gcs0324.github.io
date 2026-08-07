# 408 计算机网络剩余页面 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 按已确认的 110 分备考策略，补齐计算机网络体系结构、网络层、传输层和应用层四个 HTML 教程页面。

**Architecture:** 每章独立为一个 `doc/kaoyan-408-network-*.html`，沿用现有物理层和数据链路层的主题、导航、A/B/C 标记、例题与速记结构。内容以现行考纲主线为范围，以克隆的王道课件核对覆盖面；课件只作旧版参考，考频与真题年份不做无依据的精确承诺。

**Tech Stack:** 静态 HTML、内联 CSS、`../shared/theme.css`、`../shared/theme.js`、原生 SVG。

## Global Constraints

- 目标分数是 110/150，先保 A 类计算和稳定辨析，再覆盖 B 类，C 类只说明跳过理由。
- A 类必须包含规则来源、完整数字例题、逐步解法、结果检查和一到两个常见误区。
- B 类只用短场景解释应用；C 类不展开长例题。
- 未核实年份和题号的题目只标“真题型例题”或“常见问法”。
- 页面必须同步加载 `../shared/theme.css` 和同步的 `../shared/theme.js`，并具有粘性页内导航和移动端布局。
- 不改动工作区中与本任务无关的现有文件。

---

### Task 1: 体系结构页面

**Files:**
- Create: `doc/kaoyan-408-network-architecture.html`

**Interfaces:**
- Consumes: `shared/theme.css`, `shared/theme.js`, `WRITING.md`
- Produces: 从计网总览进入物理层的第一章教程页面

- [ ] **Step 1:** 写出考情、性能指标、分层、协议/服务/接口、OSI 与 TCP/IP 的 A/B/C 内容。
- [ ] **Step 2:** 为时延与吞吐量加入完整数值例题，明确各时延分项和瓶颈链路规则。
- [ ] **Step 3:** 加入分层封装 SVG、速记、易错和考试型练习。
- [ ] **Step 4:** 用 HTML 解析和链接检查验证页面。
- [ ] **Step 5:** 提交体系结构页面。

### Task 2: 网络层页面

**Files:**
- Create: `doc/kaoyan-408-network-network.html`

**Interfaces:**
- Consumes: 数据链路层知识、王道网络层课件覆盖清单
- Produces: IPv4、子网/CIDR、路由、ARP/ICMP/DHCP、IPv6 教程页面

- [ ] **Step 1:** 写 IPv4 首部、分片、特殊地址、NAT 的取舍内容。
- [ ] **Step 2:** 写子网划分、CIDR 聚合、最长前缀匹配的完整教程例题，并逐位解释依据。
- [ ] **Step 3:** 写跨路由器转发中 IP/MAC/ARP 的逐跳变化例题。
- [ ] **Step 4:** 写 RIP、OSPF、BGP、ICMP、DHCP、IPv6 的辨析与跳过边界。
- [ ] **Step 5:** 加入 SVG、速记、易错和考试型练习，验证后提交。

### Task 3: 传输层页面

**Files:**
- Create: `doc/kaoyan-408-network-transport.html`

**Interfaces:**
- Consumes: 网络层尽力交付语义、王道传输层课件覆盖清单
- Produces: UDP/TCP、可靠传输、连接管理、流量与拥塞控制教程页面

- [ ] **Step 1:** 写端口、复用分用、UDP/TCP 首部和语义对比。
- [ ] **Step 2:** 写 TCP 序号与确认号、超时/快速重传的完整例题。
- [ ] **Step 3:** 写三次握手、四次挥手和 2MSL 的过程图与常见题法。
- [ ] **Step 4:** 写接收窗口、拥塞窗口、慢开始与拥塞避免的逐 RTT 计算例题。
- [ ] **Step 5:** 加入速记、易错和考试型练习，验证后提交。

### Task 4: 应用层页面与入口收尾

**Files:**
- Create: `doc/kaoyan-408-network-application.html`
- Modify: `index.html`

**Interfaces:**
- Consumes: TCP/UDP 服务语义、王道应用层课件覆盖清单
- Produces: DNS、FTP、邮件、HTTP 页面以及四个新页面的首页入口

- [ ] **Step 1:** 写 C/S 与 P2P、DNS 递归/迭代查询、FTP 双连接、邮件协议和 HTTP 主线。
- [ ] **Step 2:** 用“输入 URL 后发生什么”串联 DNS、TCP、HTTP，并给时延型完整例题。
- [ ] **Step 3:** 加入常用端口、速记、易错、考试型练习和 C 类跳过清单。
- [ ] **Step 4:** 更新首页计网链接，形成体系结构到应用层的完整顺序。
- [ ] **Step 5:** 本地启动静态服务器，逐页检查桌面端/移动端、锚点、链接、控制台与页面溢出。
- [ ] **Step 6:** 统一提交并推送用户已要求的全部改动。
