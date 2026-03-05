# Notion RAG 服务设计方案

**版本**: v0.2
**日期**: 2026-03-05
**状态**: In Progress (Phase 1 代码已完成)

---

## 1. 背景

### 1.1 现状

公司使用 Notion 作为核心知识管理平台，围绕研发和业务流程构建了一套互相关联的数据库体系，主要包括：

- **流程类 DB**：Problems、Solutions、Projects、Deliverables、Tasks、Bugs，支撑从问题发现到任务交付的完整研发流水线
- **知识类 DB**：Documents（含 RCA、策略文档、会议记录、Wiki）、Designs（Engineering / UI / ML 等技术设计文档）
- **组织类 DB**：Responsibilities（AOR 职责追踪）、People（团队目录与汇报关系）

各数据库之间通过 Relation 字段互相关联，形成 Problem → Solution → Project → Task 的完整上下文链路。

### 1.2 问题与诉求

当前 Notion 内的知识分散在大量页面和数据库记录中，AI Agent 或工具（如 OpenClaw）无法直接检索和利用这些信息。希望将 Notion 数据构建为本地 RAG 服务，使 Agent 能够：

- 检索历史问题、解决方案、RCA 文档等知识
- 查询项目状态、任务优先级、Bug 严重程度等结构化信息
- 获取 AOR 职责归属和团队信息

### 1.3 目标

- 将 Notion 全量数据接入向量检索，支持语义搜索
- 采用 Hybrid RAG 提升专有名词和结构化字段的检索精度
- 暴露标准 REST API，供 Agent 和 OpenClaw 调用
- 支持增量同步，保证数据时效性

### 1.4 非目标（当前阶段）

- 不做实时 Webhook 同步（列为 Phase 2）
- 不做 Notion 权限透传（所有 Agent 共享同一索引）
- 不对外提供多租户隔离

---

## 2. 整体架构

整体分为四层：**数据抽取层 → 索引构建层 → 检索服务层 → API 接口层**。

```
Notion Workspace
       ↓ Notion API
数据抽取 & 增量同步
       ↓
清洗 & 分块
       ↓
Dense Embedding + Sparse Embedding
       ↓
Qdrant 向量数据库（双索引）
       ↓
Hybrid 检索（RRF 融合）→ Reranker 精排
       ↓
FastAPI RAG 服务
       ↓
AI Agent / OpenClaw
```

---

## 3. 技术方案

### 3.1 数据抽取

Notion 数据分为两类，处理策略不同：

**结构化 DB（Problems / Solutions / Tasks / Bugs 等）**
- 通过 Notion Database Query API 批量拉取记录
- 每条 record 作为一个独立 chunk，属性字段（Status、Priority、Assignee 等）存为 metadata，用于后续过滤
- 保留 Relation 字段，记录页面间关联关系，便于 Agent 做多跳推理

**非结构化页面（Documents / Designs / RCA 等）**
- 通过 Notion Blocks API 递归拉取页面内容，转换为 Markdown
- 代码块（含 Mermaid 图表）单独提取，不做截断，标注 type=code
- 长文档采用递归字符分块，chunk size 512 token，overlap 64 token

**增量同步**
- 利用 Notion 的 `last_edited_time` 字段识别变更页面
- 定时任务（每小时）拉取增量，对变更页面先删除旧 chunk 再重新写入
- 本地维护 `notion_id → chunk_id` 映射表，支持精准更新和删除

### 3.2 Embedding 方案

| 类型 | 模型 | 说明 |
|---|---|---|
| Dense（语义向量） | BAAI/bge-m3 | 本地部署，中英文双语支持好，1024 维 |
| Sparse（关键词向量） | BM42（FastEmbed） | 用于精确匹配专有名词、ID、状态字段 |

选择本地模型而非 OpenAI Embedding，主要考虑数据不出内网以及中文检索质量。

### 3.3 向量数据库

选用 **Qdrant**，原因：
- 原生支持 Dense + Sparse 双向量存储，天然契合 Hybrid RAG
- 支持 Payload 过滤，可按 db_type、priority、status 等字段缩小检索范围
- Docker 本地部署简单，后期可无缝迁移至云端

每个 chunk 存储内容包括：文本内容、来源 DB 类型、页面标题、Notion URL、结构化属性（状态、优先级、关联 ID）、时间戳。

### 3.4 Hybrid 检索与精排

**检索阶段：RRF 融合**
- 同时对 Dense 向量和 Sparse 向量分别检索，各取 Top-20
- 使用 Reciprocal Rank Fusion（RRF）算法合并两路结果，无需手动调权重
- 支持按 db_type 等 metadata 过滤，缩小检索范围

**精排阶段：Cross-Encoder Reranker**
- 对 RRF 后的 Top-20 结果，用 `BAAI/bge-reranker-v2-m3` 做二次精排
- 最终返回 Top-5，传入 LLM 生成答案
- 精排对长文档（RCA、Design Doc）效果提升尤为明显

### 3.5 API 接口设计

对外暴露两类接口，而非单一通用搜索，方便 Agent 精准调用：

**通用接口**
- `POST /search`：Hybrid 检索，返回相关 chunks 及来源链接（已实现）
- `POST /query`：检索 + LLM 生成，返回自然语言答案及引用来源（Phase 2，需接入 LLM）
- `GET /health`：健康检查，返回 Qdrant 点数（已实现）

**专用工具接口**（供 Agent Function Calling 使用，均已实现）
- `POST /search/problems`：按状态/阶段查询问题库
- `POST /search/bugs`：按严重程度/项目查询缺陷库
- `POST /search/docs`：查询 RCA、Wiki、策略文档
- `POST /search/people`：查询 AOR 职责归属与人员信息
- `POST /search/tasks`：查询任务库
- `POST /search/solutions`：查询解决方案库

专用接口相比通用搜索，在 Agent 推理场景下准确率更高。所有专用接口支持 `status` 和 `priority` 后过滤。

### 3.6 技术栈汇总

| 层次 | 原设计 | 实际选型 | 变更说明 |
|---|---|---|---|
| 数据抽取 | Notion Official API + 自定义脚本 | `notion-client` Python SDK + 自定义脚本 | 使用官方 SDK 而非裸 HTTP，减少样板代码 |
| 分块 | LangChain RecursiveCharacterTextSplitter | 同左 | - |
| Dense Embedding | FastEmbed BGE-M3 (1024 维) | 同左 | 曾评估 Ollama + qwen3-embedding，因 sparse/reranker 不支持而放弃 |
| Sparse Embedding | FastEmbed BM42 | 同左 | - |
| 向量数据库 | Qdrant（Docker 本地部署） | 同左 | - |
| 检索编排 | LlamaIndex QueryFusionRetriever | 自研 RRF 融合 | 去掉 LlamaIndex 依赖，自行实现 RRF 算法更轻量 |
| 精排 | sentence-transformers BGE-Reranker | FastEmbed TextCrossEncoder | 统一用 FastEmbed，避免引入 PyTorch (~2GB) |
| API 服务 | FastAPI | 同左 | - |
| 同步调度 | APScheduler | 同左（待集成） | Phase 1 先用 CLI 脚本手动触发 |
| 部署 | Docker Compose | 同左 | - |

#### 选型变更决策记录

1. **去掉 sentence-transformers**：原计划用于 Reranker，但 FastEmbed 的 `TextCrossEncoder` 已支持 `BAAI/bge-reranker-v2-m3`，且基于 ONNX 推理无需 PyTorch，依赖体积从 ~2GB 降至 ~200MB。
2. **去掉 LlamaIndex**：原计划用 `QueryFusionRetriever` 做 RRF 融合，实际 RRF 算法仅 ~30 行代码，自行实现更可控，避免引入重量级框架。
3. **Ollama 评估结论**：服务器已有 `qwen3-embedding:0.6b`（1024 维），可做 dense embedding，但 Ollama 不支持 sparse embedding 和 reranker，仍需 FastEmbed 补齐。为简化架构，统一使用 FastEmbed 全家桶。

---

## 4. 实施计划

| 阶段 | 目标 | 主要任务 | 状态 |
|---|---|---|---|
| **Phase 1** | MVP 跑通 | Notion 数据抽取、Hybrid 检索（RRF + Reranker）、/search + 专用工具接口 | **代码完成，待联调** |
| **Phase 2** | 增量同步 + 运维 | APScheduler 定时增量同步、日志监控、检索质量评估集 | 待开始 |
| **Phase 3** | 生产加固 | Docker Compose 完整部署、健康检查、Webhook 实时同步 | 待开始 |

> **Phase 1 实际产出**：与原计划相比，Phase 1 已包含全部 DB 的 Hybrid RAG + Reranker + 专用工具接口，超出原定范围（原计划 Hybrid 在 Phase 2）。这是因为 FastEmbed 统一方案使得 dense/sparse/reranker 可一次性集成，无需分阶段。

### 4.1 Phase 1 代码结构

```
src/
  config.py                  # pydantic-settings 统一配置
  utils/fault_tolerance.py   # CircuitBreaker, RetryPolicy, RateLimiter
  notion/
    client.py                # Notion SDK 封装（分页 + 限速 + 熔断）
    extractor.py             # 属性提取 -> 结构化 metadata
    block_parser.py          # Blocks -> Markdown（20+ block types）
    sync.py                  # 全量/增量同步引擎
  indexing/
    chunker.py               # 结构化记录保持完整，长文档递归分块
    embedder.py              # FastEmbed: BGE-M3 (dense) + BM42 (sparse)
    qdrant_store.py          # 双向量 upsert/delete/search
  retrieval/
    hybrid_search.py         # RRF 融合 + CrossEncoder rerank
  api/
    app.py                   # FastAPI 入口
    routes_search.py         # POST /search
    routes_tools.py          # POST /search/{problems,bugs,docs,...}
scripts/
  full_sync.py               # CLI: --mode full|incremental|discover
```

---

## 5. 风险与注意事项

- **Notion API 限速**：全量初始化阶段需控制请求频率（官方限制 3 req/s），大型工作区建议分批导出
- **chunk 粒度权衡**：Tasks/Bugs 等短记录不宜过度分块，Documents 等长文档需合理切分，避免语义断裂
- **数据敏感性**：People DB 和 Responsibilities DB 含人员信息，建议评估是否纳入索引或做脱敏处理
- **检索质量基线**：建议在 Phase 2 结束后构建评估集（20-30 条典型问题），定期回归检索质量