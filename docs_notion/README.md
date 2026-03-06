# Notion API 学习文档

> 本文档集整理自 Notion 官方 API 文档，结合当前工程实际需求编写
> 整理时间: 2024-12-22

## 📚 文档导览

### 基础入门

#### [00_getting_started.md](./00_getting_started.md) - Notion API 入门指南
**你将学到**:
- ✅ 如何创建 Notion Integration
- ✅ 获取和配置 API Token
- ✅ Internal vs Public Integration 的区别
- ✅ OAuth 2.0 授权流程
- ✅ 当前工程的配置方法
- ✅ 权限和安全最佳实践

**推荐阅读时间**: 30 分钟
**适合人群**: 新手，第一次使用 Notion API

---

### 核心功能

#### [01_working_with_databases.md](./01_working_with_databases.md) - 使用数据库
**你将学到**:
- ✅ 数据库和 Data Source 的概念
- ✅ 如何查询数据库 (Query API)
- ✅ 如何添加页面到数据库 (Create API)
- ✅ 过滤器和排序功能
- ✅ 增量同步技巧

**推荐阅读时间**: 40 分钟
**适合人群**: 需要操作 Notion 数据库的开发者

**当前工程应用**:
- ✅ `NotionConnector._query_database()` - 查询数据库页面
- ✅ `NotionConnector.fetch_data_streaming()` - 流式获取数据

---

#### [02_property_types.md](./02_property_types.md) - 属性类型详解
**你将学到**:
- ✅ 所有 19 种属性类型的详细说明
- ✅ 每种属性的 JSON 结构
- ✅ 如何读取和写入各种属性
- ✅ 完整的 Python 代码示例
- ✅ 当前工程支持情况对比

**属性类型列表**:
- 基础: checkbox, title, rich_text
- 数字日期: number, date
- 选择: select, multi_select, status
- 人员关系: people, relation
- 文件链接: url, email, phone_number, files
- 计算只读: formula, rollup, created_time, created_by, last_edited_time, last_edited_by, unique_id

**推荐阅读时间**: 60 分钟
**适合人群**: 需要提取或操作页面属性的开发者

**当前工程应用**:
- ✅ `NotionConnector._extract_properties()` - 提取页面属性
- ✅ 支持 10 种核心属性类型

---

#### [03_working_with_page_content.md](./03_working_with_page_content.md) - 页面内容处理
**你将学到**:
- ✅ Blocks（块）的概念和类型
- ✅ 如何读取页面的所有内容
- ✅ 如何创建和更新 Blocks
- ✅ 嵌套 Blocks 的递归处理
- ✅ 20+ 种常见 Block 类型详解

**Block 类型列表**:
- 文本: paragraph, heading_1/2/3
- 列表: bulleted_list_item, numbered_list_item, to_do
- 代码引用: code, quote, callout
- 媒体: image, video, audio, file
- 嵌入: embed, bookmark
- 容器: toggle, child_database, table

**推荐阅读时间**: 50 分钟
**适合人群**: 需要处理页面内容的开发者

**当前工程应用**:
- ✅ `NotionConnector._get_page_content()` - 获取页面内容
- ✅ `NotionConnector._get_blocks_recursive()` - 递归获取 Blocks
- ✅ 支持 5 种核心 Block 类型

---

#### [04_workspace_document_types.md](./04_workspace_document_types.md) - 工作区文档类型 ⭐
**你将学到**:
- ✅ 当前 Notion 工作区的 6 种文档类型
- ✅ 每种文档类型的用途和特点
- ✅ 文档类型之间的关系网络
- ✅ 属性提取和同步的优先级建议
- ✅ 基于实际数据的代码实现建议

**文档类型列表**:
- Problem (问题) - 40 页，占 80%
- Deliverable (可交付成果) - 3 页
- Task (任务) - 2 页
- Document/Resource (文档资源) - 2 页
- Solution (解决方案) - 1 页
- Simple Task (简单任务) - 1 页

**推荐阅读时间**: 30 分钟
**适合人群**: 需要了解工作区结构和优化同步策略的开发者

**当前工程应用**:
- ✅ 指导 `NotionConnector._extract_properties()` 的实现优先级
- ✅ 指导文档类型识别和分类
- ✅ 指导查询优化和过滤策略

---

#### [05_webhooks.md](./05_webhooks.md) - Webhooks 实时通知 🆕
**你将学到**:
- ✅ Notion Webhooks 的工作原理
- ✅ 支持的事件类型和触发条件
- ✅ Webhook 设置和验证流程
- ✅ HMAC-SHA256 签名验证实现
- ✅ 事件处理和错误重试机制
- ✅ 从轮询迁移到 Webhook 的最佳实践

**事件类型**:
- `page.content_updated` - 页面内容更新
- `comment.created` - 评论创建
- `data_source.schema_updated` - 数据源架构更新
- `database.schema_updated` - 数据库架构更新（已废弃）

**推荐阅读时间**: 45 分钟
**适合人群**: 需要实现实时数据同步的开发者

**当前工程应用**:
- 🔜 可替代定期轮询机制
- 🔜 实现秒级数据更新延迟
- 🔜 大幅降低 API 调用消耗

**新特性**: Notion 最新推出的 Webhook 功能（2025）

---

## 🎯 学习路径推荐

### 路径 1: 快速上手（适合已有基础）
1. 阅读 [00_getting_started.md](./00_getting_started.md) 的"当前工程配置"部分
2. 阅读 [04_workspace_document_types.md](./04_workspace_document_types.md) 了解工作区结构
3. 阅读 [01_working_with_databases.md](./01_working_with_databases.md)
4. 查看 [02_property_types.md](./02_property_types.md) 的属性对照表
5. 开始编码实践

**预计时间**: 1.5 小时

---

### 路径 2: 系统学习（适合新手）
1. 完整阅读 [00_getting_started.md](./00_getting_started.md)
2. 完整阅读 [01_working_with_databases.md](./01_working_with_databases.md)
3. 完整阅读 [02_property_types.md](./02_property_types.md)
4. 完整阅读 [03_working_with_page_content.md](./03_working_with_page_content.md)
5. 完整阅读 [04_workspace_document_types.md](./04_workspace_document_types.md)
6. 实践练习

**预计时间**: 3.5-4.5 小时

---

### 路径 3: 问题导向（适合遇到具体问题）
根据具体需求查阅相应章节:

| 需求 | 推荐章节 |
|-----|---------|
| 配置 Integration | [00_getting_started.md](./00_getting_started.md#创建第一个-integration) |
| 了解工作区结构 | [04_workspace_document_types.md](./04_workspace_document_types.md) |
| 查询数据库 | [01_working_with_databases.md](./01_working_with_databases.md#查询数据库中的页面) |
| 提取 Status 属性 | [02_property_types.md](./02_property_types.md#33-status-状态) |
| 获取页面内容 | [03_working_with_page_content.md](./03_working_with_page_content.md#1-读取页面内容) |
| 处理嵌套内容 | [03_working_with_page_content.md](./03_working_with_page_content.md#嵌套-blocks) |
| 优化属性提取 | [04_workspace_document_types.md](./04_workspace_document_types.md#对同步和属性提取的建议) |

---

## 🔧 当前工程集成情况

### 文件结构
```
app/
├── connectors/
│   └── notion.py         # Notion 连接器实现
├── services/
│   ├── rag.py            # RAG 服务（向量存储）
│   └── sync.py           # 同步服务
└── config.py             # 配置管理

docs_notion/              # 本文档目录
├── README.md             # 本文件（索引导航）
├── 00_getting_started.md # 入门指南
├── 01_working_with_databases.md # 数据库操作
├── 02_property_types.md  # 属性类型详解
├── 03_working_with_page_content.md # 页面内容处理
├── 04_workspace_document_types.md # 工作区文档类型 ⭐
├── 05_webhooks.md        # Webhooks 实时通知 🆕
└── reference/            # 参考资料（API 快速查阅）
    ├── api-endpoints.md         # API 端点速查手册
    └── workspace-setup-guide.md # 工作区设置指南
```

### 核心功能实现状态

#### ✅ 已实现
- **认证**: Internal Integration Token
- **数据获取**: 流式获取页面和数据库
- **属性提取**: 10 种核心属性类型
  - status, select, multi_select
  - date, number
  - people, relation
  - rich_text, formula, unique_id
- **内容提取**: 5 种核心 Block 类型
  - paragraph, heading_1/2/3
  - bulleted_list_item, numbered_list_item
  - code
- **增量同步**: 基于 last_edited_time
- **幂等性**: Upsert 机制（文档 ID 去重）
- **速率限制**: 350ms 延迟控制

#### ⏳ 待补充
- **属性类型**: checkbox, url, email, phone_number, files
- **Block 类型**: to_do, quote, callout, image, video, table
- **评论功能**: 获取页面评论
- **写操作**: 创建/更新页面和属性

---

## 📖 代码示例索引

### 基础操作

#### 初始化客户端
```python
from notion_client import Client
import os

notion = Client(auth=os.environ["NOTION_TOKEN"])
```

**参考**: [00_getting_started.md](./00_getting_started.md#基本-api-调用)

---

#### 测试连接
```python
async def test_connection():
    try:
        response = await client.post(
            "https://api.notion.com/v1/search",
            headers={"Authorization": f"Bearer {token}"},
            json={"page_size": 1}
        )
        return response.status_code == 200
    except Exception as e:
        print(f"连接失败: {e}")
        return False
```

**参考**: [00_getting_started.md](./00_getting_started.md#当前工程配置)

---

### 数据库操作

#### 查询数据库
```python
response = notion.databases.query(
    database_id="database-id",
    filter={
        "property": "Status",
        "status": {
            "equals": "In Progress"
        }
    }
)
```

**参考**: [01_working_with_databases.md](./01_working_with_databases.md#查询示例)

---

### 属性提取

#### 提取 Status 属性
```python
status_obj = page.properties["Status"]["status"]
if status_obj:
    status = status_obj["name"]  # "In Progress"
```

**参考**: [02_property_types.md](./02_property_types.md#33-status-状态)

---

#### 提取 Multi-select 属性
```python
tags = []
for tag_obj in page.properties["Tags"]["multi_select"]:
    tags.append(tag_obj["name"])
```

**参考**: [02_property_types.md](./02_property_types.md#32-multi-select-多选)

---

### 内容处理

#### 获取页面 Blocks
```python
response = notion.blocks.children.list(block_id="page-id")
blocks = response["results"]
```

**参考**: [03_working_with_page_content.md](./03_working_with_page_content.md#1-读取页面内容)

---

#### 递归获取嵌套 Blocks
```python
async def get_all_blocks(client, block_id, depth=0):
    if depth > 10:
        return []

    all_blocks = []
    response = await client.blocks.children.list(block_id=block_id)
    blocks = response["results"]

    for block in blocks:
        all_blocks.append(block)
        if block.get("has_children"):
            children = await get_all_blocks(client, block["id"], depth + 1)
            all_blocks.extend(children)

    return all_blocks
```

**参考**: [03_working_with_page_content.md](./03_working_with_page_content.md#递归获取所有-blocks)

---

## 📚 参考资料

`reference/` 目录包含 API 快速查阅文档，适合需要快速查找特定信息时使用：

### [api-endpoints.md](./reference/api-endpoints.md)
- **内容**: 完整的 API 端点速查手册
- **适用场景**: 需要快速查找特定 API 端点的参数和返回值
- **推荐阅读时间**: 按需查阅

### [workspace-setup-guide.md](./reference/workspace-setup-guide.md)
- **内容**: Notion 工作区设置和配置指南
- **适用场景**: 初次设置 Notion Integration 或配置工作区权限
- **推荐阅读时间**: 15-20 分钟

**注意**: 参考资料不是核心学习路径的一部分，仅作为补充查阅使用。建议优先阅读 4 个核心文档（00-03）。

---

## 🚀 实践建议

### 1. 从测试开始
创建测试脚本验证 API 调用:
```bash
poetry run python test_notion_sync.py
```

### 2. 增量开发
按功能模块逐步添加:
1. ✅ 基础连接和认证
2. ✅ 数据库查询
3. ✅ 核心属性提取
4. ⏳ 补充属性类型
5. ⏳ 补充 Block 类型

### 3. 错误处理
始终添加异常处理:
```python
try:
    response = notion.pages.retrieve(page_id=page_id)
except Exception as e:
    print(f"获取页面失败: {e}")
    # 记录日志或重试
```

### 4. 速率限制
遵守 API 速率限制:
```python
import asyncio

async def fetch_with_rate_limit():
    await asyncio.sleep(0.35)  # 350ms 延迟
    response = await fetch_data()
    return response
```

---

## 🔗 外部资源

### 官方资源
- [Notion API 官方文档](https://developers.notion.com/)
- [Notion Python SDK](https://github.com/ramnes/notion-sdk-py)
- [Notion JavaScript SDK](https://github.com/makenotion/notion-sdk-js)
- [API Reference](https://developers.notion.com/reference/intro)

### 社区资源
- [Notion Developers Slack](https://join.slack.com/t/notiondevs/shared_invite/zt-20b5996xv-DzJdLiympy6jP0GGzu3AMg)
- [Notion API Examples](https://github.com/makenotion/notion-sdk-js/tree/main/examples)
- [Stack Overflow - Notion API](https://stackoverflow.com/questions/tagged/notion-api)

### 工程相关
- [当前工程开发指南](../CLAUDE.md)
- [环境配置模板](../.env.example)
- [Notion 连接器代码](../app/connectors/notion.py)

---

## 💡 常见问题 FAQ

### Q: 为什么我的 Integration 无法访问页面？
A: 创建 Integration 后必须手动授权。参见 [00_getting_started.md#步骤-5-添加-integration-到页面](./00_getting_started.md#步骤-5-添加-integration-到页面)

### Q: 如何处理分页？
A: 使用 `next_cursor` 参数。参见 [01_working_with_databases.md#分页限制](./01_working_with_databases.md#分页限制)

### Q: 属性提取返回 None 怎么办？
A: 检查属性类型和字段名是否正确。参见 [02_property_types.md#最佳实践](./02_property_types.md#最佳实践)

### Q: 如何获取嵌套的 Block 内容？
A: 使用递归方法。参见 [03_working_with_page_content.md#递归获取所有-blocks](./03_working_with_page_content.md#递归获取所有-blocks)

---

## 📝 更新日志

### 2025-12-25
- ✅ 新增 Webhooks 文档（05_webhooks.md）
- ✅ 涵盖 Notion 最新的 Webhook 功能
- ✅ 包含完整的实现示例和安全最佳实践
- ✅ 提供从轮询迁移到 Webhook 的指南

### 2024-12-22
- ✅ 创建完整文档集
- ✅ 涵盖 5 个核心主题（00-04）
- ✅ 添加当前工程对照
- ✅ 提供学习路径建议
- ✅ 组织文档结构，分离核心文档和参考资料
- ✅ 移除不适用的 ETL/S3 相关文档
- ✅ 新增工作区文档类型分析（04_workspace_document_types.md）

---

## 🙏 贡献

欢迎补充和完善文档！

如发现错误或有改进建议，请：
1. 直接修改文档
2. 添加注释说明
3. 更新本 README

---

**祝学习愉快！** 🎉
