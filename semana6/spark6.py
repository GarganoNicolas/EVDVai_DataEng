df = spark.read.option("header", "true").parquet("/ingest/yellow_tripdata_2021-01.parquet") 
df2 = spark.read.option("header", "true").parquet("/ingest/yellow_tripdata_2021-02.parquet")


dfunion = df.union(df2)

dfunion.printSchema()


dfunion.createOrReplaceTempView("v_air")

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

df_transform.show(10)

df_transform.write.insertInto("tripdata.airport_trips")