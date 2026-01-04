🧱 Prerequisites
🔧 Prerequisites

Make sure the following are installed:

- Git
- Docker
- Docker Compose
- Kubernetes (Minikube / Kind / Cloud cluster)
- kubectl
- Docker Hub account

![Chat_app Architecture](screenshots/chatapp_arch.jpg)


## Git-Hub

### 📥 Step 1: Clone the Repository
Clone the GitHub repository to your local system:
```
git clone https://github.com/arunrout9295/kubernetes.git
```
Move into the project directory:
```
cd chat-app
```
### 🔄 Step 2: Pull Latest Changes (Always Do This First)
Before making any changes, always pull the latest code:
```
git pull origin main
```
This avoids merge conflicts and ensures you work on the latest version.

### 🌿 Step 3: (Recommended) Create a New Branch
Create a explore branch before making changes:
```
git checkout -b feature/chat-app-setup
```

### 📦 Step 6: Commit and Push Code Changes
Stage changes:
```
git add .
```
Commit:
```
git commit -m "Added backend deployment and service"
```
Push to GitHub:
```
git push origin explore/chat-app-setup
```


## 🐳DOCKER

### 🐳 Step 1: Build the Application Locally
Build and run the application using Docker Compose:
```
docker-compose up --build
```

### 🏷️ Step 2: Tag Docker Images
Tag the Images-
Backend:
```
docker tag chat_app-backend:latest arunrout9295/chat_app-backend:latest
```
```
docker tag chat_app-frontend:latest arunrout9295/chat_app-frontend:latest
```

### 📤 Step 3: Push Images to Docker Hub
Backend:
```
docker push arunrout9295/chat_app-backend:latest
```
Frontend:
```
docker push arunrout9295/chat_app-frontend:latest
```

☸️ Next Steps (Kubernetes)
- Backend Deployment & Service ✅
- MongoDB Deployment
- PersistentVolume (PV)
- PersistentVolumeClaim (PVC)
- Frontend Deployment & Service ⏳
- Ingress / Port Forwarding


### ☸️Step 1: Ensure Kubernetes Cluster Is Running
Verify Cluster Connectivity:
```
kubectl cluster-info
```
O/P:
```
Kubernetes control plane is running at https://127.0.0.1:6443
CoreDNS is running at https://127.0.0.1:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```
Check Nodes Status:
```
kubectl get nodes
```
O/P:

| NAME            | STATUS | ROLES          | AGE | VERSION |
|-----------------|--------|----------------|-----|---------|
| docker-desktop  | Ready  | control-plane | 18d | v1.25.9 |


### 🗂️ Step 2: Create Namespace
```
kind: Namespace
apiVersion: v1
metadata:
  name: chat-app
```
apply:
```
kubectl apply -f namespace.yml
```
verify:
```
kubectl get namespaces
```
### 🚀 Step 3: Backend Deployment
Create a file named backend-deployment.yml
```
kind: Deployment
apiVersion: apps/v1
metadata:
  name: backend-deployment
  namespace: chat-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      name: backend-pod
      namespace: chat-app
      labels:
        app: backend
    spec:
      containers:
      - name: chatapp-backend
        image: arunrout9295/chat_app-backend:latest
        ports: 
        - containerPort: 8000
        env:
        - name: MONGO_URL
          value: "mongodb://root:root@mongo-service:27017/chatdb?authSource=admin"
```
Apply the deployment:
```
kubectl apply -f backend-deployment.yml
```
Verify deployment and pod:
```
kubectl get deployments -n chat-app
kubectl get pods -n chat-app
```
### 🌐 Step 4: Backend Service
Create a file named backend-service.yml:
```
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: chat-app
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: ClusterIP
```
Apply the service:
```
kubectl apply -f backend-service.yml
```
Verify service:
```
kubectl get svc -n chat-app
```
### 🔁 Step 5: Access Backend Using Port Forward
Expose the backend locally using port-forward:
```
kubectl port-forward svc/backend-service 8000:8000 -n chat-app
```
Access backend:
```
http://localhost:8000
```

### ☸️ MongoDB Configuration for Kubernetes
1️⃣ PersistentVolume (PV)

2️⃣ PersistentVolumeClaim (PVC)

3️⃣ MongoDB Deployment

4️⃣ MongoDB Service

###  1️⃣ PersistentVolume (PV)
Create mongodb-pv.yml:
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mongodb-pvc
  namespace: chat-app
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: mongodb-storage

```
Apply:
```
kubectl apply -f mongodb-pv.yml
```
Verify:
```
kubectl get pv
```



### 2️⃣ PersistentVolumeClaim (PVC)
Create mongodb-pvc.yml:
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mongodb-pvc
  namespace: chat-app
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: mongodb-storage
```
Apply:
```
kubectl apply -f mongo-pvc.yml
```
Verify:
```
kubectl get pvc -n chat-app
```
Status should be:
```
Bound
```

3️⃣ MongoDB Deployment
Create mongo-deployment.yml:
```
kind: Deployment
apiVersion: apps/v1
metadata:
  name: mongodb-deployment
  namespace: chat-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      name: mongodb-pod
      namespace: chat-app
      labels:
        app: mongodb
    spec:
      containers:
      - name: chatapp-mongo
        image: mongo:6 
        ports:
        - containerPort: 27017
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          value: root
        - name: MONGO_INITDB_ROOT_PASSWORD
          value: root
      volumes:
      - name: mongo-data
        persistentVolumeClaim:
          claimName: mongodb-pvc
```
Apply:
```
kubectl apply -f mongodb-deployment.yml
```
Verify:
```
kubectl get pvc -n mongodb-service.yml
```
Exec into the MongoDB pod:
```
kubectl exec -it mongodb-deployment-84b459469d-zf7g8 -n chat-app -- mongosh -u root -p root --authenticationDatabase admin
```

```
use chatdb
show collections
db.messages.find().pretty()
```



