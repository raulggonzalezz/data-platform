# Arquitectura

## Capas
- **Plataforma compartida:** almacenamiento S3 y futuros servicios comunes.
- **Proyectos:** namespaces aislados lógicamente con sus workloads, permisos y límites.

## Topología conocida
K3d `laboratorio`, un nodo K3s. Namespaces relevantes: `seaweedfs` (SeaweedFS), `data-platform` (pruebas Spark) y `default` (prueba web histórica `mi-web`, estado actual a verificar). SeaweedFS S3 está disponible dentro del clúster en `seaweedfs-s3.seaweedfs.svc.cluster.local:8333`.

## Flujo Spark
El cliente ejecuta `spark-submit`; Kubernetes crea un Driver en el namespace del proyecto; el Driver crea Executors; los Executors procesan; los Pods terminan al acabar el trabajo. Spark no se mantiene como servicio permanente de masters/workers.

## Responsabilidades
| Mecanismo | Función |
|---|---|
| Namespace | Agrupar recursos y delimitar nombres |
| RBAC | Autorizar personas, grupos y ServiceAccounts frente a la API |
| ResourceQuota | Cuotas agregadas por namespace |
| LimitRange | Defaults y rangos de recursos por Pod/Container |
| NetworkPolicy | Controlar tráfico entre Pods/destinos |
| Secret | Entregar credenciales en runtime |

Un namespace no constituye por sí solo una frontera de seguridad completa.

## Identidades
Personas/grupos son identidades humanas autenticadas por la configuración del clúster. ServiceAccounts son identidades de workloads. No deben compartir permisos. Los Role/RoleBindings deben limitarse al namespace cuando sea posible.

## Persistencia y seguridad
Los datos duraderos van a S3. El almacenamiento local de Spark es temporal para scratch/shuffle. No se concede a la ServiceAccount Spark permiso para borrar colecciones de PVCs por defecto. Las credenciales S3 deben inyectarse desde un mecanismo de secretos acordado, nunca desde Git o la imagen.
