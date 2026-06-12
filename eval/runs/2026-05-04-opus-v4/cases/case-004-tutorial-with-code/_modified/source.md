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

`MaxConns` caps the number of simultaneous connections. If all 10 are in use, the next caller blocks until one frees up. `MinConns` keeps 2 idle connections ready so the first queries after a quiet period don't wait for a TCP handshake.

The pool checks whether connections are still alive before handing them out. Because connections drop (network blips, server restarts, idle timeouts), the pool runs background health checks and replaces dead ones automatically.
