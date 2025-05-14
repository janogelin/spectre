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