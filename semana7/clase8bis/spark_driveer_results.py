from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql import HiveContext

# Configuramos...
sc = SparkContext('local')
spark = SparkSession(sc)
hc = HiveContext(sc)

# Traemos tablas
df1 = spark.read.option("header", "true").csv("hdfs://172.17.0.2:9000/ingest/results.csv") 
df2 = spark.read.option("header", "true").csv("hdfs://172.17.0.2:9000/ingest/drivers.csv")
#df3 = spark.read.option("header", "true").csv("hdfs://172.17.0.2:9000/ingest/constructors.csv")
#df4 = spark.read.option("header", "true").csv("hdfs://172.17.0.2:9000/ingest/races.csv")

# Preparamos la primera transformacion
df1.createOrReplaceTempView("results")
df2.createOrReplaceTempView("drivers")

driver_results = spark.sql("""
    SELECT 
        CAST(d.forename AS STRING) AS driver_forename, 
        CAST(d.surname AS STRING) AS driver_surname, 
        CAST(d.nationality AS STRING) AS driver_nationality, 
        CAST(r.points AS INT) AS points
    FROM drivers d
    INNER JOIN results r ON d.driverId = r.driverId
    WHERE r.points!= 0
        """)


# Insertamos las tablas
driver_results.write.insertInto("f1.driver_results")