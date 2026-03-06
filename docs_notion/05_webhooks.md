# Notion Webhooks

> **Last Updated**: December 2025
> **Source**: [Notion Webhooks Reference](https://developers.notion.com/reference/webhooks)

## Overview

Webhooks enable real-time updates from Notion by sending HTTP POST requests to your specified endpoint when workspace activities occur. This eliminates the need for constant API polling and provides near-instant notifications of changes.

### Key Benefits
- ✅ **Real-time Updates**: Receive notifications within seconds of workspace changes
- ✅ **Reduced API Calls**: No need for periodic polling, reducing API quota consumption
- ✅ **Event-Driven Architecture**: Build responsive applications that react to Notion changes
- ✅ **Lower Latency**: Immediate notifications vs. polling intervals (minutes to seconds)

---

## Setup Process

### Step 1: Create Webhook Subscription

1. Navigate to your **Notion Integration Settings**
2. Click on the **Webhooks** tab
3. Click **"Create a subscription"**
4. Configure subscription:
   - **Webhook URL**: Enter a public, secure HTTPS URL
   - **Event Types**: Select which events to subscribe to
   - **Description**: Optional description for tracking

### Step 2: Verify Subscription

Notion will send a **one-time verification request** to your webhook URL:

**Verification Request**:
```http
POST /your-webhook-endpoint HTTP/1.1
Host: your-domain.com
Content-Type: application/json

{
  "type": "webhook_verification",
  "token": "abc123xyz789",
  "challenge": "random_string_to_echo_back"
}
```

**Your Response** (must echo back the challenge):
```json
{
  "challenge": "random_string_to_echo_back"
}
```

After successful verification, the subscription becomes **active**.

### Step 3: Implement Signature Verification

Every webhook event includes a cryptographic signature in the `X-Notion-Signature` header. You **must verify** this signature to prevent unauthorized requests.

---

## Event Types

Notion supports **24 webhook event types** across 4 categories. Events are either **aggregated** (batched within a short time window) or **non-aggregated** (sent immediately).

---

### Page Events (8 events)

#### 1. `page.content_updated` 🔄 *Aggregated*
Triggered when a page's content (blocks) is modified.

**Use Cases**: Track document changes, sync content updates, trigger workflows

**Example Payload**:
```json
{
  "type": "page.content_updated",
  "page": {"id": "page-id"},
  "workspace_id": "workspace-id",
  "integration_id": "integration-id",
  "timestamp": "2025-12-25T10:30:00.000Z"
}
```

#### 2. `page.created` 🔄 *Aggregated*
Triggered when a new page is created.

**Use Cases**: Initialize workflows, auto-setup templates, track content growth

#### 3. `page.deleted` 🔄 *Aggregated*
Triggered when a page is moved to trash.

**Use Cases**: Cleanup external references, archive synced data, audit deletions

#### 4. `page.locked` ⚡ *Non-aggregated*
Triggered when a page is locked from editing.

**Use Cases**: Enforce approval workflows, protect critical documents

#### 5. `page.moved` 🔄 *Aggregated*
Triggered when a page is moved to another location (parent change).

**Use Cases**: Update hierarchies, sync folder structures, track reorganizations

#### 6. `page.properties_updated` 🔄 *Aggregated*
Triggered when a page property is updated (status, assignee, due date, etc.).

**Use Cases**: Track task status changes, monitor assignments, update external systems

#### 7. `page.undeleted` 🔄 *Aggregated*
Triggered when a page is restored from trash.

**Use Cases**: Restore synced data, audit restorations

#### 8. `page.unlocked` ⚡ *Non-aggregated*
Triggered when a page is unlocked for editing.

**Use Cases**: Resume workflows, notify collaborators

---

### Database Events (4 events)

#### 9. `database.created` 🔄 *Aggregated*
Triggered when a new database is created.

**Use Cases**: Setup sync pipelines, initialize external schemas

#### 10. `database.deleted` 🔄 *Aggregated*
Triggered when a database is moved to trash.

**Use Cases**: Cleanup synced databases, audit deletions

#### 11. `database.moved` 🔄 *Aggregated*
Triggered when a database is moved to another location.

**Use Cases**: Update external references, track reorganizations

#### 12. `database.undeleted` 🔄 *Aggregated*
Triggered when a database is restored from trash.

**Use Cases**: Restore synced data, audit restorations

---

### Data Source Events (6 events) 🆕 *API version 2025-09-03+*

Data sources are the new unified concept for databases and linked databases.

#### 13. `data_source.content_updated` 🔄 *Aggregated*
Triggered when data source content is updated (rows added/modified).

**Use Cases**: Sync database records, trigger data pipelines

#### 14. `data_source.created` 🔄 *Aggregated*
Triggered when a new data source is created.

**Use Cases**: Initialize sync, setup external schemas

#### 15. `data_source.deleted` 🔄 *Aggregated*
Triggered when a data source is moved to trash.

**Use Cases**: Cleanup synced data, audit deletions

#### 16. `data_source.moved` 🔄 *Aggregated*
Triggered when a data source is moved to another location.

**Use Cases**: Update external references, track reorganizations

#### 17. `data_source.schema_updated` 🔄 *Aggregated*
Triggered when data source schema is modified (properties added/removed/changed).

**Use Cases**: Detect schema changes, update external data models, maintain schema synchronization

**Example Payload**:
```json
{
  "type": "data_source.schema_updated",
  "data_source": {
    "id": "database-id",
    "type": "database"
  },
  "workspace_id": "workspace-id",
  "integration_id": "integration-id",
  "timestamp": "2025-12-25T10:40:00.000Z"
}
```

#### 18. `data_source.undeleted` 🔄 *Aggregated*
Triggered when a data source is restored from trash.

**Use Cases**: Restore synced data, audit restorations

---

### Comment Events (3 events)

#### 19. `comment.created` ⚡ *Non-aggregated*
Triggered when a new comment is added to a page.

**Use Cases**: Notify users of mentions, aggregate discussion activity, build collaboration dashboards

**Example Payload**:
```json
{
  "type": "comment.created",
  "comment": {
    "id": "comment-id",
    "parent": {
      "type": "page_id",
      "page_id": "page-id"
    }
  },
  "workspace_id": "workspace-id",
  "integration_id": "integration-id",
  "timestamp": "2025-12-25T10:35:00.000Z"
}
```

#### 20. `comment.updated` ⚡ *Non-aggregated*
Triggered when a comment is edited.

**Use Cases**: Track comment edits, update synced discussions

#### 21. `comment.deleted` ⚡ *Non-aggregated*
Triggered when a comment is deleted.

**Use Cases**: Cleanup synced comments, audit deletions

---

### Deprecated Events

#### ⚠️ `database.schema_updated` (Deprecated)
**Status**: Deprecated - Use `data_source.schema_updated` instead (API version 2025-09-03+)

---

### Event Aggregation

**Aggregated Events** 🔄:
- Multiple rapid changes are batched into a single webhook event
- Reduces noise and API calls
- Typical aggregation window: a few seconds
- Examples: `page.content_updated`, `page.properties_updated`, `data_source.schema_updated`

**Non-aggregated Events** ⚡:
- Sent immediately when the event occurs
- No batching
- Examples: `comment.created`, `page.locked`, `page.unlocked`

**Note**: To get full details after receiving an aggregated event, query the Notion API with the entity ID

---

## Webhook Payload Structure

All webhook events share a consistent structure with common fields and event-specific data.

### Common Fields (All Events)

```json
{
  "id": "webhook-event-uuid",
  "timestamp": "2025-12-29T10:30:00.000Z",
  "workspace_id": "workspace-uuid",
  "workspace_name": "My Workspace",
  "subscription_id": "subscription-uuid",
  "integration_id": "integration-uuid",
  "type": "page.created",
  "authors": [
    {
      "id": "user-uuid",
      "type": "person"
    }
  ],
  "accessible_by": [
    {
      "id": "user-uuid",
      "type": "person"
    }
  ],
  "attempt_number": 1,
  "entity": {
    "id": "entity-uuid",
    "type": "page"
  },
  "data": {
    // Event-specific fields
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique identifier for this webhook event |
| `timestamp` | string (ISO 8601) | When the event occurred |
| `workspace_id` | string (UUID) | Notion workspace identifier |
| `workspace_name` | string | Workspace display name |
| `subscription_id` | string (UUID) | Webhook subscription identifier |
| `integration_id` | string (UUID) | Your integration identifier |
| `type` | string | Event type (e.g., `page.created`, `comment.created`) |
| `authors` | array | Users who triggered the event |
| `accessible_by` | array | Users who can access the entity |
| `attempt_number` | number | Delivery attempt count (starts at 1) |
| `entity` | object | The entity that was modified |
| `data` | object | Event-specific details |

### Entity Types

The `entity` object identifies the modified resource:

```json
{
  "id": "entity-uuid",
  "type": "page" | "database" | "data_source" | "comment" | "block"
}
```

### Event-Specific Payload Examples

#### Page Event Payload
```json
{
  "type": "page.created",
  "entity": {
    "id": "page-uuid",
    "type": "page"
  },
  "data": {
    "parent": {
      "id": "parent-page-uuid",
      "type": "page"
    }
  }
}
```

#### Comment Event Payload
```json
{
  "type": "comment.created",
  "entity": {
    "id": "comment-uuid",
    "type": "comment"
  },
  "data": {
    "parent": {
      "id": "page-uuid",
      "type": "page"
    }
  }
}
```

#### Data Source Event Payload
```json
{
  "type": "data_source.schema_updated",
  "entity": {
    "id": "database-uuid",
    "type": "data_source"
  },
  "data": {
    "parent": {
      "id": "parent-page-uuid",
      "type": "page"
    }
  }
}
```

### Authors Field

The `authors` array contains users who triggered the event:

```json
"authors": [
  {
    "id": "user-uuid",
    "type": "person" | "bot" | "agent"
  }
]
```

**Author Types**:
- `person`: Human user
- `bot`: Notion bot
- `agent`: API integration

### Accessible By Field

The `accessible_by` array lists users with access to the entity:

```json
"accessible_by": [
  {
    "id": "user-uuid",
    "type": "person" | "bot"
  }
]
```

**Use Cases**:
- Determine notification recipients
- Filter events by user access
- Implement access-based routing

### Attempt Number

The `attempt_number` field tracks delivery retries:
- Starts at `1` for first attempt
- Increments on each retry (max 5 attempts)
- Use for idempotency checks

**Best Practice**:
```python
async def handle_webhook(event: dict):
    event_id = event["id"]
    attempt = event["attempt_number"]

    # Check if already processed
    if is_event_processed(event_id):
        logger.info(f"Event {event_id} already processed, skipping (attempt {attempt})")
        return

    # Process event
    await process_event(event)
    mark_event_processed(event_id)
```

---

## Authentication & Security

### Signature Verification

Every webhook request includes an `X-Notion-Signature` header containing an HMAC-SHA256 signature.

#### How It Works

1. Notion computes: `HMAC-SHA256(webhook_secret, request_body)`
2. Signature is sent in `X-Notion-Signature` header
3. You compute the same signature and compare

#### Implementation (Python)

```python
import hmac
import hashlib
from fastapi import Request, HTTPException

async def verify_notion_signature(request: Request, webhook_secret: str) -> bool:
    """Verify Notion webhook signature.

    Args:
        request: FastAPI Request object
        webhook_secret: Your webhook secret from Notion

    Returns:
        True if signature is valid

    Raises:
        HTTPException: If signature verification fails
    """
    # Get signature from header
    signature = request.headers.get("X-Notion-Signature")
    if not signature:
        raise HTTPException(status_code=401, detail="Missing signature")

    # Read request body
    body = await request.body()

    # Compute expected signature
    expected_signature = hmac.new(
        webhook_secret.encode('utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()

    # Compare signatures (timing-safe comparison)
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    return True
```

#### Implementation (JavaScript/Node.js)

```javascript
const crypto = require('crypto');

function verifyNotionSignature(request, webhookSecret) {
    const signature = request.headers['x-notion-signature'];
    if (!signature) {
        throw new Error('Missing signature');
    }

    const body = JSON.stringify(request.body);
    const expectedSignature = crypto
        .createHmac('sha256', webhookSecret)
        .update(body, 'utf8')
        .digest('hex');

    if (!crypto.timingSafeEqual(
        Buffer.from(signature),
        Buffer.from(expectedSignature)
    )) {
        throw new Error('Invalid signature');
    }

    return true;
}
```

---

## Webhook Payload Structure

All webhook events follow a consistent structure:

### Common Fields

```json
{
  "type": "<event_type>",           // Event type identifier
  "workspace_id": "<workspace_id>",  // Notion workspace ID
  "integration_id": "<integration_id>", // Your integration ID
  "timestamp": "<ISO8601_timestamp>", // Event timestamp
  "<resource>": {                    // Event-specific resource
    "id": "<resource_id>",
    // ... additional resource fields
  }
}
```

### Event-Specific Fields

| Event Type | Resource Field | Description |
|------------|---------------|-------------|
| `page.content_updated` | `page` | Contains `page.id` |
| `comment.created` | `comment` | Contains `comment.id` and `parent` |
| `data_source.schema_updated` | `data_source` | Contains `data_source.id` and `type` |

---

## Requirements & Limitations

### Webhook URL Requirements

- ✅ **Must be publicly accessible** (no localhost)
- ✅ **Must use HTTPS** (SSL/TLS required)
- ✅ **Must respond within 10 seconds** (timeout limit)
- ✅ **Must return HTTP 2xx status** for successful delivery

### Event Aggregation

- Some events are **aggregated** to reduce noise
- Short **delivery delays** may occur (typically < 5 seconds)
- Multiple rapid changes may be combined into a single event

### Rate Limits

- Webhooks have **separate rate limits** from API calls
- No documented limit on webhook delivery frequency
- Ensure your endpoint can handle burst traffic

---

## Subscription Management

### Create Subscription

1. Via Notion Integration UI (recommended)
2. Subscribe to specific event types
3. Multiple subscriptions allowed per integration

### Update Subscription

1. Navigate to Webhooks tab in Integration Settings
2. Edit existing subscription
3. Change event types or webhook URL

### Delete Subscription

1. Click "Delete" on subscription in Integration Settings
2. Confirm deletion
3. Webhook events will no longer be sent

### Monitor Subscription

- View delivery logs in Integration Settings
- Check success/failure rates
- Debug failed deliveries

---

## Testing Strategies

### Manual Testing

1. **Page Content Update**:
   - Open a page connected to your integration
   - Change the page title or content
   - Verify webhook event is received

2. **Comment Creation**:
   - Add a comment to a connected page
   - Check for `comment.created` event

3. **Schema Update**:
   - Add/remove a database property
   - Verify `data_source.schema_updated` event

### Development Tools

#### Use ngrok for Local Testing

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com

# Start your local server
poetry run python scripts/start_api.py  # Port 8000

# Expose local server to public internet
ngrok http 8000

# Use the HTTPS URL in Notion webhook settings
# Example: https://abc123.ngrok.io/api/v1/webhooks/notion
```

#### Use RequestBin for Debugging

1. Visit https://requestbin.com
2. Create a temporary endpoint
3. Configure Notion webhook to send to RequestBin
4. Inspect raw webhook payloads

---

## Troubleshooting

### Common Issues

#### 1. Webhook Not Receiving Events

**Possible Causes**:
- Integration not connected to the page/database
- Insufficient integration capabilities
- Webhook subscription inactive

**Solutions**:
- Check page connections in Notion UI
- Verify integration has required capabilities
- Confirm subscription status in Integration Settings

#### 2. Signature Verification Fails

**Possible Causes**:
- Incorrect webhook secret
- Request body modification (middleware interference)
- Timing/encoding issues

**Solutions**:
- Verify webhook secret matches Notion settings
- Log raw request body before processing
- Use raw body for signature computation (no JSON parsing)

#### 3. Timeout Errors

**Possible Causes**:
- Slow webhook processing
- Network latency
- Synchronous blocking operations

**Solutions**:
- Process webhooks asynchronously
- Return 200 OK immediately, process in background
- Use job queues (Celery, RQ, etc.)

#### 4. Event Aggregation Confusion

**Issue**: Not receiving every individual change

**Explanation**: Notion aggregates rapid changes to reduce noise

**Solution**: Query the API for full details after webhook notification

---

## Best Practices

### 1. Idempotency

Webhooks may be **delivered multiple times** due to retries. Implement idempotent handling:

```python
async def handle_webhook_event(event_id: str, event_data: dict):
    # Check if event already processed
    if await is_event_processed(event_id):
        logger.info(f"Event {event_id} already processed, skipping")
        return

    # Process event
    await process_event(event_data)

    # Mark as processed
    await mark_event_processed(event_id)
```

### 2. Asynchronous Processing

Don't block webhook endpoint with heavy processing:

```python
@app.post("/webhooks/notion")
async def webhook_handler(request: Request, background_tasks: BackgroundTasks):
    # 1. Verify signature
    await verify_signature(request)

    # 2. Parse event
    event = await request.json()

    # 3. Queue for background processing
    background_tasks.add_task(process_webhook_event, event)

    # 4. Return 200 immediately
    return {"status": "accepted"}
```

### 3. Error Handling & Retries

Notion will **retry failed deliveries** (5xx errors). Handle gracefully:

```python
async def process_webhook_event(event: dict):
    try:
        # Process event
        await sync_service.sync_page(event["page"]["id"])
    except TemporaryError as e:
        # Transient error - Notion will retry
        logger.warning(f"Temporary error: {e}")
        raise  # Return 5xx to trigger retry
    except PermanentError as e:
        # Permanent error - log and continue
        logger.error(f"Permanent error: {e}")
        # Don't raise - return 200 to avoid retries
```

### 4. Logging & Monitoring

Track webhook health metrics:

```python
import time
from prometheus_client import Counter, Histogram

webhook_requests = Counter('webhook_requests_total', 'Total webhook requests')
webhook_errors = Counter('webhook_errors_total', 'Total webhook errors')
webhook_latency = Histogram('webhook_latency_seconds', 'Webhook processing latency')

@app.post("/webhooks/notion")
async def webhook_handler(request: Request):
    start_time = time.time()
    webhook_requests.inc()

    try:
        # Process webhook
        await process_webhook(request)
    except Exception as e:
        webhook_errors.inc()
        raise
    finally:
        webhook_latency.observe(time.time() - start_time)
```

### 5. Fallback to Polling

Use webhooks as primary mechanism, polling as backup:

```python
# Webhook-triggered sync (real-time)
@app.post("/webhooks/notion")
async def webhook_sync(request: Request):
    event = await request.json()
    await sync_service.sync_page(event["page"]["id"])

# Scheduled sync (fallback - runs daily)
@scheduler.scheduled_job('cron', hour=2)
async def fallback_sync():
    logger.info("Running fallback sync (webhook backup)")
    await sync_service.sync_all_pages()
```

---

## Integration with Notion Daily

### Recommended Architecture

```
Notion Webhook → FastAPI Endpoint → Background Task → Sync Service → Database
```

### Implementation Steps

1. **Add Webhook Endpoint** (`src/api/webhooks.py`)
2. **Implement Signature Verification**
3. **Queue Background Sync Tasks**
4. **Update Sync Service** for single-page sync
5. **Add Monitoring & Logging**

### Configuration

Add to `.env`:
```bash
# Notion Webhook Configuration
NOTION_WEBHOOK_SECRET=your_webhook_secret_here
NOTION_WEBHOOK_URL=https://your-domain.com/api/v1/webhooks/notion
```

### Testing

```bash
# 1. Start API server
poetry run python scripts/start_api.py

# 2. Expose to public internet (development)
ngrok http 8000

# 3. Configure webhook in Notion Integration Settings
# URL: https://abc123.ngrok.io/api/v1/webhooks/notion

# 4. Test by editing a connected Notion page
```

---

## Migration from Polling to Webhooks

### Phase 1: Add Webhook Support (Weeks 1-2)
- ✅ Implement webhook endpoint
- ✅ Add signature verification
- ✅ Test with ngrok locally

### Phase 2: Parallel Operation (Weeks 3-4)
- ✅ Deploy webhook endpoint to production
- ✅ Configure Notion webhook subscription
- ✅ Keep existing polling as backup
- ✅ Monitor webhook reliability

### Phase 3: Reduce Polling (Weeks 5-6)
- ✅ Lower polling frequency (every 6-12 hours)
- ✅ Use polling only for consistency checks
- ✅ Rely on webhooks for real-time updates

### Phase 4: Webhook-Primary (Ongoing)
- ✅ Webhooks handle 95%+ of updates
- ✅ Daily polling as safety net
- ✅ Monitor and optimize

---

## References

- [Notion Webhooks API Reference](https://developers.notion.com/reference/webhooks)
- [Notion Integration Guide](https://developers.notion.com/docs/getting-started)
- [HMAC Signature Verification](https://en.wikipedia.org/wiki/HMAC)
- [Webhook Best Practices](https://webhooks.fyi/)

---

## Changelog

- **2025-12-25**: Initial documentation based on Notion Webhooks release
- Event types: `page.content_updated`, `comment.created`, `data_source.schema_updated`
- Security: HMAC-SHA256 signature verification required
- Requirements: Public HTTPS URL, 10-second timeout, HTTP 2xx response
