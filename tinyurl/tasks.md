# TinyURL Service: Task List

## 1. Project Setup
- [ ] Initialize a new Git repository for the project.
- [ ] Create a monorepo or separate folders for API, database, cache, and telemetry components.
- [ ] Set up a `docker-compose.yml` for local development.

## 2. API Service (FastAPI + Uvicorn)
- [ ] Scaffold a FastAPI project for the URL shortener API.
- [ ] Implement endpoints:
  - [ ] `POST /api/v1/urls` (create short URL)
  - [ ] `DELETE /api/v1/urls/{alias}` (delete short URL)
  - [ ] `GET /{alias}` (redirect)
  - [ ] `GET /api/v1/analytics/{alias}` (telemetry/analytics)
- [ ] Add request validation and error handling.
- [ ] Add authentication (API key or JWT).
- [ ] Write Dockerfile for the API service.
- [ ] Add API service to `docker-compose.yml`.

## 3. Database Layer (NoSQL: Aerospike or DynamoDB)
- [ ] For local dev, use Aerospike (Docker image) or DynamoDB Local.
- [ ] Define data models for:
  - [ ] URL mapping
  - [ ] Telemetry events
  - [ ] Aggregated statistics
- [ ] Implement database access layer in the API service.
- [ ] Add Aerospike/DynamoDB service to `docker-compose.yml` (if using Aerospike).

## 4. Caching Layer (Memcached + mcrouter)
- [ ] Add Memcached and mcrouter services to `docker-compose.yml`.
- [ ] Integrate cache read/write in API service for redirection lookups.
- [ ] Implement lazy loading and LRU eviction policy.

## 5. Telemetry & Analytics
- [ ] Implement telemetry event logging on each redirect.
- [ ] Store telemetry events in the event store (NoSQL).
- [ ] Implement background job (could be a separate service or cron job) for aggregating statistics.
- [ ] Expose analytics endpoints in the API.

## 6. Background Jobs
- [ ] Implement cleanup job for:
  - [ ] Purging expired links (older than 2 years)
  - [ ] Removing links not accessed for 6 months
- [ ] Schedule jobs using cron or as a separate Dockerized service.

## 7. Monitoring & Logging
- [ ] Integrate logging (stdout, file, or external service).
- [ ] Add health check endpoints.
- [ ] Optionally, add Prometheus/Grafana for metrics (add to `docker-compose.yml`).

## 8. Object Storage (Optional, for large payloads)
- [ ] Integrate with AWS S3 or MinIO (for local dev, Docker image).
- [ ] Add S3/MinIO service to `docker-compose.yml` if needed.

## 9. Testing
- [ ] Write unit and integration tests for API endpoints.
- [ ] Add tests for database and cache integration.
- [ ] Add tests for telemetry and analytics.

## 10. Documentation
- [ ] Document API endpoints (OpenAPI/Swagger).
- [ ] Document system architecture and data flows.
- [ ] Add README with setup and usage instructions.

## 11. Deployment
- [ ] Create production-ready Dockerfiles for all services.
- [ ] Set up CI/CD pipeline (GitHub Actions, GitLab CI, etc.).
- [ ] Prepare for deployment to AWS (ECS, Lambda, or EC2). 