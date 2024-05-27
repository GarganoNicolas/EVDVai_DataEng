from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql import HiveContext

# Configuramos...
sc = SparkContext('local')
spark = SparkSession(sc)
hc = HiveContext(sc)

# Traemos las tablas
df = spark.read.option("header", "true").parquet("hdfs://172.17.0.2:9000/ingest/yellow_tripdata_2021-01.parquet") 
df2 = spark.read.option("header", "true").parquet("hdfs://172.17.0.2:9000/ingest/yellow_tripdata_2021-02.parquet")

# Unimos las tablas
dfunion = df.union(df2)


# Creamos la vista para trabajar con sql
dfunion.createOrReplaceTempView("v_air")


# Selecciono las tablas que necesito, agrego el where y las casteo
# considero no hace falta usar dos o mas pasos para esta transformacion

df_transform = spark.sql("""
        SELECT 
            CAST(tpep_pickup_datetime AS DATE), 
            CAST(airport_fee AS FLOAT), 
            CAST(payment_type AS INT), 
            CAST(tolls_amount AS FLOAT),
            CAST(total_amount AS FLOAT) 
        FROM v_air 
        WHERE airport_fee IS NOT NULL AND payment_type = 2
        """)



df_transform.write.insertInto("tripdata.airport_trips")
#df_transform.createOrReplaceTempView("a_trips")
#spark.sql("insert into tripdata.airport_trips SELECT * from a_trips")

# el insert es mas facil con python ...