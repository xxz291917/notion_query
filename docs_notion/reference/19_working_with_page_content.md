# Source: https://developers.notion.com/guides/data-apis/working-with-page-content

# Working with Page Content

## Core Overview
Pages function as containers for user-created content. Page properties are best for capturing structured information such as a due date, a category, or a relationship to another page. In contrast, content represents looser, freeform compositions.

## Block Structure

Content is organized as hierarchical block objects. Each block contains:
- Standard properties: `object`, `type`, `created_time`, `last_edited_time`, `has_children`
- Type-specific properties (e.g., `paragraph`, `to_do`)
- Optional children blocks (when `has_children` is `true`)

Blocks can nest within other blocks, though only certain types support children. Pages themselves are special block types that function as containers.

## Rich Text System

Text content uses rich text objects that combine:
- Content strings with optional hyperlinks
- Annotations (bold, italic, strikethrough, underline, code, color)
- Plain text representation
- Reference URLs

## Creating Pages with Content

The `/pages` POST endpoint accepts three parameters:

**Parent**: Specifies location using page ID format
```json
{"type": "page_id", "page_id": "[UUID]"}
```

**Properties**: Contains the required `title` field with rich text array

**Children**: Array of block objects defining initial content

When creating new blocks, keep in mind that the Notion API has size limits for the content.

## Reading Page Content

The `/blocks/{block_id}/children` GET endpoint retrieves child blocks. Important considerations:
- Returns paginated responses (maximum 100 results)
- Nested blocks require recursive calls when `has_children` is `true`
- Large page retrieval benefits from asynchronous operations

## Appending Content

The `/blocks/{block_id}/children` PATCH endpoint adds blocks to existing pages. The optional `after` parameter positions new blocks following a specific existing block rather than at the end.

## AI Meeting Notes

Transcription blocks contain structured meeting data with pointers to three content sections:
- Summary (`summary_block_id`)
- Notes (`notes_block_id`)
- Transcript (`transcript_block_id`)

Retrieval requires checking the `status` field for "notes_ready" before accessing child blocks.

## Rate Limiting & Permissions

Integrations require explicit access to parent pages through the Notion interface. The documentation recommends using the search API rather than asking users to manually provide page IDs.
