## Setting up a PostgreSQL connection pool

The `pgxpool` package manages database connection pooling for Go applications.

Install it:

```bash
go get github.com/jackc/pgx/v5/pgxpool
```

Create the pool:

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

`MaxConns` caps how many connections the pool opens at once. If your application hits this limit, callers block until a connection frees up. `MinConns` keeps a few idle connections ready so the first queries after a quiet period don't wait for a fresh TCP handshake.

The pool checks connection health in the background and reconnects automatically when a connection goes stale.
