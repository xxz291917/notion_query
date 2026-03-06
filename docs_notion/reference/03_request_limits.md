# Source: https://developers.notion.com/reference/request-limits

# Notion API Request Limits

## Rate Limiting

The Notion API enforces rate limits to maintain service consistency. The baseline threshold is an average of **three requests per second** per integration, though temporary bursts are permitted.

When rate-limited, the API returns HTTP 429 with a `"rate_limited"` error code. The response includes a `Retry-After` header indicating seconds to wait before retrying.

Two accommodation strategies exist:
- **Honor the Retry-After header** and resume requests after the specified delay
- **Implement request queuing** to naturally slow outgoing request rates

Notion reserves the right to adjust these thresholds in the future, potentially varying by workspace tier.

## Size Constraints

The API enforces multiple size restrictions returning HTTP 400 validation errors when exceeded:

**Payload limits:**
- Maximum 1000 block elements per request
- 500KB overall payload size

**Property-level limits include:**
- Text content: 2000 characters
- URLs and links: 2000 characters
- Equations: 1000 characters
- Arrays (blocks/rich text): 100 elements maximum
- Multi-select options: 100 maximum
- Relations: 100 related pages maximum
- People fields: 100 users maximum
- Email addresses: 200 characters
- Phone numbers: 200 characters

Developers should validate inputs proactively and implement error handling for oversized data from external sources.
