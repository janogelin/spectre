# Capacity Planning for BookMyShow Cinema Ticket Booking Service

## 1. Introduction
This document provides a detailed capacity planning analysis for the BookMyShow cinema ticket booking system, based on the requirements and traffic estimates found in `systemrequirements.txt` and the API design in the project files.

---

## 2. Traffic and Usage Estimates
**From systemrequirements.txt:**
- **Page views:** 3 billion per month
- **Tickets sold:** 10 million per month
- **Peak traffic:** Spikes expected for popular shows
- **Booking hold duration:** 5 minutes
- **Max seats per booking:** 10

### Derived Estimates
- **Days per month:** 30 (approximate)
- **Page views per day:** 3,000,000,000 / 30 = 100,000,000
- **Tickets per day:** 10,000,000 / 30 ≈ 333,333
- **Assume 10 page views per ticket sold (industry heuristic)**
- **Peak hour factor:** 10x average (to handle spikes)

---

## 3. Queries Per Second (QPS) Calculations
### Average QPS
- **Page views per second:**
  - 100,000,000 / 86,400 ≈ 1,157 QPS
- **Ticket sales per second:**
  - 333,333 / 86,400 ≈ 3.86 QPS

### Peak QPS (10x average)
- **Peak page view QPS:**
  - 1,157 × 10 = 11,570 QPS
- **Peak ticket sales QPS:**
  - 3.86 × 10 ≈ 39 QPS

### API Endpoint QPS (Estimate)
- **/movies/search, /cities, /cinemas, /shows, /seats:**
  - Assume 90% of page views are search/browse: 1,041 QPS avg, 10,410 QPS peak
- **/bookings/hold, /bookings/confirm:**
  - Assume 2x ticket sales QPS (holds + confirmations): 7.7 QPS avg, 77 QPS peak

---

## 4. Concurrency and Queueing
### Little's Law
- **L = λ × W**
  - L = average number of concurrent users
  - λ = arrival rate (QPS)
  - W = average time in system (seconds)
- **Booking holds:**
  - λ = 7.7 QPS (avg), W = 5 min = 300 sec
  - L = 7.7 × 300 ≈ 2,310 concurrent holds (avg)
  - Peak: 77 × 300 = 23,100 concurrent holds

---

## 5. Storage Estimates
- **Booking records:** 10 million/month × 12 = 120 million/year
- **Hold records:** Short-lived, but peak concurrent holds ≈ 23,100
- **User records:** Assume 10 million users (1 per ticket, upper bound)
- **Movie, cinema, show, seat records:** Orders of thousands, negligible compared to bookings
- **Estimated DB size:**
  - Bookings: 120M × ~1KB = ~120GB/year
  - Holds: 23,100 × ~0.5KB = ~12MB (transient)
  - Users: 10M × ~0.5KB = ~5GB
  - Total (year 1): ~125GB (plus indexes, logs, etc.)

---

## 6. Algorithms and Methods Used
- **Peak Factor:** Multiplies average by 10 to account for spikes (industry standard for ticketing/events)
- **Little's Law:** For concurrency estimation (L = λ × W)
- **Percentile Analysis:** (not shown, but recommended for latency/SLA planning)
- **Queueing Theory:** For wait/hold logic and fair queuing
- **Heuristics:** 10 page views per ticket, 1 user per ticket (upper bound)

---

## 7. Recommendations
- **Web/API Layer:**
  - Scale stateless API servers horizontally to handle 12,000+ QPS at peak
  - Use caching (CDN, Redis) for search/browse endpoints
  - Rate limit and throttle abusive clients
- **Database Layer:**
  - Use a scalable, ACID-compliant RDBMS (e.g., PostgreSQL, MySQL)
  - Partition bookings by time or region for scale
  - Use in-memory store (Redis) for holds and seat locks
- **Queueing:**
  - Use fair, FIFO queues for booking holds and expirations
- **Monitoring:**
  - Track QPS, latency, error rates, and hold expirations
- **Capacity Review:**
  - Revisit estimates quarterly and after major events

---

## 8. Example Calculation: Peak Day
- **Peak page views:** 100M × 10 = 1B (on a blockbuster release)
- **Peak QPS:** 11,570
- **Peak concurrent holds:** 23,100
- **DB write rate:** 39 QPS (peak ticket sales)

---

## 9. Assumptions & References
- All numbers from `systemrequirements.txt` and README
- Industry heuristics for web traffic and ticketing
- All calculations rounded for clarity

---

## 10. Conclusion
This plan provides a robust starting point for infrastructure sizing, with headroom for spikes and growth. All calculations and algorithms are documented for transparency and future review. 