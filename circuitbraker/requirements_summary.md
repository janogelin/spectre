# Circuit Breaker Requirements Summary

## Non-Functional Requirements

- **Fault Rate Threshold:** The system must ensure the rate of faults remains below a specified threshold to maintain reliability.
- **Failure Counting:** The circuit breaker should count failures to determine when to trip.
- **Trip Threshold:** The circuit breaker trips (opens) after 5 failed requests.
- **Open State Duration:** The circuit remains open (tripped) for 60 seconds before attempting to reset.
- **Trip Request Count:** The circuit can also trip after 10 failed requests, even if not consecutive.
- **Reset Request Count:** After the open period, 10 requests are allowed in half-open state to test recovery.

## Considerations

- **Library Evaluation:** Consider using established libraries such as Resilience4j, Polly, or Hystrix for robust implementations.
- **Health Checks:** Integrate health checks to monitor the circuit breaker and underlying services.
- **Thread Safety:** The circuit breaker must be thread-safe to handle concurrent requests in multi-threaded environments.

## Actions When Circuit Breaker is Tripped

- **Log the Event:** Record the tripping event for monitoring and debugging.
- **Stop Sending Requests:** Prevent further requests to the failed service to avoid cascading failures.
- **Notify Operations Team:** Alert the operations team for investigation and remediation.
- **Cooldown and Retry:** After the cooldown period, reduce the cooldown by half and attempt to reconnect.

## Actions When Circuit Breaker Rejects a Request

- **Log the Event:** Record the rejection for observability.
- **Buffer the Request:** Temporarily store the request for later retry. This helps prevent data loss but requires careful management to avoid memory issues.
- **Fail Over to Backup Service:** Route the request to a backup or redundant service if available, improving system resilience.
- **Fallback to Cached Response:** Serve a cached or default response to maintain user experience during outages.
- **Apply Backpressure Up the Call Stack:**
  - **Explanation:** Backpressure is a technique to signal upstream components to slow down or stop sending requests when the system is overloaded or unable to process more requests. This prevents resource exhaustion and helps maintain system stability. Backpressure can be implemented by:
    - Returning error responses (e.g., HTTP 429 Too Many Requests)
    - Blocking or delaying new requests
    - Using flow control mechanisms (e.g., reactive streams, queues)
    - Propagating signals to clients or upstream services to reduce their request rate
  - **Benefits:**
    - Prevents overload and cascading failures
    - Maintains quality of service for accepted requests
    - Encourages graceful degradation under high load
- **Cancel the Request:** Drop the request if it cannot be processed or buffered, freeing up resources.
- **Retry After Cooldown:** Attempt the request again after the cooldown period. If it fails, retry after half the cooldown period.
- **Notify Operations Team:** If repeated retries fail, escalate the issue to the operations team.
- **Return Fallback Response:** As a last resort, return a fallback or default response to the client.

## Detailed Explanations

### Buffering
Buffering involves temporarily storing requests that cannot be processed immediately due to the circuit breaker being open. This allows the system to retry these requests later. However, buffering must be managed carefully to avoid excessive memory usage or data loss. Strategies include limiting buffer size, using persistent storage, and discarding old or low-priority requests.

### Failover
Failover is the process of redirecting requests to a backup or redundant service when the primary service is unavailable. This increases system availability and resilience. The backup service should be kept in sync and tested regularly to ensure reliability during failover events.

### Fallback
Fallback mechanisms provide alternative responses when the primary service is unavailable. This can include serving cached data, default values, or user-friendly error messages. Fallbacks help maintain a good user experience during outages or failures.

### Thread Safety
Thread safety ensures that the circuit breaker can handle multiple concurrent requests without race conditions or inconsistent state. This is typically achieved using synchronization primitives (e.g., locks, atomic variables) or by using thread-safe libraries.

### Backpressure (In-Depth)
Backpressure is critical in distributed systems to prevent overload and maintain stability. When the circuit breaker is open or the system is under heavy load, backpressure signals upstream components to slow down or stop sending requests. This can be implemented using:
- **Rate Limiting:** Restrict the number of incoming requests per unit time.
- **Queue Management:** Limit the size of request queues and reject or delay excess requests.
- **Flow Control Protocols:** Use protocols that support flow control, such as TCP or reactive streams.
- **Error Signaling:** Return specific error codes (e.g., HTTP 429) to inform clients to back off.

Proper backpressure management helps prevent resource exhaustion, improves system reliability, and enables graceful degradation during high load or failure scenarios. 