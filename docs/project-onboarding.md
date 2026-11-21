# Alta de proyectos (diseño objetivo)

Cada proyecto tendrá:
1. Namespace dedicado y etiquetas estándar.
2. Role/RoleBinding para personas/grupos.
3. ServiceAccounts separadas para workloads.
4. ResourceQuota y LimitRange.
5. NetworkPolicies con reglas explícitas.
6. Secretos entregados por un mecanismo aprobado, nunca desde Git.
7. Acceso mínimo a servicios compartidos, como SeaweedFS S3.
8. Imagen base registrada en el catálogo.

Secuencia propuesta: acordar nombre/responsable/propósito; crear namespace; asignar RBAC humano; crear ServiceAccounts; aplicar cuotas/límites; aplicar políticas de red; configurar secretos; validar acceso a servicios; ejecutar trabajo de prueba.

Un RoleBinding namespaced no concede acceso a otros namespaces. Las personas y los Pods no deben compartir identidad. Los trabajos Spark requieren permisos concretos para gestionar sus Pods, no permisos de administrador del clúster.
