# Pastebin System Requirements and Technology Choices

## Functional Requirements
1. Users can upload ("paste") text and receive a unique URL for access.
2. Only text uploads are supported.
3. Data and links expire automatically after a specified timespan; users can set custom expiration.
4. Users can optionally choose a custom alias for their paste (maximum length: **32 characters**, configurable).
5. Each paste must not exceed a maximum size of **512 KB** (524,288 bytes); this limit should be configurable.

## Non-Functional Requirements
1. High reliability: No data loss for uploaded pastes.
2. High availability: Service must minimize downtime and always allow access to pastes.
3. Real-time access: Users should experience minimal latency.
4. Paste links must be unguessable and not predictable.

## Extended Requirements
1. Analytics: Track how many times a paste is accessed.
2. REST API: Service must be accessible programmatically by other services.

---

# Technology Choices and Rationale

## 1. FastAPI
- **Why:** Modern, high-performance Python web framework for building APIs quickly. Supports async for low-latency, real-time access.
- **Meets:** REST API, real-time access, high availability.

## 2. Uvicorn
- **Why:** Lightning-fast ASGI server, ideal for serving FastAPI applications in production.
- **Meets:** Real-time access, high availability.

## 3. SQLAlchemy + PostgreSQL (psycopg2-binary)
- **Why:** SQLAlchemy is a robust ORM for Python, and PostgreSQL is a reliable, production-grade relational database. Ensures data durability, supports custom aliases, and enables analytics.
- **Meets:** High reliability, analytics, custom alias, data durability.

## 4. Redis
- **Why:** In-memory data store with built-in support for expiring keys. Used for fast, temporary storage of pastes and enforcing expiration.
- **Meets:** Real-time access, automatic expiration, high availability.

## 5. Itsdangerous
- **Why:** Securely generates unguessable, URL-safe tokens for paste links.
- **Meets:** Unpredictable, secure paste URLs.

## 6. Alembic
- **Why:** Database migrations for SQLAlchemy, ensuring schema changes are managed safely.
- **Meets:** High reliability, maintainability.

## 7. Loguru
- **Why:** Modern logging library for Python, making it easy to track errors and analytics events.
- **Meets:** Analytics, reliability, maintainability.

## 8. python-dotenv & Pydantic
- **Why:** For configuration management and data validation, ensuring robust, secure, and maintainable code.
- **Meets:** Reliability, maintainability, security.

## 9. Requests
- **Why:** Enables REST API client functionality for integration testing and service-to-service communication.
- **Meets:** REST API accessibility, integration.

---

# Summary Table
| Requirement                | Technology                | Rationale                                      |
|----------------------------|---------------------------|------------------------------------------------|
| REST API                   | FastAPI, Uvicorn          | High performance, async support                |
| Data durability            | PostgreSQL, SQLAlchemy    | Reliable, transactional storage                |
| Expiring pastes            | Redis                     | Fast, supports TTL natively                    |
| Unpredictable URLs         | Itsdangerous              | Secure, URL-safe token generation              |
| Analytics                  | PostgreSQL, Loguru        | Track and store access counts                  |
| Custom alias               | PostgreSQL, SQLAlchemy    | Unique constraints, easy lookup                |
| Config & validation        | python-dotenv, Pydantic   | Secure, robust configuration                   |
| DB migrations              | Alembic                   | Safe schema evolution                          |
| Logging                    | Loguru                    | Modern, flexible logging                       |
| API client                 | Requests                  | Integration and testing                        |

---

# Additional Notes
- **Paste Size Limit Rationale:** Limiting paste size prevents abuse (e.g., DoS attacks), protects system resources, and aligns with typical user expectations for a pastebin service. The default maximum is 512 KB per paste, but this should be configurable to allow flexibility for different deployments.
- **Custom URL Length Limit Rationale:** Restricting the length of custom URLs/aliases (default: 32 characters, configurable) ensures consistency in the URL database, prevents abuse, and helps maintain efficient indexing and lookup performance. 