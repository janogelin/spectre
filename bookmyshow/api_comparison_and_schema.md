# API Comparison: REST vs SOAP for Cinema Ticket Booking Service

## REST API
- **Lightweight**: Uses HTTP and JSON, making it fast and easy to use for web and mobile clients.
- **Stateless**: Each request contains all information needed, supporting high concurrency and scalability.
- **Flexible**: Easily supports modern web/mobile apps and can be cached at HTTP level.
- **Widespread Adoption**: Most developers are familiar with REST, and tooling is abundant.
- **Easy Throttling**: API keys (like `api_dev_key`) can be used for rate limiting and abuse prevention.

## SOAP API
- **Heavyweight**: Uses XML and strict standards, which can be slower and more complex.
- **Stateful or Stateless**: Can support both, but stateful operations are more common.
- **Enterprise Focused**: Better for complex transactions and strict contracts, but overkill for public-facing, high-traffic APIs.
- **Less Flexible**: Harder to integrate with modern web/mobile apps.
- **Throttling**: Possible, but more complex to implement and manage.

## Recommendation
Given the system requirements (high concurrency, high availability, web/mobile focus, and need for throttling), **REST is recommended** for this service.

---

# Suggested REST API Schema

## Authentication & Throttling
- Every request must include an `api_dev_key` (string) in the header or as a query parameter.
- This key is used to identify the developer and apply rate limits.

## Example Endpoint: Search Movies

### Endpoint
```
GET /api/v1/movies/search
```

### Query Parameters
| Name             | Type    | Required | Description                                      |
|------------------|---------|----------|--------------------------------------------------|
| api_dev_key      | string  | Yes      | Developer API key for authentication/throttling   |
| keyword          | string  | No       | Keyword to search for (movie title, etc.)         |
| city             | string  | No       | Filter movies by city                             |
| latitude         | float   | No       | Latitude for geo-filtering                        |
| longitude        | float   | No       | Longitude for geo-filtering                       |
| radius           | float   | No       | Radius (km) for area search                       |
| start_time       | string  | No       | ISO8601 start time for movie show                 |
| end_time         | string  | No       | ISO8601 end time for movie show                   |
| postal_code      | string  | No       | Postal code to filter by                          |
| spellcheck       | boolean | No       | Enable spellcheck (true/false)                    |
| results_per_page | int     | No       | Number of results per page (pagination)           |
| sorting_order    | string  | No       | Sorting order (e.g., 'asc', 'desc', 'rating')     |
| page             | int     | No       | Page number for pagination                        |

### Example Request
```
GET /api/v1/movies/search?api_dev_key=YOUR_KEY&keyword=action&city=Paris&latitude=48.8566&longitude=2.3522&radius=10&start_time=2024-07-01T18:00:00Z&end_time=2024-07-01T23:00:00Z&postal_code=75001&spellcheck=true&results_per_page=20&sorting_order=rating&page=1
```

### Example JSON Response
```json
{
  "results": [
    {
      "movie_id": 123,
      "title": "Action Movie",
      "cinema": "Cinema Paris Centre",
      "city": "Paris",
      "show_time": "2024-07-01T20:00:00Z",
      "available_seats": 42,
      "rating": "PG-13"
    }
    // ... more results ...
  ],
  "pagination": {
    "page": 1,
    "results_per_page": 20,
    "total_results": 120
  }
}
```

---

## Why REST?
- Simpler, faster, and more scalable for high-traffic, public-facing APIs.
- JSON is natively supported by browsers and mobile apps.
- Easy to implement throttling and monitoring using API keys. 