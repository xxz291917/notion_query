# Source: https://developers.notion.com/reference/data-source

# Notion Data Source Object

## Overview
Data sources represent individual tables within a Notion database. Data sources are the individual tables of data that live under a Notion database. Pages function as child items within these sources, and their property values must align with defined property objects.

## Key Architectural Change
As of API version 2025-09-03, Notion separated the database and data source concepts. Previously combined, databases can now contain multiple data sources -- a significant shift from the earlier single data source model.

## Available Operations
The API supports four primary data source management functions:
- Creating additional sources for existing databases
- Updating source attributes and schema
- Retrieving source information
- Querying source data

## Essential Object Fields

| Field | Purpose |
|-------|---------|
| `id` | Unique UUID identifier |
| `properties` | Schema defining available fields |
| `parent` | Reference to parent database |
| `title` | Display name as rich text |
| `created_time` / `last_edited_time` | ISO 8601 timestamps |
| `in_trash` | Current archival status |

Most fields require read content capabilities, except those marked with asterisks, which are accessible to all integrations.

## Important Constraints
Notion recommends keeping schema sizes below 50KB. Oversized schema updates are rejected to preserve database performance.
