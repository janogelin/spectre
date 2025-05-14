# Pastebin Capacity Planning

## 1. Traffic Assumptions
- **New pastes per day:** 1,000,000
- **Read:Write ratio:** 5:1 (reads are 5x more common than writes)
- **Max paste size:** 10 MB
- **Average paste size:** 10 KB

---

## 2. Write and Read Rate Calculations

### New Pastes per Second
- **Daily writes:** 1,000,000
- **Seconds per day:** 86,400
- **Writes per second:**
  
  \[
  \text{Writes/sec} = \frac{1,000,000}{86,400} \approx 11.57
  \]
  
  **≈ 12 new pastes per second**

### Reads per Second
- **Read:Write ratio:** 5:1
- **Reads per day:** 5,000,000
- **Reads per second:**
  
  \[
  \text{Reads/sec} = \frac{5,000,000}{86,400} \approx 57.87
  \]
  
  **≈ 58 reads per second**

---

## 3. Storage Requirements

### Per Day
- **Average paste size:** 10 KB
- **New pastes per day:** 1,000,000
- **Storage per day:**
  
  \[
  1,000,000 \times 10\text{ KB} = 10,000,000\text{ KB} = 10,000\text{ MB} = 10\text{ GB}
  \]
  
  **≈ 10 GB per day**

### 10-Year Estimate
- **Days in 10 years:** 3,650
- **Total storage:**
  
  \[
  3,650 \times 10\text{ GB} = 36,500\text{ GB} = 36.5\text{ TB}
  \]
  
  **≈ 36.5 TB for 10 years**

---

## 4. Key Encoding Algorithm
- **Recommendation:** Use URL-safe Base62 encoding for keys (0-9, a-z, A-Z).

### Base62 vs Base64 Comparison

| Feature         | Base62                              | Base64                                 |
|----------------|-------------------------------------|----------------------------------------|
| Character Set  | 0-9, a-z, A-Z (62 chars)            | 0-9, a-z, A-Z, +, / (64 chars)         |
| URL-safe       | Yes (no special chars)              | No ("+" and "/" are not URL-safe)      |
| Padding        | None                                | Often uses '=' padding                 |
| Length         | Slightly longer than Base64         | Slightly shorter than Base62           |
| Readability    | High (no ambiguous/special chars)   | Lower (may include special chars)      |
| Usability      | Directly usable in URLs             | Needs encoding/escaping for URLs       |
| Implementation | Simple                              | Simple                                 |

#### Pros and Cons
- **Base62 Pros:**
  - Fully URL-safe without encoding or escaping
  - No padding characters
  - Readable and user-friendly
  - Good for short, shareable URLs
- **Base62 Cons:**
  - Slightly longer keys than Base64 for the same entropy

- **Base64 Pros:**
  - More compact (shorter) for the same entropy
  - Widely supported and standardized
- **Base64 Cons:**
  - Not URL-safe ("+" and "/" must be encoded)
  - May include padding ('=')
  - Less user-friendly for URLs

#### Why Base62 is Preferred
- Pastebin URLs must be short, user-friendly, and directly usable in browsers and APIs without further encoding.
- Base62 avoids special characters and padding, ensuring all keys are URL-safe and easy to share.
- The slight increase in key length is outweighed by the improved usability and safety for web links.

---

## 5. Bandwidth Estimates

### Write Requests
- **Average paste size:** 10 KB
- **Writes per second:** 12
- **Bandwidth for writes:**
  
  \[
  12 \times 10\text{ KB} = 120\text{ KB/sec}
  \]
  
  **≈ 120 KB/sec for write traffic**

### Read Requests
- **Reads per second:** 58
- **Bandwidth for reads:**
  
  \[
  58 \times 10\text{ KB} = 580\text{ KB/sec}
  \]
  
  **≈ 580 KB/sec for read traffic**

---

## 6. Memory and Caching Recommendations

### Memory Estimates
- **Active pastes in memory:** Assume caching the most recent 1 day of pastes (1,000,000 pastes)
- **Memory needed:**
  
  \[
  1,000,000 \times 10\text{ KB} = 10\text{ GB}
  \]
  
  **≈ 10 GB RAM for 1-day cache**

### Cache Recommendations
- **Cache size:** At least 10 GB (for 1 day of pastes). Increase if hot data is larger.
- **Eviction policy:** LRU (Least Recently Used) or TTL-based.
- **What to cache:**
  - Most recent and most frequently accessed pastes.
  - Metadata for analytics and quick lookups.
- **Technology:** Redis is recommended for its speed, TTL support, and scalability.

---

## 7. Summary Table
| Metric                | Value                | Notes                                  |
|---------------------- |---------------------|----------------------------------------|
| Writes/sec            | 12                  | 1M new pastes/day                      |
| Reads/sec             | 58                  | 5x writes                              |
| Storage/day           | 10 GB               | Avg 10 KB/paste                        |
| Storage/10 years      | 36.5 TB             |                                        |
| Write bandwidth       | 120 KB/sec          |                                        |
| Read bandwidth        | 580 KB/sec          |                                        |
| Cache size            | 10 GB               | 1 day of pastes                        |
| Key encoding          | Base62              | Compact, URL-safe, scalable            |

---

**All calculations assume average paste size of 10 KB. Actual requirements may be higher if users upload larger pastes or if metadata overhead is significant.** 