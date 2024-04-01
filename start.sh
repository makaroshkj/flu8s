#!/bin/sh
kubectl apply -f flussonic-namespace.yaml &&\
kubectl apply -f flussonic-secrets.yaml &&\
kubectl apply -f flussonic-configmap.yaml &&\
kubectl apply -f flussonic-ingress.yaml &&\
kubectl apply -f flussonic-ingest.yaml &&\
kubectl apply -f flussonic-transcoder.yaml &&\
kubectl apply -f config-app.yaml