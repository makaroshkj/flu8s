#!/bin/sh
kubectl delete -f flussonic-namespace.yaml &&\
kubectl delete -f flussonic-secrets.yaml &&\
kubectl delete -f flussonic-configmap.yaml &&\
kubectl delete -f flussonic-ingress.yaml &&\
kubectl delete -f flussonic-ingest.yaml &&\
kubectl delete -f flussonic-transcoder.yaml &&\
kubectl delete -f config-app.yaml