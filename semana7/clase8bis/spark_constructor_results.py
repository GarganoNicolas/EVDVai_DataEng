from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql import HiveContext

# Configuramos...
sc = SparkContext('local')
spark = SparkSession(sc)
hc = HiveContext(sc)

# Traemos tablas
df1 = spark.read.option("header", "true").csv("hdfs://172.17.0.2:9000/ingest/results.csv") 
# df2 = spark.read.option("header", "true").csv("hdfs://172.17.0.2:9000/ingest/drivers.csv")
df3 = spark.read.option("header", "true").csv("hdfs://172.17.0.2:9000/ingest/constructors.csv")
df4 = spark.read.option("header", "true").csv("hdfs://172.17.0.2:9000/ingest/races.csv")

# Preparamos la primera transformacion
df1.createOrReplaceTempView("results")
# df2.createOrReplaceTempView("drivers")
df3.createOrReplaceTempView("constructors")
df4.createOrReplaceTempView("races")

SpanishGP = spark.sql("""
    SELECT 
        CAST(c.constructorRef AS STRING) AS constructorref, 
        CAST(c.name AS STRING) AS cons_name, 
        CAST(c.nationality AS STRING) AS cons_nationality, 
        CAST(c.url AS STRING) AS url,
        CAST(r.points AS INT) AS points
    FROM constructors c
    INNER JOIN results r ON c.constructorId = r.constructorId
    INNER JOIN  races ra ON ra.raceId = r.raceId
    WHERE ra.circuitID IN (4, 12, 26, 45, 49, 67) AND r.points != 0 AND ra.year = 1991
        """)

# Insertamos la tabla
SpanishGP.write.insertInto("f1.constructor_results") 