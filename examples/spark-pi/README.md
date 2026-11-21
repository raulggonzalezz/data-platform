# SparkPi

Prueba mínima ejecutada en modo cluster con `apache/spark:3.5.7`, un Driver y un Executor. El trabajo terminó correctamente. Hubo mensajes de error en la limpieza por permisos de eliminación de colecciones; se ampliaron permisos para Pods/ConfigMaps, pero no se concedió `deletecollection` sobre PVCs porque el trabajo no necesita PVCs.
