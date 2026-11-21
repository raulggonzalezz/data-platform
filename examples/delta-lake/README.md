# Delta Lake: escribir y leer clientes en S3

## Objetivo
1. Crear un DataFrame pequeño de clientes.
2. Escribir Delta en `s3a://lakehouse/bronze/clientes`.
3. Leerlo de nuevo y comprobar registros.
4. Confirmar que existe `_delta_log`.

## Estado
El código está preparado; falta construir y validar la imagen runtime con Hadoop AWS/AWS SDK y Delta Lake, y cerrar la inyección segura de credenciales.

## Runtime
Spark 3.5.7 / Scala 2.12; Hadoop client 3.3.4; añadir `hadoop-aws:3.3.4` y la versión AWS SDK indicada por su POM; evaluar Delta 3.3.2. Driver y Executors con la misma imagen.

Endpoint S3 interno: `http://seaweedfs-s3.seaweedfs.svc.cluster.local:8333`. Usar path-style y SSL desactivado para este endpoint HTTP de laboratorio. Las credenciales deben llegar al Driver y Executors desde un Secret del namespace del proyecto. El Secret y su procedimiento de creación no forman parte de este ZIP.

No pasar claves en `--conf spark.hadoop.fs.s3a.secret.key=...` ni guardarlas en archivos versionados. El comando final de submit se cerrará tras validar la imagen y la gestión de secretos.
