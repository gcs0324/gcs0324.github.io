# AI Agent 记忆系统速查手册

> 配合《AI Agent 记忆系统技术调研报告》使用，聚焦关键公式、参数、对比表。

---

## 1. 理论框架核心

### 1.1 CoALA 四种记忆

| 记忆 | 存什么 | 边界 | 类比 |
|------|--------|------|------|
| Working | 当前决策循环的活跃变量 | 每次循环后消失 | RAM |
| Episodic | 输入-输出对、事件流、轨迹 | 长期 | 个人日记 |
| Semantic | 世界事实、抽象知识 | 长期 | 维基百科 |
| Procedural | LLM 权重 + Agent 代码 | 由设计者初始化 | OS 内核 |

### 1.2 Generative Agents 三维评分

```
score = α·recency + β·importance + γ·relevance
       (α=β=γ=1.0)
```

| 维度 | 公式 | 范围 |
|------|------|------|
| Recency | `0.995^h` | [0, 1] |
| Importance | LLM 打分 1-10 | [1, 10] |
| Relevance | `cos(embed(mem), embed(query))` | [-1, 1] |

**反思触发阈值**：最近记忆 importance 累积 > 150

### 1.3 Ebbinghaus 留存率

| 时间 | 留存率 |
|------|--------|
| 20 min | 58% |
| 1 h | 44% |
| 24 h | 33% |
| 6 d | 25% |
| 31 d | 21% |

---

## 2. 框架 6 维度速查

| 框架 | 分层 | 存储 | 写入 | 检索 | 注入 | 跨会话 |
|------|------|------|------|------|------|--------|
| **HelloAgents** | 4（工作/情景/语义/感知）| SQLite+Qdrant+Neo4j | 手动Tool | 混合评分 | Tool | ✅ |
| **MemGPT/Letta** | 3（Core/Recall/Archival）| SQL+向量库 | LLM自主 | 函数调用 | Core注入+Tool | ✅ |
| **LangChain** | 7 种类型 | 内存+向量库 | 自动 | 多种 | 拼prompt | 自定义 |
| **CrewAI** | 统一+Scope | LanceDB | 手动/自动/LLM | Composite | 自动注入 | ✅ |
| **AutoGPT** | 经典+Dream Pass | Chroma/FAISS/Pinecone+Graphiti | 自动+后台 | ANN+KG | 自动注入 | ✅ |
| **Claude Code** | 4 类作用域 | Markdown | 手动+自动 | LLM扫描 | 用户消息 | ✅本地 |
| **ChatGPT** | 3 层子系统 | OpenAI 托管 | 自动+后台 | 隐式+自动 | System prompt | ✅ |
| **Gemini** | Personalization+Memory Bank | Google 托管 | 自动+异步 | 相似度+Scope | 工具注入 | ✅ |
| **Dify/Coze** | 2-3 层 | 内置+PostgreSQL/Pinecone | 自动+关键词 | 语义/混合 | 模板注入 | ✅ |

---

## 3. 向量数据库选型

```
原型验证 → Chroma
已有PG+<500万 → PGVector
零运维 → Pinecone
百万~千万级 → Qdrant ⭐（最佳平衡）
亿级以上 → Milvus
多模态 → Weaviate
原生RRF → Qdrant / Weaviate
```

| 维度 | Qdrant | Milvus | FAISS | Chroma | PGVector | Weaviate | Pinecone |
|------|--------|--------|-------|--------|----------|----------|----------|
| P99 延迟（千万级）| 24ms | 38ms | N/A | 2s+ | 良好 | 56ms | - |
| 写入吞吐 | 8.7万/s | 5.2万/s | 极高 | 一般 | 一般 | 3.1万/s | 自动 |
| 混合检索 | ✅ RRF | ⚠️ | ❌ | ❌ | ⚠️ | ✅ | ✅ |
| 规模 | 十亿 | 百亿 | 十亿 | < 10万 | < 500万 | 十亿 | 十亿 |

---

## 4. Embedding 模型选型

| 场景 | 推荐 | MTEB | 价格 |
|------|------|------|------|
| 质量优先 | voyage-3-large | 67.1 | $0.18/M |
| 性价比 | jina-embeddings-v3 | 65.5 | $0.02/M |
| 生态成熟 | text-embedding-3-small | 62.3 | $0.02/M |
| Matryoshka | text-embedding-3-large | 64.6 | $0.13/M |
| 自托管 | GTE-large / bge-m3 | 65.4 | 免费 |
| 中文 | bge-large-zh / bge-m3 | - | 免费 |

---

## 5. 混合检索三阶段

```
Stage 1: BM25 top-50~500 ∥ 向量 top-50~500（双路并行）
Stage 2: RRF 融合（k=60）
Stage 3: Cross-Encoder 重排序 → top-3~5 → LLM
```

**Benchmark**（T2-RAGBench 金融文档）：
| 策略 | Recall@5 | nDCG@10 |
|------|---------|---------|
| 仅稠密 | 0.587 | 0.466 |
| 混合 RRF | 0.695 | 0.551 |
| **混合 + Cohere Rerank** | **0.816** | **0.683** |

**RRF 公式**：`RRFscore(d) = Σ 1/(k + rank_i(d))`，k=60

---

## 6. 时间衰减函数

| 形式 | 公式 | 案例 |
|------|------|------|
| 指数 | `e^(-λt)` | Generative Agents `0.995^h` |
| 幂律 | `1/(1+αt)` | MemoryBank |
| 拉伸指数 | `e^(-λ·t^β)` | FadeMem β=0.8 (LML) / β=1.2 (SML) |
| 半衰期 | `0.5^(t/half_life)` | CrewAI half_life=30d |
| 饱和 | `f/(1+f)` | FadeMem 访问频率 |

---

## 7. 重要度计算方式

| 方式 | 方法 | 代表 |
|------|------|------|
| 规则 | 关键词/长度/模式 | 早期系统 |
| LLM | 1-10 打分 | Generative Agents |
| 混合 | 规则+LLM | Mem0, FadeMem |
| 频率 | 访问数+衰减 | FadeMem `f̃_i` |

---

## 8. 评测 Benchmark

| Benchmark | 规模 | 核心 | 来源 |
|-----------|------|------|------|
| **LoCoMo** | 10对话/300问题 | 单跳/多跳/时间 | Stanford |
| **LongMemEval** | 500问题 | 提取/推理/弃权 | ICLR 2025 |
| **MSC** | 长期对话 | 跨会话 | DILAB-HYU |
| **BEAM** | 1M/10M token | 10 任务 | Mem0 开源 |
| **L-Eval** | 411 文档/20子任务 | 标准化 | ACL 2024 |
| **LongBench** | 双语 | 13+5+2 任务 | 清华 |

**关键数据**：
- Mem0 LoCoMo: 91.6 (旧 71.4) | LongMemEval: 93.4 (旧 67.8)
- LongMemEval 发现：商业助手长期记忆准确率下降 30%

---

## 9. 关键设计决策矩阵

| 决策 | 选项 A | 选项 B | 何时选 A | 何时选 B |
|------|--------|--------|---------|---------|
| 注入 | 自动注入 | Tool调用 | 核心人格、稳定信息 | 长尾检索、无限容量 |
| 存储 | 向量库 | 文件/图谱 | 语义检索 | 可审计、关系推理 |
| 检索 | 纯向量 | BM25+向量 | 语义为主 | 精确+语义混合 |
| 评分 | 简单加权 | 生物学启发 | MVP/原型 | 追求最优 |
| 写入 | 同步 | 异步后台 | 简单业务 | 生产级、降低延迟 |
| 压缩 | 全量 | 摘要+原始 | 短会话 | 长对话 |

---

## 10. 5 篇必读

1. **[arXiv:2304.03442](https://arxiv.org/abs/2304.03442)** Generative Agents — 三维评分事实标准
2. **[arXiv:2310.08560](https://arxiv.org/abs/2310.08560)** MemGPT — OS 式分页范式
3. **[arXiv:2309.02427](https://arxiv.org/abs/2309.02427)** CoALA — 认知架构理论框架
4. **[arXiv:2504.19413](https://arxiv.org/html/2504.19413v1)** Mem0 — 最工程化生产方案
5. **[arXiv:2601.18642](https://arxiv.org/abs/2601.18642)** FadeMem — 最先进评分算法

---

## 11. 数字速记

- **RAG vs 1M 长上下文成本比**：1 : 1250
- **1M token 缓存显存**：~100GB
- **Mem0 优势**：+26% 准确率 / -91% 延迟 / -90% token
- **FadeMem 优势**：82.1% 关键事实保留 / 55% 存储用量
- **RAG 实际可靠上限**：32K-64K（非宣传值）
- **MemGPT 反思触发**：importance 累计 > 150
- **HelloAgents 工作记忆**：默认 50 条 / TTL 60 min
- **CrewAI 半衰期**：默认 30 天
- **Mem0 批量去重阈值**：cosine ≥ 0.98
- **CrewAI 合并阈值**：0.85
- **RRF 默认 k**：60
- **Generative Agents 反思 expiration**：30 天
- **AutoGPT Dream Pass 30 天 TTL** → superseded
- **AutoGPT Dream Pass 限制**：≤10 demotions/次，≤5% 活跃事实
- **Dreaming V3 算力优化**：降至 1/5
- **ChatGPT Plus/Pro 容量**：×2

---

## 12. 框架选择决策树

```
1. 需要完全托管 + 跨设备？ → ChatGPT / Gemini
2. 中文社区 + 教学？ → HelloAgents
3. 生产级 Agent 平台？ → Letta / Mem0
4. 多 Agent 协作？ → CrewAI
5. 自主任务驱动（早期）？ → AutoGPT
6. 开发者 Coding 助手？ → Claude Code
7. 低代码 / 业务人员？ → Dify / Coze
8. 自定义 / 研究 / 快速原型？ → LangChain / LangChain4j
9. 最高准确率（延迟成本不敏感）？ → Mem0 + Cohere Rerank
```

---

**手册版本**：2026-06 ｜ **对应主报告**：`AI-Agent记忆系统技术调研报告.md`
