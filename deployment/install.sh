#!/bin/bash

# On the Kubernetes control spot
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
helm install --wait --generate-name -n gpu-operator --create-namespace nvidia/gpu-operator
# Optional, lets you assign the same GPU to multiple pods
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/nvidia/time-slicing-config-all.yaml
kubectl patch clusterpolicy/cluster-policy -n gpu-operator --type merge -p '{"spec": {"devicePlugin": {"config": {"name": "time-slicing-config-all", "default": "any"}}}}'

kubectl apply -f ~/thesis/projects/thesis_intern/deployment/storage.yaml

helm install scaphandre ~/thesis/projects/scaphandre/helm/scaphandre --set serviceMonitor.interval=1s
helm install prometheus prometheus-community/prometheus --set alertmanager.persistentVolume.enabled=false --set server.persistentVolume.enabled=false
helm install grafana grafana/grafana --values docs_src/tutorials/grafana-helm-values.yaml


kubectl apply -f ~/thesis/projects/thesis_intern/deployment/postgre/pvc.yaml
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/postgre/pv.yaml
helm install -f ~/thesis/projects/thesis_intern/deployment/postgre/values-prod.yaml rag-db oci://registry-1.docker.io/bitnamicharts/postgresql
# LLM
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/pvc.yaml
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/secret.yaml
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/deployment.yaml
# Embedding
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_large_v2/pvc.yaml
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_large_v2/deployment.yaml

kubectl apply -f ~/thesis/projects/thesis_intern/deployment/reranker/k8s/bge_reranker_v2_m3/pvc.yaml
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/reranker/k8s/bge_reranker_v2_m3/deployment.yaml