# Homework

Link to my DBT [code](https://github.com/ABZ-Aaron/ny_taxi_rides_zoomcamp).

## QUESTION 1

What is the count of records in the model fact_trips after running all models with the test run variable disabled and filtering for 2019 and 2020 data only (pickup datetime) 

```SQL
SELECT COUNT(*)
FROM `silent-oasis-338916.production.fact_trips`
WHERE pickup_datetime BETWEEN '2019-01-01' AND '2020-12-31';
```

### ANSWER: 

61599917

This isn't in line with what others got. But it looks like everyone is getting inconsistent answers for this question. Something I'll aim to investigate myself when I have time.

## QUESTION 2

What is the distribution between service type filtering by years 2019 and 2020 data as done in the videos (Yellow/Green)

```SQL
SELECT service_type,
       count(*) / (SELECT COUNT(*) FROM `silent-oasis-338916.production.fact_trips`) * 100
FROM `silent-oasis-338916.production.fact_trips`
GROUP BY service_type;
```

We can also visualise this via Google Data Studio.

### ANSWER: 

10.1 : 89.9

## QUESTION 3

What is the count of records in the model stg_fhv_tripdata after running all models with the test run variable disabled

```SQL
SELECT COUNT(*) 
FROM `silent-oasis-338916.trips_data_all.stg_fhv_tripdata`;
```

### ANSWER

42084899

## QUESTION 4

What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled (:false)

```SQL
SELECT count(*) 
FROM `silent-oasis-338916.trips_data_all.fact_fhv_trips`;
```

### ANSWER

22676253

## QUESTION 5

What is the month with the biggest amount of rides after building a tile for the fact_fhv_trips table Create a dashboard with some tiles that you find interesting to explore the data. One tile should show the amount of trips per month, as done in the videos for fact_trips, based on the fact_fhv_trips table.

I found the answer to this via Data Visual Studio rather than via SQL.

### ANSWER

January
