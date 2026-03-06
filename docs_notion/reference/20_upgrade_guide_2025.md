# Source: https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03

# Upgrade Guide: API Version 2025-09-03

## Key Changes

The Notion API version `2025-09-03` introduces first-class support for multi-source databases, allowing a single database to contain multiple linked data sources. This is a breaking change requiring code updates.

## Critical Impact

When users add additional data sources to existing databases, integrations using older API versions will encounter failures when:
- Creating pages with the database as parent
- Reading, writing, or querying databases
- Writing relation properties pointing to that database

## Migration Checklist (6 Steps)

### Step 1: Discovery
Retrieve and cache `data_source_id` values using the updated Get Database endpoint. Most API operations that used `database_id` now require a `data_source_id`.

### Step 2: Parent Updates
Switch from `database_id` to `data_source_id` when creating pages or defining relation properties.

### Step 3: Endpoint Migration
Update database operations to use `/v1/data_sources` endpoints:
- Replace "Retrieve Database" with "Retrieve Data Source"
- Update query paths from `/databases/:id/query` to `/data_sources/:id/query`
- Restructure Create/Update operations to separate database-level from data-source-level attributes

### Step 4: Search Results
Modify search filters to use `"data_source"` instead of `"database"` and handle multiple results per database.

### Step 5: SDK Upgrade
Update to TypeScript SDK v5.0.0+ to access dedicated `notion.dataSources.*` methods.

### Step 6: Webhooks
Update webhook subscriptions to version `2025-09-03` and handle new `data_source.*` event types plus the new `parent.data_source_id` field in payloads.

## Backward Compatibility Note

Relation properties now include both `database_id` and `data_source_id` in responses, but the request object must only contain `data_source_id` after upgrading.
