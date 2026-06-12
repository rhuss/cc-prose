Kubernetes uses a declarative configuration model for managing containerized applications. Its built-in scheduler distributes workloads across cluster nodes and restarts failed Pods automatically.

Enterprise adoption has grown steadily since 2020. The CNCF's 2023 survey found that 84% of responding organizations use or evaluate Kubernetes, up from 58% in 2020. Standardized Deployment patterns like rolling updates and canary releases are a big part of why.

The control plane stores cluster state in etcd, a distributed key-value store. etcd handles its own leader election and failover, so the control plane stays available even when individual nodes go down.
