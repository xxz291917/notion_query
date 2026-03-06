# Source: https://developers.notion.com/reference/page-property-values

# Page Property Values

## Core Concepts

Page properties form the foundation of Notion data structures. A page object comprises properties containing metadata about the page. When creating pages via the API, properties are set in the `properties` object body parameter. The retrieval endpoints surface property identifiers, types, and values.

**Key Point:** Pages that live in a data source are easier to query and manage. Non-database pages have only a `title` property available.

## Property Structure

Each property value object includes three primary fields:

- **`id`**: A URL-encoded identifier that remains constant even when property names change
- **`type`**: An enum specifying the property category (checkbox, date, relation, etc.)
- **Type-specific object**: Contains the actual data relevant to that property type

## Supported Property Types

Notion's API supports 24 distinct property types:

**Simple Types:** checkbox, email, number, phone_number, url

**Text Types:** rich_text, title

**Selection Types:** select, multi_select, status

**Date/Time Types:** date, created_time, last_edited_time

**Reference Types:** people, created_by, last_edited_by, relation

**Computed Types:** formula, rollup, unique_id

**File Types:** files

**Special Types:** icon, verification

## Important API Limitations

Several property types have retrieval constraints. The standard page retrieval endpoint returns a maximum of 25 inline page or person references for formula, rich_text, and title properties. For properties exceeding this limit, use the dedicated page property item endpoint.

Relations, rollups, and formula properties benefit from using the Retrieve a page property item endpoint to ensure you get an accurate, up-to-date property value.

## Notable Restrictions

Certain properties are read-only: `created_by`, `created_time`, `last_edited_by`, `last_edited_time`, `rollup`, and `verification` cannot be updated via API. Unique IDs are auto-incrementing and cannot be modified.

The API does not enforce phone number formatting, and commas are invalid in select option values.
