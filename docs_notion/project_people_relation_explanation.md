# Project.People 关系字段说明

## 问题

`Project.People` 是一个 RELATION 类型字段，它是否是列表？如果放到 edges 表里会保存多条记录吗？

## 回答

**是的！** `Project.People` 是一个**关系列表**（relation array），会在 edges 表中保存**多条记录**。

---

## 数据结构分析

### 1. Notion API 返回的原始数据格式

```json
{
  "People": {
    "id": "%3D%5DtG",
    "type": "relation",
    "relation": [
      {"id": "299c2345-ab46-8191-86c9-f8445fc05187"},
      {"id": "295c2345-ab46-8146-b4f2-e71405fc1564"},
      {"id": "29bc2345-ab46-806b-9431-c6f039a11d72"}
    ],
    "has_more": false
  }
}
```

**关键点**：
- `type: "relation"` - 这是 RELATION 类型，不是 PEOPLE 类型
- `relation: [...]` - 这是一个**数组**，可以包含多个关联的 Page ID
- 每个元素是 `{"id": "..."}` 格式

---

## 存储逻辑

### 2. extract_relation() 函数处理

```python
# src/utils/notion_parser.py (lines 158-171)
def extract_relation(prop_data: dict[str, Any]) -> list[str]:
    """Extract page IDs from relation property.

    Returns:
        List of related page IDs  # 注意：返回的是列表
    """
    if prop_data.get("type") != "relation":
        return []

    relation_array = prop_data.get("relation", [])
    return [rel.get("id", "") for rel in relation_array if rel.get("id")]
```

**返回值**：`list[str]` - 一个字符串列表，包含所有关联的 Page ID

---

### 3. _extract_relations_from_page() 处理

```python
# src/services/sync_service.py (lines 515-554)
def _extract_relations_from_page(
    self, page_data: dict[str, Any], node: Node, node_type: str
) -> set[tuple[str, str]]:
    """Extract relations from Notion page."""
    properties = page_data.get("properties", {})
    relations: set[tuple[str, str]] = set()

    # 1. Extract Node-to-Node edges from RELATION properties
    mappings = RELATION_MAPPINGS.get(node_type, [])

    for prop_name, edge_type in mappings:
        if prop_name in properties:
            related_ids = extract_relation(properties[prop_name])  # 返回列表
            for related_id in related_ids:  # 遍历列表中的每个 ID
                relations.add((related_id, edge_type))  # 每个 ID 添加一条边

    # ...
    return relations
```

**关键逻辑**：
1. `extract_relation()` 返回一个 ID 列表：`["id1", "id2", "id3"]`
2. `for related_id in related_ids` 遍历每个 ID
3. `relations.add((related_id, edge_type))` 为每个 ID 创建一条边
4. 最终返回的 `relations` 集合中包含多个 `(target_id, edge_type)` 元组

---

### 4. edges 表中的存储

```python
# src/services/sync_service.py (lines 455-465)
# Stage 2: Sync edges
current_relations = self._extract_relations_from_page(page_data, node, db_type)

# Delete all existing edges from this node
self.db.execute(
    "DELETE FROM edges WHERE source_id = ?", (node.id,)
)

# Insert new edges
for target_id, edge_type in current_relations:
    edge = Edge(source_id=node.id, target_id=target_id, edge_type=edge_type)
    self.db.upsert_edge(edge)
```

**结果**：如果 `Project.People` 有 3 个关联，edges 表会插入 **3 条记录**：

```sql
-- 示例：Project A 有 3 个 People 关联
INSERT INTO edges VALUES ('project_a_id', 'person_1_id', 'HAS_MEMBER');
INSERT INTO edges VALUES ('project_a_id', 'person_2_id', 'HAS_MEMBER');
INSERT INTO edges VALUES ('project_a_id', 'person_3_id', 'HAS_MEMBER');
```

---

## 实际数据验证

### 示例 1：Project.Tasks（已配置，有多个关联）

```sql
-- 查询：某个 Project 有 25 个 Tasks
SELECT
    substr(title, 1, 40) as project_title,
    json_array_length(json_extract(raw_properties, '$.Tasks.relation')) as tasks_count
FROM nodes
WHERE type = 'Project'
ORDER BY tasks_count DESC
LIMIT 1;

-- 结果：
-- HouseSigma blog/PR infographics tester B | 25
```

**edges 表中的存储**：

```sql
SELECT source_id, target_id, edge_type
FROM edges
WHERE source_id = '278c2345-ab46-81fc-9e26-d5571d9cbe60'
  AND edge_type = 'HAS_TASK';

-- 结果：25 条记录（每个 Task 一条边）
278c2345-ab46-81fc-9e26-d5571d9cbe60 | 278c2345-ab46-8000-af74-dc8a084e7b6a | HAS_TASK
278c2345-ab46-81fc-9e26-d5571d9cbe60 | 278c2345-ab46-806e-8445-c334ef6232d8 | HAS_TASK
278c2345-ab46-81fc-9e26-d5571d9cbe60 | 278c2345-ab46-8092-8522-ffdf24c6a89a | HAS_TASK
...（共 25 条）
```

---

### 示例 2：Project.People（未配置，当前数据中多为单个关联）

```sql
-- 当前数据统计：
SELECT
    json_array_length(json_extract(raw_properties, '$.People.relation')) as people_count,
    COUNT(*) as project_count
FROM nodes
WHERE type = 'Project'
  AND json_extract(raw_properties, '$.People.relation') != '[]'
GROUP BY people_count;

-- 结果（当前数据）：
-- people_count | project_count
-- 1            | 21  (21 个项目各有 1 个 People 关联)
```

**预期行为**（配置后）：
- 如果某个 Project 的 People 字段有 3 个关联
- edges 表会插入 **3 条记录**：
  ```
  project_id | person_1_id | HAS_MEMBER
  project_id | person_2_id | HAS_MEMBER
  project_id | person_3_id | HAS_MEMBER
  ```

---

## 总结

| 维度 | 说明 |
|------|------|
| **数据类型** | RELATION 类型（不是 PEOPLE 类型） |
| **数据结构** | 关系数组：`relation: [{"id": "..."}, ...]` |
| **Python 返回值** | `list[str]` - ID 列表 |
| **edges 表存储** | **一对多**：1 个 Project → N 个 People = N 条边记录 |
| **EdgeType** | 建议使用 `HAS_MEMBER` |
| **查询方式** | `SELECT * FROM edges WHERE source_id = ? AND edge_type = 'HAS_MEMBER'` |

---

## 与 PEOPLE 类型字段的区别

### PEOPLE 类型字段（owner_id/pm_id/assignee_id）

**数据结构**：
```json
{
  "Owner": {
    "type": "people",
    "people": [
      {"id": "user_id_1", "name": "John Doe", ...}
    ]
  }
}
```

**存储方式**：
- 存储在 Node 对象的字段中（`owner_id`, `pm_id`, `assignee_id`）
- 每个字段只能有 **1 个用户**（单值）
- 在 `_extract_relations_from_page()` 中单独处理，创建 **1 条边**

**边的创建**：
```python
if node.owner_id:
    relations.add((node.owner_id, EdgeType.OWNED_BY.value))  # 1 条边
```

---

### RELATION 类型字段（Project.People）

**数据结构**：
```json
{
  "People": {
    "type": "relation",
    "relation": [
      {"id": "page_id_1"},
      {"id": "page_id_2"},
      {"id": "page_id_3"}
    ]
  }
}
```

**存储方式**：
- 存储在 `raw_properties` JSON 字段中
- 可以有 **多个关联**（列表）
- 在 `_extract_relations_from_page()` 中遍历处理，创建 **N 条边**

**边的创建**：
```python
for prop_name, edge_type in mappings:
    if prop_name in properties:
        related_ids = extract_relation(properties[prop_name])  # 返回列表
        for related_id in related_ids:  # 遍历列表
            relations.add((related_id, edge_type))  # N 条边
```

---

## 推荐配置

```python
# src/models/schemas.py
class EdgeType(str, Enum):
    # ... 现有类型 ...
    HAS_MEMBER = "HAS_MEMBER"  # Project → User/Page (team member)

# src/services/sync_service.py
RELATION_MAPPINGS = {
    "Project": [
        # ... 现有映射 ...
        ("People", EdgeType.HAS_MEMBER.value),  # 新增：项目团队成员
    ],
}
```

**配置后的效果**：
- 1 个 Project 有 5 个 People 关联 → edges 表插入 **5 条记录**
- 可以通过 SQL 查询项目的所有团队成员
- 可以反向查询用户参与的所有项目（作为团队成员）

---

## 查询示例

### 查询项目的所有团队成员

```sql
SELECT
    p.id as project_id,
    p.title as project_title,
    u.id as member_id,
    u.name as member_name
FROM nodes p
JOIN edges e ON p.id = e.source_id AND e.edge_type = 'HAS_MEMBER'
JOIN nodes u ON e.target_id = u.id
WHERE p.id = 'project_id_here';
```

### 查询用户参与的所有项目（作为团队成员）

```sql
SELECT
    p.id as project_id,
    p.title as project_title
FROM nodes p
JOIN edges e ON p.id = e.source_id AND e.edge_type = 'HAS_MEMBER'
WHERE e.target_id = 'user_id_here';
```

---

## 注意事项

1. **性能**：一对多关系不会影响性能，edges 表已有 `source_id` 和 `edge_type` 的复合索引
2. **数据一致性**：每次同步会删除旧边重新创建，保证与 Notion 一致
3. **覆盖率**：当前 13% 的 Project 使用了 People 字段，配置后会增加约 21-30 条边记录
4. **语义清晰**：`HAS_MEMBER` 明确表示团队成员关系，区别于 `OWNED_BY`（单个负责人）
