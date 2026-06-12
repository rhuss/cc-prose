## Setting up a PostgreSQL connection pool

The `pgxpool` package handles connection pooling for Go applications using PostgreSQL.

Install it:

```bash
go get github.com/jackc/pgx/v5/pgxpool
```

Then create the pool:

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

`MaxConns` caps the number of open connections. If your application hits this limit, calls to `Acquire()` block until a connection frees up. `MinConns` keeps idle connections warm so the first few queries after a quiet period don't pay the connection setup cost.

The pool checks connection health automatically. Because connections go stale (network blips, server restarts, idle timeouts), it validates them before handing them out and reconnects when needed.
