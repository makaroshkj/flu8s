This example is just a demostration how to run trivial Flussonic cluster in [k3s](https://docs.k3s.io/quick-start).

**Prerequisites**
* Docker installed
* [kubectl](https://kubernetes.io/ru/docs/tasks/tools/install-kubectl/#%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-kubectl-%D0%B2-macos) installed
* k3s installed:
```
docker run  --privileged  -d -p 6443:6443 rancher/k3s:v1.24.10-k3s1 server
docker cp 15191db6f6bb:/etc/rancher/k3s/k3s.yaml ~/.kube/config
```
* ingress-nginx installed:
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
```

**Video pipeline:**
```
RTMP push --> flussonic-ingest --> M4S push --> flussonic-dvr <-- play HLS
                              |--> RTMP push --> telegram
```

**Description:**
* Start stream publishing (via RTMP or other protocols) to `flussonic-ingest` service;
* `flussonic-ingest` get stream configuration from `config-app` and starts publishing to telegram via RTMP and `flussonic-dvr` service via M4S;
* `flussonic-dvr` record archive to `minio` S3 storage;
* Viewer can play DVR stream (via HLS or other protocols).
`config-app` is a trivial flask app which returns Flussonic stream configuration. You can build container:
```
cd
docker build -t config-app:1.0 .
```

**How to run it**

* Edit `flussonic-secrets.yaml`. Need to write license key, edit auth and RTMP endpoint.
* Run cluster:
```
minikube start
kubectl apply -f flussonic-namespace.yaml &&\
kubectl apply -f flussonic-secrets.yaml &&\
kubectl apply -f flussonic-configmap.yaml &&\
kubectl apply -f flussonic-ingest.yaml &&\
kubectl apply -f flussonic-dvr.yaml &&\
kubectl apply -f config-app.yaml &&\
kubectl apply -f minio.yaml
```

**Useful commands for debug:**
```
kubectl-debug flussonic-dvr-n8zch -n flussonic --agentless=true --port-forward=true --agent-image=ksxack/debug-agent:v0.1
kubectl logs flussonic-dvr-n8zch -n flussonic -f
kubectl port-forward -n flussonic flussonic-dvr-n8zch 8888:80
```

**TODO:**
* Finish with minio
* Figure out with ingress. The idea is to have single ingress resource for all the external traffic:
```
http://ingest.flussonic.k8s.ru:80 --> ingest-service:80
http://ingest.flussonic.k8s.ru:8080/admin/ --> ingest-service:8080 # flussonic admin UI
rtmp://ingest.flussonic.k8s.ru:1935/static --> ingest-service:1935
srt://ingest.flussonic.k8s.ru:9999 --> ingest-service:9999

http://dvr.flussonic.k8s.ru:80 --> dvr-service:80
http://ingest.flussonic.k8s.ru:8080/admin/ --> dvr-service:8080 # flussonic admin UI

http://minio.flussonic.k8s.ru:80 --> minio-service:80 # minio admin UI
```