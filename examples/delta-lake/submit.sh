#!/bin/bash
set -euo pipefail

# Comprobar argumentos
if [[ $# -lt 1 ]]; then
    echo "Uso: $0 <job> [argumentos del job...]"
    exit 1
fi

JOB_PATH="$1"
shift

# Comprobar que existe el job
if [[ ! -f "$JOB_PATH" ]]; then
    echo "Error: no existe el job: $JOB_PATH"
    exit 1
fi

# Comprobar la IP del Pod
: "${POD_IP:?La variable POD_IP no está definida}"

# Localizar la configuración junto al propio lanzador
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

spark-submit \
    --master k8s://https://kubernetes.default.svc:443 \
    --deploy-mode client \
    --properties-file "$SCRIPT_DIR/spark-defaults.conf" \
    --conf "spark.driver.host=${POD_IP}" \
    "$JOB_PATH" \
    "$@"