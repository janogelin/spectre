# TinyURL API Design

## SOAP vs REST API Comparison

| Feature         | SOAP                                 | REST                                  |
|----------------|--------------------------------------|---------------------------------------|
| Protocol       | Strictly uses XML over HTTP, SMTP    | Uses HTTP, supports JSON, XML, etc.   |
| Flexibility    | Rigid, contract-based (WSDL)         | Flexible, resource-based              |
| Simplicity     | Complex, heavy payloads              | Simple, lightweight                   |
| Caching        | Not natively supported               | Supported via HTTP caching            |
| Error Handling | Standardized (SOAP Faults)           | Uses HTTP status codes                |
| Adoption       | Enterprise, legacy systems           | Web, mobile, modern applications      |

**Recommendation:** REST is preferred for TinyURL due to its simplicity, performance, and web-friendliness.

---

## REST API Definitions

### 1. Create Short URL
- **Endpoint:** `POST /api/v1/urls`
- **Headers:**
  - `api_dev_key: string` (required)
- **Body Parameters:**
  - `original_url: string` (required)
  - `custom_alias: string` (optional)
  - `expiration: datetime` (optional)
- **Returns (Success):**
```json
{
  "success": true,
  "short_url": "https://tiny.url/abc123",
  "alias": "abc123",
  "expiration": "2024-12-31T23:59:59Z",
  "message": "Short URL created successfully."
}
```
- **Returns (Error):**
```json
{
  "success": false,
  "error": "Custom alias already exists.",
  "message": "Failed to create short URL."
}
```
- **Safeguards:**
  - Rate limit: e.g., max 1000 creations per day per `api_dev_key`
  - Validate `original_url` format
  - Enforce alias uniqueness

### 2. Delete Short URL
- **Endpoint:** `DELETE /api/v1/urls/{alias}`
- **Headers:**
  - `api_dev_key: string` (required)
- **Path Parameters:**
  - `alias: string` (required)
- **Returns (Success):**
```json
{
  "success": true,
  "message": "Short URL deleted successfully."
}
```
- **Returns (Error):**
```json
{
  "success": false,
  "error": "Alias not found or permission denied.",
  "message": "Failed to delete short URL."
}
```
- **Safeguards:**
  - Only allow deletion by the creator's `api_dev_key`
  - Rate limit: e.g., max 100 deletions per day per `api_dev_key`

### 3. Redirect (Read)
- **Endpoint:** `GET /{alias}`
- **Returns (Success):**
  - HTTP 302 redirect to the original URL
- **Returns (Error):**
  - HTTP 404 Not Found with body:
```json
{
  "success": false,
  "error": "Alias not found or expired.",
  "message": "Redirection failed."
}
```
- **Safeguards:**
  - Rate limit: e.g., max 10,000 redirections per hour per `api_dev_key` (if authenticated)
  - For anonymous users, apply global or IP-based rate limits

---

## Abuse Prevention & Rate Limiting
- Each `api_dev_key` is assigned a configurable rate limit for:
  - URL creations (e.g., per minute/hour/day)
  - Redirections (e.g., per minute/hour)
  - Deletions (e.g., per day)
- Rate limits can be customized per key (e.g., premium vs. free users)
- Exceeding limits returns HTTP 429 (Too Many Requests) with a descriptive message
- Monitor and log abuse attempts for further action

---

## Example Error Response (Rate Limit Exceeded)
```json
{
  "success": false,
  "error": "Rate limit exceeded. Max 1000 URL creations per day.",
  "retry_after_seconds": 3600
}
``` 