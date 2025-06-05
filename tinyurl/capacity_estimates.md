# TinyURL Service Capacity Estimations

## Traffic Estimates
- **Write (New URL Shortenings):** 500 million per month
- **Read (Redirections):** 100:1 read/write ratio
- **Redirections per month:** 500 million × 100 = 50 billion

### Queries Per Second (QPS) Calculations
- **Seconds per month:** 30 days × 24 hours × 60 minutes × 60 seconds = 2,592,000 seconds
- **Write QPS:** 500,000,000 / 2,592,000 ≈ 193 writes/sec
- **Read QPS:** 50,000,000,000 / 2,592,000 ≈ 19,290 reads/sec

#### Math Explanation
- Write QPS: 500,000,000 ÷ 2,592,000 = 193
- Read QPS: 50,000,000,000 ÷ 2,592,000 = 19,290

## Storage Estimates
- **Retention period:** 5 years
- **Total writes in 5 years:** 500 million × 12 × 5 = 30 billion
- **Storage per object:** 500 bytes

  **Explanation:**
  The 500 bytes per object estimate is a conservative figure that accounts for all the data and metadata stored for each shortened URL. This includes:
  - **Short URL code (base-62 encoded):** ~8 bytes (Base-62 encoding allows for a large number of unique codes with a short length. For example, 8 base-62 characters can represent 62^8 ≈ 218 trillion unique codes, which is sufficient for the scale of this service. Each character is stored as a single byte, so an 8-character code uses 8 bytes.)
  - **Original (long) URL:** Up to 256 bytes (to accommodate most URLs)
  - **Creation timestamp:** 8 bytes
  - **Expiration timestamp:** 8 bytes
  - **User/account ID:** 8–16 bytes
  - **Access counters/analytics:** 4–16 bytes
  - **Status flags/booleans:** 1–2 bytes
  - **Other metadata (tags, custom alias, etc.):** 50–100 bytes
  - **Database overhead (indexing, alignment, etc.):** 50–100 bytes

  Adding these together, the total is typically around 450–470 bytes. Rounding up to 500 bytes provides a buffer for future extensibility and ensures the estimate is not too low. This approach is standard in capacity planning to avoid under-provisioning and to account for any additional fields or database storage overhead that may arise as the system evolves.

  **Note on Base-62 Encoding:**
  The short URL code is generated using base-62 encoding (using [A-Za-z0-9]), which is highly space-efficient. For example, with 8 characters, base-62 encoding can uniquely represent over 200 trillion URLs, which is more than enough for the estimated 30 billion records over 5 years. This encoding ensures that the short code remains compact and storage-efficient.

- **Total storage:** 30,000,000,000 × 500 bytes = 15,000,000,000,000 bytes = 15 TB

#### Math Explanation
- 500 million/month × 12 months/year × 5 years = 30 billion objects
- 30 billion × 500 bytes = 15,000,000,000,000 bytes = 15 TB

## Bandwidth Estimates
- **Write bandwidth:** 193 writes/sec × 500 bytes = 96,500 bytes/sec ≈ 94.3 KB/sec
- **Read bandwidth:** 19,290 reads/sec × 500 bytes = 9,645,000 bytes/sec ≈ 9.2 MB/sec

#### Math Explanation
- Write: 193 × 500 = 96,500 bytes/sec
- Read: 19,290 × 500 = 9,645,000 bytes/sec

## Memory Estimates (80/20 Rule)
- **80/20 rule:** 20% of URLs generate 80% of traffic
- **Popular URLs:** 20% of 30 billion = 6 billion
- **Traffic to popular URLs:** 80% of 50 billion = 40 billion redirections over 5 years
- **Popular URL redirections per second:** 40,000,000,000 / (5 × 2,592,000) ≈ 3,086/sec
- **Memory needed to cache popular URLs:** 6,000,000,000 × 500 bytes = 3,000,000,000,000 bytes = 3 TB

#### Math Explanation
- 20% of 30B = 6B
- 6B × 500 bytes = 3 TB

## Summary Table (Per Second Estimates)
| Metric                | Value                |
|-----------------------|---------------------|
| Write QPS             | 193/sec             |
| Read QPS              | 19,290/sec          |
| Write Bandwidth       | 94.3 KB/sec         |
| Read Bandwidth        | 9.2 MB/sec          |
| Storage (5 years)     | 15 TB               |
| Memory (popular URLs) | 3 TB                |

### Notes
- The system is read-heavy, with a 100:1 read/write ratio.
- Most traffic is concentrated on a small subset of URLs (80/20 rule).
- Bandwidth and memory estimates assume each object is 500 bytes.
- Duplicate requests for the same URL are common, justifying aggressive caching for popular URLs. 