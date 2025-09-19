## Lab

```sh
minikube start
```

![01-minikube-start.png](docs/images/01-minikube-start.png)

```sh
kubectl get nodes
```

![02-nodes.png](docs/images/02-nodes.png)

```sh
minikube addons enable ingress
```

![03-enable-ingress-addon.png](docs/images/03-enable-ingress-addon.png)

```sh
kubectl create namespace micro-lab
```

![04-create-namespace.png](docs/images/04-create-namespace.png)

```sh
kubectl apply -f users-deploy.yaml -n micro-lab
kubectl apply -f catalog-deploy.yaml -n micro-lab
kubectl apply -f orders-deploy.yaml -n micro-lab
kubectl apply -f gateway-ingress.yaml -n micro-lab
```

![05-deploy.png](docs/images/05-deploy.png)

```sh
kubectl get pods -n micro-lab
kubectl get svc -n micro-lab
kubectl get ingress -n micro-lab
```

![06-check.png](docs/images/06-check.png)

```sh
minikube tunnel
```

```sh
sudo echo "\n127.0.0.1 micro.local" >> /etc/hosts
```

```sh
curl http://micro.local/users
curl http://micro.local/catalog
curl http://micro.local/orders
```

![07-test.png](docs/images/07-test.png)

```sh
kubectl scale deploy catalog-deploy --replicas=3 -n micro-lab
kubectl get pods -l app=catalog -n micro-lab
```

![08-scale.png](docs/images/08-scale.png)

```sh
kubectl delete namespace micro-lab
```

## Q&A

Câu hỏi 6: Sau khi chạy kubectl apply -f users-deploy.yaml, dùng lệnh nào
để kiểm tra Pod của service users đã chạy thành công? Hãy chụp màn hình kết
quả.

> kubectl get pods -l app=users -n micro-lab
> ![qa-06.png](docs/images/qa-06.png)

Câu hỏi 7: Trong file users-deploy.yaml, hãy chỉ ra:

- Deployment quản lý bao nhiêu replica ban đầu?
- Service thuộc loại nào (ClusterIP, NodePort, LoadBalancer)?

> pod replicas: 1,
> service type: ClusterIP

Câu hỏi 8: Sau khi cài Ingress, em cần thêm dòng nào vào file /etc/hosts để
truy cập bằng tên miền micro.local?

> ```
> 127.0.0.1     micro.local     # khi enable ingress addon
> 192.168.49.2  micro.local     # dùng minikube ip khi không enable ingress addon
> ```
