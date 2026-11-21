FROM apache/spark:3.5.7

USER root

ARG HADOOP_AWS_VERSION=3.3.4
ARG AWS_SDK_VERSION=1.12.262
ARG DELTA_VERSION=3.2.1

# Conector S3A y dependencias Java.
RUN set -eux; \
    curl -fL \
      "https://repo.maven.apache.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar" \
      -o "/opt/spark/jars/hadoop-aws-${HADOOP_AWS_VERSION}.jar"; \
    curl -fL \
      "https://repo.maven.apache.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar" \
      -o "/opt/spark/jars/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar"; \
    curl -fL \
      "https://repo.maven.apache.org/maven2/io/delta/delta-spark_2.12/${DELTA_VERSION}/delta-spark_2.12-${DELTA_VERSION}.jar" \
      -o "/opt/spark/jars/delta-spark_2.12-${DELTA_VERSION}.jar"; \
    curl -fL \
      "https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar" \
      -o "/opt/spark/jars/delta-storage-${DELTA_VERSION}.jar"; \
    chown spark:spark /opt/spark/jars/*.jar

# API Python de Delta. PySpark ya viene incluido en la imagen Spark.
RUN pip3 install --no-cache-dir --no-deps "delta-spark==${DELTA_VERSION}"


# Entorno Python de la distribución Spark.
ENV PYTHONPATH="/opt/spark/python/lib/pyspark.zip:/opt/spark/python/lib/py4j-0.10.9.7-src.zip:/opt/spark/python"
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
ENV PATH="/opt/spark/bin:${PATH}"

USER spark
