from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql import HiveContext

sc = SparkContext('local')
spark = SparkSession(sc)
hc = HiveContext(sc)


df1 = spark.read.option("header", "true").csv("hdfs://172.17.0.2:9000/ingest/CarRentalData.csv") 
# df2 = spark.read.option("header", "true").option("sep", ";").csv("hdfs://172.17.0.2:9000/ingest/united-states-of-america-state-Buenos_Aires.csv") 


df1.createOrReplaceTempView("CarRentalData")

car_rental_analytics = spark.sql("""
    SELECT 
        LOWER(CAST(fuelType AS STRING)) AS fuelType,
        ROUND(CAST(rating AS INT)) AS rating,
        CAST(renterTripsTaken AS INT) AS renterTripsTaken,
        CAST(reviewCount AS INT) AS reviewCount,
        CAST(`location.city` AS STRING) AS city,
        CAST(`location.state` AS STRING) AS state_name,
        CAST(`owner.id` AS INT) AS owner_id,
        CAST(`rate.daily` AS INT) AS rate_daily,
        CAST(`vehicle.make` AS STRING) AS make,
        CAST(`vehicle.model` AS STRING) AS model,
        CAST(`vehicle.year` AS INT) AS year 
    FROM 
        CarRentalData
    WHERE 
        `location.state` != 'Texas'
""")


car_rental_analytics.write.insertInto("car_rental_db.car_rental_analytics")

