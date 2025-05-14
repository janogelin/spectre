# TinyURL Database Design (NoSQL)

## NoSQL Candidate Comparison

| Feature/Criteria      | Aerospike                        | Cassandra                          | DynamoDB                          |
|----------------------|-----------------------------------|------------------------------------|-----------------------------------|
| **Scalability**      | Excellent, automatic sharding     | Excellent, peer-to-peer            | Excellent, managed, auto-scaling  |
| **Performance**      | Very high, low latency, in-memory | High, tunable consistency/latency  | High, single-digit ms latency     |
| **Operational Model**| Simple, few nodes, easy scaling   | Complex, requires tuning           | Fully managed (AWS)               |
| **Consistency**      | Strong (configurable)             | Tunable (eventual/strong)          | Strong/eventual (configurable)    |
| **Cost**             | Efficient, self-hosted            | Efficient, self-hosted             | Pay-per-use, can be expensive     |
| **TTL Support**      | Native, per-record                | Native, per-table                  | Native, per-item                  |
| **Best For**         | High throughput, real-time, KV    | Large-scale, multi-DC, analytics   | Serverless, easy ops, AWS-native  |
| **Suitability**      | Excellent for this use case        | Good, but more ops overhead        | Excellent, if on AWS              |

---

## Rationale for NoSQL (e.g., Aerospike)
- **Scalability:** Designed to handle billions of records efficiently.
- **Performance:** Optimized for high throughput and low latency, especially for read-heavy workloads.
- **Simplicity:** No need for complex joins or relationships; each record is mostly independent.
- **Flexibility:** Schema-less or flexible schema, allowing easy evolution of data model.
- **Candidate:** Aerospike (or similar NoSQL KV stores like Redis, DynamoDB, Cassandra)

---

## Data Model

### Primary Record: Short URL Mapping
- **Key:** Alias (short code)
- **Value/Object:**
  - `original_url: string`
  - `created_by: string` (user id or api_dev_key)
  - `created_at: datetime`
  - `expiration: datetime`
  - `custom_alias: string` (optional)
  - `redirect_count: integer` (for analytics)
  - `last_accessed: datetime` (optional, for analytics/cleanup)

#### Example (Aerospike Bin Structure)
| Key (PK) | Bin: original_url | Bin: created_by | Bin: created_at | Bin: expiration | Bin: custom_alias | Bin: redirect_count | Bin: last_accessed |
|----------|------------------|-----------------|-----------------|-----------------|-------------------|--------------------|--------------------|
| abc123   | https://...      | user_42         | 2024-06-01      | 2024-12-31      | myalias           | 12345              | 2024-06-10         |

---

## Secondary Indexes (Optional)
- **created_by:** To fetch all URLs created by a user (for user dashboards, analytics, or deletion).
- **expiration:** For background cleanup/TTL processes.

---

## Storage & Partitioning
- **Sharding:** Native to Aerospike; records are distributed by key (alias) for horizontal scaling.
- **Replication:** For high availability and durability.
- **TTL:** Native support for automatic expiration of records.

---

## Access Patterns
- **Read (Redirection):**
  - Lookup by alias (primary key) → fetch original_url, check expiration, increment redirect_count (optionally async)
- **Write (Create):**
  - Insert new record with alias as key
- **Delete:**
  - Remove record by alias (and/or by user)
- **Analytics:**
  - Increment redirect_count on each access (can be batched or async for performance)

---

## Example Aerospike Set Definition
- **Set:** `urls`
- **Primary Key:** `alias`
- **Bins:**
  - `original_url`
  - `created_by`
  - `created_at`
  - `expiration`
  - `custom_alias`
  - `redirect_count`
  - `last_accessed`

---

## Why Not Relational?
- No need for joins or complex relationships
- Simpler, more scalable for this use case
- Native TTL and sharding are critical for scale

---

## Summary Table
| Field           | Type      | Description                        |
|-----------------|-----------|------------------------------------|
| alias (PK)      | string    | Short code, unique                 |
| original_url    | string    | Full URL                           |
| created_by      | string    | User or API key                    |
| created_at      | datetime  | Creation timestamp                 |
| expiration      | datetime  | Expiry timestamp                   |
| custom_alias    | string    | Optional custom alias              |
| redirect_count  | integer   | Number of redirections             |
| last_accessed   | datetime  | Last time the URL was accessed     | 