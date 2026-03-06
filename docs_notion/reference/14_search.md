# Source: https://developers.notion.com/reference/post-search

# Search

## Overview
The Notion Search endpoint allows searching all parent or child pages and data sources shared with an integration by title. Without a query parameter, it returns all shared pages or data sources, subject to integration capabilities.

**Endpoint:** `POST /v1/search`

## Key Features

**Search Scope**: Returns all pages or data sources, excluding duplicated linked databases, that have titles that include the `query` param.

**Filtering Options**: Users can limit results to either pages or data sources using the `filter` parameter.

**Pagination Support**: The endpoint supports paginated responses for managing large result sets.

## Request Parameters

- **query** (string, optional): Search term for filtering by title
- **filter** (object, optional): Restrict search to `page` or `data_source` objects
- **sort** (object, optional): Order results by `last_edited_time` in `ascending` or `descending` direction
- **start_cursor** (string, UUID format): Pagination cursor
- **page_size** (number): Results per page
- **Notion-Version** (header, required): API version (`2025-09-03`)

## Response Structure

Successful responses include:
- **type**: Always `page_or_data_source`
- **results**: Array of page or data source objects
- **has_more**: Boolean indicating additional pages exist
- **next_cursor**: Pagination cursor for subsequent requests

## Response Objects

**Pages** include: id, created_time, last_edited_time, archived status, URL, properties, icon, cover, creator, and last editor information.

**Data Sources** include: id, title, description, parent information, database parent, inline status, timestamps, properties schema, icon, cover, and URLs.

## Error Codes

The API returns standard HTTP status codes (400, 401, 403, 404, 409, 429, 500, 503) with error objects containing: code, message, and optional additional_data.

## TypeScript Example

```javascript
const response = await notion.search({
  query: "meeting notes",
  filter: { property: "object", value: "page" },
  sort: { direction: "descending", timestamp: "last_edited_time" }
})
```

## Important Notes

- To search specific data sources, use the Query endpoint instead
- Results respect integration capability limitations
- Bearer token authentication required
