## REST API rate limiting

Rate limiting caps how many requests a client can make in a given time window. Without it, a single misbehaving client can starve everyone else.

### Algorithms

- Token bucket: allows short bursts above the average rate, then throttles. Most APIs use this.
- Sliding window: tracks requests across overlapping intervals for smoother enforcement.
- Fixed window: counts requests in discrete intervals. Simple to implement, but spiky at window boundaries.

### Response headers

Use these headers so clients can self-regulate:

- `X-RateLimit-Limit`: the max requests allowed per window
- `X-RateLimit-Remaining`: how many requests the client has left
- `X-RateLimit-Reset`: when the current window resets

Return `429 Too Many Requests` with a `Retry-After` header when a client exceeds their quota. Clients that respect `Retry-After` will back off automatically; clients that don't are the ones you needed rate limiting for in the first place.
