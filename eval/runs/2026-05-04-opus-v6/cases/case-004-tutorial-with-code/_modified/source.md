## Setting up a PostgreSQL connection pool

The `pgxpool` package handles connection pooling for Go applications using PostgreSQL.

Install the package:

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

`MaxConns` caps the number of open connections. Under heavy load, requests beyond this limit wait for a connection to free up. `MinConns` keeps idle connections ready so the first few queries after a quiet period don't pay the connection setup cost.

The pool checks connection health automatically and reconnects when a connection goes stale. You don't need to handle this yourself.
