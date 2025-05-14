# Pastebin API Design

## API Paradigm Comparison

| Feature         | SOAP                        | REST                        | RPC                         |
|----------------|-----------------------------|-----------------------------|-----------------------------|
| Protocol       | XML over HTTP, SMTP, etc.   | HTTP (usually JSON)         | HTTP, gRPC, custom          |
| Data Format    | XML                         | JSON, XML, others           | JSON, Protobuf, others      |
| Verbosity      | High (XML, envelopes)       | Low (concise, resource-based)| Very low (function calls)   |
| Discoverability| WSDL                        | OpenAPI/Swagger             | IDL (e.g., proto files)     |
| Flexibility    | Strong contracts, strict    | Flexible, loosely coupled   | Tight coupling, fast        |
| Browser-native | No                          | Yes                         | No (except JSON-RPC)        |
| Caching        | Complex                     | Native HTTP caching         | Not native                  |
| Adoption       | Enterprise, legacy          | Web, mobile, modern APIs    | Internal, microservices     |
| Error Handling | Standardized (SOAP Faults)  | HTTP status codes           | Custom, varies              |

### Summary
- **SOAP:** Heavyweight, best for enterprise/legacy systems needing strict contracts. Not browser-friendly.
- **REST:** Lightweight, resource-oriented, browser-native, easy to use, and widely adopted for web APIs.
- **RPC:** Fast, simple for internal or microservice communication, but tightly coupled and less discoverable.

## Recommendation
**REST** is the best fit for Pastebin:
- Human- and browser-friendly (JSON over HTTP)
- Easy to document and consume (OpenAPI/Swagger)
- Supports stateless, scalable design
- Native HTTP caching and status codes

---

# API Endpoints and Data Types

## 1. Add Paste
- **Endpoint:** `POST /pastes`
- **Parameters (JSON body):**
  - `content` (string, required): The text to paste
  - `custom_alias` (string, optional): Custom URL alias (max 32 chars)
  - `expires_in` (integer, optional): Expiry time in seconds
- **Returns (JSON):**
  - `url` (string): Full URL to access the paste
  - `id` (string): Unique paste ID
  - `expires_at` (ISO 8601 string): Expiry timestamp

## 2. Get Paste
- **Endpoint:** `GET /pastes/{id}`
- **Parameters:**
  - `id` (string, path): Paste ID or custom alias
- **Returns (JSON):**
  - `content` (string): The pasted text
  - `created_at` (ISO 8601 string): Creation timestamp
  - `expires_at` (ISO 8601 string): Expiry timestamp
  - `access_count` (integer): Number of times accessed

## 3. Delete Paste
- **Endpoint:** `DELETE /pastes/{id}`
- **Parameters:**
  - `id` (string, path): Paste ID or custom alias
- **Returns (JSON):**
  - `success` (boolean): Whether the paste was deleted
  - `message` (string): Status or error message

---

# Data Types Summary Table
| Operation | Parameters (Type)                                   | Returns (Type)                                  |
|-----------|-----------------------------------------------------|-------------------------------------------------|
| Add       | content (string), custom_alias (string?), expires_in (int?) | url (string), id (string), expires_at (string)  |
| Get       | id (string)                                         | content (string), created_at (string), expires_at (string), access_count (int) |
| Delete    | id (string)                                         | success (bool), message (string)                |

---

**Note:** All parameters and return values use JSON types for maximum interoperability and ease of use in web and mobile clients. 