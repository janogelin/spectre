# BookMyShow Cinema Ticket Booking API

## Overview
This project provides a RESTful API for searching movies, booking tickets, and managing cinema information. It uses FastAPI and follows the OpenAPI 3.0 specification.

## Features
- Search for movies and shows by keyword, city, location, time, and more
- List cities, cinemas, shows, and seats
- Hold and confirm seat bookings
- Developer API key (`api_dev_key`) for authentication and throttling
- Returns results in JSON format
- OpenAPI (Swagger) documentation available

## Requirements
- Python 3.8+
- FastAPI
- Uvicorn

## Installation
```bash
pip install fastapi uvicorn
```

## Running the API
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation
Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Key and Throttling
- Every request must include a valid `api_dev_key` (see `app.py` for demo keys).
- Throttling: Max 10 requests per minute per key (in-memory, for demo only).

## Endpoints & Example Usage

### 1. Search Movies
```
GET /api/v1/movies/search?api_dev_key=demo-key-1&keyword=action&city=Paris
```

### 2. List Cities
```
GET /api/v1/cities?api_dev_key=demo-key-1
```
Response:
```json
{"cities": ["Paris", "London", "Berlin"]}
```

### 3. List Cinemas in a City
```
GET /api/v1/cinemas?api_dev_key=demo-key-1&city=Paris
```
Response:
```json
{"cinemas": [
  {"cinema_id": 1, "name": "Paris Central Cinema"},
  {"cinema_id": 2, "name": "Paris Grand Hall"}
]}
```

### 4. List Shows in a Cinema
```
GET /api/v1/cinemas/1/shows?api_dev_key=demo-key-1
```
Response:
```json
{"shows": [
  {"show_id": 10, "movie_title": "Action Movie", "start_time": "2024-07-01T20:00:00Z", "end_time": "2024-07-01T22:00:00Z"},
  {"show_id": 11, "movie_title": "Comedy Night", "start_time": "2024-07-01T23:00:00Z", "end_time": "2024-07-02T01:00:00Z"}
]}
```

### 5. List Seats for a Show
```
GET /api/v1/shows/10/seats?api_dev_key=demo-key-1
```
Response:
```json
{"seats": [
  {"seat_id": 1, "seat_number": "A1", "status": "available"},
  {"seat_id": 2, "seat_number": "A2", "status": "booked"},
  {"seat_id": 3, "seat_number": "A3", "status": "held"}
]}
```

### 6. Hold Seats for a Show
```
POST /api/v1/bookings/hold
Content-Type: application/json
{
  "api_dev_key": "demo-key-1",
  "show_id": 10,
  "seat_ids": [1, 3]
}
```
Response:
```json
{"hold_id": "<uuid>", "expires_at": "2024-07-01T20:05:00Z"}
```

### 7. Confirm Booking
```
POST /api/v1/bookings/confirm
Content-Type: application/json
{
  "api_dev_key": "demo-key-1",
  "hold_id": "<hold_id>",
  "user_name": "Alice",
  "user_email": "alice@example.com"
}
```
Response:
```json
{"booking_id": "<uuid>", "status": "confirmed", "seats": [1, 3]}
```

### 8. Get Booking Details
```
GET /api/v1/bookings/<booking_id>?api_dev_key=demo-key-1
```
Response:
```json
{
  "booking_id": "<uuid>",
  "user_name": "Alice",
  "user_email": "alice@example.com",
  "seats": [1, 3],
  "status": "confirmed",
  "show_id": 10,
  "cinema": "Demo Cinema",
  "movie_title": "Action Movie",
  "show_time": "2024-07-01T20:00:00Z"
}
```

### 9. Reserve Seats for a Show
```
POST /api/v1/reservations
Content-Type: application/json
{
  "api_dev_key": "demo-key-1",
  "session_id": "session-xyz",
  "movie_id": 123,
  "show_id": 10,
  "seats_to_reserve": ["A1", "A2"]
}
```
Possible Responses:
- Success:
```json
{
  "status": "success",
  "message": "Reservation successful.",
  "reservation_id": "<uuid>"
}
```
- Failed (seats unavailable):
```json
{
  "status": "failed",
  "message": "Reservation failed. Seats unavailable."
}
```
- Retry (seats held by others):
```json
{
  "status": "retry",
  "message": "Reservation failed - retry as other users are holding reserved seats."
}
```

## OpenAPI Specification
See `openapi.yaml` for the full API schema.

## Notes
- This is a demo implementation. For production, use a persistent store for API keys and throttling, and connect to a real database for movie data.

## Active Reservation Service

The **Active Reservation Service** is responsible for tracking all current seat holds and reservations in real time. It ensures that:
- No two users can hold or book the same seat at the same time.
- Holds expire after a fixed duration (e.g., 5 minutes), releasing seats for others.
- Waiting users can be notified when a seat becomes available.

### In-Memory Data Structure: Linked HashMap
To efficiently manage active reservations, the service uses a data structure similar to a **linked hashmap** (e.g., Python's `OrderedDict`):
- **Key:** (show_id, seat_number)
- **Value:** Reservation details (user/session, hold timestamp, expiry, etc.)
- **Order:** Maintains insertion order, allowing fast removal of expired holds from the front.
- **Operations:**
  - **Insert:** O(1) to add a new hold.
  - **Lookup:** O(1) to check if a seat is held or available.
  - **Expire:** O(1) to remove expired holds from the head.

This approach allows the service to:
- Quickly check seat availability for any show.
- Efficiently expire old holds and notify waiting users.
- Scale to thousands of concurrent holds with minimal latency.

For distributed deployments, this structure can be implemented in a shared in-memory store (e.g., Redis with sorted sets or streams) to maintain consistency across API servers.

---

## Reservation Expiration Algorithm

Reservation expiration is handled efficiently using the linked hashmap structure:
- Holds are inserted with an expiry timestamp.
- On each new hold, booking, or periodic cleanup, the service scans from the front of the hashmap and removes all expired holds (O(1) per expired hold).
- This ensures that only valid, non-expired holds remain in memory, and seats are released promptly for other users.

**Pseudocode Example:**
```python
from collections import OrderedDict
import time

holds = OrderedDict()  # key: (show_id, seat_number), value: (user, expiry_time)

def expire_holds():
    now = time.time()
    while holds:
        key, (user, expiry) = next(iter(holds.items()))
        if expiry < now:
            holds.popitem(last=False)  # Remove from front
        else:
            break  # All remaining holds are not expired
```

---

## Waiting User Service

The **Waiting User Service** manages users who wish to book seats that are currently held by others. It ensures fairness and notifies users when seats become available.

### Data Structure: Queue per Seat
- For each (show_id, seat_number), maintain a **queue** of waiting users (FIFO order).
- When a user attempts to hold a seat that is already held, they are added to the queue for that seat.
- When a hold expires or is released, the service checks the queue and notifies the next waiting user.

**Operations:**
- **Join Waitlist:** O(1) to append user to the queue.
- **Notify Next:** O(1) to pop and notify the next user when a seat is released.
- **Remove:** O(1) to remove a user if they cancel or timeout.

**Pseudocode Example:**
```python
from collections import deque

wait_queues = {}  # key: (show_id, seat_number), value: deque of user_ids

def join_waitlist(show_id, seat_number, user_id):
    q = wait_queues.setdefault((show_id, seat_number), deque())
    q.append(user_id)

def notify_next(show_id, seat_number):
    q = wait_queues.get((show_id, seat_number))
    if q and q:
        next_user = q.popleft()
        # send notification to next_user
```

### Fairness and Notification
- The FIFO queue ensures **first-come, first-served** access to released seats.
- Notification can be via email, push, or in-app message.
- The system can implement timeouts for waiting users to respond before offering the seat to the next in line.

---

## Service Interactions
- **Active Reservation Service** manages current holds and bookings.
- **Reservation Expiration** ensures holds are released promptly.
- **Waiting User Service** manages queues and notifications for users waiting on held seats.
- When a hold expires, the Active Reservation Service triggers the Waiting User Service to notify the next user in line.

This design ensures high fairness, responsiveness, and scalability for high-traffic ticketing scenarios.

---

## Preventing Double-Booking: Concurrency Control for Seat Reservations

Concurrency is critical in ticketing systems to ensure that **no two users can book the same seat**. The BookMyShow design addresses this at multiple levels:

### 1. Active Reservation Service (Source of Truth)
- All seat holds and bookings are tracked in the Active Reservation Service.
- Before a seat is held or booked, the service checks if it is already held or booked.

### 2. Atomic Operations and Locking
#### **In-Memory (Single Instance)**
- The linked hashmap (e.g., `OrderedDict`) is accessed atomically (using a lock or single-threaded event loop).
- **Pseudocode Example:**
```python
import threading
lock = threading.Lock()

def try_hold_seat(show_id, seat_number, user_id, expiry_time):
    with lock:
        expire_holds()
        key = (show_id, seat_number)
        if key in holds:
            return "Seat already held/booked"
        holds[key] = (user_id, expiry_time)
        return "Hold successful"
```

#### **Distributed (Multi-Instance, e.g., Redis)**
- Use a distributed lock or atomic operation in a shared store (e.g., Redis).
- **Redis Example (Lua script for atomicity):**
```lua
-- KEYS[1] = seat key, ARGV[1] = user_id, ARGV[2] = expiry timestamp
if redis.call('EXISTS', KEYS[1]) == 0 then
    redis.call('SET', KEYS[1], ARGV[1])
    redis.call('PEXPIREAT', KEYS[1], ARGV[2])
    return 'Hold successful'
else
    return 'Seat already held/booked'
end
```
- This ensures only one user can hold/book a seat at a time, even across multiple servers.

### 3. Database Constraints (Final Consistency)
- The bookings table enforces a unique constraint on (show_id, seat_id).
- If two requests try to book the same seat at the same time, only one will succeed; the other will get a constraint violation.
- **SQL Example:**
```sql
ALTER TABLE bookings ADD CONSTRAINT unique_show_seat UNIQUE (show_id, seat_id);
```

### 4. Algorithmic Flow
1. User requests to hold/book a seat.
2. Expire old holds.
3. Check seat status:
   - If available: mark as held/booked and proceed.
   - If held/booked: reject or add user to waitlist.
4. (On booking) Write to database with unique constraint.
5. Notify user of success or failure.

### 5. Summary
- **No two users can book the same seat** because:
  - All seat status changes are atomic (in-memory or distributed).
  - The system always checks the current status before allowing a hold/booking.
  - The database enforces uniqueness as a final safeguard.
  - Expired holds are promptly removed, so only valid holds are considered.

This multi-layered approach ensures robust concurrency control and fairness for all users. 