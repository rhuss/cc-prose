## Setting up a PostgreSQL connection pool

The `pgxpool` package handles connection pooling for Go apps using PostgreSQL. Install it first:

```bash
go get github.com/jackc/pgx/v5/pgxpool
```

Then create and configure the pool:

```go
config, err := pgxpool.ParseConfig("postgres://user:pass@localhost:5432/mydb")
if err != nil {
    log.Fatal(err)
}
config.MaxConns = 10
config.MinConns = 2

pool, err := pgxpool.NewWithConfig(context.Background(), config)
if err != nil {
    log.Fatal(err)
}
defer pool.Close()
```

`MaxConns` caps how many connections exist at once. Set it too low and queries queue up under load; too high and you'll exhaust PostgreSQL's own connection limit (100 by default). `MinConns` keeps idle connections warm so the first few queries after a quiet period don't pay the connection setup cost.

The pool checks connection health automatically and reconnects when a connection goes stale. You don't need to handle this yourself.
