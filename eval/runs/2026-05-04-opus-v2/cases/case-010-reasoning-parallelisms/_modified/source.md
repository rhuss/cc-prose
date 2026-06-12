Monorepo vs. polyrepo is a technical decision, but it is also a cultural one. How your teams share code says something about how they share responsibility.

The tradeoffs come down to visibility, coupling, and governance. These interact in ways that only show up at scale.

Monorepos give you one place to look. Cross-cutting refactors are cheaper because you can change callers and callees in the same commit. Tooling stays consistent. The downside is real, though: build times grow, access control gets awkward, and the repo itself becomes unwieldy. Google makes it work with Bazel and a virtual filesystem. Most teams do not have that infrastructure.

Polyrepos give teams independence. Each repo has its own CI, its own release cadence, its own owners file. Small companies and large ones have shipped successfully this way. The cost is coordination: a breaking API change means PRs across multiple repos, and nobody enjoys that.

Neither approach is better in the abstract. What matters more is the discipline behind whichever you pick. A monorepo without enforced module boundaries devolves into a ball of mud. A polyrepo without contract testing devolves into integration surprises on deploy day.

Pick based on how your teams actually work, not how you wish they worked. The structure you can maintain beats the structure you admire.
