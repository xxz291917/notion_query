# Source: https://developers.notion.com/guides/data-apis/working-with-markdown-content

# Working with Markdown Content

## Overview
The Notion API provides three operations for working with page content via enhanced markdown:

- **Create**: `POST /v1/pages` -- Create a page with markdown content (via `markdown` body param)
- **Read**: `GET /v1/pages/:page_id/markdown` -- Retrieve a page's full content as markdown
- **Update**: `PATCH /v1/pages/:page_id/markdown` -- Insert or replace content using markdown

## Supported Block Types
The markdown API handles most Notion elements, including headings, lists, code blocks, tables, and media (images, video, audio, PDF). Unsupported blocks like bookmarks and embeds appear as `<unknown>` tags.

## Creating Pages
Use `POST /v1/pages` with a `markdown` parameter instead of `children`. The request requires actual newline characters (encoded as `\n` in JSON). If `properties.title` is omitted, the first `# h1` heading is extracted as the page title.

## Retrieving Content
The `GET` endpoint returns a response object containing the markdown string, truncation status, and unknown block IDs. An optional `include_transcript` parameter adds meeting note transcripts to the output.

## Updating Pages
Two command variants exist:

- **insert_content**: Adds content after a selection or appends to the end
- **replace_content_range**: Replaces matched content with new markdown

Both use ellipsis-based selection: `"start text...end text"`. The `allow_deleting_content` flag protects child pages by default.

## Access Requirements
All endpoints require corresponding capabilities: `insert_content` for creation, `read_content` for retrieval, and `update_content` for updates. Both public and internal integrations have access to all three operations.
