from fastapi import FastAPI, Query, HTTPException, Request, Path, Body
from fastapi.responses import JSONResponse
from typing import Optional, List
from datetime import datetime, timedelta
import time
import uuid
import random

app = FastAPI(title="BookMyShow Cinema Ticket Booking API")

# In-memory API key store and throttling (for demo purposes)
API_KEYS = {"demo-key-1", "demo-key-2"}
THROTTLE_LIMIT = 10  # max requests per minute per key
THROTTLE_WINDOW = 60  # seconds
throttle_store = {}

# In-memory stores for demo
HOLD_STORE = {}
BOOKING_STORE = {}

# --- Utility functions ---
def check_throttle(api_dev_key: str):
    now = int(time.time())
    window = now // THROTTLE_WINDOW
    key = (api_dev_key, window)
    count = throttle_store.get(key, 0)
    if count >= THROTTLE_LIMIT:
        return False
    throttle_store[key] = count + 1
    return True

def validate_api_key(api_dev_key: str):
    if api_dev_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    if not check_throttle(api_dev_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

# --- Endpoints ---
@app.get("/api/v1/movies/search")
def search_movies(
    api_dev_key: str = Query(..., description="Developer API key for authentication/throttling"),
    keyword: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius: Optional[float] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    postal_code: Optional[str] = Query(None),
    spellcheck: Optional[bool] = Query(False),
    results_per_page: Optional[int] = Query(20, ge=1, le=100),
    sorting_order: Optional[str] = Query("rating", regex="^(asc|desc|rating)$"),
    page: Optional[int] = Query(1, ge=1)
):
    validate_api_key(api_dev_key)
    results = [
        {
            "movie_id": 123,
            "title": "Action Movie",
            "cinema": "Cinema Paris Centre",
            "city": city or "Paris",
            "show_time": "2024-07-01T20:00:00Z",
            "available_seats": 42,
            "rating": "PG-13"
        }
    ]
    return {
        "results": results,
        "pagination": {
            "page": page,
            "results_per_page": results_per_page,
            "total_results": 1
        }
    }

@app.get("/api/v1/cities")
def list_cities(api_dev_key: str = Query(...)):
    validate_api_key(api_dev_key)
    return {"cities": ["Paris", "London", "Berlin"]}

@app.get("/api/v1/cinemas")
def list_cinemas(api_dev_key: str = Query(...), city: str = Query(...)):
    validate_api_key(api_dev_key)
    return {"cinemas": [
        {"cinema_id": 1, "name": f"{city} Central Cinema"},
        {"cinema_id": 2, "name": f"{city} Grand Hall"}
    ]}

@app.get("/api/v1/cinemas/{cinema_id}/shows")
def list_shows(api_dev_key: str = Query(...), cinema_id: int = Path(...)):
    validate_api_key(api_dev_key)
    return {"shows": [
        {"show_id": 10, "movie_title": "Action Movie", "start_time": "2024-07-01T20:00:00Z", "end_time": "2024-07-01T22:00:00Z"},
        {"show_id": 11, "movie_title": "Comedy Night", "start_time": "2024-07-01T23:00:00Z", "end_time": "2024-07-02T01:00:00Z"}
    ]}

@app.get("/api/v1/shows/{show_id}/seats")
def list_seats(api_dev_key: str = Query(...), show_id: int = Path(...)):
    validate_api_key(api_dev_key)
    return {"seats": [
        {"seat_id": 1, "seat_number": "A1", "status": "available"},
        {"seat_id": 2, "seat_number": "A2", "status": "booked"},
        {"seat_id": 3, "seat_number": "A3", "status": "held"}
    ]}

@app.post("/api/v1/bookings/hold")
def hold_seats(
    body: dict = Body(...)
):
    api_dev_key = body.get("api_dev_key")
    show_id = body.get("show_id")
    seat_ids = body.get("seat_ids")
    if not api_dev_key or not show_id or not seat_ids:
        raise HTTPException(status_code=400, detail="Missing required fields")
    validate_api_key(api_dev_key)
    hold_id = str(uuid.uuid4())
    expires_at = (datetime.utcnow() + timedelta(minutes=5)).isoformat() + "Z"
    HOLD_STORE[hold_id] = {"show_id": show_id, "seat_ids": seat_ids, "expires_at": expires_at}
    return {"hold_id": hold_id, "expires_at": expires_at}

@app.post("/api/v1/bookings/confirm")
def confirm_booking(
    body: dict = Body(...)
):
    api_dev_key = body.get("api_dev_key")
    hold_id = body.get("hold_id")
    user_name = body.get("user_name")
    user_email = body.get("user_email")
    if not api_dev_key or not hold_id or not user_name or not user_email:
        raise HTTPException(status_code=400, detail="Missing required fields")
    validate_api_key(api_dev_key)
    hold = HOLD_STORE.get(hold_id)
    if not hold:
        raise HTTPException(status_code=400, detail="Invalid hold_id")
    booking_id = str(uuid.uuid4())
    BOOKING_STORE[booking_id] = {
        "user_name": user_name,
        "user_email": user_email,
        "seats": hold["seat_ids"],
        "status": "confirmed",
        "show_id": hold["show_id"],
        "cinema": "Demo Cinema",
        "movie_title": "Action Movie",
        "show_time": "2024-07-01T20:00:00Z"
    }
    return {"booking_id": booking_id, "status": "confirmed", "seats": hold["seat_ids"]}

@app.get("/api/v1/bookings/{booking_id}")
def get_booking(api_dev_key: str = Query(...), booking_id: str = Path(...)):
    validate_api_key(api_dev_key)
    booking = BOOKING_STORE.get(booking_id)
    if not booking:
        raise HTTPException(status_code=400, detail="Invalid booking_id")
    return {
        "booking_id": booking_id,
        **booking
    }

@app.post("/api/v1/reservations")
def reserve_seats(
    body: dict = Body(...)
):
    """
    Reserve one or more seats for a specific show.
    Parameters (in JSON body):
      - api_dev_key: str (required)
      - session_id: str (required)
      - movie_id: int (required)
      - show_id: int (required)
      - seats_to_reserve: List[str] (required)
    Returns JSON with:
      - status: 'success', 'failed', or 'retry'
      - message: str
      - reservation_id: str (if successful)
    """
    api_dev_key = body.get("api_dev_key")
    session_id = body.get("session_id")
    movie_id = body.get("movie_id")
    show_id = body.get("show_id")
    seats_to_reserve = body.get("seats_to_reserve")
    if not all([api_dev_key, session_id, movie_id, show_id, seats_to_reserve]):
        raise HTTPException(status_code=400, detail="Missing required fields")
    validate_api_key(api_dev_key)
    # Dummy logic: randomly fail, succeed, or ask to retry
    outcome = random.choice(["success", "failed", "retry"])
    if outcome == "success":
        reservation_id = str(uuid.uuid4())
        return {"status": "success", "message": "Reservation successful.", "reservation_id": reservation_id}
    elif outcome == "failed":
        return {"status": "failed", "message": "Reservation failed. Seats unavailable."}
    else:
        return {"status": "retry", "message": "Reservation failed - retry as other users are holding reserved seats."} 