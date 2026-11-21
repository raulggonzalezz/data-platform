# Catálogo de imágenes

Registrar para cada imagen: tag y digest, procedencia, runtimes/versiones, componentes incluidos, compatibilidad, fecha de prueba y estado. Evitar `latest`. Driver y Executors deben compartir la misma imagen y dependencias. No incluir secretos.

## Runtime Spark de referencia
Base observada: `apache/spark:3.5.7`.
- Spark 3.5.7
- Java Temurin 11.0.27
- Scala 2.12.18
- Python 3.8.10
- PySpark distribuido en `/opt/spark/python`
- Py4J 0.10.9.7
- Hadoop client 3.3.4 incluido
- `hadoop-aws`/AWS SDK no incluidos en la imagen inspeccionada
- Delta Lake pendiente de integrar y validar

PYTHONPATH identificado:
```text
/opt/spark/python/lib/pyspark.zip:/opt/spark/python/lib/py4j-0.10.9.7-src.zip:/opt/spark/python
```
No instalar PySpark con pip redundante si se usa la distribución Spark incluida.

Pendiente: verificar en el POM oficial la versión AWS SDK requerida por `hadoop-aws:3.3.4`; añadir y probar S3A; fijar Delta compatible con Spark 3.5.x/Scala 2.12 (se evaluará 3.3.2); validar lectura/escritura con SeaweedFS; decidir distribución offline. `apache/spark:4.3.0-java17` es solo referencia futura, no runtime aprobado.
