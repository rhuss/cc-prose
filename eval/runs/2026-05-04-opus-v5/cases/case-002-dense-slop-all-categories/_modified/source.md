Microservices split an application into small, independently deployable services, each owning its own data and communicating over the network. The idea is simple. Getting it right is not.

The main win is independent deployment. Teams push changes to their service without coordinating a release across the whole system. At Uber, this meant hundreds of deploys per day across thousands of services. At a ten-person startup, it probably means you are debugging network calls instead of shipping features.

Scaling gets more targeted. A recommendation engine under heavy load can get more instances without scaling the user profile service alongside it. But you pay for this with operational complexity: service discovery, load balancing, distributed tracing, and the constant question of what happens when the network between services fails.

Failure isolation works in theory. One service crashes, the others keep running. In practice, a single slow downstream dependency can cascade through the whole system if you have not set up circuit breakers and timeouts. Netflix built an entire chaos engineering practice around this problem because the failure modes are that surprising.

The real costs are often underestimated. Data consistency across services is hard. You lose transactions that a monolith gives you for free. Debugging a request that touches six services requires tooling (Jaeger, Zipkin, or similar) that you would never need otherwise. Sam Newman's "Building Microservices" spends more pages on the difficulties than the benefits, which tells you something.

Microservices make sense when you have multiple teams that need to ship independently and the system is large enough to justify the infrastructure overhead. For most applications under a certain size, a well-structured monolith is simpler, faster to develop, and easier to operate.
