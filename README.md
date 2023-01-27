# fastapi-py

# minikube kubernetes setting

```
minikube start
minikube ip
```

- Paste the ip address into the host folder by opening notepad.

# minikube ingress-nginx setting

```
minikube addons enable ingress
```

# minikube create secret

```
kubectl create secret generic secret  --from-literal=secret=
```

# and then start skaffold.yaml

```
skaffold dev
```
