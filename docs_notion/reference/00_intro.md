# Source: https://developers.notion.com/reference/intro

# Notion API Introduction

## Core Overview
The Notion API enables integrations to access pages, databases, and users. All requests go to `https://api.notion.com` via HTTPS using REST conventions with GET, POST, PATCH, and DELETE methods.

## Key Requirements
You need an integration token from your workspace's integration settings. Admin access is required to generate tokens.

## JSON Standards
- Resources have an `"object"` property identifying their type
- UUIDv4 `"id"` properties address resources (dashes optional in requests)
- Properties use `snake_case` formatting
- Dates follow ISO 8601 format
- Null values replace empty strings for unsetting properties

## Pagination Features
Six endpoints support cursor-based pagination, returning 10 items by default (max 100):

**Supported endpoints include:**
- List all users
- Retrieve block children
- Retrieve comments
- Query databases
- Search functionality

**Response fields:**
- `has_more` (boolean) - indicates additional results exist
- `next_cursor` (string) - retrieves next page when `has_more` is true
- `results` - endpoint-specific data array
- `type` - specifies object type in results

**Request parameters:**
- `page_size`: Items per response (default: 100, max: 100)
- `start_cursor`: Previous response's cursor for subsequent pages

## Implementation
GET requests pass parameters via query strings; POST requests use request bodies. Code samples are provided in JavaScript SDK and cURL formats.
