df1 = spark.read.option("header", "true").csv("/ingest/results.csv") 
df2 = spark.read.option("header", "true").csv("/ingest/drivers.csv")
df3 = spark.read.option("header", "true").csv("/ingest/constructors.csv")
df4 = spark.read.option("header", "true").csv("/ingest/races.csv")


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


driver_results.show()


df3.createOrReplaceTempView("constructors")
df4.createOrReplaceTempView("races")

SpanishGP = spark.sql("""
    SELECT 
        CAST(c.constructorRef AS STRING) AS constructorRef, 
        CAST(c.name AS STRING) AS cons_name, 
        CAST(c.nationality AS STRING) AS cons_nationality, 
        CAST(c.url AS STRING) AS url,
        CAST(r.points AS INT) AS points
    FROM constructors c
    INNER JOIN results r ON c.constructorId = r.constructorId
    INNER JOIN  races ra ON ra.raceId = r.raceId
    WHERE ra.circuitID IN (4, 12, 26, 45, 49, 67) AND r.points != 0 AND ra.year = 1991
        """)

SpanishGP.show(3)

driver_results.write.insertInto("f1.driver_results")
SpanishGP.write.insertInto("f1.constructor_results") 