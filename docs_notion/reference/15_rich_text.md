# Source: https://developers.notion.com/reference/rich-text

# Rich Text

## Overview
Notion's rich text feature enables customizable content styling and formatting through object structures returned by block retrieval endpoints. Rich text arrays include plain text access plus comprehensive styling options.

## Core Rich Text Object Structure

A rich text object contains five main properties:

- **type**: Enum value (`"text"`, `"mention"`, or `"equation"`)
- **Type-specific field**: Configuration object matching the type
- **annotations**: Styling metadata object
- **plain_text**: The plain text without annotations
- **href**: Optional URL for links or Notion mentions

## Annotation Styling Properties

The annotations object supports six formatting attributes:

| Property | Purpose |
|----------|---------|
| `bold` | Boolean for weight emphasis |
| `italic` | Boolean for slant styling |
| `strikethrough` | Boolean for line-through effect |
| `underline` | Boolean for underline effect |
| `code` | Boolean for monospace styling |
| `color` | Enum supporting text and background colors (blue, brown, green, orange, pink, purple, red, yellow, gray, plus background variants) |

## Rich Text Type Objects

### Text Type
Includes `content` (the actual text string) and optional `link` object with `url` property for hyperlinks.

### Equation Type
Contains LaTeX expressions via an `expression` field for inline mathematical notation.

### Mention Types
Six subtypes exist:
- Database references
- Date objects
- Link previews
- Page references
- Template mentions (date or user)
- User objects

Mentions are created in the Notion UI when a user types `@` followed by the name of the reference.

## Access & Limitations

Integrations without database or page access receive mentions with just the ID and `plain_text` as `"Untitled"`. User access restrictions show `"@Anonymous"` unless capabilities are updated. Rich text object sizes have documented limits available in the request limits reference.
