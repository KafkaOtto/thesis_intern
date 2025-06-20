#!/bin/bash

# Uninstall Helm releases
helm uninstall -n gpu-operator $(helm list -n gpu-operator -q)
helm uninstall prometheus -n monitoring
helm uninstall kepler -n kepler
helm uninstall pgvector
helm uninstall chat-backend
helm uninstall importer

#kubectl delete -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/deepseek_llama/secret.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/deepseek_7b/deployment.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/deepseek_7b/service.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/deepseek_7b/pvc.yaml

# Delete Kubernetes resources for Embedding
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_large_v2/deployment.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_large_v2/service.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_large_v2/pvc.yaml

kubectl delete secret awssecret