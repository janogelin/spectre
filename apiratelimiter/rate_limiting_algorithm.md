# Rate Limiting Algorithm Design

## 1. User Identification

- **UserID Generation:**
  - Concatenate the user's email and IP address (e.g., `user@example.com_192.168.1.1`).
  - Hash this string (e.g., using SHA-256) to create a unique, privacy-preserving user identifier.

  ```python
  import hashlib

  def get_userid(email, ip):
      raw = f"{email}_{ip}"
      return hashlib.sha256(raw.encode()).hexdigest()
  ```

---

## 2. Algorithm Choice: Fixed Window Counter

- **Why:** Simple, efficient, and fits the "3 requests per minute" requirement.
- **How it works:**
  - For each user, keep a counter and a timestamp for the start of the current window (minute).
  - On each request:
    - If the current time is within the same minute window, increment the counter.
    - If the counter exceeds 3, reject the request.
    - If the minute has changed, reset the counter and timestamp.

---

## 2a. Algorithm Choice: Sliding Window Counter

The Sliding Window algorithm addresses some of the limitations of the Fixed Window Counter by providing smoother rate limiting and reducing burstiness at window boundaries.

### How it Works
- For each user, maintain a list (or queue) of timestamps for their recent requests.
- On each request:
  - Remove timestamps older than the window (e.g., 60 seconds) from the list.
  - If the list contains fewer than the allowed number of requests (e.g., 3), allow the request and add the current timestamp.
  - If the list already contains the maximum allowed requests, reject the request.

### Pseudocode
```python
import time
import redis
import json

WINDOW_SIZE = 60  # seconds
MAX_REQUESTS = 3

r = redis.Redis(host='localhost', port=6379, db=0)

def is_allowed_sliding(email, ip):
    userid = get_userid(email, ip)
    key = f"rate_limit_sw:{userid}"
    now = int(time.time())
    # Get the list of timestamps
    data = r.get(key)
    if data:
        timestamps = json.loads(data)
    else:
        timestamps = []
    # Remove timestamps outside the window
    timestamps = [ts for ts in timestamps if now - ts < WINDOW_SIZE]
    if len(timestamps) < MAX_REQUESTS:
        timestamps.append(now)
        r.set(key, json.dumps(timestamps), ex=WINDOW_SIZE)
        return True
    else:
        return False

---

## 2b. Algorithm Choice: Sliding Window with Counters

The Sliding Window with Counters algorithm is an efficient approximation of the true sliding window, using two adjacent fixed windows and linear interpolation to estimate the request rate.

### Further Details
- The algorithm divides time into contiguous, non-overlapping windows (e.g., every minute at 00:00, 00:01, etc.).
- Each user has two counters: one for the current window and one for the previous window.
- When a request arrives, the algorithm calculates how far into the current window the request is, and uses this to weight the previous window's count.
- This approach provides a close approximation to a true sliding window, but with much lower memory and computational overhead than storing all timestamps.
- Expiry for counters is set to twice the window size to ensure both current and previous window counters are available for calculation.

### Diagram

```
Time (seconds) →
|<--- Previous Window --->|<--- Current Window --->|
|------------------------|------------------------|
^                        ^                        ^
0                        60                       120

Suppose now = 75 seconds:
- Current window: 60-120s
- Previous window: 0-60s
- Elapsed in current window: 15s
- Weight for previous window: (60-15)/60 = 0.75

Total = curr_count + prev_count * 0.75
```

### Summary Table: Algorithm Comparison

| Algorithm                  | Memory per User | Burstiness | Accuracy | Complexity | Best Use Case                |
|----------------------------|----------------|------------|----------|------------|------------------------------|
| Fixed Window               | 1 counter      | High       | Low      | Low        | Simplicity, low memory       |
| Sliding Window (timestamps)| N timestamps   | Low        | High     | Medium     | Precise, small N             |
| Sliding Window w/ Counters | 2 counters     | Low-Med    | Med-High | Low        | Large scale, good accuracy   |

---

## 3. Data Store

- Use a fast, in-memory store like **Redis** for distributed environments.
- Store per-user counters with TTL (time-to-live) of 1 minute.
  - **Key:** `rate_limit:{userid}`
  - **Value:** Integer (number of requests in current window)
  - **TTL:** 60 seconds

---

## 4. Algorithm Pseudocode

```python
import time
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def is_allowed(email, ip):
    userid = get_userid(email, ip)
    key = f"rate_limit:{userid}"
    current_count = r.get(key)
    if current_count is None:
        # First request in this window
        r.set(key, 1, ex=60)  # Set count to 1, expire in 60s
        return True
    elif int(current_count) < 3:
        r.incr(key)
        return True
    else:
        return False
```

---

## 5. Example Flow

1. **User:** `alice@example.com` from `10.0.0.1`
   - UserID: `hash("alice@example.com_10.0.0.1")`
2. **First request:**
   - No key in Redis → allow, set to 1, TTL 60s.
3. **Second/Third request (within same minute):**
   - Counter increments to 2, then 3 → allow.
4. **Fourth request (within same minute):**
   - Counter is 3 → reject (HTTP 429).
5. **After 60 seconds:**
   - Key expires, user can make requests again.

---

## 6. Advantages

- **Simplicity:** Easy to implement and reason about.
- **Performance:** Fast, O(1) Redis operations.
- **Scalability:** Works across distributed systems if all nodes use the same Redis cluster.
- **Privacy:** UserID is hashed, so email/IP are not stored in plaintext.

---

## 7. Possible Improvements

- **Sliding Window:** For smoother enforcement (avoids bursts at window edges).
- **Token Bucket:** For bursty traffic with refill rate.
- **Customizable Limits:** Store per-user or per-plan limits.

---

## 8. Problems and Limitations

While the Fixed Window Counter algorithm is simple and efficient, it has several notable limitations:

### 1. Burstiness at Window Boundaries
- **Issue:** A user can make 3 requests at the very end of one minute and 3 more at the very start of the next minute, resulting in 6 requests in a very short time (just over a minute).
- **Impact:** This can allow short bursts of traffic that exceed the intended rate limit, potentially overloading the system.

### 2. No Smoothing of Request Rate
- **Issue:** The algorithm enforces limits only within discrete time windows (e.g., per minute), not across them.
- **Impact:** There is no smoothing or spreading of requests, so usage can be spiky rather than evenly distributed.

### 3. Potential for Clock Skew
- **Issue:** In distributed systems, if different servers have slightly different clocks, the window boundaries may not align perfectly.
- **Impact:** This can lead to inconsistent enforcement of rate limits across servers.

### 4. No Support for Bursty Traffic
- **Issue:** The algorithm is strict—once the limit is hit, all further requests are blocked until the window resets.
- **Impact:** Users cannot make occasional bursts of requests, even if their overall average rate is within limits.

### 5. Lack of Granularity
- **Issue:** The window size is fixed (e.g., 1 minute). If you want to change the rate limit granularity (e.g., per 10 seconds), you need to reconfigure the system and possibly lose accuracy.
- **Impact:** Not flexible for use cases requiring finer control.

### 6. No Differentiation by Endpoint or Action
- **Issue:** The example only limits by user (email+IP). If you want to limit by endpoint, action, or other dimensions, the logic must be extended.
- **Impact:** May not be sufficient for APIs with different rate limits for different actions.

### 7. Redis Key Expiry Race Condition
- **Issue:** If two requests from the same user arrive at nearly the same time and the key does not exist, both may try to set the key, potentially allowing more than the allowed number of requests.
- **Impact:** This is a classic race condition in distributed systems.

---

### Summary Table

| Problem                        | Description/Impact                                      |
|--------------------------------|--------------------------------------------------------|
| Burstiness at boundaries       | Allows more requests in short bursts                    |
| No smoothing                   | Requests are not evenly distributed                     |
| Clock skew                     | Inconsistent limits in distributed systems              |
| No burst support               | Occasional bursts are not allowed                       |
| Lack of granularity            | Not flexible for sub-minute limits                      |
| No endpoint differentiation    | Cannot set different limits for different actions       |
| Redis race condition           | May allow more than N requests due to concurrency       |

---

**To address these issues, consider using algorithms like Sliding Window, Token Bucket, or Leaky Bucket, which provide smoother and more flexible rate limiting.** 