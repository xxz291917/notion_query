# Source: https://developers.notion.com/reference/retrieve-page-markdown

# Retrieve Page as Markdown

## Overview
The endpoint retrieves full page content as enhanced markdown, rather than using the block-based API. This approach is particularly useful for agentic systems and developer tools.

## Endpoint Details
**GET** `/v1/pages/{page_id}/markdown`

## Key Requirements
Your integration needs "read content capabilities" on the target page. Access the integrations dashboard to configure capability settings. Attempting calls without proper permissions yields a 403 status code.

## Core Functionality

**Response Format:**
The API returns a `page_markdown` object containing:
- `object`: Always "page_markdown"
- `id`: The page or block identifier
- `markdown`: Enhanced markdown rendering of page content
- `truncated`: Boolean indicating content was cut off
- `unknown_block_ids`: Array of block IDs requiring separate fetches

## Handling Unknown Blocks
Unknown blocks appear as `<unknown url="..." alt="..."/>` tags when:
- Pages exceed ~20,000 block limits (truncation)
- Content lacks integration access permissions
- Block types lack markdown support (bookmarks, embeds, link previews)

For truncated or inaccessible blocks, resubmit their IDs as the `page_id` parameter. Unsupported block types require the block-based API instead.

## Query Parameters
- `include_transcript` (boolean): Includes meeting note transcripts when true; defaults to false
- `Notion-Version` (header): Required version header (`2025-09-03`)

## Error Responses
- **404**: Page doesn't exist or integration lacks access
- **400/429**: Request exceeds rate limits
- **403**: Missing content read capabilities
- **401**: Authorization failure

## Code Example
```javascript
const response = await notion.pages.retrieveMarkdown({
  page_id: "b55c9c91-384d-452b-81db-d1ef79372b75"
})
```
