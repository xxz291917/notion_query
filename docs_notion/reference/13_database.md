# Source: https://developers.notion.com/reference/database

# Notion Database Object

## Core Concept
A database functions as a container for one or more data sources, which may be displayed inline or as full pages. The schema and rows for each data source remain independent, with database-level permissions managing access.

## Key Structural Changes (September 2025)
The API was restructured so databases now parent data sources, which in turn parent pages. Previously, these concepts were combined. After upgrading to version `2025-09-03`, databases display child `data_sources` as an array but exclude property details.

## Primary Object Fields

| Field | Type | Purpose |
|-------|------|---------|
| `object` | string | Always returns `"database"` |
| `id` | UUID string | Unique database identifier |
| `data_sources` | array | Child data sources with id and name; retrieve full details separately |
| `created_time` / `last_edited_time` | ISO 8601 | Timestamps for creation and modifications |
| `created_by` / `last_edited_by` | Partial User | User attribution objects |
| `title` | Rich text array | Database name as displayed |
| `description` | Rich text array | Database description |
| `icon` / `cover` | File or Emoji object | Visual elements |
| `parent` | object | Parent relationship information |
| `url` | string | Direct Notion database link |
| `is_inline` | boolean | Indicates inline block versus child page display |
| `public_url` | string | Public web URL if published; otherwise null |
| `in_trash` | boolean | Trash status (replaces deprecated `archived` field) |

## Related Resources
Access detailed property schemas through the Data source reference, and explore page structures through the Page documentation.
