# Notion 节点属性分析文档

本文档自动生成，包含所有节点类型的完整属性分析。

生成时间: 2025-12-31T12:37:18.324322

---

## 目录

1. [Bug](#bug) (1011 个节点)
2. [Deliverable](#deliverable) (239 个节点)
3. [Design](#design) (134 个节点)
4. [Document](#document) (661 个节点)
5. [Problem](#problem) (1974 个节点)
6. [Project](#project) (161 个节点)
7. [Solution](#solution) (1385 个节点)
8. [Task](#task) (722 个节点)

---

## Bug

**节点数量**: 1011

### BUTTON 属性

#### `Add Project`

- **类型**: Button (按钮)
- **说明**: 这是一个交互按钮，不存储数据


### DATE 属性

#### `Created Date`

- **类型**: Date (日期)
- **样本值**: 2025-12-04 ~ 无结束日期


### EMAIL 属性

#### `Contact email`

- **类型**: Email (邮箱)
- **样本值**: liweizhao@housesigma.com


### FILES 属性

#### `Screenshot / Screen recording of the bug`

- **类型**: Files (文件)
- **样本数据**: 0 个文件


### MULTI_SELECT 属性

#### `Affected service`

- **类型**: Multi-select (多选)
- **样本值**: `Other`


### PEOPLE 属性

#### `Owner`

- **类型**: People (关联到用户)
- **样本数据**: 1 个用户
- **示例**: 李维钊(Liweizhao) (`255d872b-594...`)

#### `Reported By`

- **类型**: People (关联到用户)
- **样本数据**: 1 个用户
- **示例**: 李维钊(Liweizhao) (`255d872b-594...`)


### RELATION 属性

#### `Project`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `Tasks`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 1 个关联
- **示例 ID**: `2bfc2345-ab46-80dc-8408-dd3316c2c7bf`
- **覆盖率**: 1/100 (1.0%) 的节点有数据


### RICH_TEXT 属性

#### `AI summary`

- **类型**: Rich Text (富文本)
- **样本内容**: 多个 dw_main_daily 触发器因使用 DROP 语句而失败，导致数据仓库管道受影响。建议在 trigger_dim_community 中用 TRUNCATE 替换 DROP，以避免依赖关系...

#### `Actual result`

- **类型**: Rich Text (富文本)
- **样本内容**: dw_main_daily fails. The listed triggers do not run successfully due to DROP-based clearing causing ...

#### `Clickup ID`

- **类型**: Rich Text (富文本)

#### `Description of the bug`

- **类型**: Rich Text (富文本)
- **样本内容**: Multiple triggers related to dw_main_daily fail to run and need code fixes to restore normal executi...

#### `Expected result`

- **类型**: Rich Text (富文本)
- **样本内容**: dw_main_daily completes successfully and all listed triggers run as expected. When clearing data tab...

#### `Steps to reproduce`

- **类型**: Rich Text (富文本)
- **样本内容**: 1) Trigger or manually run dw_main_daily
2) Observe execution results and logs for the triggers abov...


### SELECT 属性

#### `Severity`

- **类型**: Select (单选)
- **样本值**: `P3 - Medium` (颜色: default)


### STATUS 属性

#### `Status`

- **类型**: Status (状态)
- **样本值**: `Done` (颜色: green)


### TITLE 属性

#### `Title`

- **类型**: Title (标题)
- **样本值**: dw_main_daily trigger failures: trigger_dim_community should use TRUNCATE instead of DROP


### UNIQUE_ID 属性

#### `ID`

- **类型**: Unique ID (唯一标识)
- **样本值**: `BUG1192`


---

## Deliverable

**节点数量**: 239

### DATE 属性

#### `Due Date`

- **类型**: Date (日期)


### PEOPLE 属性

#### `Assignee`

- **类型**: People (关联到用户)
- **样本数据**: 0 个用户


### RELATION 属性

#### `Project`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 92/100 (92.0%) 的节点有数据

#### `Tasks`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 9/100 (9.0%) 的节点有数据


### STATUS 属性

#### `Status`

- **类型**: Status (状态)
- **样本值**: `Not started` (颜色: default)


### TITLE 属性

#### `Name`

- **类型**: Title (标题)


### UNIQUE_ID 属性

#### `ID`

- **类型**: Unique ID (唯一标识)
- **样本值**: `DEL5`


---

## Design

**节点数量**: 134

### DATE 属性

#### `Created Date`

- **类型**: Date (日期)
- **样本值**: 2024-09-25 ~ 无结束日期


### FORMULA 属性

#### `Clickup Link`

- **类型**: Formula (公式)
- **样本值**: {'type': 'string', 'string': None}


### PEOPLE 属性

#### `Approved by`

- **类型**: People (关联到用户)
- **样本数据**: 0 个用户

#### `Owner`

- **类型**: People (关联到用户)
- **样本数据**: 0 个用户


### RELATION 属性

#### `Solution`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 1 个关联
- **示例 ID**: `26cc2345-ab46-819a-a22e-d4ab8cfc589f`
- **覆盖率**: 65/100 (65.0%) 的节点有数据

#### `Tasks`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 3/100 (3.0%) 的节点有数据


### RICH_TEXT 属性

#### `AI summary`

- **类型**: Rich Text (富文本)

#### `Clickup ID`

- **类型**: Rich Text (富文本)
- **样本内容**: 86durfj7d


### SELECT 属性

#### `Type`

- **类型**: Select (单选)
- **样本值**: `UI/UX` (颜色: orange)


### STATUS 属性

#### `status`

- **类型**: Status (状态)
- **样本值**: `Not started` (颜色: default)


### TITLE 属性

#### `Title`

- **类型**: Title (标题)
- **样本值**: User Interaction & Design


### UNIQUE_ID 属性

#### `ID`

- **类型**: Unique ID (唯一标识)
- **样本值**: `DESIGN66`


---

## Document

**节点数量**: 661

### CREATED_BY 属性

#### `Created By`

- **类型**: created_by
- **原始数据**: ```json
{
  "id": "%3Brx%3D",
  "type": "created_by",
  "created_by": {
    "object": "user",
    "id": "e26d499e-8e13-4d9a-a0c4-f9191415ee52",
    "name": "Clickup Importer",
    "avatar_url": null,
    "type": "bot",
    "bot": {}
  }
}
```


### DATE 属性

#### `Created Date`

- **类型**: Date (日期)
- **样本值**: 2024-09-09 ~ 无结束日期


### FORMULA 属性

#### `Clickup Link`

- **类型**: Formula (公式)
- **样本值**: {'type': 'string', 'string': 'https://app.clickup.com/t/14220837/86duke097'}


### LAST_EDITED_TIME 属性

#### `Last edited time`

- **类型**: last_edited_time
- **原始数据**: ```json
{
  "id": "AHSO",
  "type": "last_edited_time",
  "last_edited_time": "2025-10-02T23:24:00.000Z"
}
```


### MULTI_SELECT 属性

#### `Type`

- **类型**: Multi-select (多选)
- **样本值**: `Post Mortem`


### PEOPLE 属性

#### `Maintained By`

- **类型**: People (关联到用户)
- **样本数据**: 0 个用户


### RELATION 属性

#### `Solution`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 1 个关联
- **示例 ID**: `26cc2345-ab46-81e8-bf17-e88acc34369b`
- **覆盖率**: 19/100 (19.0%) 的节点有数据


### RICH_TEXT 属性

#### `AI summary`

- **类型**: Rich Text (富文本)

#### `Clickup ID`

- **类型**: Rich Text (富文本)
- **样本内容**: 86duke097

#### `Clickup List Name`

- **类型**: Rich Text (富文本)

#### `Clickup Parent ID`

- **类型**: Rich Text (富文本)

#### `Clickup Parent Page`

- **类型**: Rich Text (富文本)


### TITLE 属性

#### `Title`

- **类型**: Title (标题)
- **样本值**: post mortem


### UNIQUE_ID 属性

#### `ID`

- **类型**: Unique ID (唯一标识)
- **样本值**: `DOC19`


---

## Problem

**节点数量**: 1974

### BUTTON 属性

#### `Add Child Problem`

- **类型**: Button (按钮)
- **说明**: 这是一个交互按钮，不存储数据

#### `Add Phase`

- **类型**: Button (按钮)
- **说明**: 这是一个交互按钮，不存储数据

#### `Add Project`

- **类型**: Button (按钮)
- **说明**: 这是一个交互按钮，不存储数据

#### `Add Solution`

- **类型**: Button (按钮)
- **说明**: 这是一个交互按钮，不存储数据

#### `Find Parent`

- **类型**: Button (按钮)
- **说明**: 这是一个交互按钮，不存储数据


### CREATED_BY 属性

#### `Created By`

- **类型**: created_by
- **原始数据**: ```json
{
  "id": "NOR%40",
  "type": "created_by",
  "created_by": {
    "object": "user",
    "id": "e26d499e-8e13-4d9a-a0c4-f9191415ee52",
    "name": "Clickup Importer",
    "avatar_url": null,
    "type": "bot",
    "bot": {}
  }
}
```


### CREATED_TIME 属性

#### `Created time`

- **类型**: created_time
- **原始数据**: ```json
{
  "id": "SDFj",
  "type": "created_time",
  "created_time": "2025-09-10T21:31:00.000Z"
}
```


### DATE 属性

#### `Clickup Created Date`

- **类型**: Date (日期)
- **样本值**: 2025-08-22 ~ 无结束日期


### FORMULA 属性

#### `Clickup Link`

- **类型**: Formula (公式)
- **样本值**: {'type': 'string', 'string': None}

#### `Completion`

- **类型**: Formula (公式)
- **样本值**: {'type': 'string', 'string': 'No Project/tasks found'}

#### `Index`

- **类型**: Formula (公式)
- **样本值**: {'type': 'string', 'string': ''}

#### `Solution Count`

- **类型**: Formula (公式)
- **样本值**: {'type': 'number', 'number': 0}

#### `UUID`

- **类型**: Formula (公式)
- **样本值**: {'type': 'string', 'string': '26ac2345ab4681259540e54b4fc35159'}


### LAST_EDITED_TIME 属性

#### `Last edited time`

- **类型**: last_edited_time
- **原始数据**: ```json
{
  "id": "hNy%3C",
  "type": "last_edited_time",
  "last_edited_time": "2025-10-01T09:36:00.000Z"
}
```


### MULTI_SELECT 属性

#### `Meetings`

- **类型**: Multi-select (多选)


### NUMBER 属性

#### `Impact`

- **类型**: Number (数字)
- **样本值**: None


### PEOPLE 属性

#### `Owner`

- **类型**: People (关联到用户)
- **样本数据**: 0 个用户


### RELATION 属性

#### `Child Problem(s)`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `Feedback`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `Objective`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `Parent Problem`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 1/100 (1.0%) 的节点有数据

#### `Project`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `Recurring Tasks`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `Solution`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 5/100 (5.0%) 的节点有数据

#### `Tasks`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据


### RICH_TEXT 属性

#### `AI summary`

- **类型**: Rich Text (富文本)
- **样本内容**: Users face challenges viewing recommended listings due to a horizontal scroll that only shows 10 ite...

#### `Clickup ID`

- **类型**: Rich Text (富文本)
- **样本内容**: 86dxjveta


### ROLLUP 属性

#### `Clickup_scheduling_tag`

- **类型**: rollup
- **原始数据**: ```json
{
  "id": "tSwF",
  "type": "rollup",
  "rollup": {
    "type": "array",
    "array": [],
    "function": "show_original"
  }
}
```

#### `Effort (from solution)`

- **类型**: rollup
- **原始数据**: ```json
{
  "id": "trAG",
  "type": "rollup",
  "rollup": {
    "type": "array",
    "array": [],
    "function": "show_original"
  }
}
```


### SELECT 属性

#### `Scope`

- **类型**: Select (单选)
- **样本值**: `whole` (颜色: blue)


### STATUS 属性

#### `Status`

- **类型**: Status (状态)
- **样本值**: `1-Not started` (颜色: gray)


### TITLE 属性

#### `Title`

- **类型**: Title (标题)
- **样本值**: Recommended Listings Display Limited by Horizontal Scroll and 10-Item Initial View


### UNIQUE_ID 属性

#### `ID`

- **类型**: Unique ID (唯一标识)
- **样本值**: `PLAN640`


---

## Project

**节点数量**: 161

### BUTTON 属性

#### `Add Solution`

- **类型**: Button (按钮)
- **说明**: 这是一个交互按钮，不存储数据

#### `Sign off project?`

- **类型**: Button (按钮)
- **说明**: 这是一个交互按钮，不存储数据


### CREATED_TIME 属性

#### `Created time`

- **类型**: created_time
- **原始数据**: ```json
{
  "id": "b%5ESK",
  "type": "created_time",
  "created_time": "2025-09-24T15:11:00.000Z"
}
```


### DATE 属性

#### `Dates`

- **类型**: Date (日期)
- **样本值**: 2025-09-30 ~ 2025-11-26


### MULTI_SELECT 属性

#### `Requires`

- **类型**: Multi-select (多选)


### PEOPLE 属性

#### ` Requirement sign-off `

- **类型**: People (关联到用户)
- **样本数据**: 1 个用户
- **示例**: Joseph Zeng (`ce53c3c3-11c...`)

#### `Owner`

- **类型**: People (关联到用户)
- **样本数据**: 1 个用户
- **示例**: Joseph Zeng (`ce53c3c3-11c...`)

#### `Product Release sign-off `

- **类型**: People (关联到用户)
- **样本数据**: 1 个用户
- **示例**: Joseph Zeng (`ce53c3c3-11c...`)

#### `Project Manager`

- **类型**: People (关联到用户)
- **样本数据**: 1 个用户
- **示例**: Joseph Zeng (`ce53c3c3-11c...`)

#### `Resources`

- **类型**: People (关联到用户)
- **样本数据**: 3 个用户
- **示例**: Joseph Zeng (`ce53c3c3-11c...`)

#### `Solution sign-off`

- **类型**: People (关联到用户)
- **样本数据**: 1 个用户
- **示例**: Joseph Zeng (`ce53c3c3-11c...`)


### RELATION 属性

#### `Blocked By`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `Bug`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 1/100 (1.0%) 的节点有数据

#### `Deliverables`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 31/100 (31.0%) 的节点有数据

#### `Feedback`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `Is Blocking`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `People`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 13/100 (13.0%) 的节点有数据

#### `Problem`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 1 个关联
- **示例 ID**: `278c2345-ab46-80ac-b31a-eeb7ee95465c`
- **覆盖率**: 69/100 (69.0%) 的节点有数据

#### `Solutions`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 1 个关联
- **示例 ID**: `278c2345-ab46-804f-967b-d564cb6d5fdd`
- **覆盖率**: 60/100 (60.0%) 的节点有数据

#### `Tasks`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 22 个关联
- **示例 ID**: `278c2345-ab46-8000-af74-dc8a084e7b6a`
- **覆盖率**: 64/100 (64.0%) 的节点有数据


### RICH_TEXT 属性

#### `Summary`

- **类型**: Rich Text (富文本)
- **样本内容**: Migration planning for the product space from Clickup to Notion, with Joseph Zeng as the owner and p...


### ROLLUP 属性

#### `Completion`

- **类型**: rollup
- **原始数据**: ```json
{
  "id": "notion%3A%2F%2Fprojects%2Fcompletion_rollup",
  "type": "rollup",
  "rollup": {
    "type": "number",
    "number": 1,
    "function": "percent_per_group"
  }
}
```

#### `Impact (from problem)`

- **类型**: rollup
- **原始数据**: ```json
{
  "id": "WmR%3E",
  "type": "rollup",
  "rollup": {
    "type": "array",
    "array": [
      {
        "type": "number",
        "number": 10
      }
    ],
    "function": "show_original"
  }
}
```

#### `Objective (From Problem)`

- **类型**: rollup
- **原始数据**: ```json
{
  "id": "fvss",
  "type": "rollup",
  "rollup": {
    "type": "array",
    "array": [
      {
        "type": "relation",
        "relation": []
      }
    ],
    "function": "show_original"
  }
}
```


### STATUS 属性

#### `Status`

- **类型**: Status (状态)
- **样本值**: `Done` (颜色: green)


### TITLE 属性

#### `Project name`

- **类型**: Title (标题)
- **样本值**: PLAN-2066 - Notion Migration - Product & AOR space only


### UNIQUE_ID 属性

#### `ID`

- **类型**: Unique ID (唯一标识)
- **样本值**: `PROJ4`


---

## Solution

**节点数量**: 1385

### BUTTON 属性

#### `Add Design`

- **类型**: Button (按钮)
- **说明**: 这是一个交互按钮，不存储数据

#### `Add Project`

- **类型**: Button (按钮)
- **说明**: 这是一个交互按钮，不存储数据


### DATE 属性

#### `Created Date`

- **类型**: Date (日期)


### FORMULA 属性

#### `Clickup Link`

- **类型**: Formula (公式)
- **样本值**: {'type': 'string', 'string': ''}


### LAST_EDITED_TIME 属性

#### `Last edited time`

- **类型**: last_edited_time
- **原始数据**: ```json
{
  "id": "Zev%5D",
  "type": "last_edited_time",
  "last_edited_time": "2025-09-08T21:35:00.000Z"
}
```


### MULTI_SELECT 属性

#### `Meetings`

- **类型**: Multi-select (多选)

#### `Requires`

- **类型**: Multi-select (多选)


### NUMBER 属性

#### `Effort`

- **类型**: Number (数字)
- **样本值**: 3


### PEOPLE 属性

#### `Owner`

- **类型**: People (关联到用户)
- **样本数据**: 0 个用户

#### `approved_by`

- **类型**: People (关联到用户)
- **样本数据**: 0 个用户


### RELATION 属性

#### `Designs`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 1/100 (1.0%) 的节点有数据

#### `Documents`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `Feedback`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `Problem`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 82/100 (82.0%) 的节点有数据

#### `Project`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 1/100 (1.0%) 的节点有数据

#### `Tasks`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据


### RICH_TEXT 属性

#### `AI summary`

- **类型**: Rich Text (富文本)

#### `Clickup ID`

- **类型**: Rich Text (富文本)


### ROLLUP 属性

#### `Impact (from problem)`

- **类型**: rollup
- **原始数据**: ```json
{
  "id": "Ufiy",
  "type": "rollup",
  "rollup": {
    "type": "array",
    "array": [],
    "function": "show_original"
  }
}
```


### SELECT 属性

#### `Clickup Y-Q-M`

- **类型**: Select (单选)

#### `Scope`

- **类型**: Select (单选)


### STATUS 属性

#### `Status`

- **类型**: Status (状态)
- **样本值**: `Not started` (颜色: default)

#### `Status_old`

- **类型**: Status (状态)
- **样本值**: `1 - open` (颜色: default)


### TITLE 属性

#### `Title`

- **类型**: Title (标题)
- **样本值**: (SAMPLE) Tech Feasibility sign off requested


### UNIQUE_ID 属性

#### `ID`

- **类型**: Unique ID (唯一标识)
- **样本值**: `SOL2`


---

## Task

**节点数量**: 722

### DATE 属性

#### `Completed on`

- **类型**: Date (日期)

#### `Created Date`

- **类型**: Date (日期)

#### `Due`

- **类型**: Date (日期)


### FORMULA 属性

#### `Delay`

- **类型**: Formula (公式)
- **样本值**: {'type': 'string', 'string': None}


### PEOPLE 属性

#### `Assignee`

- **类型**: People (关联到用户)
- **样本数据**: 0 个用户


### RELATION 属性

#### `Bug`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 0/100 (0.0%) 的节点有数据

#### `Deliverable`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 1/100 (1.0%) 的节点有数据

#### `Design`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 1/100 (1.0%) 的节点有数据

#### `Parent-task`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 2/100 (2.0%) 的节点有数据

#### `Problem`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 4/100 (4.0%) 的节点有数据

#### `Project`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 1 个关联
- **示例 ID**: `278c2345-ab46-81fc-9e26-d5571d9cbe60`
- **覆盖率**: 30/100 (30.0%) 的节点有数据

#### `Solution`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 1/100 (1.0%) 的节点有数据

#### `Sub-tasks`

- **类型**: Relation (关联到其他节点)
- **样本数据**: 0 个关联
- **覆盖率**: 2/100 (2.0%) 的节点有数据


### RICH_TEXT 属性

#### `AI summary`

- **类型**: Rich Text (富文本)

#### `Clickup Assignee`

- **类型**: Rich Text (富文本)

#### `Clickup Blocking`

- **类型**: Rich Text (富文本)

#### `Clickup ID`

- **类型**: Rich Text (富文本)

#### `Clickup List Name`

- **类型**: Rich Text (富文本)

#### `Clickup Parent ID`

- **类型**: Rich Text (富文本)

#### `Clickup Status`

- **类型**: Rich Text (富文本)


### SELECT 属性

#### `Priority`

- **类型**: Select (单选)
- **样本值**: `High` (颜色: red)

#### `Section`

- **类型**: Select (单选)

#### `Type`

- **类型**: Select (单选)


### STATUS 属性

#### `Status`

- **类型**: Status (状态)
- **样本值**: `Done` (颜色: green)


### TITLE 属性

#### `Task name`

- **类型**: Title (标题)
- **样本值**: Create Prioritization Matrix 


### UNIQUE_ID 属性

#### `ID`

- **类型**: Unique ID (唯一标识)
- **样本值**: `TASK21`


---
