# simple k8s mutating webhook

A simple k8s mutating webhook server for watching k8s resources change history

## Usage
```shell
kubectl create ns ops-debug
kubectl apply -f worker.yaml
# edit mutating for resource you want to watch
kubectl apply -f mutating.yaml
# view log
kubectl logs -n ops-debug ops-debug-webhook -f
```
