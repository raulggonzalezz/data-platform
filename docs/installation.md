# Instalación y entorno

## Requisitos
Windows 11, Docker Desktop (WSL2), Ubuntu WSL, `kubectl`, `k3d`, `helm` y AWS CLI. Docker Desktop debe estar iniciado para operar el clúster.

## Clúster
Creación usada:
```bash
k3d cluster create laboratorio \
  --servers 1 \
  --agents 0 \
  --port "8080:80@loadbalancer"
```
Contexto esperado `k3d-laboratorio`. Verificar siempre:
```bash
kubectl config current-context
kubectl get nodes -o wide
kubectl get namespaces
```
Versión observada: `v1.35.5+k3s1`.

## SeaweedFS
Repositorio Helm:
```bash
helm repo add seaweedfs https://seaweedfs.github.io/seaweedfs/helm
helm repo update
```
Release observado: `seaweedfs`, namespace `seaweedfs`, chart `4.54.0`, app `4.54`. PVCs observados Bound: master 1Gi, volume 20Gi, filer 5Gi, StorageClass `local-path`.

Comprobar:
```bash
helm list -n seaweedfs
kubectl get pods,pvc,svc -n seaweedfs
```
Endpoint S3 interno:
`http://seaweedfs-s3.seaweedfs.svc.cluster.local:8333`

Acceso desde WSL:
```bash
kubectl port-forward -n seaweedfs svc/seaweedfs-s3 8333:8333
```
Dejar la terminal abierta. Tras reiniciar, volver a ejecutar el port-forward.

## Prueba S3 desde host
No guardar estas variables en archivos versionados:
```bash
export AWS_ACCESS_KEY_ID="lakeadmin"
read -rsp "Introduce la clave S3: " AWS_SECRET_ACCESS_KEY
echo
export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION="us-east-1"
aws --endpoint-url http://localhost:8333 s3 ls
```
Se observó el bucket `lakehouse`. Prueba de escritura/lectura:
```bash
printf 'prueba S3\n' > prueba-s3.txt
aws --endpoint-url http://localhost:8333 s3 cp prueba-s3.txt s3://lakehouse/pruebas/prueba-s3.txt
aws --endpoint-url http://localhost:8333 s3 cp s3://lakehouse/pruebas/prueba-s3.txt -
```
Un HTTP 403 `AccessDenied` sin firma puede ser normal cuando S3 exige autenticación.

## Spark
`apache/spark:3.5.7` se usó para SparkPi en modo cluster. Incluye Java 11, Spark 3.5.7, Scala 2.12 y Python 3.8.10. Binario: `/opt/spark/bin/spark-submit`. Driver y Executor terminaron correctamente. Hubo errores de limpieza por permisos; se ampliaron permisos para Pods/ConfigMaps, pero se decidió no dar `deletecollection` sobre PVCs porque Spark no necesita PVCs para persistencia.

Comprobar estado antes de repetir:
```bash
kubectl get pods,pvc -n data-platform
kubectl get role,rolebinding,serviceaccount -n data-platform
```

## Reinicios
Docker Desktop debe estar iniciado; `kubectl port-forward` se reinicia manualmente; variables `AWS_*` exportadas solo viven en esa terminal.
