# Notion API Endpoints

This document provides details on the Notion API endpoints used for ETL content extraction.

## Base URL

```
https://api.notion.com/v1
```

## Authentication

All requests require authentication via header:
```
Authorization: Bearer secret_your_integration_token_here
Notion-Version: 2025-09-03
Content-Type: application/json
```

## API Structure

Notion follows a flat API structure with object-specific endpoints:
**Integration** → **Search/Discovery** → **Object Retrieval** → **Content Extraction**

- **Integration Token**: Workspace-scoped authentication
- Each endpoint targets specific object types
- Explicit permissions required for each page/database

## Core Endpoints for ETL (by Object Type)

### 1. Integration Information

**Endpoint**: `GET /users/me`
**Description**: Get information about the integration (bot user)

**Example**:
```bash
curl -H "Authorization: Bearer secret_token" \
     -H "Notion-Version: 2025-09-03" \
  "https://api.notion.com/v1/users/me"
```

**Response**:
```json
{
  "object": "user",
  "id": "bot-user-id",
  "name": "ETL Integration",
  "avatar_url": null,
  "type": "bot",
  "bot": {
    "owner": {
      "type": "workspace",
      "workspace": true
    }
  }
}
```

### 2. Content Discovery (Search)

**Endpoint**: `POST /search`
**Description**: Search for pages, databases, and other content accessible to the integration

**Parameters**:
- `query` (string): Text to search for
- `sort` (object): Sort criteria
- `filter` (object): Filter by object type or property
- `start_cursor` (string): Pagination cursor
- `page_size` (number): Results per page (max 100, default 100)

**Example**:
```bash
curl -X POST \
  -H "Authorization: Bearer secret_token" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "value": "page",
      "property": "object"
    },
    "sort": {
      "direction": "descending",
      "timestamp": "last_edited_time"
    }
  }' \
  "https://api.notion.com/v1/search"
```

**Filter Options**:
```json
{
  "filter": {
    "value": "page",        // "page" or "database"
    "property": "object"
  }
}
```

**Time-based Filtering** (for incremental extraction):
```json
{
  "filter": {
    "timestamp": "last_edited_time",
    "last_edited_time": {
      "after": "2025-09-10T00:00:00.000Z"
    }
  }
}
```

### 3. Page Operations

#### Get Page Metadata
**Endpoint**: `GET /pages/{page_id}`
**Description**: Retrieve page properties and metadata (not content)

**Parameters**:
- ~~`filter_properties` (array): Specific properties to retrieve~~ **DEPRECATED**: This parameter causes API validation errors

**Example**:
```bash
curl -H "Authorization: Bearer secret_token" \
     -H "Notion-Version: 2025-09-03" \
  "https://api.notion.com/v1/pages/12345678-abcd-efgh-ijkl-123456789012"
```

#### Get Page Content (via Blocks)
**Endpoint**: `GET /blocks/{block_id}/children`
**Description**: Retrieve page content as block hierarchy

**Parameters**:
- `start_cursor` (string): Pagination cursor
- `page_size` (number): Blocks per page (max 100, default 100)

**Example**:
```bash
curl -H "Authorization: Bearer secret_token" \
     -H "Notion-Version: 2025-09-03" \
  "https://api.notion.com/v1/blocks/12345678-abcd-efgh-ijkl-123456789012/children"
```

#### Create Page
**Endpoint**: `POST /pages`
**Description**: Create a new page

**Example**:
```bash
curl -X POST \
  -H "Authorization: Bearer secret_token" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {
      "type": "page_id",
      "page_id": "parent-page-id"
    },
    "properties": {
      "title": {
        "title": [
          {
            "text": {
              "content": "New Page Title"
            }
          }
        ]
      }
    }
  }' \
  "https://api.notion.com/v1/pages"
```

#### Update Page
**Endpoint**: `PATCH /pages/{page_id}`
**Description**: Update page properties

**Example**:
```bash
curl -X PATCH \
  -H "Authorization: Bearer secret_token" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "title": {
        "title": [
          {
            "text": {
              "content": "Updated Page Title"
            }
          }
        ]
      }
    }
  }' \
  "https://api.notion.com/v1/pages/12345678-abcd-efgh-ijkl-123456789012"
```

#### Archive Page (Remove from Data Source)
**Endpoint**: `PATCH /pages/{page_id}`
**Description**: Archive a page to remove it from data source or restore it

**IMPORTANT**: Notion API does not support DELETE operations on pages. Pages must be archived using PATCH with `archived: true`.

**Parameters**:
- `archived` (boolean): Set to `true` to archive (remove), `false` to restore

**Example**:
```bash
curl -X PATCH \
  -H "Authorization: Bearer secret_token" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "archived": true
  }' \
  "https://api.notion.com/v1/pages/12345678-abcd-efgh-ijkl-123456789012"
```

**Common Mistakes**:
- ❌ `DELETE /pages/{page_id}` - This endpoint does not exist
- ❌ `DELETE /data_sources/{id}/pages/{page_id}` - This endpoint does not exist
- ❌ `PATCH /pages/batch` - Batch operations are not supported
- ✅ `PATCH /pages/{page_id}` with `{"archived": true}` - Correct approach

### 4. Block Operations

#### Get Block Details
**Endpoint**: `GET /blocks/{block_id}`
**Description**: Retrieve specific block information

**Example**:
```bash
curl -H "Authorization: Bearer secret_token" \
     -H "Notion-Version: 2025-09-03" \
  "https://api.notion.com/v1/blocks/block-uuid"
```

#### Append Block Children
**Endpoint**: `PATCH /blocks/{block_id}/children`
**Description**: Add new blocks as children to existing block

**Example**:
```bash
curl -X PATCH \
  -H "Authorization: Bearer secret_token" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [
            {
              "text": {
                "content": "New paragraph content"
              }
            }
          ]
        }
      }
    ]
  }' \
  "https://api.notion.com/v1/blocks/parent-block-id/children"
```

### 5. Data Source Operations

#### Get Database Schema (for Data Source setup)
**Endpoint**: `GET /databases/{database_id}`
**Description**: Retrieve database schema and metadata for data source configuration

**Example**:
```bash
curl -H "Authorization: Bearer secret_token" \
     -H "Notion-Version: 2025-09-03" \
  "https://api.notion.com/v1/databases/database-uuid"
```

#### Query Data Source
**Endpoint**: `POST /data_sources/{data_source_id}/query`
**Description**: Query pages within a specific data source with filtering and sorting

**Parameters**:
- `filter` (object): Filter criteria based on data source properties
- `sorts` (array): Sort specifications
- `start_cursor` (string): Pagination cursor
- `page_size` (number): Results per page (max 100, default 100)
- ~~`filter_properties` (array): Specific properties to retrieve~~ **DEPRECATED**: This parameter causes API validation errors

**Example**:
```bash
curl -X POST \
  -H "Authorization: Bearer secret_token" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "and": [
        {
          "property": "Status",
          "select": {
            "equals": "In Progress"
          }
        },
        {
          "property": "ID",
          "rich_text": {
            "contains": "86dxjgpx6"
          }
        }
      ]
    },
    "sorts": [
      {
        "property": "Created Date",
        "direction": "descending"
      }
    ],
    "page_size": 50
  }' \
  "https://api.notion.com/v1/data_sources/26fc2345-ab46-81ac-a43c-000befe7113e/query"
```

**Response Format**:
```json
{
  "object": "list",
  "results": [
    {
      "object": "page",
      "id": "page-uuid",
      "created_time": "2025-09-15T12:00:00.000Z",
      "last_edited_time": "2025-09-15T12:30:00.000Z",
      "properties": {
        "ID": {
          "id": "property-id",
          "type": "rich_text",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "86dxjgpx6"
              },
              "plain_text": "86dxjgpx6"
            }
          ]
        }
      }
    }
  ],
  "next_cursor": "cursor-string",
  "has_more": true
}
```

### 6. Comment Operations

#### Get Comments
**Endpoint**: `GET /comments`
**Description**: Retrieve comments for a specific page or block

**Parameters**:
- `block_id` (string): Block ID to get comments for
- `start_cursor` (string): Pagination cursor
- `page_size` (number): Comments per page (max 100, default 100)

**Example**:
```bash
curl -H "Authorization: Bearer secret_token" \
     -H "Notion-Version: 2025-09-03" \
  "https://api.notion.com/v1/comments?block_id=page-or-block-uuid"
```

#### Create Comment
**Endpoint**: `POST /comments`
**Description**: Add a comment to a page or block

**Example**:
```bash
curl -X POST \
  -H "Authorization: Bearer secret_token" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {
      "page_id": "page-uuid"
    },
    "rich_text": [
      {
        "text": {
          "content": "This is a comment on the page."
        }
      }
    ]
  }' \
  "https://api.notion.com/v1/comments"
```

### 7. File Upload Operations

#### Upload File
**Endpoint**: `POST /files`
**Description**: Upload a file to Notion and get a reference

**Example**:
```bash
curl -X POST \
  -H "Authorization: Bearer secret_token" \
  -H "Notion-Version: 2025-09-03" \
  -F "file=@/path/to/local/file.pdf" \
  "https://api.notion.com/v1/files"
```

**Response**:
```json
{
  "object": "file",
  "id": "file-upload-uuid",
  "url": "https://prod-files-secure.s3.us-west-2.amazonaws.com/...",
  "expiry_time": "2025-09-11T15:30:00.000Z"
}
```

### 8. User Operations

#### List Users
**Endpoint**: `GET /users`
**Description**: List users in the workspace

**Parameters**:
- `start_cursor` (string): Pagination cursor
- `page_size` (number): Users per page (max 100, default 100)

**Example**:
```bash
curl -H "Authorization: Bearer secret_token" \
     -H "Notion-Version: 2025-09-03" \
  "https://api.notion.com/v1/users"
```

#### Get User
**Endpoint**: `GET /users/{user_id}`
**Description**: Get specific user information

**Example**:
```bash
curl -H "Authorization: Bearer secret_token" \
     -H "Notion-Version: 2025-09-03" \
  "https://api.notion.com/v1/users/user-uuid"
```

## Pagination

All list endpoints support cursor-based pagination:
- Use `start_cursor` parameter for subsequent requests
- Check `has_more` in response to determine if more results exist
- Use `next_cursor` from response as `start_cursor` for next request
- Maximum `page_size` is 100 items

**Pagination Example**:
```python
def get_all_pages(client):
    all_pages = []
    start_cursor = None
    
    while True:
        params = {"page_size": 100}
        if start_cursor:
            params["start_cursor"] = start_cursor
        
        response = client.search(filter={"property": "object", "value": "page"}, **params)
        
        all_pages.extend(response["results"])
        
        if not response["has_more"]:
            break
        
        start_cursor = response["next_cursor"]
    
    return all_pages
```

## Rate Limiting

### Current Limits
- **Average**: 3 requests per second per integration
- **Burst**: Some requests above average allowed temporarily
- **Response**: HTTP 429 when limits exceeded

### Headers to Monitor
```
Retry-After: 2
```

### Best Practices
- Implement exponential backoff for 429 responses
- Respect `Retry-After` header values
- Add delays between requests (333ms for 3/second average)
- Use request queues for batch operations

### Batch Processing Considerations

**Enhanced NotionClient Implementation:**
- Default request delay: 0.1 seconds (reduced for batch operations)
- Comment creation adds additional API calls (1 per comment)
- Page creation with comments: N+1 API calls (1 for page + N for comments)
- Statistics tracking updated inline with each operation

**Rate Limiting for Comments:**
```python
# Comment creation example with proper delays
def create_page_comments(client, page_id, clickup_task):
    """Create comments for migrated page"""
    comments_created = 0

    for comment in clickup_task.get('comments', []):
        try:
            # Create individual comment
            comment_response = client._make_request(
                "POST", "comments", {
                    "parent": {"page_id": page_id},
                    "rich_text": [{
                        "text": {
                            "content": format_comment_content(comment)
                        }
                    }]
                }
            )
            comments_created += 1

            # Rate limiting delay for comment creation
            time.sleep(0.1)  # 10 requests per second max

        except Exception as e:
            print(f"Failed to create comment: {str(e)}")

    return comments_created
```

**Rate Limiting Implementation**:
```python
import time
import requests
from functools import wraps

def rate_limited(requests_per_second=3):
    min_interval = 1.0 / requests_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            
            # Handle rate limiting
            if hasattr(ret, 'status_code') and ret.status_code == 429:
                retry_after = int(ret.headers.get('Retry-After', 2))
                time.sleep(retry_after)
                return func(*args, **kwargs)  # Retry once
            
            return ret
        
        return wrapper
    return decorator

@rate_limited(requests_per_second=3)
def make_request(url, headers, **kwargs):
    return requests.get(url, headers=headers, **kwargs)
```

## Error Handling

### Common HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid request format)
- `401`: Unauthorized (invalid or missing token)
- `403`: Forbidden (integration lacks permission to resource)
- `404`: Not Found (resource doesn't exist)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error
- `502`: Bad Gateway
- `503`: Service Unavailable

### Error Response Format
```json
{
  "object": "error",
  "status": 400,
  "code": "invalid_request",
  "message": "The request body could not be decoded as JSON.",
  "developer_survey": "https://notionup.typeform.com/to/bllBsoI4"
}
```

### Common Error Codes
- `unauthorized`: Invalid authentication token
- `forbidden`: Insufficient permissions
- `object_not_found`: Requested resource not found
- `rate_limited`: Request rate limit exceeded
- `invalid_request`: Malformed request
- `validation_error`: Request validation failed
- `conflict_error`: Resource conflict (e.g., duplicate operation)

## Filter and Sort Examples

### Database Query Filters

#### Text Property Filter
```json
{
  "property": "Name",
  "title": {
    "contains": "Project"
  }
}
```

#### Select Property Filter
```json
{
  "property": "Status",
  "select": {
    "equals": "In Progress"
  }
}
```

#### Date Property Filter
```json
{
  "property": "Due Date",
  "date": {
    "after": "2025-09-01"
  }
}
```

#### People Property Filter
```json
{
  "property": "Assignee",
  "people": {
    "contains": "user-uuid"
  }
}
```

#### Compound Filters
```json
{
  "and": [
    {
      "property": "Status",
      "select": {
        "equals": "In Progress"
      }
    },
    {
      "property": "Due Date",
      "date": {
        "before": "2025-12-31"
      }
    }
  ]
}
```

### Sort Specifications
```json
{
  "sorts": [
    {
      "property": "Due Date",
      "direction": "ascending"
    },
    {
      "property": "Priority",
      "direction": "descending"
    },
    {
      "timestamp": "created_time",
      "direction": "descending"
    }
  ]
}
```

## Python Request Examples

### Basic Setup
```python
import requests
import json
from datetime import datetime

class NotionClient:
    def __init__(self, token, version="2022-06-28"):
        self.token = token
        self.version = version
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": version,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json()
```

### Search Operations
```python
def search_pages(client, query=None, last_edited_after=None):
    """Search for pages with optional filters"""
    payload = {
        "filter": {"property": "object", "value": "page"},
        "sort": {
            "direction": "descending",
            "timestamp": "last_edited_time"
        }
    }
    
    if query:
        payload["query"] = query
    
    if last_edited_after:
        payload["filter"] = {
            "timestamp": "last_edited_time",
            "last_edited_time": {
                "after": last_edited_after.isoformat()
            }
        }
    
    return client._make_request("POST", "search", json=payload)

def search_databases(client):
    """Search for all accessible databases"""
    payload = {
        "filter": {"property": "object", "value": "database"},
        "sort": {
            "direction": "descending", 
            "timestamp": "last_edited_time"
        }
    }
    
    return client._make_request("POST", "search", json=payload)
```

### Content Extraction
```python
def get_page_content(client, page_id):
    """Get page metadata and block content"""
    # Get page properties
    page = client._make_request("GET", f"pages/{page_id}")
    
    # Get page blocks
    blocks = get_all_blocks(client, page_id)
    
    return {
        "page": page,
        "blocks": blocks
    }

def get_all_blocks(client, parent_id):
    """Recursively get all blocks and their children"""
    all_blocks = []
    start_cursor = None
    
    while True:
        params = {"page_size": 100}
        if start_cursor:
            params["start_cursor"] = start_cursor
        
        response = client._make_request(
            "GET", 
            f"blocks/{parent_id}/children",
            params=params
        )
        
        for block in response["results"]:
            all_blocks.append(block)
            
            # Recursively get child blocks
            if block.get("has_children"):
                children = get_all_blocks(client, block["id"])
                block["children"] = children
        
        if not response["has_more"]:
            break
        
        start_cursor = response["next_cursor"]
    
    return all_blocks
```

### Data Source Operations
```python
def query_data_source(client, data_source_id, filter_obj=None, sorts=None):
    """Query data source with optional filtering and sorting

    Note: filter_properties parameter removed as it causes API validation errors
    """
    payload = {}

    if filter_obj:
        payload["filter"] = filter_obj

    if sorts:
        payload["sorts"] = sorts

    # Note: filter_properties parameter deprecated - causes API errors

    all_results = []
    start_cursor = None

    while True:
        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = client._make_request(
            "POST",
            f"data_sources/{data_source_id}/query",
            json=payload
        )

        all_results.extend(response["results"])

        if not response["has_more"]:
            break

        start_cursor = response["next_cursor"]

    return all_results

def find_page_by_property(client, data_source_id, property_name, property_value, property_type="rich_text"):
    """Find pages in data source by specific property value"""
    filter_obj = {
        "property": property_name,
        property_type: {
            "equals": property_value
        }
    }

    results = query_data_source(
        client,
        data_source_id,
        filter_obj=filter_obj
        # Note: filter_properties parameter deprecated - causes API errors
    )

    return results
```

### Page Archival Operations
```python
def archive_page(client, page_id, archive=True):
    """Archive or restore a Notion page

    Args:
        client: Notion client instance
        page_id: Page ID to archive
        archive: True to archive (remove), False to restore

    Returns:
        Response from Notion API
    """
    return client._make_request(
        "PATCH",
        f"pages/{page_id}",
        {
            "archived": archive
        }
    )

def remove_duplicates_from_data_source(client, page_ids):
    """Archive multiple duplicate pages from data source

    Note: Notion API doesn't support batch operations or DELETE endpoints.
    Pages must be archived individually using PATCH requests.

    Args:
        client: Notion client instance
        page_ids: List of page IDs to archive

    Returns:
        Dict with success/failure counts
    """
    archived_count = 0
    failed_count = 0

    for page_id in page_ids:
        try:
            archive_page(client, page_id, archive=True)
            archived_count += 1
            print(f"✅ Archived page {page_id}")

            # Rate limiting - important for API compliance
            time.sleep(0.2)

        except Exception as e:
            failed_count += 1
            print(f"❌ Failed to archive page {page_id}: {str(e)}")

    return {
        "archived": archived_count,
        "failed": failed_count,
        "total": len(page_ids)
    }
```

### Comment Extraction and Creation

#### Get Comments
```python
def get_page_comments(client, page_id):
    """Get all comments for a page"""
    all_comments = []
    start_cursor = None

    while True:
        params = {
            "block_id": page_id,
            "page_size": 100
        }
        if start_cursor:
            params["start_cursor"] = start_cursor

        response = client._make_request("GET", "comments", params=params)

        all_comments.extend(response["results"])

        if not response["has_more"]:
            break

        start_cursor = response["next_cursor"]

    return all_comments
```

#### Create Comment with Migration Context
```python
def create_comment_from_clickup(client, page_id, clickup_comment):
    """Create Notion comment from ClickUp comment with proper formatting"""

    # Format comment with metadata header
    username = clickup_comment.get("user", {}).get("username", "Unknown")
    timestamp_ms = clickup_comment.get("date", "0")

    # Convert timestamp to readable format
    try:
        timestamp = datetime.fromtimestamp(int(timestamp_ms) / 1000)
        date_str = timestamp.strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        date_str = "Unknown Date"

    comment_text = clickup_comment.get("comment_text", "")

    # Format with header
    formatted_content = f"ClickUp Comment by {username} on {date_str}:\n\n{comment_text}"

    # Create comment via API
    comment_data = {
        "parent": {"page_id": page_id},
        "rich_text": [{
            "text": {"content": formatted_content}
        }]
    }

    return client._make_request("POST", "comments", comment_data)
```

### File Operations
```python
def upload_file(client, file_path, file_name=None):
    """Upload file to Notion"""
    if not file_name:
        file_name = os.path.basename(file_path)
    
    with open(file_path, 'rb') as file:
        files = {'file': (file_name, file)}
        
        # Remove Content-Type header for file upload
        headers = {
            "Authorization": f"Bearer {client.token}",
            "Notion-Version": client.version
        }
        
        response = requests.post(
            f"{client.base_url}/files",
            headers=headers,
            files=files
        )
        
        response.raise_for_status()
        return response.json()
```

## Complete ETL Example

```python
from datetime import datetime, timedelta

def extract_workspace_content(client, since_date=None):
    """Extract all accessible content from workspace"""
    
    if not since_date:
        since_date = datetime.now() - timedelta(days=1)
    
    extracted_content = {
        "pages": [],
        "databases": [],
        "comments": [],
        "extraction_timestamp": datetime.now().isoformat()
    }
    
    # 1. Search for updated pages
    pages_response = search_pages(client, last_edited_after=since_date)
    
    for page in pages_response["results"]:
        page_id = page["id"]
        
        # Get full page content
        page_content = get_page_content(client, page_id)
        extracted_content["pages"].append(page_content)
        
        # Get page comments
        comments = get_page_comments(client, page_id)
        if comments:
            extracted_content["comments"].append({
                "page_id": page_id,
                "comments": comments
            })
    
    # 2. Query data sources (if you have known data source IDs)
    # Note: Data source IDs are typically obtained from database configuration
    data_source_ids = ["26fc2345-ab46-81ac-a43c-000befe7113e"]  # Example data source ID

    for data_source_id in data_source_ids:
        try:
            # Get data source entries
            data_source_entries = query_data_source(client, data_source_id)

            extracted_content["databases"].append({
                "data_source_id": data_source_id,
                "entries": data_source_entries
            })
        except Exception as e:
            print(f"Error querying data source {data_source_id}: {str(e)}")
    
    return extracted_content

# Usage
client = NotionClient("secret_your_token_here")
content = extract_workspace_content(client)
```

This comprehensive API reference provides all the endpoints and examples needed for robust Notion ETL operations, with proper error handling, rate limiting, and pagination support.