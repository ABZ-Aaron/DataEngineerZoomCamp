-- QUESTION 3
-- How many taxi trips were there on January 15?
SELECT COUNT(*) 
FROM yellow_taxi_data 
WHERE CAST(tpep_pickup_datetime AS DATE) = '2021-01-15';

-- QUESTION 4
-- On which day it was the largest tip in January? (note: it's not a typo, it's "tip", not "trip")
SELECT tpep_pickup_datetime
FROM yellow_taxi_data
WHERE tip_amount = (SELECT MAX(tip_amount)
FROM yellow_taxi_data 
WHERE EXTRACT(MONTH FROM tpep_pickup_datetime) = 1);

-- QUESTION 5
-- What was the most popular destination for passengers picked up in central park on January 14? 
-- Enter the zone name (not id). If the zone name is unknown (missing), write "Unknown"
SELECT dol."Zone" drop_off_zone,
		COUNT(*) total
FROM yellow_taxi_data ytd
JOIN yellow_taxi_zone_data pul ON pul."LocationID" = ytd."PULocationID"
JOIN yellow_taxi_zone_data dol ON dol."LocationID" = ytd."DOLocationID"
WHERE LOWER(pul."Zone") = LOWER('central park') AND
	   CAST(tpep_pickup_datetime AS DATE) = '2021-01-14'
GROUP BY dol."Zone"
ORDER BY total DESC;

-- QUESTION 6
-- What's the pickup-dropoff pair with the largest average price for a ride 
-- (calculated based on total_amount)? Enter two zone names separated by a slash. 
-- For example:"Jamaica Bay / Clinton East". If any of the zone names are unknown (missing), 
-- write "Unknown". For example, "Unknown / Clinton East".
SELECT AVG(total_amount) total, 
		pul."Zone" pick_up_zone, 
		dol."Zone" drop_off_zone
FROM yellow_taxi_data ytd
JOIN yellow_taxi_zone_data pul ON pul."LocationID" = ytd."PULocationID"
JOIN yellow_taxi_zone_data dol ON dol."LocationID" = ytd."DOLocationID"
GROUP BY pul."Zone", dol."Zone"
ORDER BY total DESC;