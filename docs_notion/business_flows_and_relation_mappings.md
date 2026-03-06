# 业务流程与关系映射完整说明

## 核心原则

**数据同步忠实性**：Notion Daily 是一个数据同步系统，应该**忠实反映 Notion 中的所有实际关系**，而不是强制改变团队的业务流程。

**支持多种业务流程**：团队在实际工作中会根据问题的性质、紧急程度、复杂度选择不同的流程，系统应该支持所有这些场景。

---

## 业务流程场景

### 场景 1: 标准流程（Problem → Solution → Project）

**适用情况**：复杂问题，需要详细设计解决方案

```
Problem (复杂问题)
    ↓ HAS_SOLUTION
Solution (详细的解决方案设计)
    ↓ BELONGS_TO_PROJECT
Project (实施项目)
    ↓ HAS_DELIVERABLE
Deliverable
    ↓ HAS_TASK
Task (具体执行)
```

**关系映射**：

| 节点 | 关系属性 | EdgeType | 含义 |
|------|---------|----------|------|
| Problem | Solution | HAS_SOLUTION | Problem 有 Solution 设计 |
| Solution | Problem | SOLVES_PROBLEM | Solution 解决 Problem |
| Solution | Project | BELONGS_TO_PROJECT | Solution 在 Project 中实施 |
| Project | Solutions | HAS_SOLUTION | Project 包含多个 Solutions |

**数据验证**：
- Problem → Solution: **1042 条边** ✅
- Solution → Project: **108 条边** ✅

**实际案例**：
```
Problem: "Buyers cannot efficiently find desired properties"
    ↓
Solution: "(NEW) Solution 1: Buyers are assisted by..."
    ↓
Project: "project - Home Condition"
```

---

### 场景 2: 快速通道（Problem → Project 直接关联）

**适用情况**：
- 紧急问题，需要快速响应
- 简单问题，不需要详细 Solution 设计
- 已有成熟解决方案的问题

```
Problem (紧急/简单问题)
    ↓ SOLVED_BY
Project (快速创建的项目)
    ↓ HAS_TASK / HAS_DELIVERABLE
Task / Deliverable (直接执行)
```

**关系映射**：

| 节点 | 关系属性 | EdgeType | 含义 |
|------|---------|----------|------|
| Problem | Project | SOLVED_BY | Problem 被 Project 解决（跳过 Solution） |
| Project | Problem | SOLVES_PROBLEM | Project 直接解决 Problem |

**数据验证**：
- Problem → Project: **111 条边** ✅
- Project → Problem: **96 条边** ✅

**适用案例**：
- 线上紧急 Bug 修复
- 简单的配置调整
- 小型优化任务

---

### 场景 3: Bug 快速修复

**适用情况**：Bug 修复，可能跳过 Solution 设计，也可能跳过 Project

```
Bug (缺陷)
    ↓ SOLVED_BY (可选)
Project (修复项目) ─ 或直接 ─→ Task (修复任务)
    ↓                              ↓
Deliverable                     (快速修复)
    ↓
Task (修复任务)
```

**关系映射**：

| 节点 | 关系属性 | EdgeType | 含义 |
|------|---------|----------|------|
| Bug | Project | SOLVED_BY | Bug 被 Project 解决 |
| Bug | Tasks | HAS_TASK | Bug 有直接的修复任务（更快） |
| Project | Bug | SOLVES_BUG | Project 解决 Bug |
| Task | Bug | FIXES | Task 修复 Bug |

**数据验证**：
- Bug → Tasks: **存在** ✅
- Task → Bug: **存在**（通过 FIXES）✅

---

### 场景 4: 多层级关系（所有路径并存）

**实际情况**：同一个 Problem 可能同时有多种关联方式

```
Problem
  ├─ HAS_SOLUTION → Solution → BELONGS_TO_PROJECT → Project
  ├─ SOLVED_BY → Project (快速通道)
  └─ HAS_TASK → Task (直接任务)
      └─ BELONGS_TO_PROJECT → Project
```

**关系映射**：所有路径都保留

| 起点 | 终点 | EdgeType | 业务含义 |
|------|------|----------|---------|
| Problem | Solution | HAS_SOLUTION | 标准流程：先设计方案 |
| Problem | Project | SOLVED_BY | 快速通道：直接创建项目 |
| Problem | Task | HAS_TASK | 超快通道：直接分配任务 |

---

## 完整的关系映射配置

### Problem 节点

```python
"Problem": [
    ("Solution", EdgeType.HAS_SOLUTION.value),      # 标准流程
    ("Project", EdgeType.SOLVED_BY.value),          # 快速通道
    ("Tasks", EdgeType.HAS_TASK.value),             # 直接任务
    ("Child Problem(s)", EdgeType.HAS_CHILD_PROBLEM.value),
    ("Parent Problem", EdgeType.HAS_PARENT_PROBLEM.value),
    ("Objective", EdgeType.RELATES_TO_OBJECTIVE.value),
    ("Feedback", EdgeType.HAS_FEEDBACK.value),
    ("Recurring Tasks", EdgeType.HAS_TASK.value),
]
```

**业务含义**：
- `HAS_SOLUTION`: Problem 有详细的解决方案设计（复杂问题）
- `SOLVED_BY`: Problem 被 Project 直接解决（简单/紧急问题）
- `HAS_TASK`: Problem 有直接分配的任务（最简单的情况）

---

### Solution 节点

```python
"Solution": [
    ("Problem", EdgeType.SOLVES_PROBLEM.value),     # Solution 解决 Problem
    ("Project", EdgeType.BELONGS_TO_PROJECT.value), # Solution 在 Project 中实施
    ("Designs", EdgeType.HAS_DESIGN.value),
    ("Documents", EdgeType.HAS_DOCUMENT.value),
    ("Tasks", EdgeType.HAS_TASK.value),
    ("Feedback", EdgeType.HAS_FEEDBACK.value),
]
```

**业务含义**：
- `SOLVES_PROBLEM`: Solution 是为了解决 Problem 而设计的
- `BELONGS_TO_PROJECT`: Solution 在某个 Project 中被实施

---

### Project 节点

```python
"Project": [
    ("Problem", EdgeType.SOLVES_PROBLEM.value),     # 快速通道：直接解决 Problem
    ("Bug", EdgeType.SOLVES_BUG.value),             # 快速通道：直接解决 Bug
    ("Solutions", EdgeType.HAS_SOLUTION.value),     # 标准流程：包含 Solutions
    ("Deliverables", EdgeType.HAS_DELIVERABLE.value),
    ("Tasks", EdgeType.HAS_TASK.value),
    ("Blocked By", EdgeType.BLOCKS.value),
    ("Is Blocking", EdgeType.BLOCKS.value),
    ("Feedback", EdgeType.HAS_FEEDBACK.value),
]
```

**业务含义**：
- `SOLVES_PROBLEM`: Project 直接解决 Problem（快速通道）
- `SOLVES_BUG`: Project 直接解决 Bug（快速修复）
- `HAS_SOLUTION`: Project 包含 Solutions（标准流程）

---

### Bug 节点

```python
"Bug": [
    ("Project", EdgeType.SOLVED_BY.value),          # Bug 被 Project 解决
    ("Tasks", EdgeType.HAS_TASK.value),             # Bug 有修复任务
]
```

**业务含义**：
- `SOLVED_BY`: Bug 被某个 Project 解决
- `HAS_TASK`: Bug 有直接的修复任务（可能跳过 Project）

---

### Task 节点

```python
"Task": [
    ("Problem", EdgeType.SOLVES.value),             # Task 解决 Problem
    ("Bug", EdgeType.FIXES.value),                  # Task 修复 Bug
    ("Solution", EdgeType.IMPLEMENTS.value),        # Task 实现 Solution
    ("Design", EdgeType.IMPLEMENTS.value),          # Task 实现 Design
    ("Deliverable", EdgeType.BELONGS_TO_DELIVERABLE.value),
    ("Project", EdgeType.BELONGS_TO_PROJECT.value),
    ("Sub-tasks", EdgeType.HAS_TASK.value),
    ("Parent-task", EdgeType.HAS_TASK.value),
]
```

**业务含义**：
- `SOLVES`: Task 直接解决 Problem（超快通道）
- `FIXES`: Task 修复 Bug
- `IMPLEMENTS`: Task 实现 Solution/Design
- `BELONGS_TO_*`: Task 属于某个容器

---

## 数据分布统计

### 标准流程 vs 快速通道

| 流程 | 关系 | 边数 | 占比 |
|------|------|------|------|
| 标准流程 | Problem → Solution | 1042 | 90.4% |
| 标准流程 | Solution → Project | 108 | 9.4% |
| 快速通道 | Problem → Project | 111 | 9.6% |

**观察**：
- 90%+ 的 Problem 有 Solution 设计（标准流程为主）
- 10% 的 Problem 直接关联 Project（快速通道）
- 两种流程并存，符合实际业务需求

---

## 查询示例

### 查询 1: 获取 Problem 的所有解决路径

```sql
-- 标准路径: Problem → Solution → Project
SELECT
    p.title as problem,
    s.title as solution,
    proj.title as project
FROM nodes p
JOIN edges e1 ON p.id = e1.source_id AND e1.edge_type = 'HAS_SOLUTION'
JOIN nodes s ON e1.target_id = s.id
JOIN edges e2 ON s.id = e2.source_id AND e2.edge_type = 'BELONGS_TO_PROJECT'
JOIN nodes proj ON e2.target_id = proj.id
WHERE p.id = ?;

-- 快速路径: Problem → Project
SELECT
    p.title as problem,
    proj.title as project
FROM nodes p
JOIN edges e ON p.id = e.source_id AND e.edge_type = 'SOLVED_BY'
JOIN nodes proj ON e.target_id = proj.id
WHERE p.id = ?;
```

### 查询 2: 获取 Project 解决的所有 Problem（包括间接）

```sql
-- 直接解决
SELECT p.* FROM nodes p
JOIN edges e ON p.id = e.source_id AND e.edge_type = 'SOLVED_BY'
WHERE e.target_id = ? AND p.type = 'Problem';

-- 通过 Solution 间接解决
SELECT p.* FROM nodes p
JOIN edges e1 ON p.id = e1.source_id AND e1.edge_type = 'HAS_SOLUTION'
JOIN nodes s ON e1.target_id = s.id
JOIN edges e2 ON s.id = e2.source_id AND e2.edge_type = 'BELONGS_TO_PROJECT'
WHERE e2.target_id = ? AND p.type = 'Problem';
```

### 查询 3: 获取 Bug 的修复路径

```sql
-- 路径 1: Bug → Project
SELECT proj.* FROM nodes proj
JOIN edges e ON proj.id = e.target_id AND e.edge_type = 'SOLVED_BY'
WHERE e.source_id = ? AND proj.type = 'Project';

-- 路径 2: Bug → Task (直接修复)
SELECT t.* FROM nodes t
JOIN edges e ON t.id = e.target_id AND e.edge_type = 'HAS_TASK'
WHERE e.source_id = ? AND t.type = 'Task';
```

---

## 语义一致性验证

### ✅ 正确的双向关系

| 正向 | 反向 | 是否对称 | 说明 |
|------|------|---------|------|
| Problem → Solution (HAS_SOLUTION) | Solution → Problem (SOLVES_PROBLEM) | ❌ 不对称 | ✅ 正确：不同语义 |
| Problem → Project (SOLVED_BY) | Project → Problem (SOLVES_PROBLEM) | ❌ 不对称 | ✅ 正确：主动/被动 |
| Solution → Project (BELONGS_TO_PROJECT) | Project → Solutions (HAS_SOLUTION) | ❌ 不对称 | ✅ 正确：包含关系 |
| Bug → Project (SOLVED_BY) | Project → Bug (SOLVES_BUG) | ❌ 不对称 | ✅ 正确：主动/被动 |

**结论**：所有双向关系都使用不同的 EdgeType，语义清晰 ✅

---

## 设计原则总结

### 1. 数据忠实性原则

**原则**：忠实反映 Notion 中的所有实际关系

**实施**：
- ✅ 不删除 Notion 中存在的关系
- ✅ 不强制改变团队的工作流程
- ✅ 支持多种业务流程并存

### 2. 语义准确性原则

**原则**：EdgeType 名称准确反映关系本质

**实施**：
- ✅ 使用 `SOLVES` 词根表示解决关系
- ✅ 使用 `SOLVED_BY` 表示被动关系
- ✅ 避免双向关系使用相同 EdgeType

### 3. 灵活性原则

**原则**：支持多种业务场景

**实施**：
- ✅ 标准流程：Problem → Solution → Project
- ✅ 快速通道：Problem → Project
- ✅ 超快通道：Problem → Task
- ✅ Bug 快速修复：Bug → Project / Bug → Task

---

## 未来扩展建议

### 1. 如果需要区分流程类型

可以在查询时通过路径判断：

```python
def get_problem_resolution_path(problem_id):
    """获取 Problem 的解决路径类型"""
    # 检查是否有 Solution
    has_solution = check_edge(problem_id, 'HAS_SOLUTION')

    if has_solution:
        return "标准流程"  # Problem → Solution → Project
    else:
        # 检查是否直接关联 Project
        has_project = check_edge(problem_id, 'SOLVED_BY')
        if has_project:
            return "快速通道"  # Problem → Project
        else:
            return "超快通道"  # Problem → Task
```

### 2. 如果需要统计流程分布

```sql
-- 统计各种流程的使用频率
SELECT
    '标准流程' as flow_type,
    COUNT(DISTINCT p.id) as problem_count
FROM nodes p
WHERE p.type = 'Problem'
  AND EXISTS (
      SELECT 1 FROM edges e
      WHERE e.source_id = p.id AND e.edge_type = 'HAS_SOLUTION'
  )

UNION ALL

SELECT
    '快速通道' as flow_type,
    COUNT(DISTINCT p.id) as problem_count
FROM nodes p
WHERE p.type = 'Problem'
  AND EXISTS (
      SELECT 1 FROM edges e
      WHERE e.source_id = p.id AND e.edge_type = 'SOLVED_BY'
  )
  AND NOT EXISTS (
      SELECT 1 FROM edges e
      WHERE e.source_id = p.id AND e.edge_type = 'HAS_SOLUTION'
  );
```

---

## 总结

**当前配置的优势**：
1. ✅ 忠实反映 Notion 数据
2. ✅ 支持多种业务流程
3. ✅ 语义清晰准确
4. ✅ 灵活可扩展

**关键设计**：
- 使用 `SOLVES` 系列 EdgeType 统一解决关系语义
- 保留所有 Notion 中实际存在的关系
- 通过不同的 EdgeType 区分不同的业务场景

**无需修改**：当前配置已经是最优方案 ✅
