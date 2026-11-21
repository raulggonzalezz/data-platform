# Data Platform on Kubernetes

Repositorio IaC y documentación de la plataforma de datos del laboratorio. Estado inicial: documenta lo conocido y probado; los manifiestos estáticos definitivos y la gestión de secretos quedan pendientes.

## Objetivos
- Configuración de servicios compartidos.
- Alta futura de proyectos/namespaces, personas/grupos y ServiceAccounts.
- RBAC, cuotas, límites y políticas de red.
- Catálogo versionado de imágenes base.
- Ejemplos reproducibles de trabajos.

## Estado conocido
- K3d/K3s `laboratorio`, un nodo `k3d-laboratorio-server-0`, Kubernetes `v1.35.5+k3s1`.
- Contexto `k3d-laboratorio`; Docker Desktop con backend WSL2.
- `seaweedfs` contiene SeaweedFS instalado con Helm chart 4.54.0.
- `data-platform` es el namespace de pruebas Spark.
- Endpoint S3 interno: `http://seaweedfs-s3.seaweedfs.svc.cluster.local:8333`.
- SparkPi ejecutado correctamente con `apache/spark:3.5.7` en modo cluster.
- Ejemplo Delta Lake preparado; ejecución end-to-end pendiente.
- Gestión de secretos pendiente de diseño.

## Estructura
`platform/` servicios y políticas compartidas; `projects/` plantillas de proyectos; `users/` identidades y permisos; `images/` imágenes base y catálogo; `examples/` trabajos de prueba; `helm/` valores; `docs/` documentación.

## Principios
1. Servicios compartidos y proyectos en namespaces separados.
2. Spark bajo demanda: Driver y Executors efímeros, sin master/workers permanentes.
3. Datos persistentes en S3; disco de Pods solo temporal.
4. Mínimo privilegio; no conceder borrado de PVCs a Spark por defecto.
5. Nunca guardar secretos en Git, Dockerfiles ni imágenes.
6. Un namespace no es por sí solo una frontera de seguridad: combinar RBAC, NetworkPolicy y cuotas.
7. Laboratorio de un nodo, no arquitectura HA de producción.

## Inicio
```bash
cd ~/proyectos/data-platform
git init
```
Revisar `docs/architecture.md` y `docs/installation.md`. Un README en un directorio no implica que el componente esté desplegado.
