# Source: https://developers.notion.com/reference/block

# Notion Block Object

## Overview
The Notion Block API enables developers to interact with block objects -- fundamental content units within Notion pages. A block object represents a piece of content within Notion, including headings, paragraphs, lists, media, and more.

## Core Block Structure

Every block contains essential metadata:
- **object**: Always "block"
- **id**: UUIDv4 identifier
- **type**: Specifies the block category (paragraph, heading_1, image, etc.)
- **parent**: References the containing page or block
- **created_time/last_edited_time**: ISO 8601 timestamps
- **created_by/last_edited_by**: User attribution
- **has_children**: Boolean indicating nested blocks
- **in_trash**: Deletion status (replaces deprecated "archived")

## Supported Block Types

The API supports 28+ block types, organized by functionality:

**Text Blocks**: paragraph, heading_1/2/3, bulleted_list_item, numbered_list_item, quote, callout, toggle, to_do

**Media Blocks**: image, audio, video, file, pdf, embed, bookmark, link_preview

**Structural**: table, table_row, column_list, column, divider, breadcrumb

**Special**: code, equation, synced_block, child_page, child_database, template, table_of_contents, transcription

Unsupported blocks appear with type "unsupported" and include a "block_type" field identifying the underlying type.

## Child Block Support

Certain blocks support nested children: paragraphs, lists, headings (when toggleable), callouts, quotes, to-dos, tables, templates, synced blocks, and toggles.

## Rich Text Integration

Many blocks utilize rich_text arrays, providing formatted content with annotations (bold, italic, strikethrough, code, color) and convenient plain_text extraction.

## Key Constraints

- Table width is immutable post-creation
- Synced block content updates aren't supported
- Template block creation deprecated as of March 2023
- Transcription blocks are read-only

## API Access

Retrieve block children via the dedicated endpoint; type-specific information appears in objects matching each block's type property.
