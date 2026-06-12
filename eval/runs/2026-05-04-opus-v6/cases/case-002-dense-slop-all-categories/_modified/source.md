Microservices split an application into small, independently deployable services that communicate over the network. Each service owns its data and runs in its own process.

The main benefit is independent deployment. When one team ships a change to the checkout service, they don't need to coordinate a release with the team that handles search. In practice this matters most at scale. A team of five working on a single codebase probably doesn't need microservices, and will spend more time fighting the infrastructure than shipping features.

You can scale individual services based on actual load. If your image-processing service is the bottleneck, you add more instances of that service without touching anything else. Failures also stay more contained: a bug in the recommendation engine doesn't have to take down the whole site, though in practice this depends on how well you've handled timeouts and circuit breakers.

The tradeoffs are real. Network calls replace function calls, so you get latency, partial failures, and serialization overhead that didn't exist before. Data consistency across services is genuinely hard. You'll need distributed tracing to debug production issues, because a single request now touches half a dozen services. Operational complexity goes up, period.

Sam Newman's "Building Microservices" (O'Reilly, 2nd ed., 2021) is the standard reference. For a more skeptical take, Martin Fowler's "Monolith First" article argues you should start monolithic and extract services only when the pain justifies the cost. I think that's right for most teams.
