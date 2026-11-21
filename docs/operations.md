# Operación

## Inspección
```bash
kubectl get nodes -o wide
kubectl get namespaces
kubectl get pods -A -o wide
kubectl get svc -A
kubectl get pvc -A
helm list -A
```
Para Spark:
```bash
kubectl get pods -n data-platform -w
kubectl describe pod -n data-platform <pod>
kubectl logs -n data-platform <driver-pod>
```

## Limpieza
Los Pods `Completed` suelen estar en fase `Succeeded`:
```bash
kubectl get pods -n data-platform
kubectl delete pods -n data-platform --field-selector=status.phase=Succeeded
```
Inspeccionar antes de borrar. No eliminar PVCs como limpieza rutinaria de trabajos Spark.

## Recursos
Consultar valores actuales, no asumir que mediciones históricas siguen vigentes:
```bash
kubectl top nodes
kubectl top pods -A
docker stats --no-stream
```
Los Pods corren dentro del contenedor de nodo K3d; no sumar dos veces el consumo de Pods y del contenedor K3d.

## Helm
Antes de actualizar:
```bash
helm list -n seaweedfs
helm get values seaweedfs -n seaweedfs
helm get manifest seaweedfs -n seaweedfs
```
Versionar valores revisados y saneados. No exportar secretos reales.

## Diagnóstico
- `kubectl` no conecta: comprobar Docker Desktop y contexto `k3d-laboratorio`.
- S3 no responde: comprobar port-forward, Service y Pods SeaweedFS.
- `SignatureDoesNotMatch`: comprobar que cliente y servidor usan la misma credencial, endpoint y región; no copiar claves a ciegas.
- Errores de limpieza Spark: identificar recurso y verbo exactos; no conceder permisos amplios por comodidad.
