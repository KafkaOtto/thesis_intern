#!/bin/bash

NAMESPACE="default"

# Add Helm repo and install GPU operator
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
helm install --wait --generate-name \
     -n gpu-operator --create-namespace \
     nvidia/gpu-operator \
     --set driver.enabled=false

helm install pgvector ~/thesis/projects/thesis_intern/deployment/postgre/helm-pgvector/helm/pgvector --set postgresql.password=root

PG_POD_NAME=$(kubectl get pods -n "$NAMESPACE" --no-headers -o custom-columns=":metadata.name" | grep '^pgvector-' | head -n 1)
if [ -z "$PG_POD_NAME" ]; then
  echo "Error: No pod starting with 'pgvector-' found in namespace $NAMESPACE"
  exit 1
fi

echo "Detected pod: $PG_POD_NAME"
sleep 20

echo "📦 Copying SQL scripts to pod..."
INIT_SCRIPT="$HOME/thesis/projects/thesis_intern/deployment/postgre/scripts/1__initialization_script.sql"
SCHEMA_SCRIPT="$HOME/thesis/projects/thesis_intern/deployment/postgre/scripts/2__schema_script_embd384.sql"
kubectl cp "$INIT_SCRIPT" "$NAMESPACE/$PG_POD_NAME:/tmp/1__initialization_script.sql"
kubectl cp "$SCHEMA_SCRIPT" "$NAMESPACE/$PG_POD_NAME:/tmp/2__schema_script.sql"

echo "🚀 Running initialization script..."
kubectl exec -i "$PG_POD_NAME" -n "$NAMESPACE" -- bash -c "PGPASSWORD=root psql -U postgres -f /tmp/1__initialization_script.sql"

echo "🚀 Running schema script..."
kubectl exec -i "$PG_POD_NAME" -n "$NAMESPACE" -- bash -c "PGPASSWORD=root psql -U postgres -f /tmp/2__schema_script.sql"

kubectl apply -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_small_v2/pvc.yaml
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_small_v2/deployment_gpu.yaml
kubectl apply -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_small_v2/service.yaml

EMB_POD_NAME=$(kubectl get pods -n "$NAMESPACE" --no-headers -o custom-columns=":metadata.name" | grep '^e5-large-v2' | head -n 1)

echo "Waiting for pod $EMB_POD_NAME to be in Ready status..."

kubectl wait --namespace "$NAMESPACE" --for=condition=Ready pod/$EMB_POD_NAME --timeout=120s

echo "pod $EMB_POD_NAME in Ready status..."

DOCKER_PAS=$(aws ecr get-login-password --region eu-central-1)

kubectl create secret docker-registry "awssecret" \
  --docker-server=214775410005.dkr.ecr.eu-central-1.amazonaws.com \
  --docker-email=zhinuan.guo@softwareimprovementgroup.com \
  --docker-username=AWS \
  --docker-password="$DOCKER_PAS"


helm install -f /home/otto/thesis/projects/thesis_intern/deployment/data_importer/k8s/values-t3-e5-small-v2.yaml importer /home/otto/thesis/projects/thesis_intern/deployment/data_importer/k8s

echo "Waiting for importer pod to start..."
until kubectl get pods -o name | grep -q importer-springboot-helm-chart; do
  sleep 2
done

IMPORTER_POD=$(kubectl get pods -o name | grep importer-springboot-helm-chart | head -n1)
if [ -z "$IMPORTER_POD" ]; then
  echo "Error: Importer pod not found"
  exit 1
fi

echo "Waiting for $IMPORTER_POD to complete..."
while true; do
  STATUS=$(kubectl get "$IMPORTER_POD" -o jsonpath='{.status.phase}')
  if [[ "$STATUS" == "Succeeded" || "$STATUS" == "Failed" ]]; then
    echo "Importer pod completed with status: $STATUS"
    break
  fi
  sleep 5
done

kubectl exec -i "$PG_POD_NAME" -n "$NAMESPACE" -- bash -c "PGPASSWORD=root psql -U postgres -d ragdb -c 'SELECT COUNT(*) FROM text_segments;'"

kubectl delete -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_small_v2/deployment_gpu.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_small_v2/service.yaml
kubectl delete -f ~/thesis/projects/thesis_intern/deployment/embedding/k8s/e5_small_v2/pvc.yaml
