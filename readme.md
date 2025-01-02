# simple k8s mutating webhook

A simple k8s mutating webhook server for watching k8s resources change history

## Usage
```shell
kubectl create ns ops-debug
kubectl apply -f worker.yaml
# edit mutating for resource you want to watch
kubectl apply -f mutating.yaml
kubectl exec -it -n ops-debug ops-debug-webhook -- bash
python server.py 
# view log
```