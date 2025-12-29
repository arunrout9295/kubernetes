

## Kubernetes Dashboard Setup

Kubernetes dashboard recommended config yaml file
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```


## Create YAML file for Kubernetes Dashboard

```
kind: ServiceAccount
apiVersion: v1
metadata:
  name: admin-user
  namespace: kubernetes-dashboard  # Built-in value already created in cluster while apply the dashboard config file

---

kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: admin-user-binding
  namespace: kubernetes-dashboard

subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin

```

Apply the Configuration:
```
kubectl apply -f dashboard_admin_user.yml
```

Get the Access Token Retrieve the Token for the admin-user:
```
kubectl -n kubernetes-dashboard create token admin-user
```
Copy the Token for use in the Dashboard login.

Access the Dashboard start the Dashboard using kubectl proxy:
```
kubectl proxy --port=8001 --address=0.0.0.0 --accept-hosts='.*'
```

Open the Dashboard in your Browser(use http not https):
```
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```
use the Token from the previous step to login.



common command
```
kubectl get pods -n kubernetes-dashboard
```

```
kubectl get svc -n kubernetes-dashboard
```

