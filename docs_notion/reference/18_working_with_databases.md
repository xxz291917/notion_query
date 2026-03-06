# Source: https://developers.notion.com/guides/data-apis/working-with-databases

# Working with Databases

## Overview
Databases in Notion are collections of pages that can be filtered, sorted, and organized. The API enables integrations to sync databases with external systems and build workflows around them.

## Database Structure
Databases contain data sources, which serve as parents for pages (rows). Each data source has:
- **Properties (Schema)**: Columns defined with specific types
- **Pages**: Individual rows conforming to the schema

**Important Limitation**: Notion's API does not currently support linked data sources.

## Database Properties
Property objects describe columns and include:
- A `type` field (title, number, date, people, etc.)
- Type-specific configuration nested under a matching key

**Maximum Recommendation**: Notion recommends schemas not exceed 50KB to maintain performance.

## Database Parent Structure
When retrieving a database via API, the response includes:
- `object`: "database"
- `id`: Database identifier
- `data_sources`: Array with id and name
- `properties`: Schema definition

## Adding Pages to Databases

**Required Parameters**:
- `parent`: Must specify `data_source_id`
- `properties`: Object with property names/IDs as keys, property value objects as values

**Example Parent Object**:
```json
{
  "type": "data_source_id",
  "data_source_id": "248104cd-477e-80af-bc30-000bd28de8f9"
}
```

**Finding IDs**: Database IDs appear in Notion URLs; data source IDs are retrieved via the Retrieve Database endpoint or the Notion app's "Manage data sources" menu.

## Querying Pages in Data Sources

Use the **Query a data source endpoint** to find pages based on criteria.

### Filtering
Filters support:
- Simple conditions (single property)
- Compound conditions (multiple properties with AND/OR logic)

**Example Date Filter**:
```json
{
  "property": "Last ordered",
  "date": {
    "past_week": {}
  }
}
```

### Sorting
Sort objects order results by properties or timestamps:
```json
{
  "timestamp": "created_time",
  "direction": "descending"
}
```

**Available Timestamps**: `created_time`, `last_edited_time`

## Response Format
Queries return paginated responses with maximum 100 results per request, including `has_more` and `next_cursor` for pagination.

## Special Database Types (Not Supported)
1. **Linked databases**: Show databases in multiple locations
2. **Wiki databases**: Organize child pages with verification capabilities

Both are currently unsupported by the Public API.

## Recommended Workflow
For flexible integrations:
1. Call Retrieve Database endpoint
2. Call Retrieve Data Source endpoint
3. Build property objects programmatically based on returned schema
4. Use those objects to create or update pages
