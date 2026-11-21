Usar una entorno de trabajo con Jupyter y acceso a git para bajar código y ejecutarlo contra S3 y Spark

## **1. Importar la imagen en K3d**

Primero, desde Ubuntu WSL:

```
cd ~/sw/data-platform

k3d image import mi-data-working:3.5.7 -c laboratorio
```

Comprueba que está disponible en el nodo:

```
docker exec k3d-laboratorio-server-0 crictl images | grep mi-data-working
```

## **2. Crear el Pod interactivo**

Vamos a empezar con un Pod llamado `working` en el namespace `data-platform`.

Tendrá:

- Nuestra imagen `mi-data-working:3.5.7`.
- Git y JupyterLab.
- La ServiceAccount `spark-driver` para poder lanzar trabajos Spark.
- Las credenciales S3 del Secret `lakehouse-s3`.
- Un puerto para acceder a Jupyter desde Windows.

Crea el manifiesto:

```
nano projects/templates/working-pod.yaml
```

Contenido:

```

apiVersion: v1
kind: Pod
metadata:
  name: working
  namespace: data-platform
  labels:
    app: working
spec:
  serviceAccountName: spark-driver
  restartPolicy: Always
  containers:
    - name: working
      image: mi-data-working:3.5.7
      imagePullPolicy: IfNotPresent
      ports:
        - name: jupyter
          containerPort: 8888
      env:
        - name: AWS_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: lakehouse-s3
              key: AWS_ACCESS_KEY_ID
        - name: AWS_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: lakehouse-s3
              key: AWS_SECRET_ACCESS_KEY
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
      command:
        - bash
        - -lc
        - jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
      resources:
        requests:
          cpu: "500m"
          memory: "1Gi"
        limits:
          cpu: "2"
          memory: "3Gi"

```

Guarda el archivo y aplícalo:

```
kubectl apply -f projects/templates/working-pod.yaml
```

Comprueba su estado:

```
kubectl get pods -n data-platform -w
```

Cuando aparezca `Running`, pulsa `Ctrl+C`.

## **3. Entrar en el entorno**

Entraremos en el contenedor:

```
kubectl exec -it working -n data-platform -- bash
```

Ya estaremos dentro del entorno de trabajo. Comprueba:

```
whoami
git --version
jupyter lab --version
spark-submit --version
```

## **4. Conectar Jupyter con tu navegador**

En otra terminal de Ubuntu WSL, ejecutaremos:

```
kubectl port-forward -n data-platform pod/working 8888:8888
```

Después abre en Windows:

[Abrir JupyterLab](http://localhost:8888?utm_source=chatgpt.com)

Jupyter generará un token de acceso. Si lo solicita, lo puedes consultar en los logs del Pod:

```
kubectl logs -n data-platform working
```

## **Ejecutar el pod sin defaults**

```
spark-submit \
  --master k8s://https://kubernetes.default.svc:443 \
  --deploy-mode client \
  --name delta-lakehouse-test \
  --conf spark.kubernetes.namespace=data-platform \
  --conf spark.kubernetes.container.image=mi-data-runtime:3.5.7 \
  --conf spark.kubernetes.container.image.pullPolicy=IfNotPresent \
  --conf spark.kubernetes.driver.pod.name=working \
  --conf spark.driver.host="$POD_IP" \
  --conf spark.driver.bindAddress=0.0.0.0 \
  --conf spark.driver.port=7078 \
  --conf spark.blockManager.port=7079 \
  --conf spark.executor.instances=1 \
  --conf spark.executor.cores=1 \
  --conf spark.executor.memory=512m \
  --conf spark.executor.memoryOverhead=256m \
  --conf spark.hadoop.fs.s3a.endpoint=http://seaweedfs-s3.seaweedfs.svc.cluster.local:8333 \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.hadoop.fs.s3a.connection.ssl.enabled=false \
  --conf spark.hadoop.fs.s3a.aws.credentials.provider=com.amazonaws.auth.EnvironmentVariableCredentialsProvider \
  --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
  --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
  examples/delta-lake/job.py
```

## **Ejecutar el pod usando spark-defaults.conf**

```
spark-submit \
  --master k8s://https://kubernetes.default.svc:443 \
  --deploy-mode client \
  --properties-file examples/delta-lake/spark-defaults.conf \
  examples/delta-lake/job.py
```