# Working with Databases - Notion API 文档

> 来源: https://developers.notion.com/docs/working-with-databases
> 整理时间: 2024-12-22

## 概述

Notion 数据库是结构化数据的容器，本文档介绍如何通过 API 操作数据库。

### 数据库类型
- **常规数据库 (Regular Databases)**: API 完全支持
- **链接数据源 (Linked Data Sources)**: API 不支持
- **Wiki 数据库**: API 有限支持

## 数据库结构

### 核心组件
1. **Database Object**: 包含数据源信息
2. **Data Source Object**: 定义 schema 和 properties
3. **Pages**: 数据库中的单个条目

### 数据源属性 (Data Source Properties)
- 每个数据源必须有一个 "title" 属性
- 属性有不同类型：Text, Number, Date, People, Select, Multi-select, Status, Relation 等
- 每个属性都有配置对象 (configuration object)

## 添加页面到数据库

### API 端点
使用 `Create a page` 端点创建数据库页面

### 必需参数
- `parent`: 指定父数据源 ID
- `properties`: 匹配数据库 schema 的属性值

### 代码示例

```javascript
const response = await notion.pages.create({
  parent: {
    data_source_id: '248104cd-477e-80af-bc30-000bd28de8f9',
  },
  properties: {
    'Grocery item': {
      type: 'title',
      title: [{
        type: 'text',
        text: { content: 'Tomatoes' },
      }],
    },
    Price: {
      type: 'number',
      number: 1.49,
    },
    'Last ordered': {
      type: 'date',
      date: { start: '2021-05-11' },
    },
  },
});
```

### Python 示例 (推测)

```python
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])

response = notion.pages.create(
    parent={
        "data_source_id": "248104cd-477e-80af-bc30-000bd28de8f9"
    },
    properties={
        "Grocery item": {
            "type": "title",
            "title": [{
                "type": "text",
                "text": {"content": "Tomatoes"}
            }]
        },
        "Price": {
            "type": "number",
            "number": 1.49
        },
        "Last ordered": {
            "type": "date",
            "date": {"start": "2021-05-11"}
        }
    }
)
```

## 查询数据库中的页面

### API 端点
使用 `Query a data source` 端点查询页面

### 功能
- 应用过滤器查找特定页面
- 按多种条件排序结果
- 分页获取结果

### 查询示例

```javascript
const response = await notion.dataSources.query({
  data_source_id: dataSourceId,
  filter: {
    property: 'Last ordered',
    date: { past_week: {} }
  },
  sorts: [{
    timestamp: 'created_time',
    direction: 'descending',
  }]
});
```

### 过滤器类型
- **日期过滤器**: `past_week`, `past_month`, `next_week`, 等
- **文本过滤器**: `equals`, `contains`, `starts_with`, 等
- **数字过滤器**: `equals`, `greater_than`, `less_than`, 等
- **复合过滤器**: `and`, `or`

## 关键限制和注意事项

### Schema 大小限制
- **推荐**: 最大 50KB
- 超过限制会影响性能

### 分页限制
- 每次请求最多返回 100 条结果
- 使用 `next_cursor` 获取下一页

### 权限要求
- 需要正确的 Integration 权限才能访问数据库
- 确保 Integration 已被添加到目标数据库

## 与当前工程的对应关系

### 当前实现位置
- **文件**: `app/connectors/notion.py`
- **方法**:
  - `fetch_data_streaming()`: 流式获取数据
  - `_query_database()`: 查询数据库页面
  - `process_single_item()`: 处理单个页面

### 已实现功能
✅ 查询数据库 (Query a data source)
✅ 获取页面内容 (Get page content)
✅ 提取页面属性 (Extract properties)
✅ 处理各种属性类型 (status, select, date, people, relation, etc.)

### 未实现功能
❌ 创建数据库页面 (Create page in database)
❌ 更新数据库页面 (Update page properties)
❌ 过滤器查询 (Advanced filtering)
❌ 自定义排序 (Custom sorting)

## 相关 API 端点参考

### 数据库相关
- `GET /v1/databases/{database_id}` - 获取数据库信息
- `POST /v1/databases/{database_id}/query` - 查询数据库

### 页面相关
- `POST /v1/pages` - 创建页面
- `PATCH /v1/pages/{page_id}` - 更新页面
- `GET /v1/pages/{page_id}` - 获取页面信息

### 搜索相关
- `POST /v1/search` - 搜索所有可访问的页面和数据库

## 下一步学习方向

1. **属性类型详解**: 深入理解各种属性类型的结构
2. **过滤器和排序**: 学习高级查询技巧
3. **页面内容**: 了解如何处理页面的 blocks
4. **分页处理**: 掌握大量数据的流式处理
5. **错误处理**: 了解常见错误和处理方法

## 实用技巧

### 1. 增量同步
使用 `last_edited_time` 过滤器只获取更新的页面：

```javascript
filter: {
  timestamp: 'last_edited_time',
  last_edited_time: {
    after: '2024-01-01T00:00:00Z'
  }
}
```

### 2. 批量处理
使用分页机制处理大量数据：

```javascript
let hasMore = true;
let cursor = undefined;

while (hasMore) {
  const response = await notion.dataSources.query({
    data_source_id: dataSourceId,
    start_cursor: cursor,
    page_size: 100
  });

  // 处理结果
  processResults(response.results);

  hasMore = response.has_more;
  cursor = response.next_cursor;
}
```

### 3. 属性值提取
不同属性类型的值提取方式不同：

```javascript
// Title 属性
const title = page.properties.Name.title[0]?.plain_text || '';

// Select 属性
const status = page.properties.Status.select?.name || '';

// Multi-select 属性
const tags = page.properties.Tags.multi_select.map(t => t.name);

// Date 属性
const dueDate = page.properties.DueDate.date?.start || null;

// People 属性
const assignees = page.properties.Assignee.people.map(p => p.name);
```

## 参考资源

- [Notion API 官方文档](https://developers.notion.com/)
- [属性类型参考](https://developers.notion.com/reference/property-object)
- [分页说明](https://developers.notion.com/reference/intro#pagination)
- [过滤器参考](https://developers.notion.com/reference/post-database-query-filter)
