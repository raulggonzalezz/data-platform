from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

TABLE_PATH = "s3a://lakehouse/bronze/clientes"

def main():
    spark = SparkSession.builder.appName("delta-lakehouse-write-read").getOrCreate()
    clientes = [
        (1, "Ana", "Madrid"),
        (2, "Luis", "Barcelona"),
        (3, "Marta", "Valencia"),
    ]
    df = spark.createDataFrame(clientes, schema=["id", "nombre", "ciudad"])

    # Overwrite hace que el ejemplo sea repetible.
    df.write.format("delta").mode("overwrite").save(TABLE_PATH)

    leidos = spark.read.format("delta").load(TABLE_PATH)
    total = leidos.count()
    print(f"Registros leídos desde Delta: {total}")
    leidos.orderBy(col("id")).show(truncate=False)

    if total != len(clientes):
        raise RuntimeError(f"Esperados {len(clientes)} registros; leídos {total}")
    if not DeltaTable.isDeltaTable(spark, TABLE_PATH):
        raise RuntimeError(f"No se detecta una tabla Delta en {TABLE_PATH}")

    print("Validación Delta completada correctamente.")
    spark.stop()

if __name__ == "__main__":
    main()
