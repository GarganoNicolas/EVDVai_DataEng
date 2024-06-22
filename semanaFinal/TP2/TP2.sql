SELECT 
fueltype, 
rating
FROM 
car_rental_db.car_rental_analytics
WHERE rating <= 4
AND (fueltype = 'hybrid' OR fueltype = 'electric');
SELECT 
COUNT(fueltype) AS consulta_a
FROM 
car_rental_db.car_rental_analytics
WHERE 
rating <= 4
AND (fueltype = 'hybrid' OR fueltype = 'electric');
SELECT 
make, year
FROM 
car_rental_db.car_rental_analytics
WHERE 
year >= 2010
AND year <= 2015;
SELECT 
COUNT(make) AS consulta_d
FROM 
car_rental_db.car_rental_analytics
WHERE 
year >= 2010
AND year <= 2015;
SELECT 
city AS consulta_e,
COUNT(city) AS recuento_alquileres_ecologicos
FROM 
car_rental_db.car_rental_analytics
WHERE 
fueltype IN ('hybrid', 'electric')
GROUP BY
city
ORDER BY
recuento_alquileres_ecologicos DESC
LIMIT 5;
SELECT 
fueltype,
AVG(reviewcount) AS promedio_de_reviews
FROM 
car_rental_db.car_rental_analytics
GROUP BY fueltype 
ORDER BY
promedio_de_reviews DESC;


