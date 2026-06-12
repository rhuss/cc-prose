Kubernetes uses declarative configuration to manage containerized applications. You describe the desired state in YAML, and the scheduler places workloads across cluster nodes to maintain availability.

Enterprise adoption has grown steadily. The CNCF 2024 survey found that 84% of respondents use or evaluate Kubernetes in production, up from 58% in 2020. Standardized Deployment and Service abstractions make it easier to move workloads between clusters and providers.

The control plane stores cluster state in etcd, a distributed key-value store. etcd handles leader election and automatic failover, so the cluster keeps running when individual nodes go down.
