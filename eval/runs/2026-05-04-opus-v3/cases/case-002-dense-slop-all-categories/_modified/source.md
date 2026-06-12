Microservices split a system into small, independently deployable services that communicate over the network. Each service owns its data and runs in its own process.

The main benefit is independent deployment. Teams ship changes to one service without coordinating a release across the whole system. At Spotify, squads deploy their services multiple times a day without waiting on other teams. At a monolith shop, that same change waits for the next release train.

Independent scaling is real but narrower than people think. If your checkout service gets 10x the traffic of your catalog service, you can throw more instances at checkout without overprovisioning everything else. Most teams I've talked to say this matters for maybe two or three services, not all of them.

The costs are concrete. You now have network calls where you used to have function calls, which means latency, partial failures, and retry logic. Data consistency gets harder because you can't just wrap things in a database transaction anymore. Debugging a request that touches five services requires distributed tracing (Jaeger, Zipkin, or similar), and if you don't have that set up before you split, you'll regret it.

Sam Newman's "Building Microservices" (2nd ed., 2021) is probably the most practical reference. His advice: don't start with microservices. Start with a well-structured monolith, identify the seams, and extract services where you have a clear reason (independent scaling, different deployment cadence, different team ownership). Splitting for the sake of splitting just trades one set of problems for a worse set.
