# AI Agent 记忆系统（Memory System）技术调研报告

> **调研时间**：2026 年 6 月
> **调研范围**：理论框架、9 个主流框架实现、存储与检索技术、评分算法、生命周期、架构分歧
> **目标**：为 Agent 框架选型与记忆系统设计提供可决策的技术依据

---

## 目录

- [第 1 章 理论框架](#第-1-章-理论框架)
  - 1.1 CoALA：面向语言 Agent 的认知架构
  - 1.2 Generative Agents：Memory Stream 与三维评分
  - 1.3 认知心理学三大基础模型
- [第 2 章 主流框架的记忆实现（按 6 维度结构化）](#第-2-章-主流框架的记忆实现)
  - 2.1 HelloAgents
  - 2.2 MemGPT / Letta
  - 2.3 LangChain / LangChain4j
  - 2.4 CrewAI
  - 2.5 AutoGPT（含 Dream Pass）
  - 2.6 Claude Code
  - 2.7 OpenAI ChatGPT Memory（Dreaming V3）
  - 2.8 Google Gemini / Memory Bank
  - 2.9 Dify / Coze
  - 2.10 框架横向对比表
- [第 3 章 存储与检索技术](#第-3-章-存储与检索技术)
  - 3.1 向量数据库对比
  - 3.2 知识图谱在记忆中的角色（GraphRAG / Mem0ᵍ）
  - 3.3 Embedding 模型选型
  - 3.4 混合检索策略（BM25 + 向量 + RRF + HyDE + Rerank）
- [第 4 章 检索评分算法](#第-4-章-检索评分算法)
  - 4.1 Generative Agents 三维评分公式
  - 4.2 FadeMem 生物学启发评分
  - 4.3 CrewAI Composite Scoring
  - 4.4 时间衰减函数汇总
  - 4.5 重要度计算方式对比
- [第 5 章 记忆生命周期管理](#第-5-章-记忆生命周期管理)
  - 5.1 写入策略
  - 5.2 淘汰与遗忘策略
  - 5.3 整合（Consolidation）
  - 5.4 多用户 / 多租户隔离
- [第 6 章 架构分歧与未解决问题](#第-6-章-架构分歧与未解决问题)
  - 6.1 Tool 调用 vs 自动注入
  - 6.2 记忆压缩
  - 6.3 1M token 上下文对记忆系统的影响
  - 6.4 评测标准与 Benchmark
- [第 7 章 推荐阅读：5 篇核心资料](#第-7-章推荐阅读5-篇核心资料)
- [附录 A：参考文献与链接索引](#附录-a参考文献与链接索引)
- [附录 B：「待验证」事项清单](#附录-b待验证事项清单)

---

## 第 1 章 理论框架

### 1.1 CoALA：面向语言 Agent 的认知架构

**论文**：Sumers, Yao, Narasimhan, Griffiths. *Cognitive Architectures for Language Agents*. TMLR 2024. [arXiv:2309.02427](https://arxiv.org/abs/2309.02427)

#### 1.1.1 四种记忆的定义、边界与存储内容

| 记忆类型 | 定义 | 存储内容 | 边界 | 类比 |
|---------|------|---------|------|------|
| **工作记忆（Working Memory）** | 当前决策循环中活跃的符号变量 | 感知输入、LLM 推理结果、目标状态、从长期记忆检索到的信息 | 每个决策循环后消失，除非显式写入长期记忆 | 计算机 RAM |
| **情景记忆（Episodic Memory）** | 早期决策循环的经验 | 输入-输出对、事件流、游戏轨迹、Agent 自身行为历史 | 长期，可在后续决策中被检索与反思 | 个人日记 |
| **语义记忆（Semantic Memory）** | 关于世界与自身的事实性知识 | 世界事实、从经验抽象出的规则、Agent 自身知识 | 长期，可由外部数据库初始化 | 维基百科 |
| **程序性记忆（Procedural Memory）** | 决定 Agent 如何行动 | 隐式（LLM 权重）+ 显式（Agent 代码：推理 / 检索 / 落地 / 学习） | 由设计者初始化，风险较高 | 操作系统内核 |

#### 1.1.2 CoALA 决策循环

```
感知（Grounding：传感器输入 → 工作记忆）
    ↓
规划阶段（Planning）
    ├── 提议 Proposal：LLM 采样候选动作
    ├── 评估 Evaluation：为候选动作赋值（启发式 / LLM 困惑度 / 学习值）
    └── 选择 Selection：argmax / softmax / 多数投票
    ↓
执行阶段（Execution）
    ├── 执行选定动作（外部落地动作 / 内部学习动作）
    └── 环境反馈 → 工作记忆
    ↓
（循环回到规划阶段）
```

#### 1.1.3 理论来源：与 SOAR 的关系

| SOAR 组件 | CoALA 对应 | 说明 |
|----------|-----------|------|
| 工作记忆 | Working Memory | 反映 Agent 当前状况 |
| 程序性长期记忆 | Procedural Memory | 存储产生式规则 |
| 语义长期记忆 | Semantic Memory | 存储世界事实 |
| 情景长期记忆 | Episodic Memory | 存储过去行为序列 |
| 决策循环 | 决策循环 | 提议 → 评估 → 选择 → 执行 |
| Chunking | Learning actions | 将经验写入长期记忆 |

**CoALA 的关键创新**：
- 用**自然语言**统一所有内部表示（区别于传统认知架构的多模态符号表示）
- 引入**Reasoning Action**（推理动作）—— 灵活产生新知识和启发式
- 用 LLM 替代手写规则，但仍保留 SOAR 风格的显式决策过程

> **「待验证」**：CoALA 论文正文中**未详细讨论 ACT-R**（仅在参考文献中列出 Anderson & Lebiere 2003）。其主要理论来源是 **SOAR**，而非 ACT-R。

---

### 1.2 Generative Agents：Memory Stream 与三维评分

**论文**：Park et al. *Generative Agents: Interactive Simulacra of Human Behavior*. UIST 2023. [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)

#### 1.2.1 Memory Stream 设计

每条记忆条目结构：

```python
class ConceptNode:
    created: datetime         # 创建时间戳
    last_accessed: datetime   # 最近访问时间戳
    description: str          # 自然语言描述
    embedding_key: str        # 用于生成 embedding 的文本
    poignancy: int            # 重要性评分 1-10
    keywords: List[str]       # 关键词列表
    filling: Any              # 附加内容（对话记录、源记忆节点ID）
    expiration: datetime      # 到期时间（可空）
    depth: int                # 0=原始观察, 1=推理, 2=反思
```

**示例**：
```json
{
  "description": "conversing about Isabella inviting Klaus to her Valentine's Day party at Hobbs Cafe on February 14th, 2023 from 5pm to 7pm.",
  "poignancy": 6,
  "keywords": ["Klaus Mueller", "Isabella Rodriguez"]
}
```

#### 1.2.2 三维检索评分公式

$$\text{score} = \alpha \cdot \text{recency} + \beta \cdot \text{importance} + \gamma \cdot \text{relevance}$$

默认权重：`α = β = γ = 1.0`

**三个分量**：

| 维度 | 公式 | 来源 | 范围 |
|------|------|------|------|
| **Recency** | `0.995^h`（h = 自上次访问以来的游戏小时数） | 指数衰减 | [0, 1] |
| **Importance** | LLM 打分 1-10 整数 | 1=琐事（刷牙），10=重要（分手 / 录取） | [1, 10] |
| **Relevance** | `cosine(embed(memory), embed(query))` | embedding 余弦相似度 | [-1, 1] |

**LLM 打分 Prompt**：
```
On a scale of 1 to 10, where 1 is purely mundane 
(e.g., brushing teeth, making the bed) and 10 is 
extremely poignant (e.g., a break-up, college acceptance), 
rate the possible poignancy of the following memory.

Memory: <memory_description>
Rating: <fill_in>
```

**关键配置**（`config.py`）：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `RECENCY_WEIGHT` | 1.0 | 近期性权重 |
| `IMPORTANCE_WEIGHT` | 1.0 | 重要性权重 |
| `RELEVANCE_WEIGHT` | 1.0 | 相关性权重 |
| `RECENCY_DECAY` | 0.995 | 每小时指数衰减因子 |
| `REFLECTION_THRESHOLD` | 150.0 | 触发反思的累积重要性阈值 |

#### 1.2.3 反思（Reflection）机制

**触发条件**：最近记忆的 importance 总分超过 150

**流程**：
1. 选取最近 100 条记忆作为种子
2. LLM 从种子中提出 3 个高层次问题
3. 对每个问题检索相关记忆
4. LLM 综合生成 3-5 条 **reflection statements**（标记为 `type=thought`, `depth=2`）
5. 反思记忆的 expiration 设为 30 天后

**递归反思**：反思产生的记忆可作为更高层反思的种子，形成记忆的树状结构。

---

### 1.3 认知心理学三大基础模型

#### 1.3.1 Atkinson-Shiffrin 多存储模型（1968）

```
感官输入 → 【感觉记忆】（0.25ms~2s）
             ↓ 注意（Attention）
            【短期记忆】（15-30s，7±2 项目，Miller's Magical Number）
             ↓ 精细复述（Elaborative Rehearsal）
            【长期记忆】（无限容量，语义编码）
```

**对 AI Agent 的影响**：
- **三层架构**：MemGPT、CAM-Agent 直接采用
- **容量限制**：LLM 上下文窗口管理的理论依据
- **注意机制**：Attention 即"信息过滤门槛"

#### 1.3.2 Ebbinghaus 遗忘曲线（1885）

**原始公式**：
$$b = \frac{100k}{(\log t)^c + k}$$

其中 `k ≈ 1.84`, `c ≈ 1.25`，`t` = 时间（分钟），`b` = 保持的记忆量。

**精确留存率**：

| 时间 | 遗忘率 | 留存率 |
|------|--------|--------|
| 20 分钟 | 42% | **58%** |
| 1 小时 | 56% | **44%** |
| 24 小时 | 67% | **33%** |
| 6 天 | 75% | **25%** |
| 31 天 | 79% | **21%** |

**简化形式**（AI 中常用）：`R = e^(-t/S)` 或 `R = e^(-λt)`

**对 AI Agent 的影响**：
- 时间衰减函数（MemGPT FIFO eviction、PowerMem）
- 间隔重复调度（FOREVER 论文）
- MemoryBank 显式建模 Ebbinghaus 曲线

#### 1.3.3 Baddeley 工作记忆模型（1974/2000）

**四元模型**（2000 扩展版）：

```
        【中央执行系统】Central Executive
              ↓ 控制/协调
  ┌───────────┼───────────┬──────────────┐
【语音环路】  【视觉空间画板】  【情景缓冲区】
Phonological  Visuospatial  Episodic Buffer
   Loop      Sketchpad    （2000 年加入）
   ↓             ↓              ↓
  2秒语音    3-4 视觉对象    多模态整合
  听觉编码   视觉/空间编码    4 个组块容量
```

**对 AI Agent 的影响**：
- **多组件工作记忆**：分离视觉、语言、状态子模块
- **中央执行系统** → Agent 决策器 / 规划器
- **情景缓冲区** → 多源信息（感知、记忆、知识）整合
- **容量限制** → LLM 上下文管理策略

#### 1.3.4 三大理论对 AI 记忆设计的映射总结

| 认知理论 | 对 AI Agent 记忆的影响 | 代表实现 |
|----------|----------------------|----------|
| Atkinson-Shiffrin（1968） | 三层架构（感觉→短期→长期） | MemGPT、CAM-Agent |
| Ebbinghaus（1885） | 时间衰减函数、间隔复习 | PowerMem、FOREVER、MemoryBank |
| Baddeley（1974/2000） | 多组件工作记忆、中央执行 | 多层次 Agent 架构 |
| ACT-R 激活传播 | 记忆检索优先级排序 | Generative Agents 的 recency |
| SOAR 决策循环 | Agent 决策循环设计 | CoALA 决策循环 |

---

## 第 2 章 主流框架的记忆实现

> **统一描述维度**（每个框架都按以下 6 维结构化）：
> 1. **分层架构** — 记忆分几层、每层叫什么、存什么
> 2. **存储后端** — 用什么存储（数据库、文件等）
> 3. **写入策略** — 自动 / 手动 / LLM 决策
> 4. **检索机制** — 评分公式、权重、多路融合
> 5. **注入方式** — 自动拼进 prompt / Tool 调用
> 6. **生命周期** — 遗忘 / 淘汰 / 整合 / 跨会话
> 7. **独特设计** — 该框架最有特色的地方

---

### 2.1 HelloAgents（Datawhale）

**仓库**：[github.com/datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) ｜ **文档**：[第 8 章 记忆与检索](https://github.com/datawhalechina/hello-agents/blob/main/docs/chapter8/%E7%AC%AC%E5%85%AB%E7%AB%A0%20%E8%AE%B0%E5%BF%86%E4%B8%8E%E6%A3%80%E7%B4%A2.md)

#### 2.1.1 分层架构（4 层）

```
HelloAgents 记忆系统
├── 工作记忆 WorkingMemory    - 当前对话上下文
├── 情景记忆 EpisodicMemory   - 具体事件和交互历史
├── 语义记忆 SemanticMemory   - 抽象知识和概念
└── 感知记忆 PerceptualMemory - 多模态数据（图像、音频）
```

| 记忆类型 | 存储内容 | 存储后端 | 容量限制 | 生命周期 |
|---------|---------|---------|---------|---------|
| 工作记忆 | 当前对话上下文 | 纯内存 | 默认 50 条 | TTL 60 分钟 |
| 情景记忆 | 交互事件 | SQLite + Qdrant | 无限 | 持久化 |
| 语义记忆 | 实体、关系、知识 | Qdrant + Neo4j | 无限 | 持久化 |
| 感知记忆 | 多模态数据 | SQLite + Qdrant（按模态分离）| 无限 | 持久化 |

#### 2.1.2 存储后端

- **SQLite**：结构化持久化、复杂查询（情景 / 感知记忆）
- **Qdrant**：高性能向量检索（全部 4 种）
- **Neo4j**：知识图谱管理、关系推理（语义记忆）
- **纯内存**：临时快速访问（工作记忆）

#### 2.1.3 写入策略

**手动调用 + MemoryTool**：

```python
memory_tool.execute("add",
    content="2024年3月15日，用户张三完成了第一个Python项目",
    memory_type="episodic",
    importance=0.8,
    event_type="milestone"
)
```

#### 2.1.4 检索机制（混合评分）

| 记忆类型 | 评分公式 |
|---------|---------|
| **工作记忆** | `(TF-IDF × 0.7 + 关键词 × 0.3) × 时间衰减 × (0.8 + 重要性 × 0.4)` |
| **情景记忆** | `(向量相似度 × 0.8 + 时间近因性 × 0.2) × (0.8 + 重要性 × 0.4)` |
| **语义记忆** | `(向量相似度 × 0.7 + 图相似度 × 0.3) × (0.8 + 重要性 × 0.4)` |
| **感知记忆** | `(向量相似度 × 0.8 + 时间近因性 × 0.2) × (0.8 + 重要性 × 0.4)` |

**时间近因性**（指数衰减）：
```python
recency_score = math.exp(-0.1 * age_hours / 24)  # 24小时内保持高分
```

#### 2.1.5 注入方式

**通过 MemoryTool 作为工具调用** 注入 LLM：

```python
agent.register_tool(MemoryTool(memory_manager))
response = agent.run("你还记得我之前说的Python项目吗？")
# LLM 会主动调用 memory_tool.search(query="Python项目")
```

#### 2.1.6 生命周期

**三种遗忘策略**：
- `importance_based` — 基于重要性淘汰
- `time_based` — 基于时间淘汰（max_age_days）
- `capacity_based` — 基于容量淘汰

**记忆整合（Consolidation）**：
```python
memory_tool.execute("consolidate",
    from_type="working", to_type="episodic",
    importance_threshold=0.7
)
```

#### 2.1.7 独特设计

- **多模态感知记忆**：用 CLIP / CLAP 编码图像 / 音频，按模态分独立 collection
- **知识图谱自动构建**：语义记忆自动提取实体-关系存入 Neo4j
- **新会话自动检索**：持久化层（情景/语义/感知）支持跨会话检索

---

### 2.2 MemGPT / Letta

**论文**：[arXiv:2310.08560](https://arxiv.org/abs/2310.08560) *MemGPT: Towards LLMs as Operating Systems* ｜ **仓库**：[github.com/letta-ai/letta](https://github.com/letta-ai/letta) ｜ **文档**：[docs.letta.com](https://docs.letta.com) ｜ **DeepWiki**：[letta-ai/letta/3-memory-system](https://deepwiki.com/letta-ai/letta/3-memory-system)

#### 2.2.1 分层架构（3 层，OS 风格）

```
MemGPT/Letta Agent 架构
├── 主上下文 (Main Context) - 固定大小上下文窗口
│   ├── 系统指令 System Instructions - 只读
│   ├── 核心记忆 Core Memory - 固定大小，可通过函数调用编辑
│   │   ├── Persona 子块 - Agent 人设
│   │   └── Human 子块 - 用户信息
│   └── 对话历史 - 含递归摘要（FIFO 队列）
└── 外部上下文 (External Context) - 上下文外存储
    ├── 召回存储 Recall Storage - 完整事件历史
    └── 档案存储 Archival Storage - 通用读写数据
```

| 记忆层 | 存储内容 | 存储后端 | 最大大小 | 检索方式 |
|-------|---------|---------|---------|---------|
| 核心记忆 | Agent 人设、用户信息 | In-context Block | 每块默认 2000 字符 | 直接在上下文中 |
| 召回记忆 | 完整对话历史 | SQL + 向量嵌入 | 受上下文窗口限制 | 文本搜索 + 语义相似度 |
| 档案记忆 | 长期知识存储 | 向量数据库（pgvector / Turbopuffer / Pinecone）| 无限 | 语义相似度 + 标签 + 时间戳 |

#### 2.2.2 存储后端

- **核心记忆 Block**：PostgreSQL（ORM）
- **消息 Message**：PostgreSQL + 向量数据库（**双写模式**）
- **段落 Passage**：pgvector / Turbopuffer / Pinecone

#### 2.2.3 写入策略

**LLM 自主决策**（通过 6 个内存管理函数）：

| 函数 | 功能 |
|------|------|
| `send_message` | 向用户发送消息 |
| `core_memory_append` | 追加到核心记忆 |
| `core_memory_replace` | 替换核心记忆内容 |
| `conversation_search` | 搜索对话历史 |
| `archival_memory_insert` | 添加到档案记忆 |
| `archival_memory_search` | 搜索档案记忆 |

#### 2.2.4 检索机制

**函数调用驱动的显式检索**：
- `conversation_search(query, start_date, end_date)` — 混合搜索（文本匹配 + 语义）
- `archival_memory_search(query, k)` — 语义搜索

#### 2.2.5 注入方式

- **核心记忆**：始终在上下文中（`<memory_blocks><persona>...</persona><human>...</human></memory_blocks>`）
- **外部记忆**：通过函数调用结果注入

#### 2.2.6 生命周期

**虚拟上下文管理**（类比 OS 虚拟内存）：

| OS 概念 | MemGPT 对应 |
|--------|------------|
| 主存 / RAM | 主上下文 |
| 磁盘存储 | 外部上下文 |
| 虚拟内存 | 虚拟上下文管理 |

**页面替换策略**：
- 主上下文对话历史使用 **FIFO 队列**
- 被逐出的消息在队列首个索引中维护**递归摘要**
- 完整消息可通过 Recall Storage 重新检索回主上下文

#### 2.2.7 独特设计

- **OS 式分页**：把记忆从"存储问题"升级为"调度问题"
- **自我编辑记忆**：Agent 自主决定何时如何管理记忆
- **块版本控制**（Letta）：乐观锁、历史跟踪、checkpointing
- **Git 支持**：记忆块可持久化到 Git 仓库

---

### 2.3 LangChain / LangChain4j

**仓库**：[github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain) ｜ [github.com/langchain4j/langchain4j](https://github.com/langchain4j/langchain4j) ｜ [LangChain4j ChatMemory 教程](https://langchain4j.cn/tutorials/chat-memory.html)

#### 2.3.1 分层架构（7 种记忆类型，按功能分 3 层）

| 层 | 类型 | 存储内容 | 容量管理 | 适用场景 |
|----|------|---------|---------|---------|
| **基础层** | ConversationBufferMemory | 完整消息 | 无限制 | 短对话、调试 |
| | ConversationEntityMemory | 实体-事实映射 | 跟踪所有实体 | 个性化 |
| **窗口层** | ConversationBufferWindowMemory | 最近 K 轮 | K 条 | 快速原型 |
| | ConversationTokenBufferMemory | 最近 N token | token 上限 | 控成本 |
| **压缩层** | ConversationSummaryMemory | 对话摘要 | 摘要长度 | 长对话 |
| | ConversationSummaryBufferMemory | 摘要 + 最近 | max_token_limit | 平衡 |
| | VectorStoreRetrieverMemory | 向量化历史 | 无限 | 大规模检索 |

#### 2.3.2 存储后端

- **BufferMemory 系列**：内存 List
- **SummaryMemory**：内存 String
- **EntityMemory**：内存 Dictionary
- **VectorStoreRetrieverMemory**：向量数据库（FAISS / Chroma / Pinecone / PGVector 等）
- **LangChain4j**：通过 `ChatMemoryStore` 接口自定义持久化

#### 2.3.3 写入策略

**自动写入**（Chain 执行过程中）：

```python
class BaseMemory:
    def load_memory_variables(self, inputs):   # 读取
        pass
    def save_context(self, inputs, outputs):   # 写入
        pass
```

#### 2.3.4 检索机制

| 类型 | 检索方式 | 评分 |
|------|---------|------|
| BufferMemory | 返回完整历史 | 无评分 |
| BufferWindow | 返回最近 K 条 | 滑动窗口 |
| TokenBuffer | 返回最近 N token | token 计数 |
| Summary | 返回摘要 | 无（LLM 生成） |
| SummaryBuffer | 摘要 + 窗口 | 混合 |
| Entity | 返回实体事实 | 实体查找 |
| VectorStoreRetriever | 向量相似度 | 余弦相似度 / MMR |

#### 2.3.5 注入方式

**自动拼进提示词**：

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的助手。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
```

#### 2.3.6 生命周期

- **BufferWindow**：超出 K 直接丢弃（FIFO）
- **TokenBuffer**：超出 token 上限删除旧消息
- **SummaryBuffer**：超出 max_token_limit 时将最旧内容移入摘要
- **跨会话**：默认不支持，需自定义 `PersistentChatMemoryStore`

#### 2.3.7 独特设计

- **统一接口**：`load_memory_variables()` + `save_context()`
- **可插拔**：记忆作为独立组件可灵活替换
- **LangChain4j 工具消息特殊处理**：含 ToolExecutionRequest 的 AiMessage 被淘汰时，孤立 ToolExecutionResultMessage 自动淘汰

---

### 2.4 CrewAI

**仓库**：[github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) ｜ **文档**：[docs.crewai.com/concepts/memory](https://docs.crewai.com/concepts/memory) ｜ **DeepWiki**：[Unified Memory Architecture](https://deepwiki.com/crewAIInc/crewAI/7.1-unified-memory-architecture)

#### 2.4.1 分层架构（统一 Memory + Scope）

CrewAI 已**用统一的 `Memory` 类取代**传统的 short-term / long-term / entity / external 分层，通过 **Scope（作用域）** 实现类似分层的能力：

```
/（根）
├── /company/engineering    /company/product
├── /project/alpha          /project/beta
└── /agent/researcher       /agent/writer
```

| 传统概念 | CrewAI 实现 |
|---------|------------|
| Short-term | Recency scoring 优先召回最近记忆 |
| Long-term | LanceDB 持久化，半衰期可配置（默认 30 天）|
| Entity | source 标签 + private 标志 |
| Contextual | Hierarchical Scopes |

#### 2.4.2 存储后端

- **默认**：LanceDB（`./.crewai/memory`）
- **自定义路径**：`storage="./my_memory"` 或环境变量 `CREWAI_STORAGE_DIR`
- **自定义后端**：实现 `StorageBackend` 协议

#### 2.4.3 写入策略

```python
# 手动
memory.remember("We chose PostgreSQL.", source="user:alice", private=True)
memory.remember_many([...])  # 批量（后台线程）

# 自动（Crew）
crew = Crew(memory=True)  # 每个 task 完成后自动提取事实
# task 执行前自动 recall 注入 prompt

# LLM 决策
# 未显式指定 scope/categories/importance 时，LLM 自动推断
```

#### 2.4.4 检索机制

**Composite Scoring（复合评分）**：
```
composite = semantic_weight × similarity + recency_weight × decay + importance_weight × importance
```

- `similarity` = `1 / (1 + distance)`（向量索引）
- `decay` = `0.5^(age_days / half_life_days)`
- 默认权重：semantic=0.5, recency=0.3, importance=0.2

**两种召回深度**：
- **Shallow**：纯向量搜索，无 LLM，~200ms
- **Deep**：多步 RecallFlow（查询分析 → scope 选择 → 并行向量搜索 → 递归探索）

#### 2.4.5 注入方式

**Crew 中自动注入**（每个 task 执行前）；**Flow 中手动注入**（`self.recall()`）。

#### 2.4.6 生命周期

- **遗忘**：`memory.forget(scope="/project/old")`
- **重置**：`memory.reset(scope=...)`
- **记忆合并**（Consolidation）：相似度 > 0.85 时 LLM 决定 keep / update / delete / insert_new
- **批次内去重**：cosine similarity ≥ 0.98 静默丢弃
- **非阻塞写入** + **读屏障**：`recall()` 自动 `drain_writes()`

#### 2.4.7 独特设计

- **统一 Memory API** + Scope 作用域
- **Shallow/Deep 双召回模式**
- **LLM 增强编码管道**（自动推断 scope/categories/importance）

---

### 2.5 AutoGPT（含 Dream Pass）

**仓库**：[github.com/Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) ｜ **Dream Pass PR**：[#13243](https://github.com/Significant-Gravitas/AutoGPT/pull/13243) ｜ [CSDN 分析](https://blog.csdn.net/weixin_42576804/article/details/155926681)

#### 2.5.1 分层架构（两套并行系统）

| 系统 | 层级 | 存储内容 | 实现 |
|------|------|---------|------|
| **经典系统** | 短期记忆 | 最近几轮操作缓存 | 上下文窗口 |
| | 长期记忆 | 任务目标、关键发现、经验总结 | 向量数据库 |
| **Dream Pass** | 图记忆 | 实体、事实 | Graphiti + FalkorDB（6380 端口）|
| | Episode 记忆 | 最近 10 个会话，50 个 episode | 聊天会话记录 |
| | 试探性记忆 | 跨会话弱关联 | Graphiti status=tentative |

#### 2.5.2 存储后端

- **经典**：Chroma / FAISS / Pinecone / Qdrant
- **Dream Pass**：Graphiti 知识图谱 + FalkorDB 图数据库

#### 2.5.3 写入策略

**经典系统自动写入**：每次操作（搜索、读文件、生成代码）后提取关键语义 → embedding → 存入向量数据库。

**Dream Pass 三阶段巩固**（离线运行，用户不在时）：

| 阶段 | 睡眠类比 | 模型 | 温度 | 功能 |
|------|---------|------|------|------|
| 1 — 巩固 | NREM | claude-sonnet-4-6 | 0.2 | 提取稳定事实 |
| 2 — 重组 | REM | claude-opus-4-7 + 扩展思考 | 0.9 | 发现跨会话弱关联 |
| 3 — 净化 & 提交 | — | claude-sonnet-4-6 | 0.0 | 确定性过滤 |

**四种操作**：Writes（status=active）/ Proposals（status=tentative）/ Demotions（UUID 退役边）/ Entity invalidations

#### 2.5.4 检索机制

**经典系统**：ANN 检索（毫秒级响应）
**Dream Pass**：记忆确认（Ratification）生命周期
```
tentative ──(宽限窗口内被引用)──▶ active
         ──(被否定)──────────▶ contradicted
         ──(30天TTL无命中)───▶ superseded
```

#### 2.5.5 注入方式

**经典系统自动注入提示词**；**Dream Pass 后台异步处理**（不增加实时聊天延迟）。

#### 2.5.6 生命周期

- **防偏移机制**：每隔几步主动检索原始目标
- **最大降级上限**：每次 pass ≤10 次降级，且 ≤5% 活跃事实
- **30 天 TTL**：试探性记忆 30 天内未确认自动标记为 superseded
- **调度**：`dream_pass`（单次）/ `nightly`（每用户 ~03:00）/ `rebuild`（周日 ~04:00）
- **执行路径**：`sync_baseline`（秒级）/ `anthropic_batch`（50% 成本折扣，1 小时延迟）

#### 2.5.7 独特设计

- **思考—行动—观察—反思** 循环
- **Dream Pass 模仿人类睡眠记忆巩固**（NREM/REM 类比）
- **记忆确认生命周期**（tentative → active/contradicted/superseded）
- **批处理成本优化**：Anthropic Batch API 50% 折扣

---

### 2.6 Claude Code

**官方文档**：[docs.anthropic.com/en/docs/claude-code/memory](https://docs.anthropic.com/en/docs/claude-code/memory) ｜ **源码分析**：[Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code)

#### 2.6.1 分层架构（4 类作用域文件 + Auto Memory）

**CLAUDE.md 文件层级**：

| 类型 | 路径 | 作用域 |
|------|------|--------|
| 组织级托管策略 | `/Library/Application Support/ClaudeCode/CLAUDE.md` 等 | 全组织所有用户、所有项目 |
| 用户级指令 | `~/.claude/CLAUDE.md` | 当前用户所有项目 |
| 项目级指令 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 当前项目（可版本控制）|
| 本地个人指令 | `./CLAUDE.local.md`（gitignore）| 当前项目，仅当前用户 |

**Auto Memory 目录**：
```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # 简洁索引，每次会话启动加载
├── debugging.md       # 主题文件按需读取
├── api-conventions.md
└── ...
```

#### 2.6.2 存储后端

**完全文件式存储**（无向量数据库）：

| 存储 | 格式 |
|------|------|
| CLAUDE.md | Markdown |
| Auto Memory 目录 | Markdown |
| `.claude/rules/` | Markdown（支持 YAML frontmatter） |

**设计哲学**：**可审计性优于查询能力**（auditability > query power）。

#### 2.6.3 写入策略

**手动写入**：用户主动编写 CLAUDE.md，可通过 `@path/to/file` 导入（最多 4 层递归）。

**自动写入**（Auto Memory，v2.1.59+ 默认开启）：
- 关闭：`/memory`、`autoMemoryEnabled: false`、`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`
- 触发：仅记录对后续会话有参考价值的信息（构建命令、调试经验、用户纠正等）
- 主题拆分：MEMORY.md 保持简洁，详细内容按主题拆分到独立文件

#### 2.6.4 检索机制

**⚠️ 关键特点：不使用 embedding 或向量相似度搜索**

- 读取记忆文件头部 → 选择最多 **5 个相关文件** → 完全依赖 LLM 扫描
- MEMORY.md 每次仅加载前 **200 行 / 25KB**（先到为准）
- 主题文件按需通过标准文件工具读取
- `.claude/rules/` 可通过 YAML frontmatter `paths` 字段配置路径匹配

#### 2.6.5 注入方式

**加载顺序**（越靠后优先级越高）：

1. 组织级托管 CLAUDE.md
2. 用户级 `~/.claude/CLAUDE.md`
3. 文件系统根目录向上遍历到当前工作目录的所有 CLAUDE.md / .local.md
4. 无路径作用域的 `.claude/rules/`
5. Auto Memory MEMORY.md 前 200 行
6. 项目级 CLAUDE.md / .local.md
7. 子目录已触发的 CLAUDE.md 和路径作用域规则

**作为用户消息注入**（不是系统提示）→ 概率性遵守（非确定性）。

#### 2.6.6 生命周期

**5 层渐进式惰性降级**（每次模型调用前按顺序执行）：

| 阶段 | 名称 |
|------|------|
| 1 | Budget Reduction（预算缩减）|
| 2 | Snip（裁剪）|
| 3 | Microcompact（微压缩）|
| 4 | Context Collapse（读取时投影，非破坏性）|
| 5 | Auto-Compact（完整模型摘要，最后手段）|

#### 2.6.7 独特设计

- **文件式记忆**，无向量数据库
- **可审计性优先**
- **9 个有序加载源**构建上下文窗口
- **路径作用域规则**（YAML frontmatter）
- **自动记忆仅本地存储**，不跨设备同步

---

### 2.7 OpenAI ChatGPT Memory（Dreaming V3）

**官方文档**：[help.openai.com Memory in ChatGPT](https://help.openai.com/en/articles/8900141-memory-in-chatgpt) ｜ **Dreaming V3 说明**：[mornai.cn](https://www.mornai.cn/news/llm/chatgpt-memory-upgrade-dreaming-v3/) ｜ **完整指南**：[gptprompts.ai](https://gptprompts.ai/chatgpt-memory-guide)

#### 2.7.1 分层架构（三层子系统）

| 层级 | 名称 | 存储内容 | 作用 |
|------|------|---------|------|
| 1 | Recent Messages | 近期消息时序记录 | 当前会话连贯性（约 1 天）|
| 2 | Chat History | 摘要 + 向量检索 | 历史对话背景 |
| 3 | User Insights | 跨多轮对话的高阶分析 | 贡献约 80% 个性化提升 |

#### 2.7.2 存储后端

OpenAI 托管存储（具体实现未公开）：
- **Saved Memories**：可编辑列表（用户可在设置中查看、修改、删除）
- **Reference Chat History**：隐式推理，无可视化列表
- **Dreaming V3 合成结果**：以可读摘要形式呈现在 Memory Summary 页

#### 2.7.3 写入策略

**Saved Memories 自动写入**：ChatGPT 在判断信息属于"后续对话大概率需要复用的上下文"时自动写入（姓名、职业、偏好、硬约束等）。

**Reference Chat History 自动提取**：无用户侧可控规则，对话需要时自动从过往聊天中提取。

**Dreaming V3 关键设计**：**不在对话中实时写入，而是在对话结束后于后台异步处理**

对话结束时批量扫描历史聊天：
1. 提取长期有效信息（写作风格偏好、项目目标、饮食禁忌、惯用编程语言/框架）
2. 丢弃临时噪声（一次性行程、测试性提问）
3. 处理冲突与更新（自动合并，不会让旧记忆干扰新对话）
4. 标注置信度

#### 2.7.4 检索机制

- **Saved Memories**：对话开始时读取并注入
- **Reference Chat History**：对话过程中自动召回
- **Dreaming V3**：合成结果以摘要形式呈现

#### 2.7.5 注入方式

- **Saved Memories**：自动注入 system prompt
- **Reference Chat History**：需要时自动召回（`I remember you mentioned...` 提示）
- **Custom Instructions** 优先级高于记忆

#### 2.7.6 生命周期（用户控制）

**两个独立开关**：
- 参考已保存记忆（Saved Memories）
- 参考聊天历史（Reference Chat History）

**其他控制**：
- 逐条删除：设置 > 个性化 > 记忆 > 管理
- 临时聊天：点击「临时聊天」图标（该会话不读/写任何记忆）
- 完全重置：关开关 + 清记忆 + 清聊天历史 + 退出重登

#### 2.7.7 独特设计

- **Dreaming V3 架构**：后台异步处理
- **三层子系统**：当前对话 + 历史 + 用户洞察
- **置信度标注**
- **算力优化**：服务免费用户所需算力降至旧版 **1/5**
- **记忆容量提升**：美国 Plus/Pro 用户 ×2
- **独立记忆**：各自定义 GPT 拥有独立记忆

**当前开放进度（2026 年 6 月）**：美国 Plus/Pro 已开放；其他国家 Plus/Pro 几周内；免费版提供轻量级短期连贯性。**Dreaming 不对 API 开放**。

---

### 2.8 Google Gemini / Memory Bank

**官方文档**：
- [Gemini Enterprise Personalization](https://docs.cloud.google.com/gemini/enterprise/docs/configure-personalization)
- [Agent Platform Memory Bank](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank)

#### 2.8.1 分层架构

**Gemini Enterprise**：
- User Personalization Profile（姓名、角色、行业、偏好）
- Conversation History（过往聊天）
- Saved Memories（用户明确要求记住的信息）
- Connected Data Sources（Outlook、OneDrive 等）

**Gemini Enterprise Agent Platform - Memory Bank**：
- 完全托管的长期记忆银行
- 基于 Scope 的数据隔离
- 支持多模态理解

#### 2.8.2 存储后端

- **Gemini Enterprise**：Google 托管存储
- **Memory Bank**：完全托管、持久化、可访问的存储

**Scope 隔离示例**：
```json
{
  "scope": { "agent_name": "My agent", "user": "my user ID" },
  "fact": "I use Memory Bank to manage my memories."
}
```

#### 2.8.3 写入策略

**Memory Bank 记忆生成**：
1. **Memory Extraction** — 仅提取最有意义的信息
2. **Memory Consolidation** — 与现有记忆整合，支持演化
3. **Asynchronous Generation** — 后台生成，不增加实时延迟
4. **Continuous Event Ingestion** — 流式事件摄入，自动触发批处理
5. **Customizable Extraction** — 配置 few-shot 示例
6. **Multimodal Understanding** — 处理多模态信息生成文本洞察

#### 2.8.4 检索机制

**简单检索**：检索所有记忆
**相似性搜索**：仅检索最相关记忆（基于 Scope 隔离）

#### 2.8.5 注入方式

- **Agent Development Kit (ADK) 集成** + `VertexAiMemoryBankService`
- 其他框架：将 Memory Bank 代码包装在工具和回调中
- `RetrieveMemories` 工具检索后插入 prompt

#### 2.8.6 生命周期

- **Automatic Expiration**：设置 TTL 确保过时信息自动删除
- **Memory Revisions**：自动维护记忆修订，可检查记忆如何演化
- **管理员控制**：Gemini Enterprise > Configurations > Feature Management > Memory and customization

#### 2.8.7 独特设计

- **企业级个人化**：连接工作应用（Outlook、OneDrive）提取洞察
- **Memory Bank** 完全托管服务
- **Scope 隔离**：为每个作用域维护隔离记忆集合
- **异步生成 + 修订追踪**

**安全提示**：存在提示注入和记忆中毒风险，建议使用 Model Armor 检查、红队测试、沙箱执行。

---

### 2.9 Dify / Coze（低代码平台）

**Dify 文档**：[dify.ai/blog Conversation Variables](https://dify.ai/blog/dify-conversation-variables-building-a-simplified-openai-memory) ｜ [docs.dify.ai 知识库](https://docs.dify.ai/zh/use-dify/knowledge/readme)
**Coze 文档**：[coze.cn long_memory](https://www.coze.cn/open/docs/guides/long_memory) ｜ [Coze 记忆功能深度调研](https://github.com/zizhu-ai/daily-wallpaper/blob/main/%E6%89%A3%E5%AD%90%E5%B9%B3%E5%8F%B0%E8%AE%B0%E5%BF%86%E5%8A%9F%E8%83%BD%E6%B7%B1%E5%BA%A6%E8%B0%83%E7%A0%94%E6%8A%A5%E5%91%8A_2025.md)

#### 2.9.1 分层架构

**Dify**：
- Conversation Variables（会话变量，会话级）
- Conversation History（对话历史，持久化）
- Knowledge Base（知识库，外部文档）

**Coze（三层架构）**：

| 层 | 名称 | 功能 | 生命周期 |
|----|------|------|---------|
| 1 | 变量存储 | 键值对记录对话变量 | 会话级/临时 |
| 2 | 数据库存储 | 结构化数据，支持自然语言增删改查 | 持久化 |
| 3 | 长期记忆 | "记忆银行"，跨会话智能检索 | 永久保存 |

#### 2.9.2 存储后端

- **Dify**：内置数据库 + 支持多种向量数据库作为知识库后端
- **Coze**：平台内置存储 + PostgreSQL 自建 / Pinecone / Weaviate

#### 2.9.3 写入策略

**Dify 工作流中实现记忆提取**：
1. **判断是否存储** LLM 节点（yes/no）
2. **提取记忆** LLM 节点（输出 facts / preferences / memories）
3. **变量赋值节点**（append 模式持续更新）

**Coze**：
```python
importance_threshold = 0.3  # 默认阈值
memory_type ENUM('preference', 'fact', 'experience', 'goal')
# 自动触发为主，辅以关键词判断
```

#### 2.9.4 检索机制

- **Dify**：对话变量作为 string 引用，Array[object] 需转义节点
- **Coze**：semantic_search（语义搜索）/ hybrid（混合检索）
- 核心参数：max_results=5, relevance_threshold=0.7, importance_threshold=0.3

#### 2.9.5 注入方式

- **Dify**：Object to String 节点转义后注入 prompt
- **Coze**：API `additional_messages` 注入，或通过工作流 context_builder 模板

```python
context_template = "用户历史偏好：{memories}\n当前状态：{variables}\n用户问题：{user_input}"
```

#### 2.9.6 生命周期

**Coze 数据库表设计**：
```sql
CREATE TABLE memory_fragments (
    user_id VARCHAR(255),
    memory_content TEXT,
    memory_type ENUM('preference', 'fact', 'experience', 'goal'),
    importance_score FLOAT,
    created_at, last_accessed, access_frequency INT DEFAULT 0
);
```

**多租户隔离**：
- 向量数据库 filter：`{user_id: {"$eq": user_id}}`
- Weaviate `with_where` operator

#### 2.9.7 独特设计

- **Dify**：可视化工作流编排、低代码配置
- **Coze**：三层记忆架构、自然语言数据库操作、工作流节点直接调用 `long_term_memory`、多租户隔离

---

### 2.10 框架横向对比表

| 框架 | 分层 | 存储后端 | 写入策略 | 检索机制 | 注入方式 | 跨会话 | 多模态 | 知识图谱 |
|------|------|---------|---------|---------|---------|--------|--------|---------|
| **HelloAgents** | 4 层 | SQLite + Qdrant + Neo4j | 手动（MemoryTool）| 混合评分（多因子）| Tool 调用 | ✅ | ✅ | ✅（Neo4j）|
| **MemGPT/Letta** | 3 层 | SQL + 向量库 | LLM 自主（函数调用）| 函数调用显式检索 | Core 在上下文 + 外部 Tool | ✅ | ❌ | ❌ |
| **LangChain** | 7 种 | 内存 + 向量库 | 自动（Chain）| 自动注入 | 拼进 prompt | 自定义 | ❌ | ✅（Entity）|
| **CrewAI** | Scope 统一 | LanceDB | 手动 / 自动 / LLM 决策 | Composite Scoring | 自动注入（Crew）| ✅ | ❌ | ❌ |
| **AutoGPT** | 经典 + Dream Pass | Chroma / FAISS / Pinecone + Graphiti | 自动 + 后台巩固 | ANN + 知识图谱 | 自动注入 | ✅ | ❌ | ✅ |
| **Claude Code** | 4 类作用域 | Markdown 文件 | 手动 + 自动 | LLM 扫描（无向量）| 用户消息注入 | ✅（本地）| ❌ | ❌ |
| **ChatGPT** | 3 层子系统 | OpenAI 托管 | 自动 + 后台异步（Dreaming）| 隐式 + 自动 | 注入 system prompt | ✅ | ❌ | ❌ |
| **Gemini** | Personalization + Memory Bank | Google 托管 | 自动 + 异步生成 | 相似性搜索 + Scope | 工具注入 | ✅ | ✅ | ❌ |
| **Dify/Coze** | 2-3 层 | 内置 + PostgreSQL/Pinecone/Weaviate | 自动 + 关键词判断 | 语义/混合检索 | 模板注入 | ✅ | ❌ | ❌ |

---

## 第 3 章 存储与检索技术

### 3.1 向量数据库对比

| 维度 | **Qdrant** | **Milvus** | **FAISS** | **Chroma** | **PGVector** | **Weaviate** | **Pinecone** |
|------|-----------|-----------|----------|-----------|-------------|-------------|-------------|
| 实现语言 | Rust | Go/C++ | C++ | Python | C（PG 扩展）| Go | SaaS |
| 部署方式 | 自托管/云 | 自托管/云 | 本地库 | 嵌入式/本地 | PG 扩展 | 自托管/云 | 纯 SaaS |
| 索引类型 | HNSW | HNSW/DISKANN/IVF | HNSW/IVF/PQ/Flat | HNSW | HNSW/IVFFlat | HNSW/Flat | HNSW |
| **混合检索** | ✅ 原生 RRF | ⚠️ 需配置 | ❌ | ❌ | ⚠️ 需 tsvector | ✅ 原生 | ✅ Alpha |
| 元数据过滤 | ✅ 丰富 | ✅ 强 | ❌ 极有限 | ⚠️ 基础 | ✅ SQL 原生 | ✅ 强 | ✅ |
| 数据规模 | 十亿级 | 百亿级 | 十亿级 | < 10 万 | < 500 万 | 十亿级 | 十亿级 |
| **P99 延迟**（千万级）| 8ms 中位 / 24ms P99 | 12ms / 38ms | N/A | 50ms→2s | 良好 | 18ms / 56ms | 取决于方案 |
| 写入吞吐 | 8.7 万条/秒 | 5.2 万条/秒 | 极高 | 一般 | 一般 | 3.1 万条/秒 | 自动扩展 |
| HNSW Recall | 97.8% | 94.2% | 高 | 一般 | 取决于参数 | 91.5% | 高 |
| GPU 加速 | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| 成本（托管）| $199/月起 | $299/月起 | 免费 | 免费 | 免费 | $250/月起 | 按量付费 |
| 与 Agent 集成 | LangChain/LlamaIndex/CrewAI | LangChain/LlamaIndex | LangChain 广泛 | LangChain 原生 | LangChain/SQLAlchemy | LangChain 深度 | LangChain |
| **适合场景** | 高性能生产、混合检索 | 亿级超大规模 | 学术研究、嵌入式 | 原型/Demo | 已有 PG、中小规模 | 多模态、语义搜索 | 零运维 SaaS |

#### 3.1.1 选型决策树

```
原型验证 → Chroma
已有 PostgreSQL + 数据量 < 500 万 → PGVector
不想管服务器 → Pinecone
百万~千万级 + 自托管 → Qdrant（性能与易用最佳平衡）
亿级以上 + 有专职运维 → Milvus
多模态搜索 → Weaviate
需要原生混合检索 → Qdrant（RRF）/ Weaviate
```

**关键洞察**：
- **Qdrant** 是 AI Agent 记忆场景当前最佳平衡选择：低延迟（8ms 中位）、原生 RRF 混合检索、Rust 高性能
- **Chroma 仅适合原型**，> 10 万条后性能急剧下降
- **PGVector** 杀手锏是向量搜索 + SQL 事务同查询完成

### 3.2 知识图谱在记忆中的角色

#### 3.2.1 Microsoft GraphRAG

**论文**：[arXiv:2404.16130](https://arxiv.org/abs/2404.16130) *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*

**核心架构**：
```
原始文档 → TextUnits 切分 → 实体+关系+Claims 提取 (LLM) → 知识图谱
    → Leiden 层次聚类 → 自底向上生成社区摘要
    → 查询时：Global Search（社区摘要）/ Local Search（实体邻居）/ DRIFT Search
```

**关键论文**：[arXiv:1810.08473](https://arxiv.org/abs/1810.08473) *Leiden 算法*

**vs 传统 RAG**：通过知识图谱 + 社区摘要，在 comprehensiveness 和 diversity 指标上显著超越基线 RAG——可回答"数据集的整体主题是什么？"这类全局问题。

#### 3.2.2 Mem0ᵍ：图 + 向量混合

**论文**：[arXiv:2504.19413](https://arxiv.org/html/2504.19413v1) *Mem0: A Memory Layer for AI Agents*

**核心数据**：
- 准确率比 OpenAI Memory 高 **26%**
- 延迟降低 **91%**
- Token 消耗节省 **90%**（Mem0 平均 7k vs Zep 的 600k）

**图记忆架构**：
- 节点 V：实体（类型、embedding、创建时间戳）
- 边 E：关系三元组 `(source, relation, target)`
- 标签 L：实体语义类型（Person、Location、Event）

**双重检索**：
1. **实体中心**：识别查询实体 → 相似度定位 → 邻接子图（< 50ms）
2. **语义三元组**：查询向量化 → 三元组相似度匹配

**更新流程**：嵌入计算 → 节点检索 → 冲突检测（ADD/UPDATE/DELETE/NOOP）→ 动态节点管理

#### 3.2.3 知识图谱 vs 纯向量检索

| 维度 | 纯向量检索 | 知识图谱 |
|------|----------|---------|
| 检索方式 | 语义相似度 | 图遍历 + 语义匹配 |
| 跨实体推理 | ❌ | ✅ 多跳推理 |
| 可解释性 | 低 | 高（显式推理路径）|
| 事实追溯 | ❌ | ✅ 三元组结构 |
| 全局理解 | ❌ | ✅ 社区摘要 |
| 幻觉风险 | 高 | 低（图结构约束）|
| 构建成本 | 低 | 高 |
| 新领域适应 | 快 | 慢 |

### 3.3 Embedding 模型选型

#### 3.3.1 主流模型对比（2026 年 4 月数据）

| 模型 | 提供商 | 维度 | MTEB Avg | 价格/1M Token | 最大 Token | 多语言 | 长文本 |
|------|--------|------|----------|-------------|----------|--------|--------|
| **voyage-3-large** | Voyage AI | 1,024 | **67.1** | $0.18 | 32,000 | ✅ | ✅ |
| embed-v4 | Cohere | 1,024 | 66.3 | $0.10 | 512 | ✅ | ❌ |
| jina-embeddings-v3 | Jina AI | 1,024 | 65.5 | **$0.02** | 8,192 | ✅ | ✅ |
| GTE-large-en-v1.5 | Alibaba(开源) | 1,024 | 65.4 | 免费 | 8,192 | ✅ | ✅ |
| text-embedding-3-large | OpenAI | 3,072 | 64.6 | $0.13 | 8,191 | ✅ | ⚠️ |
| BGE-large-en-v1.5 | BAAI(开源) | 1,024 | 63.6 | 免费 | 512 | ✅ | ❌ |
| text-embedding-004 | Google | 768 | 63.0 | 免费/0.025 | 2,048 | ✅ | ❌ |
| nomic-embed-text-v1.5 | Nomic AI(开源) | 768 | 62.3 | 免费 | 8,192 | ✅ | ✅ |
| text-embedding-3-small | OpenAI | 1,536 | 62.3 | **$0.02** | 8,191 | ✅ | ⚠️ |
| E5-large-v2 | Microsoft(开源) | 1,024 | 62.0 | 免费 | 512 | ❌ | ❌ |
| voyage-3-lite | Voyage AI | 512 | 61.4 | $0.02 | 32,000 | ✅ | ✅ |
| all-MiniLM-L6-v2 | SBERT(开源) | 384 | ~58 | 免费 | 256 | ❌ | ❌ |

#### 3.3.2 选型建议

| 场景 | 推荐 | 理由 |
|------|------|------|
| 检索质量优先 | **voyage-3-large** | MTEB 最高 67.1，32K 上下文 |
| 性价比最优 | **jina-embeddings-v3** | 65.5 分 / $0.02/1M token |
| 生态最成熟 | **text-embedding-3-small** | 最广泛集成 |
| 需要 Matryoshka 降维 | **text-embedding-3-large** | 3072→256 维，质量损失 < 2% |
| 自托管 / 数据主权 | **GTE-large-en-v1.5 / bge-m3** | 开源免费，接近商业性能 |
| 中文场景 | **bge-large-zh-v1.5 / bge-m3** | 中文专项优化 |
| 多语言 + 长文本 + 零成本 | **bge-m3** | 100+ 语言，8192 token，三种检索方式 |

#### 3.3.3 关键模型深度分析

**bge-m3（BAAI）**：
- 100+ 语言，8192 token
- 三种检索方式（稠密 / 稀疏 / 多向量）—— 替代 BM25 + 向量 + ColBERT 三件套
- MTEB 多语言检索超越 text-embedding-3-large

**mxbai-embed-large**：
- 1024 维开源，可通过 Ollama 本地运行
- 中文检索任务上 Recall@5 可反超 OpenAI

**nomic-embed-text-v1.5**：
- 768 维，8192 token
- 完全可复现：[arXiv:2402.01613](https://arxiv.org/html/2402.01613v2)
- 短/长文本性能均超越 text-embedding-ada-002

**核心洞察**：embedding 成本在 RAG 系统中可忽略，主要开销在向量存储和生成式推理。

### 3.4 混合检索策略

#### 3.4.1 BM25 + 向量检索：互补失败模式

| 查询类型 | BM25 | 稠密检索 | 胜出方 |
|----------|------|---------|--------|
| 精确匹配 "SKU AZ-4471" | ✅ | ❌ 罕见词 | BM25 |
| 语义查询 "how do I return a broken item" | ❌ | ✅ 匹配 "refund policy" | 稠密 |
| 明确关键词 "return policy" | ✅ | ✅ | 两者 |
| 错误代码 "ERR_4021 fix" | ✅ | ❌ | BM25 |
| 模糊查询 "best practices for onboarding" | ❌ | ✅ | 稠密 |

#### 3.4.2 生产级混合检索三阶段架构

```
Stage 1: 双路并行检索（BM25 top-50~500 + 稠密向量 top-50~500）
Stage 2: RRF 融合排序
Stage 3: Cross-Encoder 重排序（top-50~200 → top-3~5）→ LLM
```

#### 3.4.3 RRF（Reciprocal Rank Fusion）

**公式**：`RRFscore(d) = Σ 1 / (k + rank_i(d))`，**k = 60**（默认，Cormack et al. 2009）

**k 值选择**：
- k=30~40：更重视 top-1 精度（问答）
- k=80~100：更重视跨列表共识（研究型检索）

**优势**：完全忽略原始分数（无需归一化）、无需调参、默认即稳健。

**各平台实现**：

| 平台 | 融合方法 | 备注 |
|------|---------|------|
| **Qdrant (v1.10+)** | 服务器端 RRF | Query API 原生多阶段管道 |
| **Weaviate (v1.24+)** | 相对分数融合（RSF）| ⚠️ v1.24 默认从 RRF 改为 RSF |
| **Pinecone** | Alpha 加权线性融合 | 需注意 BM25 分数主导 |
| **Elasticsearch** | 原生 RRF（企业版）| 免费版用 ranx 库客户端 RRF |

#### 3.4.4 HyDE（Hypothetical Document Embeddings）

**论文**：[arXiv:2212.10496](https://arxiv.org/abs/2212.10496) *Precise Zero-Shot Dense Retrieval without Relevance Labels*

**原理**：
1. 用户查询 → LLM 生成**假设性回答文档**
2. 对假设性文档做 embedding
3. 用假设文档的 embedding 去检索实际文档

**核心洞察**：查询是简短问题，文档是详细段落——通过让 LLM 先"想象"答案，桥接 query-document 分布差距。

**适用**：零样本场景、查询极短、专业领域
**限制**：依赖 LLM 生成质量、引入额外延迟、可能含幻觉

#### 3.4.5 Cross-Encoder 重排序（Reranking）

| 模型 | 参数 | 特点 |
|------|------|------|
| **bge-reranker-v2-m3** | 多语言 | 开源最强多语言 reranker，中文效果突出 |
| **bge-reranker-large** | 560M | 英文 + 中文，2.24GB |
| **bge-reranker-base** | 278M | 轻量版，1.11GB |
| **Cohere Rerank 3.5** | 商业 | 商业最强，多语言 |

**Benchmark 数据**（T2-RAGBench 金融文档）：

| 检索策略 | Recall@5 | MRR@3 | nDCG@10 |
|----------|---------|-------|---------|
| 仅稠密检索 | 0.587 | 0.351 | 0.466 |
| 仅 BM25 | 0.644 | 0.411 | 0.515 |
| 混合 RRF (k=60) | 0.695 | 0.433 | 0.551 |
| **混合 + Cohere 重排序** | **0.816** | **0.605** | **0.683** |

- 混合+重排序 vs 纯稠密：Recall@5 提升 **+39.0%**
- 混合+重排序 vs 混合 RRF：Recall@5 提升 **+17.4%**

**延迟代价**：双路并行 +10~50ms，Cross-Encoder +100~300ms

---

## 第 4 章 检索评分算法

### 4.1 Generative Agents 三部曲评分

```
Score = α_recency · n(recency) + α_importance · n(importance) + α_relevance · n(relevance)
```

| 分量 | 公式 | 来源 | 范围 |
|------|------|------|------|
| Recency | `0.995^h`（h = 自上次访问以来的游戏小时数）| 指数衰减 | [0, 1] |
| Importance | LLM 打分 1-10 整数 | Prompt：1=琐事，10=分手/录取 | [1, 10] |
| Relevance | `cos(embed(memory), embed(query))` | embedding 余弦相似度 | [-1, 1] |

**三个分量均做 min-max 归一化到 [0, 1]，默认权重 α=1.0**

### 4.2 FadeMem 生物学启发评分

**论文**：[arXiv:2601.18642](https://arxiv.org/abs/2601.18642) *FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory*

#### 4.2.1 双层记忆结构

每条记忆表示：`m_i(t) = (c_i, s_i, v_i(t), τ_i, f_i)`
- `c_i` = embedding，`s_i` = 原文，`v_i(t)` = 当前强度 ∈ [0, 1]，`τ_i` = 创建时间，`f_i` = 访问频率

#### 4.2.2 三因素重要性分数

```
I_i(t) = α · rel(c_i, Q_t) + β · f_i/(1+f_i) + γ · recency(τ_i, t)
```

- `rel(c_i, Q_t)` = 当前记忆与近期上下文 Q_t 的语义相关性
- `f_i/(1+f_i)` = 访问频率的**饱和函数**（避免无限大）
- `recency(τ_i, t) = exp(-δ(t - τ_i))` = 指数时间衰减

**时间衰减访问率**：`f̃_i = Σ_j exp(-κ(t - t_j))`（最近刚被访问的记忆更值钱）

#### 4.2.3 生物启发遗忘曲线

```
v_i(t) = v_i(0) · exp(-λ_i · (t - τ_i)^β_i)
```

**衰减率受重要性调节**：`λ_i = λ_base · exp(-μ · I_i(t))`

**层间衰减形状不同**：
```
β_i = 0.8 (sub-linear), if m_i ∈ LML  # 忘得更慢
β_i = 1.2 (super-linear), if m_i ∈ SML  # 忘得更快
```

**半衰期数据**（λ_base=0.1, I_i=0）：
- LML 半衰期 ≈ **11.25 天**
- SML 半衰期 ≈ **5.02 天**

#### 4.2.4 实验性能

| 方法 | 关键事实保留率 | 上下文信息 | 存储用量 |
|------|--------------|----------|---------|
| LangChain | 71.2% | 65.3% | 100% |
| Mem0 | 78.4% | 69.1% | 100% |
| MemGPT | 75.6% | 62.8% | 85.3% |
| **FadeMem** | **82.1%** | **71.0%** | **55.0%** |

- 高重要性记忆衰减速度比 baseline 慢 **3-5 倍**
- 23% 的低重要性记忆因访问模式被提升到 LML

### 4.3 CrewAI Composite Scoring

```
composite = semantic_weight × similarity + recency_weight × decay + importance_weight × importance
```

- `similarity` = `1 / (1 + distance)`（向量索引）
- `decay` = `0.5^(age_days / half_life_days)`
- 默认权重：semantic=0.5, recency=0.3, importance=0.2
- 默认半衰期：30 天

### 4.4 时间衰减函数汇总

| 函数形式 | 公式 | 特点 | 使用案例 |
|---------|------|------|---------|
| **指数衰减** | `e^(-λt)` | 快速遗忘，数学性质好 | Generative Agents (0.995^h), FadeMem recency |
| **幂律衰减** | `1/(1+αt)` | 长尾遗忘，更符合人类记忆 | MemoryBank, 认知科学文献 |
| **高斯衰减** | `e^(-t²/2σ²)` | 前期遗忘慢，中期加速 | 部分实验性系统 |
| **拉伸指数** | `e^(-λ·t^β)` | β>1 超指数，β<1 亚指数 | **FadeMem (LML: β=0.8, SML: β=1.2)** |
| **饱和函数** | `f/(1+f)` | 访问频率上限约束 | FadeMem 访问频率分量 |
| **半衰期衰减** | `0.5^(t/half_life)` | 半衰期直观易调 | **CrewAI** |

### 4.5 重要度计算方式对比

| 方式 | 方法 | 优点 | 缺点 | 使用案例 |
|------|------|------|------|---------|
| **规则-based** | 关键词匹配、内容长度、模式 | 快速、确定性强 | 泛化差、需维护规则 | 早期系统 |
| **LLM-based** | LLM 打 1-10 分 | 灵活、语义理解 | 成本高、不稳定 | Generative Agents, FadeMem |
| **混合方式** | 规则初筛 + LLM 精评 | 平衡成本和精度 | 复杂度高 | Mem0, FadeMem |
| **频率-based** | 访问次数 + 时间衰减 | 自动、无额外成本 | 可能忽略语义重要性 | FadeMem f̃_i |

### 4.6 实验验证状态

| 系统/论文 | 是否验证 | 验证方式 | 关键指标 |
|----------|---------|---------|---------|
| Generative Agents | ✅ | Smallville 沙盒 25 个 Agent | 行为可信度评估 |
| MemGPT | ✅ | 多轮对话一致性 | 对话质量评分 |
| Mem0 | ✅ | LoCoMo / LongMemEval / BEAM | J 值、延迟、Token 消耗 |
| FadeMem | ✅ arXiv | LTI-Bench, MSC, LoCoMo | 82.1% 关键事实保留率 |
| MemoryBank | ✅ | 长期对话记忆测试 | 保留率 vs 遗忘率 |

---

## 第 5 章 记忆生命周期管理

### 5.1 写入策略

#### 5.1.1 写入策略对比

| 框架 | 策略 | 触发方式 | 结构/非结构 | 异步/同步 |
|------|------|---------|------------|----------|
| **AutoGPT（经典）** | 全量 Embedding + 硬截断 | 每次循环自动 | 非结构化向量 | 同步 |
| **Mem0** | ADD-only 异步提取 | 后台（Agent 响应后）| 自然语言 + 实体图 | 异步 |
| **CrewAI** | LLM 自动推断元数据 | Task/Flow 完成或手动 | 自然语言 + 分层作用域 | 异步非阻塞 |
| **MemGPT/Letta** | Core 自动 + Archival 工具 | LLM 自我触发 | Core 非结构 / Archival 向量 | 混合 |
| **HelloAgents** | 4 层分类存储 | 工具调用 | 结构化（向量 + 图 + SQL）| 混合 |
| **ChatGPT Dreaming V3** | 后台批量合成 | 对话结束后 | 自然语言 + 摘要 + 置信度 | 异步 |
| **AutoGPT Dream Pass** | 巩固 → 重组 → 净化 | 后台批处理 | 知识图谱 + 实体/事实 | 异步 |
| **Claude Code** | 用户主动 + 自动启发 | 持续 + 用户触发 | Markdown | 同步 |
| **Dify/Coze** | 关键词判断 + LLM | 自动 + 阈值 | 自然语言 | 异步 |

#### 5.1.2 关键设计决策

- **全量记录 vs 重要筛选**：AutoGPT 早期"全量"策略因低质记忆堆积失败；现代系统普遍采用 LLM 筛选
- **同步 vs 异步**：现代系统（ChatGPT Dreaming V3、AutoGPT Dream Pass）趋向**异步后台处理**以降低延迟
- **ADD-only**：Mem0 主张不覆盖旧事实，新旧并存保留时间上下文
- **结构化 vs 非结构**：MemGPT/Letta 用 Block 自然语言；Mem0 加图；HelloAgents 用 Neo4j 实体图

### 5.2 淘汰与遗忘策略

| 策略 | 代表框架 | 机制 | 认知科学对应 |
|------|---------|------|------------|
| **重要性淘汰** | Mem0 | 写入时 LLM 四操作判断 | 情感 / 闪光灯记忆 |
| **时间淘汰** | CrewAI, MemoryBank | 指数衰减（半衰期）| Ebbinghaus 遗忘曲线 |
| **容量淘汰** | LangChain, HelloAgents | FIFO / LRU / 硬截断 | 工作记忆容量限制 |
| **搜索衰减** | Mem0 | 不删除，仅降权 | Bjork 提取强度理论 |
| **会话边界** | 通用实践 | 每会话保留 Summary | 海马体-皮层巩固 |
| **虚拟分页** | MemGPT / Letta | FIFO + 递归摘要 + 检索回访 | OS 虚拟内存 |

#### 5.2.1 Mem0 精细遗忘机制

每次写入时 LLM 判断四操作：
- `ADD`（新建）
- `UPDATE`（合并）
- `DELETE`（删除冲突）
- `NOOP`（忽略）

显式 API：`delete(memory_id)`、`batch_delete`、`filter-based deletion`

**Memory Decay**（搜索时重排序层，非物理删除）：最近访问记忆 1.5x boost，未使用的 dampen 至 0.3x，可 opt-in 启用。

### 5.3 整合（Consolidation）

| 框架 | 整合机制 |
|------|---------|
| **Mem0** | Graph Memory（实体链接），实现跨记忆连接，LoCoMo multi-hop reasoning +23.1 |
| **A-MEM**（NeurIPS 2025）| 类似 Zettelkasten 笔记法；新记忆整合可触发旧记忆上下文表征和属性的更新 |
| **CrewAI** | consolidation_threshold 0.85 → LLM 决定 keep/update/delete/insert_new |
| **Generative Agents** | 双层：Observation Stream（原始）+ Reflection（综合），两者并存，检索时共同参与评分 |
| **AutoGPT Dream Pass** | NREM 巩固 → REM 重组 → 净化提交三阶段 |

#### 5.3.1 去重机制

- **Mem0**：哈希去重（写入时）+ embedding 相似度去重
- **CrewAI**：batch 内 cosine similarity ≥ 0.98 直接丢弃
- **MemGPT**：无显式去重，依赖 Agent 自主调用 `core_memory_replace`

### 5.4 多用户 / 多租户隔离

| 框架 | 隔离方案 |
|------|---------|
| **Mem0** | `source` 标记（user:alice）+ `private` 标志；filter-based deletion |
| **HelloAgents** | Qdrant 集合隔离 + 元数据过滤（user_id / rag_namespace）|
| **CrewAI** | Hierarchical Scopes（`/customer/acme-corp`），Agent 只能访问限定子树 |
| **Dify** | PostgreSQL 多租户，Docker Compose / K8s Helm Charts 水平扩展 |
| **Coze** | Go 微服务架构 + 平台内置数据库 + 多租户扩展 |
| **ChatGPT** | 跨设备同步（iOS/Android/macOS/Windows/Web），但交互元数据因设备而异 |
| **Gemini Memory Bank** | Scope 隔离 + 数据隔离 + 自动过期（TTL）|

**隐私合规**：CNIL 2025 年 GDPR 合规 AI 建议强调数据最小化、保留期限限制、可审计性。Mem0 的 TTL 和显式删除、MemoryBank 的遗忘曲线均符合"数据保留期限"原则。

---

## 第 6 章 架构分歧与未解决问题

### 6.1 Tool 调用 vs 自动注入

#### 6.1.1 三种模式对比

| 模式 | 代表系统 | 优点 | 缺点 | 适用场景 |
|------|---------|------|------|---------|
| **纯自动注入** | ChatGPT | 简单、无检索丢失 | 窗口占用大、污染风险 | 个人助手、可控记忆量 |
| **纯 Tool** | 早期 MemGPT | 精准、无限容量 | LLM 决策负担、延迟 | 研究原型、自主 Agent |
| **混合（最佳实践）** | Letta | 核心在场 + 长尾按需 | 架构复杂 | 生产级 Agent 平台 |
| **自动提取 + 检索** | Mem0 | 工程化完备、多信号 | 需向量 + 图 + BM25 基础设施 | SaaS 级记忆服务 |

#### 6.1.2 注入位置的影响

- **System prompt**（ChatGPT, Letta Core Memory）：模型视为"指令"，遵守概率高
- **User message**（Claude Code CLAUDE.md）：模型视为"上下文"，概率性遵守
- **Tool result**（Letta Archival, MemGPT）：动态检索，按需注入
- **提示词模板变量**（LangChain MessagesPlaceholder）：自动填充

#### 6.1.3 趋势：混合模式

**Letta 是当前最成熟的混合方案**：
- Core Memory（人设 / 用户信息）**自动注入** system prompt
- Archival Memory（长尾 / 历史）**通过 Tool 调用** 按需检索
- 兼顾"核心人格稳定"和"长尾检索效率"

### 6.2 记忆压缩

#### 6.2.1 压缩方法对比

| 压缩方法 | 信息保留度 | 检索精度 | 实现复杂度 | 代表 |
|----------|----------|---------|----------|------|
| **全量原始** | 100% | 高（小量时）| 低 | LangChain Buffer |
| **滚动摘要** | 中等 | 中 | 低 | LangChain SummaryBuffer, Letta 溢出处理 |
| **关键词 / 实体提取** | 低 | 中 | 低 | Mem0 实体提取、CrewAI 元数据 |
| **结构化三元组** | 中 | 高（关系推理）| 高 | HelloAgents Neo4j, MAGMA (2026) |
| **原始 + 摘要并存** | 高 | 高 | 高 | Generative Agents, Mem0 |

#### 6.2.2 关键设计选择

- **Letta 溢出处理**：增量摘要 + 分级压缩（优先压缩最旧消息）
- **Mem0**：不主动压缩历史，控制检索 token（< 7,000 / query），ADD-only 保留完整事实
- **Generative Agents**：Observation + Reflection 双层，**原始记忆 + 反思记忆并存**
- **MAGMA（2026）**：每记忆项用**多图**表示（Multi-Graph Agentic Memory Architecture）

### 6.3 1M token 上下文对记忆系统设计的影响

#### 6.3.1 "Lost in the Middle" 问题

**论文**：[arXiv:2307.03172](https://arxiv.org/abs/2307.03172) *Lost in the Middle: How Language Models Use Long Contexts*

- 即使 1M token 窗口，模型性能呈 **U 型曲线**：开头和末尾关注度高，中间信息检索下降 20+ 百分点
- Llama-3.1-405B 在 32K 后开始下降；GPT-4 在 64K 前下降
- **大多数模型在达到宣传最大值前准确率就已大幅下降**

#### 6.3.2 "大海捞针"测试的误导性

- Gemini 1.5 Pro 在 NIAH（单事实隐藏）中达 99.7%
- 但**多事实检索场景平均召回率仅约 60%**
- NoLiMa（针与问题无词汇重合）和 NeedleChain（多跳推理）中模型表现显著下降

#### 6.3.3 成本与延迟权衡

| 方案 | 延迟 | 成本 |
|------|------|------|
| 端到端 RAG | ~1 秒 | ~$0.00008 / 次 |
| 160K token 长上下文 | ~20 秒 | 显著高 |
| 890K token 超长上下文 | > 60 秒 | GPT-4.1 1M 约 $2 / 次 |
| 缓存 1M token | ~100GB GPU 显存 | - |

**RAG vs 长上下文成本差距约 1,250 倍**

#### 6.3.4 工程折中方案

- **智能路由**（Self-Route, EMNLP 2024）：简单查询走 RAG，复杂多跳/全局理解走长上下文
- **LlamaIndex Small-to-Big Retrieval**：索引细粒度分块，推理时扩展为更大上下文
- **生产建议**：从 RAG 开始；长上下文留给真正需要全局理解、延迟不敏感的任务；实际可靠上限为 **32K-64K**（非宣传值）

### 6.4 评测标准与 Benchmark

#### 6.4.1 主流 Benchmark 对比

| Benchmark | 规模 | 核心维度 | 来源 |
|-----------|------|---------|------|
| **LoCoMo** | 10 conversations, ~300 questions | 单跳 / 多跳 / 开放域 / 时间回忆 | Stanford（Mem0 官方评估）|
| **LongMemEval** | 500 questions, 可扩展历史 | 信息提取、多会话推理、时间推理、知识更新、弃权 | [arXiv:2410.10813](https://arxiv.org/abs/2410.10813)（ICLR 2025）|
| **MSC**（Multi-Session Chat）| 人工编写长期对话 | 跨会话保留能力 | DILAB-HYU |
| **MemoryBank** | 模拟 + 真实对话 | 长期陪伴、人格理解、共情 | [arXiv:2305.10250](https://arxiv.org/abs/2305.10250) |
| **BEAM** | 1M / 10M token scale | 10 任务类别（偏好跟随、信息提取、时间推理、矛盾解决等）| [github.com/mem0ai/memory-benchmarks](https://github.com/mem0ai/memory-benchmarks) |
| **LongBench** | 双语、多任务 | 13 英文 + 5 中文 + 2 代码任务 | 清华 |
| **L-Eval** | 411 篇长文档，平均 7217 词 | 20 子任务标准化评估 | [arXiv:2307.11088](https://arxiv.org/abs/2307.11088)（ACL 2024）|

#### 6.4.2 关键评测数据

**Mem0 在 LoCoMo 上**：新算法 **91.6** vs 旧算法 71.4（+20.2）
- 最大提升：时间查询 +29.6，多跳推理 +23.1
- 平均 token 仅 6,956

**Mem0 在 LongMemEval 上**：新算法 **93.4** vs 旧算法 67.8（+25.6）
- 最大提升：单会话助手记忆 +53.6，时间推理 +42.1

**Mem0 在 BEAM 上**：1M scale 总体 **64.1**，10M scale **48.6**
- 10M 时时间推理、事件排序、多会话推理显著下降（16-26%）—— 视为**开放问题**

**LongMemEval 关键发现**：商业聊天助手和长期上下文 LLM 在持续交互中记忆准确率下降 **30%**

#### 6.4.3 评测维度清单

- 准确率（事实回忆）
- 时序推理（Temporal Reasoning）
- 跨会话一致性（Multi-session Consistency）
- 个性化程度（Personalization）
- 隐私保护（Privacy / Right to be Forgotten）
- **Token 效率**（Mem0 强调：生产级系统需在准确率、成本、延迟间平衡）

#### 6.4.4 未解决问题

1. **10M+ token 记忆的可扩展性**：BEAM 10M 评测显示退化 26-35%，需更高阶时间关系表征
2. **事实过时检测**：当前系统普遍无法自动检测记忆是否过时（如已取消的旅行计划）
3. **跨设备一致性**：ChatGPT 交互元数据因设备而异，导致行为不一致
4. **纯长上下文 vs RAG 边界**：生产环境延迟、成本、attention 衰减使 RAG 仍不可替代，但最佳路由策略尚无统一标准
5. **隐私与合规**：GDPR "被遗忘权"与 ADD-only、去重合并、跨图链接存在根本张力

---

## 第 7 章 推荐阅读：5 篇核心资料

> 如果时间有限，建议按以下顺序精读这 5 篇资料，能在最短时间内建立 AI Agent 记忆系统的完整心智模型：

### 第 1 篇（必读）：Generative Agents

**论文**：[arXiv:2304.03442](https://arxiv.org/abs/2304.03442) *Generative Agents: Interactive Simulacra of Human Behavior* (Park et al., 2023)

**为什么必读**：
- 第一个**完整实现**的 LLM Agent 长期记忆系统
- **三维评分公式**（recency + importance + relevance）已成为后续所有 Agent 记忆检索的**事实标准**
- 配套**反思机制**（Reflection）首次实现"记忆的记忆"层级
- 配套**开源代码**清晰可读

**阅读重点**：第 4 章 Memory Stream 和 Retrieval 部分

### 第 2 篇（必读）：MemGPT

**论文**：[arXiv:2310.08560](https://arxiv.org/abs/2310.08560) *MemGPT: Towards LLMs as Operating Systems* (Packer et al., 2023)

**为什么必读**：
- 第一个将**操作系统虚拟内存**类比引入 LLM Agent 记忆系统的设计
- 重新定义记忆问题的范式：从"存储问题"升级为"调度问题"
- Letta（商业化）已成为生产级 Agent 记忆的事实标准之一

**阅读重点**：第 3 章 Context Management System 架构

### 第 3 篇（必读）：CoALA

**论文**：[arXiv:2309.02427](https://arxiv.org/abs/2309.02427) *Cognitive Architectures for Language Agents* (Sumers et al., TMLR 2024)

**为什么必读**：
- 第一篇系统化梳理 LLM Agent **认知架构**的学术论文
- 将认知心理学（SOAR）传统与 LLM 时代结合
- 四种记忆分类（Working / Episodic / Semantic / Procedural）成为**业内通用术语**

**阅读重点**：第 3-4 章概念框架和决策循环

### 第 4 篇（强烈推荐）：Mem0

**论文**：[arXiv:2504.19413](https://arxiv.org/html/2504.19413v1) *Mem0: A Memory Layer for AI Agents*

**为什么推荐**：
- 目前**最工程化**的记忆系统设计
- 准确率 +26%、延迟 -91%、Token -90% 的具体数据来自严格 benchmark
- 图记忆（Mem0ᵍ）+ 向量记忆 + 文本记忆的三路融合是当前最成熟的方案
- **生产级**的 ADD-only、TTL、批量去重、显式删除

**阅读重点**：3.2 GraphRAG 章节 + 4. Evaluation 章节

### 第 5 篇（强烈推荐）：FadeMem

**论文**：[arXiv:2601.18642](https://arxiv.org/abs/2601.18642) *FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory*

**为什么推荐**：
- 当前**最先进的记忆评分算法**：重要性调节衰减率 + 分层拉伸指数衰减
- 用**认知科学的两阶段遗忘规律**（β=0.8 / β=1.2）建立理论桥梁
- 实验数据强：82.1% 关键事实保留率，仅用 55% 存储
- 未来记忆系统遗忘机制设计的重要参考

**阅读重点**：3.2 Decay Mechanism + 4. Experiments

### 备选清单

如果以上 5 篇都已读，可继续：

- **Lost in the Middle**：[arXiv:2307.03172](https://arxiv.org/abs/2307.03172) — 长上下文的局限性
- **LongMemEval**：[arXiv:2410.10813](https://arxiv.org/abs/2410.10813) — 评测标准
- **A-MEM**：[arXiv:2502.12110](https://arxiv.org/abs/2502.12110) — Zettelkasten 笔记法启发的记忆架构
- **MemoryBank**：[arXiv:2305.10250](https://arxiv.org/abs/2305.10250) — Ebbinghaus 曲线显式建模
- **HelloAgents 第 8 章**：[GitHub 文档](https://github.com/datawhalechina/hello-agents/blob/main/docs/chapter8/%E7%AC%AC%E5%85%AB%E7%AB%A0%20%E8%AE%B0%E5%BF%86%E4%B8%8E%E6%A3%80%E7%B4%A2.md) — 中文工程实践最佳入门

---

## 附录 A：参考文献与链接索引

### A.1 核心论文（arXiv）

| 论文 | arXiv ID | 链接 |
|------|---------|------|
| Cognitive Architectures for Language Agents (CoALA) | 2309.02427 | [arxiv.org/abs/2309.02427](https://arxiv.org/abs/2309.02427) |
| Generative Agents | 2304.03442 | [arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442) |
| MemGPT: Towards LLMs as Operating Systems | 2310.08560 | [arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560) |
| MemoryBank | 2305.10250 | [arxiv.org/abs/2305.10250](https://arxiv.org/abs/2305.10250) |
| Mem0: A Memory Layer for AI Agents | 2504.19413 | [arxiv.org/html/2504.19413v1](https://arxiv.org/html/2504.19413v1) |
| FadeMem | 2601.18642 | [arxiv.org/abs/2601.18642](https://arxiv.org/abs/2601.18642) |
| A-MEM: Agentic Memory for LLM Agents | 2502.12110 | [arxiv.org/abs/2502.12110](https://arxiv.org/abs/2502.12110) |
| LongMemEval | 2410.10813 | [arxiv.org/abs/2410.10813](https://arxiv.org/abs/2410.10813) |
| Lost in the Middle | 2307.03172 | [arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172) |
| L-Eval | 2307.11088 | [arxiv.org/abs/2307.11088](https://arxiv.org/abs/2307.11088) |
| HyDE | 2212.10496 | [arxiv.org/abs/2212.10496](https://arxiv.org/abs/2212.10496) |
| Microsoft GraphRAG | 2404.16130 | [arxiv.org/abs/2404.16130](https://arxiv.org/abs/2404.16130) |
| Leiden 算法 | 1810.08473 | [arxiv.org/abs/1810.08473](https://arxiv.org/abs/1810.08473) |

### A.2 框架与仓库

| 框架 | 仓库 |
|------|------|
| Letta (MemGPT) | [github.com/letta-ai/letta](https://github.com/letta-ai/letta) |
| HelloAgents | [github.com/datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) |
| LangChain | [github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain) |
| LangChain4j | [github.com/langchain4j/langchain4j](https://github.com/langchain4j/langchain4j) |
| CrewAI | [github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) |
| AutoGPT | [github.com/Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) |
| Microsoft GraphRAG | [github.com/microsoft/graphrag](https://github.com/microsoft/graphrag) |
| Mem0 | [github.com/mem0ai/mem0](https://github.com/mem0ai/mem0) |
| Mem0 Benchmarks | [github.com/mem0ai/memory-benchmarks](https://github.com/mem0ai/memory-benchmarks) |
| A-MEM | [github.com/WujiangXu/A-mem](https://github.com/WujiangXu/A-mem) |
| MemoryBank | [github.com/enjoeyland/MemoryBank](https://github.com/enjoeyland/MemoryBank) |
| LongMemEval | [github.com/xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) |
| HyDE | [github.com/texttron/hyde](https://github.com/texttron/hyde) |
| Qdrant | [github.com/qdrant/qdrant](https://github.com/qdrant/qdrant) |
| Milvus | [github.com/milvus-io/milvus](https://github.com/milvus-io/milvus) |
| FAISS | [github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss) |
| Chroma | [github.com/chroma-core/chroma](https://github.com/chroma-core/chroma) |
| PGVector | [github.com/pgvector/pgvector](https://github.com/pgvector/pgvector) |
| Weaviate | [github.com/weaviate/weaviate](https://github.com/weaviate/weaviate) |

### A.3 官方文档

- **Claude Code Memory**: [docs.anthropic.com/en/docs/claude-code/memory](https://docs.anthropic.com/en/docs/claude-code/memory)
- **ChatGPT Memory**: [help.openai.com/en/articles/8900141-memory-in-chatgpt](https://help.openai.com/en/articles/8900141-memory-in-chatgpt)
- **Gemini Enterprise Personalization**: [docs.cloud.google.com/gemini/enterprise/docs/configure-personalization](https://docs.cloud.google.com/gemini/enterprise/docs/configure-personalization)
- **Gemini Memory Bank**: [docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank)
- **CrewAI Memory**: [docs.crewai.com/concepts/memory](https://docs.crewai.com/concepts/memory)
- **Letta Docs**: [docs.letta.com](https://docs.letta.com)
- **Letta DeepWiki**: [deepwiki.com/letta-ai/letta/3-memory-system](https://deepwiki.com/letta-ai/letta/3-memory-system)
- **CrewAI DeepWiki**: [deepwiki.com/crewAIInc/crewAI/7.1-unified-memory-architecture](https://deepwiki.com/crewAIInc/crewAI/7.1-unified-memory-architecture)
- **Mem0 Memory Evaluation**: [docs.mem0.ai/core-concepts/memory-evaluation](https://docs.mem0.ai/core-concepts/memory-evaluation)
- **Microsoft Agent Framework Neo4j Memory**: [learn.microsoft.com/zh-cn/agent-framework/integrations/neo4j-memory](https://learn.microsoft.com/zh-cn/agent-framework/integrations/neo4j-memory)
- **Dify Conversation Variables**: [dify.ai/blog/dify-conversation-variables](https://dify.ai/blog/dify-conversation-variables-building-a-simplified-openai-memory)
- **Coze 长期记忆**: [coze.cn/open/docs/guides/long_memory](https://www.coze.cn/open/docs/guides/long_memory)

### A.4 技术博客与分析

- [CoALA 中文解读](https://zhuanlan.zhihu.com/p/1898165626373116869)
- [Generative Agents 中文解读](https://zhuanlan.zhihu.com/p/689687139)
- [HelloAgents 第 8 章 记忆与检索](https://github.com/datawhalechina/hello-agents/blob/main/docs/chapter8/%E7%AC%AC%E5%85%AB%E7%AB%A0%20%E8%AE%B0%E5%BF%86%E4%B8%8E%E6%A3%80%E7%B4%A2.md)
- [MemGPT 架构解析 - Leonie Monigatti](https://www.leoniemonigatti.com/papers/memgpt.html)
- [MemGPT 智能体内存管理架构深度解析](https://www.atcfu.com/ai-articles/memgpt-memory/)
- [ChatGPT Memory 完整指南 2026](https://gptprompts.ai/chatgpt-memory-guide)
- [ChatGPT Memory 升级 Dreaming V3](https://www.mornai.cn/news/llm/chatgpt-memory-upgrade-dreaming-v3/)
- [ChatGPT Memory and the Bitter Lesson](https://www.shloked.com/writing/chatgpt-memory-bitter-lesson)
- [Claude Code 源码分析 - Dive into Claude Code](https://github.com/VILA-Lab/Dive-into-Claude-Code)
- [Claude Code 记忆系统深度解析](https://www.codefather.cn/post/2039963868477812738)
- [AutoGPT 记忆模块设计原理](https://blog.csdn.net/weixin_42576804/article/details/155926681)
- [AutoGPT 运行原理解析](https://zhuanlan.zhihu.com/p/625094476)
- [向量数据库选型实战 2026](https://walterwang0x01.github.io/portfolio/posts/vector-database-selection/)
- [向量数据库深度测评：Milvus vs Qdrant vs Weaviate](https://www.holysheep.ai/articles/zh-xiangliangshujukuxuanxingmilvus-vs-qdrant-vs-weavi-2026-04-15-0040.html)
- [Embedding 模型选型 2026](https://blog.linpolly.com/blog/embedding-model-selection-2026-openai-voyage-cohere-jina-comparison)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [RAG 混合检索 + RRF 深度解析](https://www.smallyoung.cn/docs/028-RAG%E6%B7%B7%E5%90%88%E6%A3%80%E7%B4%A2%E4%B8%8ERRF%E7%AE%97%E6%B3%95%E6%B7%B1%E5%BA%A6%E8%A7%A3%E6%9E%90)
- [Rerank 模型横比](https://wangyong9999.github.io/lakehouse-wiki/compare/rerank-models/)
- [长上下文 vs RAG 生产决策框架](https://tianpan.co/zh/blog/2026-04-09-long-context-vs-rag-production-decision-framework)
- [Atkinson-Shiffrin 模型](https://www.simplypsychology.org/multi-store.html)
- [Ebbinghaus 遗忘曲线精确留存率](https://studycardsai.com/blog/ebbinghaus-forgetting-curve-exact-percentages)
- [Baddeley 工作记忆模型](https://zhuanlan.zhihu.com/p/92238579)
- [ACT-R 与 SOAR 对比](https://jeffliulab.github.io/ai-notes/05_AI_Agents/02_Cognitive_Architectures/ACT-R%E4%B8%8ESOAR/)
- [扣子平台记忆功能深度调研](https://github.com/zizhu-ai/daily-wallpaper/blob/main/%E6%89%A3%E5%AD%90%E5%B9%B3%E5%8F%B0%E8%AE%B0%E5%BF%86%E5%8A%9F%E8%83%BD%E6%B7%B1%E5%BA%A6%E8%B0%83%E7%A0%94%E6%8A%A5%E5%91%8A_2025.md)
- [Dify vs Coze 深度对比](https://developer.volcengine.com/articles/7538385008784834579)

---

## 附录 B：「待验证」事项清单

调研中遇到的信息缺失或不确定项，建议在生产使用前进一步验证：

| 编号 | 事项 | 涉及框架 / 论文 | 建议验证方式 |
|------|------|---------------|------------|
| 1 | CoALA 论文中是否详细讨论 ACT-R | CoALA | 阅读原论文 PDF 全文 |
| 2 | Ebbinghaus 公式对数形式与指数形式 `R=e^(-t/S)` 的精确转换关系 | Ebbinghaus | 查阅原始 1885 年论文 |
| 3 | Generative Agents 反思机制的具体 LLM Prompt 完整内容 | Generative Agents | 查阅论文附录或开源代码 |
| 4 | CoALA 是否借鉴了 SOAR 的 impasse→subgoal 机制 | CoALA | 阅读原论文第 4.6 节 |
| 5 | Baddeley 模型各组件在 AI 实现中的量化参数映射 | Baddeley | 实验性论文 |
| 6 | ChatGPT Memory 详细技术实现（OpenAI 未公开）| ChatGPT | 关注 OpenAI 后续技术报告 |
| 7 | ChatGPT Memory 官方文档链接（help.openai.com/en/articles/8900141）| ChatGPT | 链接可能已更新 |
| 8 | AutoGPT Dream Pass PR #13243 是否已合并 | AutoGPT | GitHub 仓库最新状态 |
| 9 | Weaviate v1.24+ 默认 RRF 改为 RSF 的具体影响范围 | Weaviate | 官方 changelog |
| 10 | Gemini Memory Bank 是否对外开放使用 | Gemini | Google Cloud 文档最新状态 |
| 11 | Coze 开源版与商业版的记忆系统差异 | Coze | Coze 官方文档 |
| 12 | 各框架在 1M+ token 长上下文下的具体性能基准 | 跨框架 | 等待更新 benchmark |
| 13 | Mem0 在 BEAM 10M 评测中各项指标下降的具体百分比 | Mem0 | Mem0 评估博客 |
| 14 | MAGMA 论文（arXiv:2601.03236）的具体引用准确性 | MAGMA | 验证 arXiv ID |

---

**报告结束**

> 本报告基于 2026 年 6 月公开信息综合整理。如发现错误或需要补充，请通过 GitHub Issue 反馈。
> 建议配合 [`memory-system-cheatsheet.md`](./memory-system-cheatsheet.md) 快速查阅关键参数和公式。
