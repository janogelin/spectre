w# TinyURL Telemetry & Statistics Design

## 1. Overview
Telemetry is essential for understanding usage patterns, diagnosing issues, and providing analytics to users. For TinyURL, telemetry focuses on redirection events and captures metadata such as country, timestamp, referral, and platform.

---

## 2. Data to Collect
For each redirection event, collect:
- **Short URL alias** (string)
- **Timestamp** (datetime, UTC)
- **Country** (string, derived from IP geolocation)
- **Referral** (string, HTTP referrer header, if available)
- **Platform** (string, user agent or device type)
- **IP address** (string, for geolocation and abuse detection)
- **User ID** (if authenticated, optional)

---

## 3. Storage Strategies
### a. NoSQL Event Store (Recommended)
- Use a time-series or event-oriented NoSQL database (e.g., Amazon DynamoDB, Amazon Timestream, or Aerospike).
- Each event is a separate record, allowing for high write throughput and easy analytics.

#### Example Schema
| Field         | Type      | Description                        |
|--------------|-----------|------------------------------------|
| alias        | string    | Short URL alias                    |
| timestamp    | datetime  | When the redirect occurred         |
| country      | string    | Country code (e.g., US, IN)        |
| referral     | string    | Referrer URL or platform           |
| platform     | string    | Device/browser info                |
| ip_address   | string    | Source IP address                  |
| user_id      | string    | User or API key (if available)     |

- **Partitioning:** Partition by alias and date for efficient queries (e.g., `alias#2024-06-12`).
- **TTL:** Optionally set TTL for telemetry data (e.g., retain for 1-2 years).

### b. Aggregated Statistics Table
- For fast analytics, maintain a separate table with aggregated stats (e.g., daily/weekly/monthly counts per alias, country, platform).
- Update aggregates asynchronously (e.g., via background jobs or stream processing).

#### Example Aggregated Schema
| Field         | Type      | Description                        |
|--------------|-----------|------------------------------------|
| alias        | string    | Short URL alias                    |
| date         | date      | Aggregation date                   |
| country      | string    | Country code                       |
| platform     | string    | Device/browser info                |
| referral     | string    | Referrer or platform               |
| count        | integer   | Number of redirections             |

---

## 4. Data Collection Flow
1. **Redirection request received**
2. **Extract telemetry:**
   - Parse headers for referrer, user agent, IP
   - Geolocate IP to country
   - Parse user agent for platform
3. **Write event:** Store event in telemetry/event table
4. **(Optional) Update aggregate:** Queue update for aggregate stats

---

## 5. Privacy & Compliance
- Mask or hash IP addresses if required by privacy laws (GDPR, CCPA)
- Allow users to opt out of analytics if needed
- Retain telemetry for a limited period (configurable TTL)

---

## 6. Example Event Record (JSON)
```json
{
  "alias": "abc123",
  "timestamp": "2024-06-12T14:23:45Z",
  "country": "US",
  "referral": "https://searchengine.com",
  "platform": "iOS/Safari",
  "ip_address": "203.0.113.42",
  "user_id": "user_42"
}
```

---

## 7. Query Examples
- Redirections by country for a given alias and date range
- Top referral sources for a short URL
- Platform/device breakdown for a user's links
- Time-series of redirection counts

---

## 8. Storage Options
- **Event Store:** DynamoDB, Timestream, Aerospike, or BigQuery
- **Aggregates:** DynamoDB, Redis (for hot stats), or RDBMS for reporting

---

## 9. Visualization & Analytics
- Use BI tools (e.g., AWS QuickSight, Grafana) for dashboards
- Expose analytics via REST API endpoints for users 