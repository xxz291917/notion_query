# Notion 工作区文档类型

> 本文档描述当前 Notion 工作区中的文档类型和数据库结构
> 分析时间: 2024-12-22
> 数据来源: NOTION_DATABASE_ANALYSIS.md

## 📊 概览

当前 Notion 工作区采用**问题驱动的工作流**，包含 6 种主要文档类型，共 50 个页面分布在 7 个数据库中。

### 文档类型分布

```
Problem (问题)        ████████████████████████████████████████ 80% (40页)
Deliverable (交付)    ██████ 6% (3页)
Task (任务)           ████ 4% (2页)
Document (文档)       ████ 4% (2页)
Solution (方案)       ██ 2% (1页)
Simple Task (简单任务) ██ 2% (1页)
```

---

## 🗂️ 文档类型详解

### 1. Problem (问题) ⭐ 主要类型

**数量**: 40 个页面（占 80%）

**用途**: 问题管理和追踪系统

**核心特点**:
- ✅ 支持父子层级结构（Parent Problem / Child Problem）
- ✅ 关联多种其他文档类型（Solution、Tasks、Project、Objective）
- ✅ 包含 33 个属性（Status、Owner、Impact、Scope 等）

**关键属性**:
- `Status` (status) - 当前状态
- `Owner` (people) - 负责人
- `Impact` (number) - 影响程度
- `Scope` (select) - 范围
- `Meetings` (multi_select) - 相关会议

**关系属性**:
- `Parent Problem` (relation) - 父问题
- `Child Problem(s)` (relation) - 子问题
- `Solution` (relation) - 对应的解决方案
- `Tasks` (relation) - 相关任务
- `Project` (relation) - 关联项目
- `Objective` (relation) - 关联目标

**示例页面**:
- "Consume more knowledge at each session"
- "Understand how listings compare to one another"
- "We do not have sufficient trigger at the right con"

**在代码中的表示**:
```python
doc_type = "page"  # 或 "database_page"
metadata = {
    "properties": {
        "Status": "In Progress",
        "Owner": ["张三"],
        "Impact": 8,
        "Parent Problem": ["parent-page-id"],
        "Child Problem(s)": ["child-1-id", "child-2-id"]
    }
}
```

---

### 2. Deliverable (可交付成果)

**数量**: 3 个页面（占 6%）

**用途**: 项目可交付成果管理

**核心特点**:
- ✅ 关联项目和任务
- ✅ 追踪交付状态和截止日期
- ✅ 包含 7 个属性

**关键属性**:
- `Name` (title) - 交付成果名称
- `Status` (status) - 当前状态
- `Assignee` (people) - 负责人
- `Due Date` (date) - 截止日期
- `ID` (unique_id) - 唯一标识

**关系属性**:
- `Project` (relation) - 关联项目
- `Tasks` (relation) - 相关任务

**示例页面**:
- "Write City Landing Page Enhancement Tech Solution"
- "City Landing Page Web Development + Testing"
- "City Landing Page API Development + Testing"

**在代码中的表示**:
```python
doc_type = "database_page"
metadata = {
    "properties": {
        "Status": "In Progress",
        "Assignee": ["李四"],
        "Due Date": "2024-12-31",
        "Project": ["project-id"]
    }
}
```

---

### 3. Task (任务)

**数量**: 2 个页面（占 4%）

**用途**: 详细任务跟踪和管理

**核心特点**:
- ✅ 26 个属性，功能丰富
- ✅ 支持复杂的关系关联（Problem、Solution、Project、Deliverable 等）
- ✅ 包含优先级、截止日期、完成时间等详细信息

**关键属性**:
- `Task name` (title) - 任务名称
- `Status` (status) - 当前状态
- `Priority` (select) - 优先级
- `Assignee` (people) - 负责人
- `Due` (date) - 截止日期
- `Completed on` (date) - 完成日期
- `Type` (select) - 任务类型
- `Section` (select) - 所属部分

**关系属性** (复杂关联):
- `Problem` (relation) - 关联问题
- `Solution` (relation) - 关联解决方案
- `Project` (relation) - 关联项目
- `Deliverable` (relation) - 关联交付成果
- `Design` (relation) - 关联设计
- `Bug` (relation) - 关联 Bug
- `Parent-task` (relation) - 父任务
- `Sub-tasks` (relation) - 子任务

**计算字段**:
- `Delay` (formula) - 延期计算

**示例页面**:
- "US1 Native Test"
- "US1 Update Code"

**在代码中的表示**:
```python
doc_type = "database_page"
metadata = {
    "properties": {
        "Status": "Done",
        "Priority": "High",
        "Assignee": ["王五"],
        "Due": "2024-12-25",
        "Problem": ["problem-id"],
        "Solution": ["solution-id"]
    }
}
```

---

### 4. Document/Resource (文档资源)

**数量**: 2 个页面（占 4%）

**用途**: 文档和资源管理

**核心特点**:
- ✅ 包含 14 个属性
- ✅ 支持文档类型分类
- ✅ 记录维护者和创建日期

**关键属性**:
- `Title` (title) - 文档标题
- `Type` (multi_select) - 文档类型
- `Maintained By` (people) - 维护者
- `Created Date` (date) - 创建日期

**关系属性**:
- `Solution` (relation) - 关联解决方案

**示例页面**:
- "server list"
- "Byte Me Team Work Log"

**在代码中的表示**:
```python
doc_type = "database_page"
metadata = {
    "properties": {
        "Title": "server list",
        "Type": ["Technical", "Reference"],
        "Maintained By": ["赵六"],
        "Solution": ["solution-id"]
    }
}
```

---

### 5. Solution (解决方案)

**数量**: 1 个页面（占 2%）

**用途**: 技术解决方案文档

**核心特点**:
- ✅ 25 个属性，包含详细的技术设计信息
- ✅ 关联 Problem、Tasks、Project、Designs 等多种文档类型
- ✅ 包含工作量评估和审批流程

**关键属性**:
- `Title` (title) - 解决方案标题
- `Status` (status) - 当前状态
- `Owner` (people) - 负责人
- `approved_by` (people) - 审批人
- `Effort` (number) - 工作量评估
- `Scope` (select) - 范围
- `Requires` (multi_select) - 依赖需求

**关系属性**:
- `Problem` (relation) - 对应的问题
- `Tasks` (relation) - 实现任务
- `Project` (relation) - 关联项目
- `Designs` (relation) - 设计文档
- `Documents` (relation) - 相关文档
- `Feedback` (relation) - 反馈

**计算字段**:
- `Impact (from problem)` (rollup) - 从问题汇总影响

**示例页面**:
- "Solution for Showing Time Data Processing Pipeline"

**在代码中的表示**:
```python
doc_type = "database_page"
metadata = {
    "properties": {
        "Status": "Approved",
        "Owner": ["张三"],
        "approved_by": ["Tech Lead"],
        "Effort": 40,
        "Problem": ["problem-id"],
        "Tasks": ["task-1-id", "task-2-id"]
    }
}
```

---

### 6. Simple Task (简单任务)

**数量**: 1 个页面（占 2%）

**用途**: 轻量级任务管理

**核心特点**:
- ✅ 仅 4 个属性，简单快速
- ✅ 适合快速记录和跟踪

**关键属性**:
- `Task name` (title) - 任务名称
- `Status` (status) - 状态
- `Assignee` (people) - 负责人
- `Due date` (date) - 截止日期

**示例页面**:
- "Deal Review"

**在代码中的表示**:
```python
doc_type = "database_page"
metadata = {
    "properties": {
        "Status": "To Do",
        "Assignee": ["李四"],
        "Due date": "2024-12-30"
    }
}
```

---

## 🔗 文档类型关系体系

### 工作流程图

```
Objective (目标)
    ↓
Problem (问题) ⭐ 80% 的内容
    ├── Parent Problem (父问题)
    ├── Child Problem(s) (子问题)
    ↓
Solution (解决方案)
    ↓
Project (项目)
    ↓
Deliverable (可交付成果)
    ↓
Tasks (任务)
    ├── Task (复杂任务)
    └── Simple Task (简单任务)
    ↓
Document/Resource (支持文档)
```

### 关系字段频率

| 关系字段 | 出现频率 | 说明 |
|---------|---------|------|
| Parent Problem | 40次 | 问题层级结构的核心 |
| Objective | 40次 | 目标驱动的工作流 |
| Child Problem(s) | 27次 | 问题分解 |
| Project | 5次 | 项目关联 |
| Tasks | 3次 | 任务关联 |
| Deliverable | 1次 | 交付物关联 |
| Solution | 1次 | 解决方案关联 |

---

## 💡 对同步和属性提取的建议

### 1. 优先级排序

基于文档数量和重要性：

**P0 - 必须支持**:
- Problem (80% 的内容)
  - Status, Owner, Impact, Scope
  - Parent Problem, Child Problem(s), Solution, Tasks, Objective

**P1 - 高优先级**:
- Task (复杂关系网络)
  - Status, Priority, Assignee, Due
  - Problem, Solution, Project, Deliverable 关系
- Deliverable (项目关键输出)
  - Status, Assignee, Due Date
  - Project, Tasks 关系

**P2 - 中优先级**:
- Solution (技术文档)
  - Status, Owner, Effort
  - Problem, Tasks, Project 关系
- Document (支持资料)
  - Type, Maintained By

**P3 - 低优先级**:
- Simple Task (数量少)
  - 基本属性即可

### 2. 属性提取重点

根据实际使用情况，重点提取：

**状态类**:
- `Status` (status) - 所有类型都有
- `Priority` (select) - Task 专有

**人员类**:
- `Owner` / `Assignee` (people)
- `approved_by` (people) - Solution 专有

**时间类**:
- `Due Date` / `Due` (date)
- `Completed on` (date)
- `Created Date` (date)

**关系类**:
- `Parent Problem` (relation) - 最高频
- `Child Problem(s)` (relation)
- `Objective` (relation) - 最高频
- `Solution` (relation)
- `Tasks` (relation)
- `Project` (relation)

**评估类**:
- `Impact` (number) - Problem 专有
- `Effort` (number) - Solution 专有

### 3. 代码实现建议

在 `app/connectors/notion.py` 的 `_extract_properties()` 方法中：

```python
def _extract_properties(self, item: dict) -> dict:
    """提取并解析 Notion 页面的所有属性"""
    properties = item.get("properties", {})
    if not properties:
        return {}

    parsed_props = {}

    for prop_name, prop_data in properties.items():
        prop_type = prop_data.get("type")

        try:
            # 1. Status (最重要，所有类型都有)
            if prop_type == "status":
                status_obj = prop_data.get("status")
                parsed_props[prop_name] = status_obj.get("name") if status_obj else None

            # 2. People (Owner/Assignee)
            elif prop_type == "people":
                people = prop_data.get("people", [])
                parsed_props[prop_name] = [
                    person.get("name") or person.get("id")
                    for person in people
                ]

            # 3. Relation (关系网络)
            elif prop_type == "relation":
                relations = prop_data.get("relation", [])
                parsed_props[prop_name] = [rel.get("id") for rel in relations]

            # 4. Date (时间追踪)
            elif prop_type == "date":
                date_obj = prop_data.get("date")
                if date_obj:
                    start = date_obj.get("start")
                    end = date_obj.get("end")
                    parsed_props[prop_name] = {
                        "start": start,
                        "end": end
                    } if end else start

            # 5. Number (Impact/Effort)
            elif prop_type == "number":
                parsed_props[prop_name] = prop_data.get("number")

            # 6. Select/Multi-select
            elif prop_type == "select":
                select_obj = prop_data.get("select")
                parsed_props[prop_name] = select_obj.get("name") if select_obj else None

            elif prop_type == "multi_select":
                multi_select = prop_data.get("multi_select", [])
                parsed_props[prop_name] = [opt.get("name") for opt in multi_select]

            # 其他类型...

        except Exception as e:
            print(f"⚠️  解析属性失败 {prop_name} ({prop_type}): {e}")
            parsed_props[prop_name] = None

    return parsed_props
```

### 4. 查询优化建议

基于文档类型和属性，支持以下查询场景：

**按状态过滤**:
```python
filter = {"properties.Status": "In Progress"}
```

**按负责人过滤**:
```python
filter = {"properties.Owner": "张三"}
```

**按文档类型过滤**:
```python
filter = {"doc_type": "database_page", "database_title": "Problem Database"}
```

**按关系查找**:
```python
# 查找某个 Problem 的所有 Solution
filter = {"properties.Problem": ["problem-id"]}
```

---

## 📝 总结

### 关键发现

1. **Problem 为核心**: 80% 的内容集中在 Problem 类型
2. **深度关联网络**: Problem 通过 relation 字段关联到几乎所有其他类型
3. **问题驱动工作流**: Objective → Problem → Solution → Project → Deliverable → Tasks
4. **ClickUp 迁移痕迹**: 保留了 ClickUp 集成字段

### 同步优先级

1. **P0**: Problem (40 页) - 核心内容
2. **P1**: Task + Deliverable (5 页) - 执行层
3. **P2**: Solution + Document (3 页) - 技术层
4. **P3**: Simple Task (1 页) - 辅助

### 属性提取优先级

1. **Status** - 所有类型必需
2. **People** (Owner/Assignee) - 责任归属
3. **Relation** - 关系网络核心
4. **Date** - 时间追踪
5. **Number** (Impact/Effort) - 评估指标

---

## 🔗 相关文档

- [Notion 数据库分析报告](../NOTION_DATABASE_ANALYSIS.md) - 完整的数据库结构分析
- [属性类型详解](./02_property_types.md) - 19 种属性类型的详细说明
- [数据库操作](./01_working_with_databases.md) - 如何查询和操作数据库
- [Notion 连接器代码](../app/connectors/notion.py) - 实际实现代码

---

**文档创建时间**: 2024-12-22
**最后更新**: 2024-12-22
