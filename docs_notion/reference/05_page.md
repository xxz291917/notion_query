# Source: https://developers.notion.com/reference/page

# Notion Page Object

## Overview
The Page object represents a single Notion page containing property values accessible through the API.

## Key Properties

**Always Available** (marked with *):
- `object`: Always returns `"page"`
- `id`: Unique UUIDv4 identifier

**Metadata Fields**:
- `created_time` and `last_edited_time`: ISO 8601 formatted timestamps
- `created_by` and `last_edited_by`: Partial User objects
- `url`: The Notion page's web address
- `public_url`: Public-facing URL if published; otherwise `null`

**Status & Organization**:
- `in_trash`: Boolean indicating trash status (replaces deprecated `archived` field)
- `icon`: Emoji or file-based icon
- `cover`: File object for page cover images
- `parent`: References parent container (database, page, or workspace)

## Property Structure

The `properties` field behavior depends on parent type:
- For page or workspace parents: only `title` is valid
- For database parents: properties conform to the database schema

Properties marked with an * are available to integrations with any capabilities. Other properties require read content capabilities.

## Content Access

Page content exists as blocks, retrievable via the retrieve block children endpoint and modifiable through append block children operations.
