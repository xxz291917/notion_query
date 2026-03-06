# Notion API 入门指南

> 来源: https://developers.notion.com/docs/getting-started
> 相关文档:
> - https://developers.notion.com/docs/create-a-notion-integration
> - https://developers.notion.com/docs/authorization
> 整理时间: 2024-12-22

## 目录
1. [什么是 Notion Integration](#什么是-notion-integration)
2. [创建第一个 Integration](#创建第一个-integration)
3. [认证和授权](#认证和授权)
4. [基本 API 调用](#基本-api-调用)
5. [当前工程配置](#当前工程配置)

---

## 什么是 Notion Integration

### Integration 类型

#### 1. Internal Integration (内部集成)
**适用场景**: 单个工作区内使用

**特点**:
- ✅ 绑定到单个 Notion 工作区
- ✅ 使用固定的 Integration Token
- ✅ 需要手动添加到页面/数据库
- ✅ 简单直接，适合个人或团队使用

**当前工程使用**: ✅ Internal Integration

---

#### 2. Public Integration (公共集成)
**适用场景**: 面向多个用户的应用

**特点**:
- ✅ 可被任何 Notion 用户使用
- ✅ 使用 OAuth 2.0 授权流程
- ✅ 用户可选择性授权页面
- ✅ 适合 SaaS 产品或公开分发的应用

**示例**: Notion 市场上的第三方应用

---

## 创建第一个 Integration

### 步骤 1: 前往 Integration 管理页面

访问: [https://www.notion.com/my-integrations](https://www.notion.so/profile/integrations)

### 步骤 2: 创建新 Integration

1. 点击 **"+ New integration"**
2. 填写 Integration 信息:
   - **Name**: Integration 名称 (例如: "AIBox Knowledge Sync")
   - **Logo**: 可选，上传图标
   - **Associated workspace**: 选择关联的工作区

### 步骤 3: 配置权限 (Capabilities)

选择 Integration 需要的权限:

| 权限类型 | 说明 | 当前工程需求 |
|---------|------|-------------|
| **Read content** | 读取页面和数据库内容 | ✅ 需要 |
| **Update content** | 更新页面和数据库 | ❌ 不需要（只读） |
| **Insert content** | 创建新页面和数据库 | ❌ 不需要 |
| **Read comments** | 读取评论 | ⚠️ 可选 |
| **Insert comments** | 添加评论 | ❌ 不需要 |
| **Read user information** | 读取用户信息 | ✅ 需要（获取作者信息） |

### 步骤 4: 获取 API Token

1. 进入 **"Secrets"** 标签页
2. 复制 **"Internal Integration Secret"**
3. **重要**: 妥善保管 Token，不要泄露

**Token 格式**:
```
secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 步骤 5: 添加 Integration 到页面

**关键步骤**: Integration 创建后默认无法访问任何页面，必须手动授权！

#### 如何授权页面:
1. 打开 Notion 页面或数据库
2. 点击右上角 **"..."** 菜单
3. 选择 **"+ Add connections"**
4. 搜索并选择你的 Integration
5. 确认授权

**授权范围**:
- 授权后，Integration 可以访问该页面及其所有子页面
- 如果是数据库，可以访问数据库中的所有页面

---

## 认证和授权

### Internal Integration 认证流程

**超简单**: 只需要一个 Token！

```python
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])

# 就这么简单，可以开始调用 API 了
```

### Public Integration OAuth 2.0 流程

**步骤概览**:

```
1. 用户点击"连接 Notion"
   ↓
2. 重定向到 Notion 授权页面
   ↓
3. 用户选择要授权的页面
   ↓
4. Notion 回调你的应用 (带上 code)
   ↓
5. 用 code 换取 access_token
   ↓
6. 用 access_token 调用 API
```

#### 详细流程

**1. 构建授权 URL**
```python
authorization_url = (
    "https://api.notion.com/v1/oauth/authorize"
    f"?client_id={CLIENT_ID}"
    f"&response_type=code"
    f"&owner=user"
    f"&redirect_uri={REDIRECT_URI}"
)
```

**2. 用户授权后获取 code**
```
用户同意后，Notion 会重定向到:
https://your-app.com/callback?code=AUTHORIZATION_CODE
```

**3. 用 code 换取 access_token**
```python
import requests
import base64

# 构建 Basic Auth
auth_header = base64.b64encode(
    f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
).decode()

response = requests.post(
    "https://api.notion.com/v1/oauth/token",
    headers={
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json"
    },
    json={
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri
    }
)

tokens = response.json()
access_token = tokens["access_token"]
refresh_token = tokens["refresh_token"]  # 用于刷新
```

**4. 使用 access_token 调用 API**
```python
notion = Client(auth=access_token)
```

**5. 刷新 access_token**
```python
response = requests.post(
    "https://api.notion.com/v1/oauth/token",
    headers={
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json"
    },
    json={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
)

new_tokens = response.json()
new_access_token = new_tokens["access_token"]
```

---

## 基本 API 调用

### 环境配置

**环境变量设置 (.env)**:
```bash
# Internal Integration
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 或者 Public Integration
NOTION_ACCESS_TOKEN=secret_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

### Python SDK 安装

```bash
pip install notion-client

# 或使用 Poetry
poetry add notion-client
```

### 基础示例

#### 1. 初始化客户端
```python
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])
```

#### 2. 搜索页面
```python
# 搜索所有可访问的页面和数据库
response = notion.search(
    filter={
        "property": "object",
        "value": "page"
    },
    sort={
        "direction": "descending",
        "timestamp": "last_edited_time"
    }
)

pages = response["results"]
for page in pages:
    print(f"页面: {page['id']}")
```

#### 3. 查询数据库
```python
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

response = notion.databases.query(
    database_id=database_id,
    filter={
        "property": "Status",
        "status": {
            "equals": "In Progress"
        }
    }
)

pages = response["results"]
```

#### 4. 获取页面内容
```python
page_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# 获取页面基本信息
page = notion.pages.retrieve(page_id=page_id)

# 获取页面的 blocks (内容)
blocks = notion.blocks.children.list(block_id=page_id)
```

#### 5. 创建页面 (如果有写权限)
```python
new_page = notion.pages.create(
    parent={
        "database_id": database_id
    },
    properties={
        "Name": {
            "title": [
                {
                    "text": {
                        "content": "新任务"
                    }
                }
            ]
        },
        "Status": {
            "status": {
                "name": "Not Started"
            }
        }
    }
)
```

---

## 当前工程配置

### 配置文件位置
- **文件**: `app/config.py`
- **环境变量**: `.env`

### 当前配置

**`.env` 文件**:
```bash
# Notion API
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**`app/config.py`**:
```python
class Settings(BaseSettings):
    # Notion
    notion_token: str = Field(default="", env="NOTION_TOKEN")
```

### NotionConnector 实现

**文件**: `app/connectors/notion.py`

**关键代码**:
```python
class NotionConnector(BaseConnector):
    API_BASE = "https://api.notion.com/v1"
    API_VERSION = "2022-06-28"

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.token = config.get("token")

    def _get_headers(self) -> dict[str, str]:
        """构建 API 请求头"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.API_VERSION,
            "Content-Type": "application/json",
        }

    async def test_connection(self) -> bool:
        """测试连接"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.API_BASE}/search",
                    headers=self._get_headers(),
                    json={"page_size": 1}
                )
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"Notion connection test failed: {e}")
            return False
```

### 如何配置当前工程

#### 步骤 1: 创建 Integration
1. 访问 https://www.notion.com/my-integrations
2. 创建 Internal Integration
3. 配置权限: Read content, Read user information
4. 复制 Token

#### 步骤 2: 配置环境变量
```bash
# 编辑 .env 文件
NOTION_TOKEN=secret_你的Token
```

#### 步骤 3: 授权页面
1. 打开 Notion 工作区
2. 对需要同步的页面/数据库执行: ... → Add connections → 选择你的 Integration

#### 步骤 4: 测试连接
```bash
poetry run python scripts/sync_data.py test-connections
```

---

## 权限和安全

### Token 安全最佳实践

#### ✅ 正确做法
```python
# 使用环境变量
import os
token = os.environ["NOTION_TOKEN"]

# 或使用 .env 文件 + python-dotenv
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("NOTION_TOKEN")
```

#### ❌ 错误做法
```python
# 永远不要硬编码 Token！
token = "secret_xxxxxxxxxxxxxxxx"  # ❌ 危险！

# 永远不要提交 Token 到 Git！
# 确保 .env 在 .gitignore 中
```

### 权限控制

#### Integration 权限级别
1. **页面级别**: 只能访问明确授权的页面
2. **数据库级别**: 可以访问数据库及其所有页面
3. **工作区级别**: 无法自动访问整个工作区（需要逐个授权）

#### 最小权限原则
- 只请求必需的权限
- 定期审查 Integration 权限
- 移除不再使用的 Integration

---

## API 限制和配额

### 速率限制 (Rate Limiting)

| 限制类型 | 限制值 |
|---------|--------|
| 请求频率 | 平均每秒 3 个请求 |
| 突发流量 | 短时间内可超过，但会被限流 |

### 当前工程的处理

**文件**: `app/connectors/notion.py`

```python
class NotionConnector(BaseConnector):
    RATE_LIMIT_DELAY = 0.35  # 350ms 延迟 ≈ 2.8 req/s

    async def fetch_data_streaming(self, last_sync: Optional[datetime] = None):
        async with httpx.AsyncClient(timeout=30.0) as client:
            async for item in self._search_all(client, last_sync):
                await asyncio.sleep(self.RATE_LIMIT_DELAY)  # 🔧 速率限制
                # ... 处理数据
```

### 分页限制
- 每次请求最多返回 100 条结果
- 使用 `next_cursor` 获取下一页

---

## 常见问题 (FAQ)

### Q1: 为什么我的 Integration 无法访问页面？
**A**: Integration 创建后默认无权限，必须手动添加到页面：
1. 打开页面
2. ... → Add connections
3. 选择你的 Integration

### Q2: Token 过期了怎么办？
**A**:
- **Internal Integration**: Token 不会过期，除非手动重置
- **Public Integration**: 使用 refresh_token 刷新

### Q3: 如何获取页面 ID？
**A**:
- 方法 1: 从页面 URL 提取
  ```
  https://notion.so/My-Page-123abc456def?v=xxx
                      ^^^^^^^^^^^^^^^^
                         这是 Page ID
  ```
- 方法 2: 使用 Search API 查找

### Q4: 可以访问其他工作区的页面吗？
**A**: Internal Integration 只能访问绑定的工作区

### Q5: 如何处理 API 错误？
**A**: 常见错误码:
- `400`: 请求参数错误
- `401`: Token 无效
- `403`: 无权限访问
- `404`: 页面不存在
- `429`: 请求过于频繁
- `500`: Notion 服务器错误

---

## 下一步学习

1. ✅ [使用数据库](./01_working_with_databases.md)
2. ✅ [属性类型详解](./02_property_types.md)
3. 📖 [处理页面内容](https://developers.notion.com/docs/working-with-page-content)
4. 📖 [搜索 API](https://developers.notion.com/reference/post-search)
5. 📖 [API 参考文档](https://developers.notion.com/reference/intro)

---

## 参考资源

### 官方资源
- [Notion API 官方文档](https://developers.notion.com/)
- [Notion Python SDK](https://github.com/ramnes/notion-sdk-py)
- [Notion JavaScript SDK](https://github.com/makenotion/notion-sdk-js)

### 社区资源
- [Notion Developers Slack](https://join.slack.com/t/notiondevs/shared_invite/zt-20b5996xv-DzJdLiympy6jP0GGzu3AMg)
- [Notion API 示例集合](https://github.com/makenotion/notion-sdk-js/tree/main/examples)

### 当前工程相关
- [CLAUDE.md](../CLAUDE.md) - 工程开发指南
- [.env.example](../.env.example) - 环境变量模板
- [app/connectors/notion.py](../app/connectors/notion.py) - Notion 连接器实现
