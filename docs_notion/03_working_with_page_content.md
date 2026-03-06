# Notion API 页面内容处理

> 来源: https://developers.notion.com/docs/working-with-page-content
> 整理时间: 2024-12-22

## 概述

Notion 页面的内容由 **Blocks（块）** 组成。每个段落、标题、列表、图片等都是一个 Block。

## Blocks 核心概念

### 什么是 Block？

Block 是 Notion 内容的基本单元，类似于：
- HTML 中的 `<div>`、`<p>`、`<h1>` 等元素
- Markdown 中的段落、标题、列表

### Block 的通用属性

每个 Block 都有这些公共属性：

```json
{
  "object": "block",
  "id": "block-uuid",
  "type": "paragraph",  // Block 类型
  "created_time": "2024-01-01T00:00:00.000Z",
  "last_edited_time": "2024-01-02T00:00:00.000Z",
  "created_by": { "object": "user", "id": "user-uuid" },
  "last_edited_by": { "object": "user", "id": "user-uuid" },
  "has_children": false,  // 是否有子 Blocks
  "archived": false,
  "parent": { "type": "page_id", "page_id": "page-uuid" }
}
```

---

## Block 类型详解

### 1. 文本类 Blocks

#### Paragraph (段落)
```json
{
  "type": "paragraph",
  "paragraph": {
    "rich_text": [
      {
        "type": "text",
        "text": {
          "content": "这是一个段落",
          "link": null
        },
        "annotations": {
          "bold": false,
          "italic": false,
          "strikethrough": false,
          "underline": false,
          "code": false,
          "color": "default"
        }
      }
    ],
    "color": "default"
  }
}
```

**Python 读取**:
```python
def extract_paragraph(block):
    rich_text = block["paragraph"]["rich_text"]
    text = "".join([item["text"]["content"] for item in rich_text])
    return text
```

---

#### Heading 1/2/3 (标题)
```json
{
  "type": "heading_1",  // 或 heading_2, heading_3
  "heading_1": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "这是一级标题" }
      }
    ],
    "color": "default",
    "is_toggleable": false
  }
}
```

**Python 读取**:
```python
def extract_heading(block):
    block_type = block["type"]  # heading_1, heading_2, heading_3
    rich_text = block[block_type]["rich_text"]
    text = "".join([item["text"]["content"] for item in rich_text])

    # 转换为 Markdown
    level = block_type.split("_")[1]
    return f"{'#' * int(level)} {text}"
```

---

### 2. 列表类 Blocks

#### Bulleted List (无序列表)
```json
{
  "type": "bulleted_list_item",
  "bulleted_list_item": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "列表项" }
      }
    ],
    "color": "default"
  }
}
```

#### Numbered List (有序列表)
```json
{
  "type": "numbered_list_item",
  "numbered_list_item": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "第一项" }
      }
    ],
    "color": "default"
  }
}
```

#### To-Do List (待办列表)
```json
{
  "type": "to_do",
  "to_do": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "待办事项" }
      }
    ],
    "checked": false,  // 是否完成
    "color": "default"
  }
}
```

**Python 读取**:
```python
def extract_todo(block):
    rich_text = block["to_do"]["rich_text"]
    text = "".join([item["text"]["content"] for item in rich_text])
    checked = block["to_do"]["checked"]
    checkbox = "[x]" if checked else "[ ]"
    return f"{checkbox} {text}"
```

---

### 3. 代码和引用类 Blocks

#### Code Block (代码块)
```json
{
  "type": "code",
  "code": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "def hello():\n    print('Hello')" }
      }
    ],
    "language": "python",  // 编程语言
    "caption": []
  }
}
```

**支持的语言**: python, javascript, java, c, cpp, go, rust, sql, html, css, etc.

**Python 读取**:
```python
def extract_code(block):
    rich_text = block["code"]["rich_text"]
    code = "".join([item["text"]["content"] for item in rich_text])
    language = block["code"]["language"]
    return f"```{language}\n{code}\n```"
```

---

#### Quote Block (引用)
```json
{
  "type": "quote",
  "quote": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "这是一段引用" }
      }
    ],
    "color": "default"
  }
}
```

---

#### Callout (提示框)
```json
{
  "type": "callout",
  "callout": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "重要提示" }
      }
    ],
    "icon": {
      "type": "emoji",
      "emoji": "💡"
    },
    "color": "yellow_background"
  }
}
```

---

### 4. 媒体类 Blocks

#### Image (图片)
```json
{
  "type": "image",
  "image": {
    "type": "external",  // 或 "file"
    "external": {
      "url": "https://example.com/image.png"
    }
  }
}
```

**Python 读取**:
```python
def extract_image(block):
    image = block["image"]
    if image["type"] == "external":
        url = image["external"]["url"]
    elif image["type"] == "file":
        url = image["file"]["url"]
    return f"![Image]({url})"
```

---

#### Video / Audio / File (视频/音频/文件)
```json
{
  "type": "video",  // 或 audio, file
  "video": {
    "type": "external",
    "external": {
      "url": "https://youtube.com/watch?v=xxx"
    }
  }
}
```

---

### 5. 嵌入和链接类 Blocks

#### Embed (嵌入)
```json
{
  "type": "embed",
  "embed": {
    "url": "https://example.com"
  }
}
```

#### Bookmark (书签)
```json
{
  "type": "bookmark",
  "bookmark": {
    "url": "https://example.com",
    "caption": []
  }
}
```

---

### 6. 数据库和容器类 Blocks

#### Child Database (子数据库)
```json
{
  "type": "child_database",
  "child_database": {
    "title": "Database Title"
  }
}
```

#### Table (表格)
```json
{
  "type": "table",
  "table": {
    "table_width": 3,
    "has_column_header": true,
    "has_row_header": false
  }
}
```

#### Toggle (折叠块)
```json
{
  "type": "toggle",
  "toggle": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "点击展开" }
      }
    ],
    "color": "default"
  },
  "has_children": true
}
```

---

## 嵌套 Blocks

### 概念

Blocks 可以包含子 Blocks，形成树形结构：

```
Page
├── Paragraph
├── Toggle
│   ├── Paragraph (子内容)
│   └── To-Do (子内容)
└── Bulleted List
    └── Bulleted List (嵌套列表)
```

### 识别嵌套 Blocks

```python
def has_children(block):
    return block.get("has_children", False)
```

### 递归获取所有 Blocks

```python
async def get_all_blocks(client, block_id, depth=0, max_depth=10):
    """递归获取所有 Blocks，包括嵌套的"""
    if depth > max_depth:
        return []

    all_blocks = []

    # 获取直接子 Blocks
    response = await client.blocks.children.list(block_id=block_id)
    blocks = response["results"]

    for block in blocks:
        all_blocks.append(block)

        # 如果有子 Blocks，递归获取
        if block.get("has_children"):
            children = await get_all_blocks(
                client,
                block["id"],
                depth + 1,
                max_depth
            )
            all_blocks.extend(children)

    return all_blocks
```

---

## API 操作

### 1. 读取页面内容

#### 获取页面的所有 Blocks
```python
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])

# 获取页面的直接子 Blocks
response = notion.blocks.children.list(block_id="page-id")
blocks = response["results"]

# 处理分页
while response["has_more"]:
    response = notion.blocks.children.list(
        block_id="page-id",
        start_cursor=response["next_cursor"]
    )
    blocks.extend(response["results"])
```

#### 转换为纯文本
```python
def blocks_to_text(blocks):
    """将 Blocks 转换为纯文本"""
    text_parts = []

    for block in blocks:
        block_type = block["type"]

        # 文本类 Blocks
        if block_type in ["paragraph", "heading_1", "heading_2", "heading_3"]:
            rich_text = block[block_type]["rich_text"]
            text = "".join([item["text"]["content"] for item in rich_text])
            text_parts.append(text)

        # 列表类 Blocks
        elif block_type in ["bulleted_list_item", "numbered_list_item"]:
            rich_text = block[block_type]["rich_text"]
            text = "".join([item["text"]["content"] for item in rich_text])
            text_parts.append(f"• {text}")

        # 待办事项
        elif block_type == "to_do":
            rich_text = block["to_do"]["rich_text"]
            text = "".join([item["text"]["content"] for item in rich_text])
            checked = "[x]" if block["to_do"]["checked"] else "[ ]"
            text_parts.append(f"{checked} {text}")

        # 代码块
        elif block_type == "code":
            rich_text = block["code"]["rich_text"]
            code = "".join([item["text"]["content"] for item in rich_text])
            text_parts.append(f"Code: {code}")

    return "\n".join(text_parts)
```

---

### 2. 创建带内容的页面

```python
new_page = notion.pages.create(
    parent={
        "database_id": "database-id"
    },
    properties={
        "Name": {
            "title": [
                {
                    "text": {
                        "content": "新页面标题"
                    }
                }
            ]
        }
    },
    children=[
        {
            "type": "heading_1",
            "heading_1": {
                "rich_text": [
                    {
                        "text": {
                            "content": "第一部分"
                        }
                    }
                ]
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "text": {
                            "content": "这是段落内容"
                        }
                    }
                ]
            }
        },
        {
            "type": "to_do",
            "to_do": {
                "rich_text": [
                    {
                        "text": {
                            "content": "待办事项"
                        }
                    }
                ],
                "checked": False
            }
        }
    ]
)
```

---

### 3. 追加 Blocks 到页面

```python
# 在页面末尾追加内容
notion.blocks.children.append(
    block_id="page-id",
    children=[
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "text": {
                            "content": "新增的段落"
                        }
                    }
                ]
            }
        }
    ]
)
```

---

### 4. 更新 Block

```python
# 更新段落内容
notion.blocks.update(
    block_id="block-id",
    paragraph={
        "rich_text": [
            {
                "text": {
                    "content": "更新后的内容"
                }
            }
        ]
    }
)
```

---

### 5. 删除 Block

```python
# 归档（软删除）Block
notion.blocks.delete(block_id="block-id")
```

---

## 当前工程实现

### 实现位置
**文件**: `app/connectors/notion.py`

### 当前实现

```python
async def _get_page_content(self, client: httpx.AsyncClient, page_id: str) -> str:
    """获取页面内容（Blocks）"""
    try:
        # 获取所有 blocks
        blocks = await self._get_blocks_recursive(client, page_id)

        # 提取文本内容
        content_parts = []
        for block in blocks:
            block_type = block.get("type", "")

            # 处理文本类 blocks
            if block_type in ["paragraph", "heading_1", "heading_2", "heading_3"]:
                text = self._extract_rich_text(block.get(block_type, {}).get("rich_text", []))
                if text:
                    content_parts.append(text)

            # 处理列表类 blocks
            elif block_type in ["bulleted_list_item", "numbered_list_item"]:
                text = self._extract_rich_text(block.get(block_type, {}).get("rich_text", []))
                if text:
                    content_parts.append(f"• {text}")

            # 处理代码块
            elif block_type == "code":
                code_text = self._extract_rich_text(block.get("code", {}).get("rich_text", []))
                if code_text:
                    content_parts.append(f"Code: {code_text}")

        return "\n\n".join(content_parts)

    except Exception as e:
        print(f"Failed to get page content: {e}")
        return ""


async def _get_blocks_recursive(
    self, client: httpx.AsyncClient, block_id: str, depth: int = 0
) -> list[dict[str, Any]]:
    """递归获取所有 blocks（包括嵌套的）"""
    MAX_DEPTH = 10

    if depth > MAX_DEPTH:
        return []

    all_blocks = []

    try:
        # 获取直接子 blocks
        response = await client.get(
            f"{self.API_BASE}/blocks/{block_id}/children",
            headers=self._get_headers(),
            params={"page_size": 100}
        )
        response.raise_for_status()
        data = response.json()

        blocks = data.get("results", [])
        all_blocks.extend(blocks)

        # 递归获取嵌套的 blocks
        for block in blocks:
            if block.get("has_children", False):
                children = await self._get_blocks_recursive(
                    client, block["id"], depth + 1
                )
                all_blocks.extend(children)

        # 处理分页
        while data.get("has_more", False):
            response = await client.get(
                f"{self.API_BASE}/blocks/{block_id}/children",
                headers=self._get_headers(),
                params={
                    "page_size": 100,
                    "start_cursor": data["next_cursor"]
                }
            )
            response.raise_for_status()
            data = response.json()

            blocks = data.get("results", [])
            all_blocks.extend(blocks)

            # 递归处理新获取的 blocks
            for block in blocks:
                if block.get("has_children", False):
                    children = await self._get_blocks_recursive(
                        client, block["id"], depth + 1
                    )
                    all_blocks.extend(children)

    except Exception as e:
        print(f"Error getting blocks for {block_id}: {e}")

    return all_blocks
```

### 已支持的 Block 类型

当前工程支持以下 Block 类型：
- ✅ paragraph (段落)
- ✅ heading_1/2/3 (标题)
- ✅ bulleted_list_item (无序列表)
- ✅ numbered_list_item (有序列表)
- ✅ code (代码块)
- ✅ 递归获取嵌套 Blocks

### 未支持的 Block 类型

- ❌ to_do (待办列表)
- ❌ quote (引用)
- ❌ callout (提示框)
- ❌ image/video/file (媒体)
- ❌ embed/bookmark (嵌入)
- ❌ table (表格)

---

## 最佳实践

### 1. 分页处理

```python
def get_all_blocks_with_pagination(notion, block_id):
    """处理分页获取所有 Blocks"""
    all_blocks = []
    start_cursor = None

    while True:
        if start_cursor:
            response = notion.blocks.children.list(
                block_id=block_id,
                start_cursor=start_cursor
            )
        else:
            response = notion.blocks.children.list(block_id=block_id)

        all_blocks.extend(response["results"])

        if not response["has_more"]:
            break

        start_cursor = response["next_cursor"]

    return all_blocks
```

### 2. 递归深度限制

```python
MAX_DEPTH = 10  # 防止无限递归

async def get_blocks_safe(client, block_id, depth=0):
    if depth > MAX_DEPTH:
        print(f"⚠️  达到最大递归深度: {MAX_DEPTH}")
        return []

    # ... 继续处理
```

### 3. 错误处理

```python
def safe_extract_text(block, block_type):
    """安全地提取文本，处理异常情况"""
    try:
        if block_type not in block:
            return ""

        rich_text = block[block_type].get("rich_text", [])
        if not rich_text:
            return ""

        text = "".join([item.get("text", {}).get("content", "") for item in rich_text])
        return text
    except Exception as e:
        print(f"提取文本失败: {e}")
        return ""
```

### 4. Rich Text 处理

```python
def extract_rich_text(rich_text_array):
    """提取富文本内容，保留格式信息"""
    parts = []

    for item in rich_text_array:
        content = item.get("text", {}).get("content", "")
        annotations = item.get("annotations", {})

        # 应用格式
        if annotations.get("bold"):
            content = f"**{content}**"
        if annotations.get("italic"):
            content = f"*{content}*"
        if annotations.get("code"):
            content = f"`{content}`"

        parts.append(content)

    return "".join(parts)
```

---

## 性能优化

### 1. 批量获取

```python
# ❌ 低效：逐个获取
for page_id in page_ids:
    blocks = notion.blocks.children.list(block_id=page_id)

# ✅ 高效：并发获取
import asyncio

async def get_blocks_batch(page_ids):
    tasks = [get_blocks_async(page_id) for page_id in page_ids]
    return await asyncio.gather(*tasks)
```

### 2. 缓存常用 Blocks

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_blocks_cached(page_id):
    return notion.blocks.children.list(block_id=page_id)
```

---

## 限制和注意事项

### API 限制
- 每次请求最多 100 个 Blocks
- 需要使用分页获取更多内容
- 速率限制: 平均每秒 3 个请求

### Block 大小限制
- 单个 Block 最大 2000 字符
- 页面总大小有限制

### 不支持的 Block 类型
某些 Notion 功能（如 Synced Blocks、Link Preview）API 不完全支持

---

## 参考资源

- [Block Object Reference](https://developers.notion.com/reference/block)
- [Rich Text Object](https://developers.notion.com/reference/rich-text)
- [Retrieve Block Children](https://developers.notion.com/reference/get-block-children)
- [Append Block Children](https://developers.notion.com/reference/patch-block-children)
