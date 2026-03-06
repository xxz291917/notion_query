# Notion 属性统计汇总

本文档提供所有节点类型的属性快速参考。

生成时间: 2025-12-31T12:38:41.050618

---

## 节点类型概览

| 节点类型 | 数量 | RELATION 属性 | PEOPLE 属性 | 其他属性 |
|---------|------|--------------|------------|----------|
| Bug | 1011 | 2 | 2 | 15 |
| Deliverable | 239 | 2 | 1 | 4 |
| Design | 134 | 2 | 2 | 8 |
| Document | 661 | 1 | 1 | 12 |
| Problem | 1974 | 8 | 1 | 24 |
| Project | 161 | 9 | 6 | 12 |
| Solution | 1385 | 6 | 2 | 17 |
| Task | 722 | 8 | 1 | 17 |

---

## RELATION 属性映射表

用于配置 `RELATION_MAPPINGS`，标记实际使用的属性。

### Bug

```python
"Bug": [
    ("Project", EdgeType.???),  # 覆盖率: 0.0%
    ("Tasks", EdgeType.???),  # 覆盖率: 1.0%
],
```

### Deliverable

```python
"Deliverable": [
    ("Project", EdgeType.???),  # 覆盖率: 92.0%
    ("Tasks", EdgeType.???),  # 覆盖率: 9.0%
],
```

### Design

```python
"Design": [
    ("Tasks", EdgeType.???),  # 覆盖率: 3.0%
    ("Solution", EdgeType.???),  # 覆盖率: 65.0%
],
```

### Document

```python
"Document": [
    ("Solution", EdgeType.???),  # 覆盖率: 19.0%
],
```

### Problem

```python
"Problem": [
    ("Tasks", EdgeType.???),  # 覆盖率: 0.0%
    ("Parent Problem", EdgeType.???),  # 覆盖率: 1.0%
    ("Objective", EdgeType.???),  # 覆盖率: 0.0%
    ("Project", EdgeType.???),  # 覆盖率: 0.0%
    ("Solution", EdgeType.???),  # 覆盖率: 5.0%
    ("Child Problem(s)", EdgeType.???),  # 覆盖率: 0.0%
    ("Feedback", EdgeType.???),  # 覆盖率: 0.0%
    ("Recurring Tasks", EdgeType.???),  # 覆盖率: 0.0%
],
```

### Project

```python
"Project": [
    ("People", EdgeType.???),  # 覆盖率: 13.0%
    ("Problem", EdgeType.???),  # 覆盖率: 69.0%
    ("Bug", EdgeType.???),  # 覆盖率: 1.0%
    ("Deliverables", EdgeType.???),  # 覆盖率: 31.0%
    ("Solutions", EdgeType.???),  # 覆盖率: 60.0%
    ("Feedback", EdgeType.???),  # 覆盖率: 0.0%
    ("Tasks", EdgeType.???),  # 覆盖率: 64.0%
    ("Is Blocking", EdgeType.???),  # 覆盖率: 0.0%
    ("Blocked By", EdgeType.???),  # 覆盖率: 0.0%
],
```

### Solution

```python
"Solution": [
    ("Documents", EdgeType.???),  # 覆盖率: 0.0%
    ("Designs", EdgeType.???),  # 覆盖率: 1.0%
    ("Project", EdgeType.???),  # 覆盖率: 1.0%
    ("Problem", EdgeType.???),  # 覆盖率: 82.0%
    ("Feedback", EdgeType.???),  # 覆盖率: 0.0%
    ("Tasks", EdgeType.???),  # 覆盖率: 0.0%
],
```

### Task

```python
"Task": [
    ("Deliverable", EdgeType.???),  # 覆盖率: 1.0%
    ("Design", EdgeType.???),  # 覆盖率: 1.0%
    ("Problem", EdgeType.???),  # 覆盖率: 4.0%
    ("Bug", EdgeType.???),  # 覆盖率: 0.0%
    ("Solution", EdgeType.???),  # 覆盖率: 1.0%
    ("Sub-tasks", EdgeType.???),  # 覆盖率: 2.0%
    ("Parent-task", EdgeType.???),  # 覆盖率: 2.0%
    ("Project", EdgeType.???),  # 覆盖率: 30.0%
],
```

---

## PEOPLE 属性汇总

用于确定哪些节点需要创建用户边（OWNED_BY/MANAGED_BY/ASSIGNED_TO）。

| 节点类型 | PEOPLE 属性 | 说明 |
|---------|------------|------|
| Bug | `Reported By`, `Owner` | 需要创建用户边 |
| Deliverable | `Assignee` | 需要创建用户边 |
| Design | `Approved by`, `Owner` | 需要创建用户边 |
| Document | `Maintained By` | 需要创建用户边 |
| Problem | `Owner` | 需要创建用户边 |
| Project | ` Requirement sign-off `, `Resources`, `Product Release sign-off `, `Solution sign-off`, `Project Manager`, `Owner` | 需要创建用户边 |
| Solution | `approved_by`, `Owner` | 需要创建用户边 |
| Task | `Assignee` | 需要创建用户边 |

---

## 属性类型分布

| 属性类型 | 出现次数 |
|---------|---------|
| relation | 38 |
| rich_text | 25 |
| people | 16 |
| button | 10 |
| date | 10 |
| formula | 9 |
| select | 8 |
| status | 8 |
| unique_id | 8 |
| title | 8 |
| multi_select | 6 |
| rollup | 6 |
| last_edited_time | 3 |
| created_by | 2 |
| number | 2 |
| created_time | 2 |
| email | 1 |
| files | 1 |

---
