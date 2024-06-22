from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql import HiveContext
from pyspark.sql.functions import col, to_date


sc = SparkContext('local')
spark = SparkSession(sc)
hc = HiveContext(sc)


df1 = spark.read.option("header", "true").option("sep", ";").csv("hdfs://172.17.0.2:9000/ingest/2021-informe-ministerio.csv") 
df2 = spark.read.option("header", "true").option("sep", ";").csv("hdfs://172.17.0.2:9000/ingest/202206-informe-ministerio.csv")
df3 = spark.read.option("header", "true").option("sep", ";").csv("hdfs://172.17.0.2:9000/ingest/aeropuertos_detalle.csv")


dfunion = df1.union(df2)


aeropuerto_tabla_todo = dfunion.select(
    to_date(dfunion["Fecha"], "dd/MM/yyyy").alias("fecha"),
    dfunion["Hora UTC"].alias("horaUTC"),
    dfunion["Clase de Vuelo (todos los vuelos)"].alias("clase_de_vuelo"),
    dfunion["Clasificación Vuelo"].alias("clasificacion_de_vuelo"),
    dfunion["Tipo de Movimiento"].alias("tipo_de_movimiento"),
    dfunion["Aeropuerto"].alias("aeropuerto"),
    dfunion["Origen / Destino"].alias("origen_destino"),
    dfunion["Aerolinea Nombre"].alias("aerolinea_nombre"),
    dfunion["Aeronave"].alias("aeronave"),
    dfunion["Pasajeros"].cast("int").alias("pasajeros")
).fillna({'pasajeros': 0})

aeropuerto_tabla = aeropuerto_tabla_todo.filter(col("fecha") < '2022-06-30')


aeropuerto_detalles = df3.select(
    col("local").alias("aeropuerto"),
    col("oaci").alias("oaci"),
    col("iata").alias("iata"),
    col("tipo").alias("tipo"),
    col("denominacion").alias("denominacion"),
    col("coordenadas").alias("coordenadas"),
    col("latitud").alias("latitud"),
    col("longitud").alias("longitud"),
    col("elev").cast("float").alias("elev"),
    col("uom_elev").alias("uom_elev"),
    col("ref").alias("ref"),
    col("distancia_ref").cast("float").alias("distancia_ref"),
    col("direccion_ref").alias("direccion_ref"),
    col("condicion").alias("condicion"),
    col("control").alias("control"),
    col("region").alias("region"),
    (col("uso") + col("trafico")).alias("uso_trafico"),
    col("sna").alias("sna"),
    col("concesionado").alias("concesionado"),
    col("provincia").alias("provincia")
).fillna({'distancia_ref': 0})


aeropuerto_tabla.write.insertInto("administracionNacionalDeAviacionCivil.aeropuerto_tabla")
aeropuerto_detalles.write.insertInto("administracionNacionalDeAviacionCivil.aeropuerto_detalles_tabla") 