#!/bin/bash

# Uninstall Helm releases
helm uninstall scaphandre
helm uninstall prometheus
helm uninstall grafana
helm uninstall rag-db

# Delete Kubernetes resources
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/postgres/pvc.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/postgres/pv.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/pvc.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/secret.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/llm/k8s/llama3_1/deployment.yaml

# Optionally delete any remaining PVCs
kubectl delete pvc --all