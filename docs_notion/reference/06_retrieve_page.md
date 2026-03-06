# Source: https://developers.notion.com/reference/retrieve-a-page

# Retrieve a Page

## Overview
The Retrieve a Page endpoint fetches a Page object using a specified page ID. It returns page properties rather than content; use the Retrieve Block Children endpoint for actual page content.

## Key Limitations
**Property References Cap:** This endpoint will not accurately return properties that exceed 25 references. For properties with more than 25 references, use the Retrieve a Page Property endpoint instead.

Properties affected by the 25-reference limit include:
- **People**: Cannot guarantee returning more than 25 people
- **Relations**: Returns `has_more: true` if exceeding 25 related pages
- **Rich Text**: Maximum 25 inline page or person mentions
- **Title**: Maximum 25 inline page or person mentions

## Endpoint Details

**HTTP Method:** GET
**URL:** `https://api.notion.com/v1/pages/{page_id}`

### Required Headers
- `Notion-Version: 2025-09-03` (latest API version)
- `Authorization: Bearer [NOTION_API_KEY]`

### Path Parameters
- `page_id` (string, UUID format): The identifier of the page to retrieve

### Query Parameters
- `filter_properties` (array of strings, max 100 items): Filter specific property IDs in the response. Properties not present on the page won't appear in results.

## Response Format

The endpoint returns either:
1. **partialPageObjectResponse** - Minimal response with object type and ID
2. **pageObjectResponse** - Complete response including:
   - `object`: Always "page"
   - `id`: Page UUID
   - `created_time` / `last_edited_time`: ISO 8601 timestamps
   - `archived` / `in_trash` / `is_locked`: Boolean flags
   - `url`: Notion page URL
   - `public_url`: Published web URL (nullable)
   - `parent`: Parent object (database, data source, page, block, or workspace)
   - `properties`: Page property values (conforms to database schema if page is in database)
   - `icon`: Page emoji, file, external URL, or custom emoji (nullable)
   - `cover`: File or external URL cover image (nullable)
   - `created_by` / `last_edited_by`: Partial user objects

## Property Value Types Supported

### Simple Properties
- Number, URL, Select, Multi-select, Status, Date, Email, Phone Number
- Checkbox, Files, Created By, Created Time, Last Edited By, Last Edited Time
- Formula (boolean, date, number, string variants), Button, Unique ID
- Verification (unverified/verified/expired states), Place (coordinates + address)

### Array-Based Properties
- **Title**: Array of rich text items (max 100)
- **Rich Text**: Array of rich text items (max 100)
- **People**: Array of user objects or groups (max 100)
- **Relations**: Array of related page IDs with `has_more` flag (max 100)

### Rollup Properties
Support functions including: count, sum, average, median, min, max, percent_checked, earliest_date, latest_date, and 20+ others.

## Rich Text Object Types
- **Text**: Content with optional inline links
- **Mention**: User, date, link preview, link mention, page, database, template mention, or custom emoji
- **Equation**: LaTeX expressions (KaTeX compatible)

Each rich text item includes annotations (bold, italic, strikethrough, underline, code, color) and `href` for links.

## Error Responses

| Status | Code | Meaning |
|--------|------|---------|
| 400 | invalid_json, invalid_request, validation_error | Malformed request |
| 401 | unauthorized | Missing/invalid authentication |
| 403 | restricted_resource | Lacks read content capabilities |
| 404 | object_not_found | Page doesn't exist or inaccessible |
| 429 | rate_limited | Request rate exceeded |
| 500 | internal_server_error | Server error |
| 503 | service_unavailable | Service temporarily unavailable |

## Code Example

```javascript
import { Client } from "@notionhq/client"

const notion = new Client({ auth: process.env.NOTION_API_KEY })

const response = await notion.pages.retrieve({
  page_id: "b55c9c91-384d-452b-81db-d1ef79372b75"
})
```

## Integration Requirements
This endpoint requires an integration to have read content capabilities. Calls without proper permissions return HTTP 403.

## Parent Object Behavior
If the page's parent is a database, property values follow database property schemas. Non-database pages only return a `title` property value.
