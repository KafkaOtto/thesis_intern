#!/bin/bash
NAMESPACE="default"
helm install prometheus prometheus-community/kube-prometheus-stack \
    --namespace monitoring \
    --create-namespace \
    --set global.serviceMonitor.interval=5s \
    --wait

helm install kepler kepler/kepler \
 --namespace kepler \
 --create-namespace \
 --set serviceMonitor.enabled=true \
 --set serviceMonitor.labels.release=prometheus \
  --set image.tag="release-0.7.11" \
  --set serviceMonitor.interval=5s \
  --wait

# LLM
kubectl apply -f "$BASE_DIR/deployment/llm/k8s/llama3_1/secret.yaml"
kubectl apply -f "$BASE_DIR/deployment/llm/k8s/llama3_1/deployment.yaml"
kubectl apply -f "$BASE_DIR/deployment/llm/k8s/llama3_1/service.yaml"
kubectl apply -f "$BASE_DIR/deployment/llm/k8s/llama3_1/pvc.yaml"


# Embedding
kubectl apply -f "$BASE_DIR/deployment/embedding/k8s/e5_small_v2/pvc.yaml"
kubectl apply -f "$BASE_DIR/deployment/embedding/k8s/e5_small_v2/deployment.yaml"
kubectl apply -f "$BASE_DIR/deployment/embedding/k8s/e5_small_v2/service.yaml"

helm install -f "$BASE_DIR/deployment/backend/k8s/values-t3-e5-small-v2.yaml" chat-backend "$BASE_DIR/deployment/backend/k8s"

LLM_POD_NAME=$(kubectl get pods -n "$NAMESPACE" --no-headers -o custom-columns=":metadata.name" | grep '^llama' | head -n 1)

echo "Waiting for pod $LLM_POD_NAME to be in Ready status..."

kubectl wait --namespace "$NAMESPACE" --for=condition=Ready pod/$LLM_POD_NAME --timeout=1200s

echo "pod $LLM_POD_NAME in Ready status..."

while [[ -z "${EMB_POD_NAME:-}" ]]; do
  EMB_POD_NAME=$(kubectl get pods -n "$NAMESPACE" --no-headers -o custom-columns=":metadata.name" | grep '^e5-small-v2' | head -n 1)
  sleep 2
done
echo "Waiting for pod $EMB_POD_NAME to be in Ready status..."

kubectl wait --namespace "$NAMESPACE" --for=condition=Ready pod/$EMB_POD_NAME --timeout=1200s

echo "pod $EMB_POD_NAME in Ready status..."

while [[ -z "${BACKEND_POD_NAME:-}" ]]; do
  BACKEND_POD_NAME=$(kubectl get pods -n "$NAMESPACE" --no-headers -o custom-columns=":metadata.name" | grep '^chat-backend' | head -n 1 || true)
  sleep 2
done
while [[ $(kubectl get pod $BACKEND_POD_NAME -n "$NAMESPACE" -o jsonpath='{.status.phase}') != "Running" ]]; do
  echo "Waiting for backend pod to be in Running status..."
  sleep 5
done

sleep 20