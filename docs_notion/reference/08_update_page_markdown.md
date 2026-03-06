# Source: https://developers.notion.com/reference/update-page-markdown

# Update Page Content as Markdown

## Overview
The PATCH `/v1/pages/{page_id}/markdown` endpoint allows updating page content using enhanced markdown. Two operation types are supported: inserting new content or replacing existing ranges.

## Operation Types

### Insert Content
Adds new markdown to a page. Use the `after` parameter with ellipsis-based selection ("start text...end text") to insert at a specific location, or omit it to append at the end.

**Required fields:**
- `type`: "insert_content"
- `content`: The markdown to add

### Replace Content Range
Replaces matched content with new markdown. The `content_range` parameter uses the same ellipsis-based selection format.

**Required fields:**
- `type`: "replace_content_range"
- `content`: Replacement markdown
- `content_range`: Selection to replace

**Optional field:**
- `allow_deleting_content`: Set to true to permit deletion of child pages/databases

## Key Requirements

Your integration needs "update content capabilities" on the target page. Access the My integrations dashboard to configure this. Without proper permissions, requests return HTTP 403.

## Important Notes

- JSON requires `\n` escape sequences for newlines; use single quotes in cURL to preserve them
- The interactive API explorer doesn't support multiline input; test with cURL or SDKs
- Synced pages cannot be updated
- The response includes `truncated` and `unknown_block_ids` fields for large pages

## Common Errors

| Code | Scenario |
|------|----------|
| `validation_error` | Selection doesn't match, would delete protected content, or targets non-page blocks |
| `object_not_found` | Page doesn't exist or lacks access |

## Authentication
Bearer token authentication required via `Authorization` header.
