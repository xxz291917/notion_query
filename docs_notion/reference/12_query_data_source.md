# Source: https://developers.notion.com/reference/query-a-data-source

# Query a Data Source

## Overview
The endpoint retrieves a filtered and paginated list of pages within a data source. The response may return fewer results than requested via `page_size`, and includes a `next_cursor` for pagination when applicable.

## Key Concepts

**Databases and Wikis**: Wiki data sources can contain pages or databases as children. For wikis, the API returns child data sources rather than direct database results, facilitating easier subsequent API requests.

## Request Parameters

**Endpoint:** `POST /v1/data_sources/{data_source_id}/query`

**Path Parameter:**
- `data_source_id` (required): UUID of the target data source

**Query Parameters:**
- `filter_properties[]`: Comma-separated property IDs or names to optimize performance

**Request Body:**
- `filter`: Compound or single property/timestamp filters
- `sorts`: Array of sort objects specifying property and direction
- `page_size`: Number of results per request
- `start_cursor`: UUID for pagination continuation
- `archived`: Boolean to include/exclude archived items
- `in_trash`: Boolean to filter trash status
- `result_type`: Optional enum (`page` or `data_source`) for wiki results

## Filtering

Filters mirror Notion UI functionality. Multiple conditions chain via "and" or "or" operators. Supported filter types include: checkbox, select, multi-select, date, people, text-based properties, relations, formulas, rollups, and timestamps.

**Example filter structure:**
```json
{
  "and": [
    { "property": "Done", "checkbox": { "equals": true } },
    { "or": [{ "property": "Tags", "contains": "A" }] }
  ]
}
```

## Sorting

Sorts operate on database properties or timestamps (`created_time`, `last_edited_time`). Earlier sorts take precedence. Order matters when multiple sorts apply.

## Performance Recommendations

- Use `filter_properties` to reduce payload size and API response time
- Apply specific filter conditions to minimize result sets
- Divide oversized databases into smaller segments
- Prune unused complex properties (rollups, relations, formulas)
- Implement webhooks to reduce polling frequency

## Response Format

Returns a list object containing:
- `results`: Array of page or data source objects
- `next_cursor`: Pagination token (null if no more results)
- `has_more`: Boolean indicating additional pages exist

## Error Handling

| Status | Meaning |
|--------|---------|
| 404 | Data source not found or access denied |
| 403 | Missing read content capabilities |
| 400/429 | Request validation or rate limit exceeded |

## Permissions

The integration's parent database must be shared explicitly. Share via database menu -> "Add connections" -> search integration.
