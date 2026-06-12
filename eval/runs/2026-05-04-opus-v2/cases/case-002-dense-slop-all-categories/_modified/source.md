Microservices split an application into small, independently deployable services that communicate over the network. Each service owns its data and runs in its own process.

The main benefit is independent deployment. Teams ship changes to one service without coordinating a release across the whole system. At Uber, this meant going from weekly monolith deploys to thousands of production changes per day, though they've since written extensively about the operational cost that came with it.

Independent scaling is real but often oversold. Most services in a typical system don't have meaningfully different load profiles. You can scale a single hot service without touching the rest, which matters when it matters, but that's fewer services than people assume.

The tradeoffs are concrete:

- Network calls replace function calls. Latency goes up. You need retries, timeouts, and circuit breakers where you previously needed nothing.
- Data consistency gets harder. Transactions that used to be a single database commit now span services. You end up building sagas or accepting eventual consistency.
- Debugging a request that touches six services requires distributed tracing. Without it, you're reading logs from six different systems and guessing at causality.
- Every service needs its own CI/CD pipeline, monitoring, and on-call rotation. The operational overhead scales with the number of services, not the number of engineers.

Microservices make sense when teams are large enough that coordination costs dominate. For a team of five, a well-structured monolith is almost always simpler. Sam Newman's "Building Microservices" puts this well: start with a monolith and extract services when you feel the pain, not before.
