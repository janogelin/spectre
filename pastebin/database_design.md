# Pastebin Database Design

## Design Goals
- Support billions of records (high scalability)
- Efficiently store small metadata (<1 KB) and medium-sized paste content (up to a few MB)
- Minimal relationships (optionally, user-paste linkage)
- Read-heavy workload

---

## Table Overview
1. **pastes**: Stores paste content and metadata
2. **users** (optional): Stores user information (if user accounts are supported)

---

## 1. `pastes` Table
| Column         | Type           | Description                                 | Indexing/Notes                |
|---------------|----------------|---------------------------------------------|-------------------------------|
| id            | VARCHAR(32)    | Primary key (Base62 or custom alias)        | PK, unique, indexed           |
| content       | BYTEA / TEXT   | Paste content (up to a few MB)              |                               |
| created_at    | TIMESTAMP      | Creation time                               | Indexed (for TTL/cleanup)     |
| expires_at    | TIMESTAMP      | Expiry time (nullable)                      | Indexed (for TTL/cleanup)     |
| access_count  | BIGINT         | Number of times accessed                    |                               |
| user_id       | VARCHAR(64)    | (Optional) Creator user ID                  | FK to users.id, nullable      |
| size_bytes    | INTEGER        | Size of content in bytes                    |                               |
| is_deleted    | BOOLEAN        | Soft delete flag                            | Indexed                       |

- **Primary Key:** `id` (Base62-encoded or custom alias)
- **Indexes:**
  - Primary key on `id`
  - Index on `expires_at` for efficient cleanup
  - Index on `created_at` for analytics/TTL
  - Index on `user_id` if user-paste queries are needed
  - Index on `is_deleted` for fast filtering
- **Partitioning:**
  - Consider partitioning by `created_at` (e.g., monthly) for easier data management and archiving
  - For very large scale, use sharding by hash of `id`

---

## 2. `users` Table (Optional)
| Column      | Type         | Description                | Indexing/Notes         |
|-------------|--------------|----------------------------|------------------------|
| id          | VARCHAR(64)  | Primary key (user ID)      | PK, unique, indexed    |
| username    | VARCHAR(64)  | Unique username            | Unique, indexed        |
| email       | VARCHAR(128) | User email                 | Unique, indexed        |
| created_at  | TIMESTAMP    | Account creation time      |                        |

---

## Schema Example (PostgreSQL)
```sql
CREATE TABLE pastes (
    id VARCHAR(32) PRIMARY KEY,
    content BYTEA NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP,
    access_count BIGINT DEFAULT 0,
    user_id VARCHAR(64),
    size_bytes INTEGER NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE INDEX idx_pastes_expires_at ON pastes(expires_at);
CREATE INDEX idx_pastes_created_at ON pastes(created_at);
CREATE INDEX idx_pastes_user_id ON pastes(user_id);
CREATE INDEX idx_pastes_is_deleted ON pastes(is_deleted);

CREATE TABLE users (
    id VARCHAR(64) PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(128) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## Scaling and Performance Considerations
- **Partitioning/Sharding:**
  - Use time-based partitioning (e.g., monthly) for the `pastes` table to manage billions of records efficiently.
  - For extreme scale, shard by hash of `id` across multiple database instances.
- **Read Optimization:**
  - Use in-memory caching (e.g., Redis) for hot pastes and metadata.
  - Use covering indexes for frequent queries (e.g., by `id`, `expires_at`).
- **Storage:**
  - Store large paste content in `BYTEA`/`TEXT` for simplicity, or use object storage (e.g., S3) for very large pastes and keep only metadata in the DB.
- **Cleanup:**
  - Regularly delete or archive expired and deleted pastes to reclaim space.
- **Soft Deletes:**
  - Use `is_deleted` for safe, reversible deletions and to support analytics.

---

## Summary
- The schema is optimized for high write and read throughput, minimal relationships, and efficient cleanup.
- Partitioning and sharding strategies ensure scalability to billions of records.
- Optional user linkage supports future extensibility without impacting core performance. 