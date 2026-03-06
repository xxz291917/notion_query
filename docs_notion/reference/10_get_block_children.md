# Source: https://developers.notion.com/reference/get-block-children

# Retrieve Block Children

## Overview
The Retrieve Block Children endpoint returns a paginated array of child block objects contained within a specified block. This is essential for accessing page content, which is modeled as blocks in Notion's architecture.

**Endpoint:** `GET /v1/blocks/{block_id}/children`

## Key Characteristics

- Returns only the first level of children for the specified block
- Requires read content capabilities for the integration
- May return fewer results than the specified `page_size`
- Supports cursor-based pagination for iterating through results

## Request Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `block_id` | Path | String (UUID) | Yes | The ID of the block containing children |
| `start_cursor` | Query | String (UUID) | No | Cursor for pagination |
| `page_size` | Query | Number | No | Maximum results per request |
| `Notion-Version` | Header | String | Yes | API version (latest: `2025-09-03`) |

## Response Format

Successful responses (HTTP 200) return an object with this structure:

```json
{
  "type": "block",
  "object": "list",
  "next_cursor": "string or null",
  "has_more": boolean,
  "results": [
    { /* block objects */ }
  ]
}
```

The `results` array contains either partial or complete block object responses representing child blocks.

## Supported Block Types

The endpoint returns various block types including:
- Text blocks (paragraphs, headings, quotes)
- List items (bulleted, numbered)
- Interactive blocks (to-do, toggle, synced blocks)
- Content blocks (code, callout, divider)
- Media blocks (image, video, audio, PDF, file)
- Structural blocks (table, columns, database references)
- Specialized blocks (equation, breadcrumb, transcription)

## Error Responses

| Status | Code | Meaning |
|--------|------|---------|
| 400 | `invalid_request`, `validation_error` | Malformed request |
| 401 | `unauthorized` | Missing/invalid authentication |
| 403 | `restricted_resource` | Integration lacks read permissions |
| 404 | `object_not_found` | Block doesn't exist or inaccessible |
| 429 | `rate_limited` | Request limit exceeded |
| 500/503 | Server errors | Service unavailable |

## Integration Requirements

This endpoint requires integrations to possess "read content capabilities." Without these permissions, requests return HTTP 403 responses.

## Code Example (TypeScript SDK)

```javascript
import { Client } from "@notionhq/client"

const notion = new Client({ auth: process.env.NOTION_API_KEY })

const response = await notion.blocks.children.list({
  block_id: "c02fc1d3-db8b-45c5-a222-27595b15aea7",
  start_cursor: undefined,
  page_size: 50
})
```

## Pagination Details

The response includes `next_cursor` and `has_more` fields enabling cursor-based pagination. When `has_more` is true, use the returned `next_cursor` value in subsequent requests to retrieve additional results.
