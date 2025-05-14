# TinyURL Service Requirements

## Functional Requirements
1. Given a URL, the service should generate a shorter and unique alias of it. This is called a short link. This link should be short enough to be easily copied and pasted into applications.
2. When users access a short link, the service should redirect them to the original link.
3. Users should optionally be able to pick a custom short URL link for their URL.
4. Links will expire after a standard default timespan. Users should be able to specify the expiration time.

## Non-Functional Requirements
1. The system should be highly available. We do not want the redirections to start failing.
2. URL redirection should happen in real-time with minimal latency.
3. Shortened links should not be guessable (not predictable).

## Extended Requirements
1. Analytics; e.g., how many times a redirection happened.
2. Our service should also be accessible through the REST APIs by other services. 