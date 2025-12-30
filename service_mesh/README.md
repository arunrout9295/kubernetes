## 🍔 Service Mesh – Real-World Example (Zomato-style)

Consider an application like Zomato, which consists of multiple microservices such as menu service, order service, payment service, delivery service, and restaurant service.

These services need to communicate with each other securely, reliably, and efficiently. Instead of handling concerns like traffic routing, retries, timeouts, security, and monitoring inside each service, we introduce a service mesh.

A service mesh manages service-to-service communication internally by using sidecar proxies, ensuring features like mutual TLS security, traffic control, observability, and fault tolerance without changing application code.

```
User
  |
API Gateway
  |
-------------------------------
|   Menu   |  Order  | Payment |
|  Service | Service | Service |
-------------------------------
        |
     Service Mesh
(traffic, security, retries,monitoring,mTLS)
```

Descriptions:

A service mesh is used to manage internal communication between microservices by handling security, traffic management, and observability at the infrastructure level.