I've been using AI coding tools for about a year now, and my feelings are mixed. They're genuinely good at churning out boilerplate, scaffolding tests, writing the kind of code nobody wants to write by hand. But the moment I stop paying attention, they quietly introduce bugs that compile fine and pass lint.

The problem isn't whether these tools are useful. They are. The problem is that "useful" and "reliable" aren't the same thing. I've caught generated code that reimplemented a function already in our codebase, used a deprecated API, and once, memorably, invented a config flag that doesn't exist.

Teams adopting these tools need to treat the output the way you'd treat a pull request from a new hire who's very fast but never reads the existing code. Review everything. Write tests first. Don't let the speed trick you into skipping the parts that actually matter.

Whether AI-assisted coding changes how we build software long-term, I honestly don't know. What I do know is that right now, the bottleneck was never typing speed.
