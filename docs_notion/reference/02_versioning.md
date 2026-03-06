# Source: https://developers.notion.com/reference/versioning

# Notion API Versioning

## Core Concepts

The Notion API employs date-based versioning to manage backwards-incompatible changes. The current version is **2025-09-03**.

### Required Header

All REST API requests must include the `Notion-Version` header.

## Implementation Examples

**cURL Request:**
```bash
curl https://api.notion.com/v1/users/01da9b00-e400-4959-91ce-af55307647e5 \
  -H "Authorization: Bearer secret_t1CdN9S8yicG5eWLUOfhcWaOscVnFXns" \
  -H "Notion-Version: 2025-09-03"
```

**JavaScript SDK:**
The SDK automatically sets the appropriate version header. You can override it by passing `notionVersion` when initializing the Client:
```javascript
const notion = new Client({
  auth: process.env.NOTION_ACCESS_TOKEN,
  notionVersion: "2025-09-03"
});
```

## Version Release Triggers

New versions are released exclusively for backwards-incompatible changes (like property name modifications). New features and endpoints don't trigger version updates — they're available across existing API versions.

## SDK and Compatibility

The JavaScript SDK uses semantic versioning separately from the API. Major SDK versions may drop support for older API versions. For instance, v5.0.0 and above dropped support for `2022-06-28` and earlier.

## Backwards Compatibility

The platform currently maintains indefinite support for older API versions, though future deprecation would include advance notice and migration guidance.
