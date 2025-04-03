#!/bin/bash

helm install scaphandre ~/thesis/projects/scaphandre/helm/scaphandre --set serviceMonitor.interval=1s
helm install prometheus prometheus-community/prometheus --set alertmanager.persistentVolume.enabled=false --set server.persistentVolume.enabled=false
helm install grafana grafana/grafana --values docs_src/tutorials/grafana-helm-values.yaml
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/postgres/pvc.yaml
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/postgres/pv.yaml
helm install -f ~/thesis/projects/thesis_intern/deployment/postgres/values-prod.yaml rag-db oci://registry-1.docker.io/bitnamicharts/postgresql
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/pvc.yaml
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/secret.yaml
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/deployment.yaml