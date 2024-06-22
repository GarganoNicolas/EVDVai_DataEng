SELECT 
COUNT(aeronave) AS cantidad_de_vuelos
FROM
administracionnacionaldeaviacioncivil.aeropuerto_tabla
WHERE
fecha >= '2021-01-01' 
AND fecha <= '2022-01-31';

SELECT 
SUM(pasajeros) AS cantidad_de_pasajeros
FROM
administracionnacionaldeaviacioncivil.aeropuerto_tabla
WHERE
fecha >= '2021-01-01' 
AND fecha <= '2022-06-30'
AND aerolinea_nombre ='AEROLINEAS ARGENTINAS SA';

SELECT
    at.fecha,
    at.horautc,
    at.aeropuerto,
    adt_origen.ref AS ciudad_origen,
    at.origen_destino,
    adt_destino.ref AS ciudad_destino,
    at.pasajeros
FROM
    administracionnacionaldeaviacioncivil.aeropuerto_tabla at
LEFT JOIN
    administracionnacionaldeaviacioncivil.aeropuerto_detalles_tabla adt_origen ON at.aeropuerto = adt_origen.aeropuerto
LEFT JOIN
    administracionnacionaldeaviacioncivil.aeropuerto_detalles_tabla adt_destino ON at.origen_destino = adt_destino.aeropuerto
WHERE
    at.fecha >= '2022-01-01' 
    AND at.fecha <= '2022-06-30';
   
SELECT DISTINCT 
aerolinea_nombre,
COUNT(pasajeros) OVER(PARTITION BY aerolinea_nombre) as pasajeros_transportados
FROM
administracionnacionaldeaviacioncivil.aeropuerto_tabla
WHERE
fecha >= '2022-01-01' 
AND fecha <= '2022-06-30'
AND aerolinea_nombre IS NOT NULL
AND aerolinea_nombre != '0'
ORDER BY pasajeros_transportados DESC
LIMIT 10;

SELECT DISTINCT 
aeronave,
COUNT(aeronave) OVER(PARTITION BY aeronave) as aeronave_recuento_de_despegues
FROM
administracionnacionaldeaviacioncivil.aeropuerto_tabla
WHERE
fecha >= '2021-01-01' 
AND fecha <= '2022-06-30'
AND aeronave != '0'
AND (aeropuerto = 'EZE' OR aeropuerto = 'AER')
ORDER BY aeronave_recuento_de_despegues DESC
LIMIT 10;

SELECT DISTINCT 
	aet.aeronave,
    COUNT(aet.aeronave) OVER(PARTITION BY aet.aeronave) as aeronave_recuento_de_despegues
FROM
    administracionnacionaldeaviacioncivil.aeropuerto_tabla aet
LEFT JOIN
    administracionnacionaldeaviacioncivil.aeropuerto_detalles_tabla adt_origen ON aet.aeropuerto = adt_origen.aeropuerto
WHERE
fecha >= '2021-01-01' 
AND fecha <= '2022-06-30'
AND (adt_origen.provincia LIKE '%BUENOS AIRES%')
AND aet.aeronave != '0'
ORDER BY aeronave_recuento_de_despegues DESC
LIMIT 10;

SELECT DISTINCT 
    aet.aeronave,
    COUNT(*) OVER(PARTITION BY aet.aeronave) as aeronave_recuento_de_despegues,
    COUNT(CASE WHEN adt_origen.provincia = 'BUENOS AIRES' THEN 1 ELSE NULL END) OVER(PARTITION BY aet.aeronave) as `PROVINCIA DE BUENOS AIRES`,
    COUNT(CASE WHEN adt_origen.provincia = 'CIUDAD AUTÓNOMA DE BUENOS AIRES' THEN 1 ELSE NULL END) OVER(PARTITION BY aet.aeronave) as `CIUDAD DE BUENOS AIRES`
FROM
    administracionnacionaldeaviacioncivil.aeropuerto_tabla aet
LEFT JOIN
    administracionnacionaldeaviacioncivil.aeropuerto_detalles_tabla adt_origen ON aet.aeropuerto = adt_origen.aeropuerto
WHERE
    fecha >= '2021-01-01' 
    AND fecha <= '2022-06-30'
    AND adt_origen.provincia LIKE '%BUENOS AIRES%'
    AND aet.aeronave != '0'
ORDER BY 
    aeronave_recuento_de_despegues DESC
LIMIT 10;

SELECT provincia 
FROM administracionnacionaldeaviacioncivil.aeropuerto_detalles_tabla adt
WHERE provincia LIKE '%BUENOS AIRES%'






