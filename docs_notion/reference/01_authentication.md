# Source: https://developers.notion.com/reference/authentication

# Notion API Authentication

## Overview
The Notion API uses HTTP `Authorization` headers with bearer tokens for both authentication and authorization of requests.

## Key Points

**Bearer Token Basics:**
Bearer tokens are issued when you create an integration, or each time a user completes an OAuth flow for public integrations.

**Required Header:**
Requests must include `Authorization: Bearer [token]` along with the API version header.

**Example cURL Request:**
```bash
curl https://api.notion.com/v1/users \
  -H "Authorization: Bearer secret_t1CdN9S8yicG5eWLUOfhcWaOscVnFXns" \
  -H "Notion-Version: 2025-09-03"
```

**SDK Implementation:**
The Notion SDK for JavaScript simplifies token handling by accepting the bearer token once during client initialization:
```javascript
new Client({ auth: process.env.NOTION_ACCESS_TOKEN })
```
This eliminates the need to pass credentials with each request.

**Integration Attribution:**
Operations performed through integrations appear in Notion with a bot attribution, where the bot's name and avatar are controlled in the integration settings.

## Additional Resources
- Complete documentation available at https://developers.notion.com/llms.txt
- Further guidance in the Authorization guide referenced in the original content
