Kubernetes uses a declarative configuration model for managing containerized applications. Its scheduler assigns workloads across cluster nodes and restarts failed Pods to maintain availability.

Enterprise adoption has grown steadily since 2020, largely because container orchestration standardizes how teams deploy and scale services across environments.

The control plane stores cluster state in etcd, a distributed key-value store. etcd supports automatic failover and leader election, so the cluster stays operational when individual nodes go down.
