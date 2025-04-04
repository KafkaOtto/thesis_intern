#!/bin/bash

# Uninstall Helm releases
helm uninstall scaphandre
helm uninstall prometheus
helm uninstall grafana
helm uninstall rag-db

kubectl delete -f ~/thesis/projects/thesis_intern/deployment/storage.yaml

# Delete Kubernetes resources
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/postgre/pvc.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/postgre/pv.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/pvc.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/secret.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/deployment.yaml
# Embedding
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_large_v2/pvc.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_large_v2/deployment.yaml

# Reranker
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/reranker/k8s/bge_reranker_v2_m3/pvc.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/reranker/k8s/bge_reranker_v2_m3/deployment.yaml

# Optionally delete any remaining PVCs
kubectl delete pvc --all

helm uninstall -n gpu-operator $(helm list -n gpu-operator -q)
kubectl delete namespace gpu-operator
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/nvidia/time-slicing-config-all.yaml