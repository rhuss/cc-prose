Kubernetes uses declarative configuration to manage containerized applications. You describe the desired state in YAML, and the scheduler places workloads across nodes to meet availability constraints.

Enterprise adoption has grown steadily since 2018, mostly because teams wanted a standard way to deploy containers without reinventing service discovery and rollback for each project.

The control plane stores cluster state in etcd, a distributed key-value store. etcd handles failover and leader election automatically, so the cluster keeps running when individual nodes go down.
