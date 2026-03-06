# Notion API 属性类型详解

> 来源: https://developers.notion.com/reference/property-object
> 整理时间: 2024-12-22

## 概述

Notion 数据库中的每个页面都有属性 (Properties)，属性定义了页面的结构化数据。本文档详细说明所有支持的属性类型。

## 属性类型分类

### 1. 基础属性类型

#### 1.1 Checkbox (复选框)
**用途**: 存储布尔值 (true/false)

**Schema 结构**:
```json
{
  "id": "string",
  "name": "Completed",
  "type": "checkbox",
  "checkbox": {}
}
```

**读取值**:
```python
is_completed = page.properties["Completed"]["checkbox"]  # True or False
```

**写入值**:
```python
properties = {
    "Completed": {
        "checkbox": True
    }
}
```

---

#### 1.2 Title (标题) ⭐ 必需
**用途**: 每个数据库必须有一个 title 属性作为主标识

**Schema 结构**:
```json
{
  "id": "title",
  "name": "Name",
  "type": "title",
  "title": {}
}
```

**读取值**:
```python
title = ""
if page.properties["Name"]["title"]:
    title = page.properties["Name"]["title"][0]["plain_text"]
```

**写入值**:
```python
properties = {
    "Name": {
        "title": [
            {
                "type": "text",
                "text": {"content": "My Page Title"}
            }
        ]
    }
}
```

---

#### 1.3 Rich Text (富文本)
**用途**: 存储格式化文本内容

**读取值**:
```python
text = ""
for text_obj in page.properties["Description"]["rich_text"]:
    text += text_obj["plain_text"]
```

**写入值**:
```python
properties = {
    "Description": {
        "rich_text": [
            {
                "type": "text",
                "text": {"content": "This is a description"}
            }
        ]
    }
}
```

---

### 2. 数字和日期类型

#### 2.1 Number (数字)
**用途**: 存储数值

**Schema 结构**:
```json
{
  "id": "string",
  "name": "Price",
  "type": "number",
  "number": {
    "format": "number"  // 或 "number_with_commas", "percent", "dollar", "euro", 等
  }
}
```

**读取值**:
```python
price = page.properties["Price"]["number"]  # float or None
```

**写入值**:
```python
properties = {
    "Price": {
        "number": 99.99
    }
}
```

---

#### 2.2 Date (日期)
**用途**: 存储日期或日期范围

**Schema 结构**:
```json
{
  "id": "string",
  "name": "Due Date",
  "type": "date",
  "date": {}
}
```

**读取值**:
```python
date_obj = page.properties["Due Date"]["date"]
if date_obj:
    start_date = date_obj["start"]  # "2024-12-31" or "2024-12-31T10:00:00Z"
    end_date = date_obj.get("end")  # 可选
```

**写入值**:
```python
# 单个日期
properties = {
    "Due Date": {
        "date": {
            "start": "2024-12-31"
        }
    }
}

# 日期范围
properties = {
    "Event Date": {
        "date": {
            "start": "2024-12-01",
            "end": "2024-12-31"
        }
    }
}
```

---

### 3. 选择类型

#### 3.1 Select (单选)
**用途**: 从预定义选项中选择一个

**Schema 结构**:
```json
{
  "id": "string",
  "name": "Priority",
  "type": "select",
  "select": {
    "options": [
      {"id": "1", "name": "High", "color": "red"},
      {"id": "2", "name": "Medium", "color": "yellow"},
      {"id": "3", "name": "Low", "color": "green"}
    ]
  }
}
```

**读取值**:
```python
select_obj = page.properties["Priority"]["select"]
if select_obj:
    priority = select_obj["name"]  # "High", "Medium", 或 "Low"
    color = select_obj["color"]    # "red", "yellow", 或 "green"
```

**写入值**:
```python
properties = {
    "Priority": {
        "select": {
            "name": "High"
        }
    }
}
```

---

#### 3.2 Multi-select (多选)
**用途**: 从预定义选项中选择多个

**Schema 结构**:
```json
{
  "id": "string",
  "name": "Tags",
  "type": "multi_select",
  "multi_select": {
    "options": [
      {"id": "1", "name": "Important", "color": "red"},
      {"id": "2", "name": "Urgent", "color": "orange"}
    ]
  }
}
```

**读取值**:
```python
tags = []
for tag_obj in page.properties["Tags"]["multi_select"]:
    tags.append(tag_obj["name"])
# tags = ["Important", "Urgent"]
```

**写入值**:
```python
properties = {
    "Tags": {
        "multi_select": [
            {"name": "Important"},
            {"name": "Urgent"}
        ]
    }
}
```

---

#### 3.3 Status (状态)
**用途**: 工作流状态跟踪，支持分组

**Schema 结构**:
```json
{
  "id": "string",
  "name": "Status",
  "type": "status",
  "status": {
    "options": [
      {"id": "1", "name": "Not Started", "color": "gray"},
      {"id": "2", "name": "In Progress", "color": "blue"},
      {"id": "3", "name": "Done", "color": "green"}
    ],
    "groups": [
      {"id": "g1", "name": "To Do", "option_ids": ["1"]},
      {"id": "g2", "name": "In Progress", "option_ids": ["2"]},
      {"id": "g3", "name": "Complete", "option_ids": ["3"]}
    ]
  }
}
```

**读取值**:
```python
status_obj = page.properties["Status"]["status"]
if status_obj:
    status = status_obj["name"]  # "In Progress"
    color = status_obj["color"]  # "blue"
```

**写入值**:
```python
properties = {
    "Status": {
        "status": {
            "name": "In Progress"
        }
    }
}
```

---

### 4. 人员和关系类型

#### 4.1 People (人员)
**用途**: 标记用户或团队成员

**Schema 结构**:
```json
{
  "id": "string",
  "name": "Assignee",
  "type": "people",
  "people": {}
}
```

**读取值**:
```python
assignees = []
for person in page.properties["Assignee"]["people"]:
    name = person.get("name") or person["id"]
    assignees.append(name)
```

**写入值**:
```python
properties = {
    "Assignee": {
        "people": [
            {"id": "user-uuid-1"},
            {"id": "user-uuid-2"}
        ]
    }
}
```

---

#### 4.2 Relation (关联)
**用途**: 关联到其他数据库页面

**Schema 结构**:
```json
{
  "id": "string",
  "name": "Related Tasks",
  "type": "relation",
  "relation": {
    "database_id": "target-database-uuid",
    "type": "dual_property"
  }
}
```

**读取值**:
```python
related_ids = []
for relation in page.properties["Related Tasks"]["relation"]:
    related_ids.append(relation["id"])
```

**写入值**:
```python
properties = {
    "Related Tasks": {
        "relation": [
            {"id": "page-uuid-1"},
            {"id": "page-uuid-2"}
        ]
    }
}
```

---

### 5. 文件和链接类型

#### 5.1 URL (网址)
**用途**: 存储 URL 链接

**读取值**:
```python
url = page.properties["Website"]["url"]  # string or None
```

**写入值**:
```python
properties = {
    "Website": {
        "url": "https://example.com"
    }
}
```

---

#### 5.2 Email (邮箱)
**用途**: 存储电子邮件地址

**读取值**:
```python
email = page.properties["Contact"]["email"]  # string or None
```

**写入值**:
```python
properties = {
    "Contact": {
        "email": "user@example.com"
    }
}
```

---

#### 5.3 Phone Number (电话号码)
**用途**: 存储电话号码

**读取值**:
```python
phone = page.properties["Phone"]["phone_number"]  # string or None
```

**写入值**:
```python
properties = {
    "Phone": {
        "phone_number": "+1-234-567-8900"
    }
}
```

---

#### 5.4 Files (文件)
**用途**: 上传文件或链接外部文件

**读取值**:
```python
files = []
for file_obj in page.properties["Attachments"]["files"]:
    files.append({
        "name": file_obj["name"],
        "url": file_obj.get("file", {}).get("url") or file_obj.get("external", {}).get("url")
    })
```

**写入值**:
```python
properties = {
    "Attachments": {
        "files": [
            {
                "name": "Document.pdf",
                "external": {"url": "https://example.com/doc.pdf"}
            }
        ]
    }
}
```

---

### 6. 计算和只读类型

#### 6.1 Formula (公式)
**用途**: 根据表达式自动计算值

**Schema 结构**:
```json
{
  "id": "string",
  "name": "Total",
  "type": "formula",
  "formula": {
    "expression": "prop(\"Price\") * prop(\"Quantity\")"
  }
}
```

**读取值**:
```python
formula_obj = page.properties["Total"]["formula"]
formula_type = formula_obj["type"]  # "string", "number", "boolean", "date"

if formula_type == "number":
    value = formula_obj["number"]
elif formula_type == "string":
    value = formula_obj["string"]
elif formula_type == "boolean":
    value = formula_obj["boolean"]
elif formula_type == "date":
    value = formula_obj["date"]
```

**注意**: Formula 属性只读，不能直接写入

---

#### 6.2 Rollup (汇总)
**用途**: 从关联页面聚合数据

**只读属性**，不能直接写入

---

#### 6.3 Created Time (创建时间)
**用途**: 页面创建时间戳

**读取值**:
```python
created_time = page.properties["Created"]["created_time"]
# "2024-12-22T10:00:00.000Z"
```

**注意**: 只读属性

---

#### 6.4 Created By (创建者)
**用途**: 页面创建者

**读取值**:
```python
creator = page.properties["Created By"]["created_by"]
creator_name = creator.get("name") or creator["id"]
```

**注意**: 只读属性

---

#### 6.5 Last Edited Time (最后编辑时间)
**用途**: 页面最后编辑时间戳

**读取值**:
```python
last_edited = page.properties["Last Edited"]["last_edited_time"]
# "2024-12-22T15:30:00.000Z"
```

**注意**: 只读属性

---

#### 6.6 Last Edited By (最后编辑者)
**用途**: 最后编辑页面的用户

**读取值**:
```python
editor = page.properties["Last Edited By"]["last_edited_by"]
editor_name = editor.get("name") or editor["id"]
```

**注意**: 只读属性

---

#### 6.7 Unique ID (唯一标识符)
**用途**: 自动生成的唯一 ID

**Schema 结构**:
```json
{
  "id": "string",
  "name": "ID",
  "type": "unique_id",
  "unique_id": {
    "prefix": "TASK"  // 可选前缀
  }
}
```

**读取值**:
```python
unique_id_obj = page.properties["ID"]["unique_id"]
prefix = unique_id_obj.get("prefix", "")
number = unique_id_obj["number"]
full_id = f"{prefix}{number}"  # "TASK-123"
```

**注意**: 自动生成，不能直接写入

---

## 属性类型对照表

| 属性类型 | 可读 | 可写 | 用途 | 当前工程支持 |
|---------|------|------|------|-------------|
| checkbox | ✅ | ✅ | 布尔值 | ❌ |
| title | ✅ | ✅ | 页面标题 | ✅ |
| rich_text | ✅ | ✅ | 富文本 | ✅ |
| number | ✅ | ✅ | 数字 | ✅ |
| date | ✅ | ✅ | 日期 | ✅ |
| select | ✅ | ✅ | 单选 | ✅ |
| multi_select | ✅ | ✅ | 多选 | ✅ |
| status | ✅ | ✅ | 状态 | ✅ |
| people | ✅ | ✅ | 人员 | ✅ |
| relation | ✅ | ✅ | 关联 | ✅ |
| url | ✅ | ✅ | 网址 | ❌ |
| email | ✅ | ✅ | 邮箱 | ❌ |
| phone_number | ✅ | ✅ | 电话 | ❌ |
| files | ✅ | ✅ | 文件 | ❌ |
| formula | ✅ | ❌ | 公式 | ✅ |
| rollup | ✅ | ❌ | 汇总 | ❌ |
| created_time | ✅ | ❌ | 创建时间 | ❌ |
| created_by | ✅ | ❌ | 创建者 | ❌ |
| last_edited_time | ✅ | ❌ | 编辑时间 | ❌ |
| last_edited_by | ✅ | ❌ | 编辑者 | ❌ |
| unique_id | ✅ | ❌ | 唯一ID | ✅ |

## 当前工程实现状态

### 已实现 (app/connectors/notion.py)
```python
def _extract_properties(self, item: dict[str, Any]) -> dict[str, Any]:
    # ✅ status
    # ✅ select
    # ✅ multi_select
    # ✅ date
    # ✅ people
    # ✅ relation
    # ✅ rich_text
    # ✅ number
    # ✅ formula
    # ✅ unique_id
```

### 建议补充
```python
# ❌ checkbox
# ❌ url
# ❌ email
# ❌ phone_number
# ❌ files
# ❌ created_by
# ❌ created_time
# ❌ last_edited_by
# ❌ last_edited_time
```

## 最佳实践

### 1. 属性命名
- 使用清晰描述性的名称
- 避免特殊字符
- 保持一致的命名风格

### 2. 默认值处理
```python
# 安全地读取属性值
def safe_get_property(page, prop_name, prop_type):
    try:
        prop_data = page["properties"].get(prop_name, {})
        value = prop_data.get(prop_type)
        return value
    except Exception:
        return None
```

### 3. 批量属性提取
```python
def extract_all_properties(page):
    """提取页面的所有属性"""
    extracted = {}

    for prop_name, prop_data in page["properties"].items():
        prop_type = prop_data["type"]

        # 根据类型提取值
        if prop_type == "title":
            extracted[prop_name] = get_title(prop_data)
        elif prop_type == "select":
            extracted[prop_name] = get_select(prop_data)
        # ... 其他类型

    return extracted
```

## 参考资源

- [Property Object Reference](https://developers.notion.com/reference/property-object)
- [Property Value Object](https://developers.notion.com/reference/property-value-object)
- [Page Object](https://developers.notion.com/reference/page)
