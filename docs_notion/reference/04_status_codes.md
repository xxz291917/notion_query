# Source: https://developers.notion.com/reference/status-codes

# Notion API Status Codes

## Overview
The Notion API employs HTTP status codes to categorize request outcomes. Detailed error information appears in response bodies via `"code"` and `"message"` properties.

## Success Response
**HTTP 200**: Notion successfully processed the request.

## Error Classifications

### Client Errors (4xx)

**400 Bad Request** covers multiple validation issues:
- `invalid_json`: Request body cannot be parsed as JSON
- `invalid_request_url`: Malformed request URL
- `invalid_request`: Unsupported operation
- `invalid_grant`: Authorization credentials are invalid, expired, or revoked
- `validation_error`: Request parameters don't match expected schema
- `missing_version`: Required `Notion-Version` header absent

**401 Unauthorized**: `unauthorized` indicates invalid bearer token

**403 Forbidden**: `restricted_resource` signals insufficient permissions for the given token

**404 Not Found**: `object_not_found` means the resource doesn't exist or wasn't shared with the integration

**409 Conflict**: `conflict_error` occurs during transaction failures or, rarely, when file upload providers experience outages

**429 Too Many Requests**: `rate_limited` indicates exceeding request allowances; consult rate limit documentation for details

### Server Errors (5xx)

**500 Internal Server Error**: Unexpected failures requiring Notion support contact

**502 Bad Gateway**: Upstream connection issues; retry recommended

**503 Service Unavailable**: Can result from response timeouts exceeding 60 seconds or database unavailability (`database_connection_unavailable`)

**504 Gateway Timeout**: Request processing timeout; retry later
