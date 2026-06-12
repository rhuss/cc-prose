Kubernetes uses a declarative configuration model for managing containerized applications. You describe the desired state, and the scheduler places workloads across nodes to keep things running if something fails.

Enterprise adoption has grown steadily since 2020. The CNCF's 2023 survey found that 84% of organizations either use or evaluate Kubernetes, mostly to standardize how they deploy and run services across environments.

The control plane stores cluster state in etcd, a distributed key-value store. etcd handles its own leader election and failover, so the control plane stays available even when individual nodes go down.
