# Homework

## Question 1:

What is count for fhv vehicles data for year 2019
Can load the data for cloud storage and run a count(*)

ANSWER:

```SQL
SELECT COUNT(*)  
FROM `silent-oasis-338916.trips_data_all.fhv_non_partitoned`;
```

There are `42084899` records.

## Question 2:

How many distinct dispatching_base_num we have in fhv for 2019
Can run a distinct query on the table from question 1

ANSWER:

```SQL
SELECT COUNT(DISTINCT dispatching_base_num) 
FROM `silent-oasis-338916.trips_data_all.fhv_non_partitoned`;
```

There are `792` distinct dispatching base numbers.

## Question 3:

Best strategy to optimise if query always filter by dropoff_datetime and order by dispatching_base_num
Review partitioning and clustering video.
We need to think what will be the most optimal strategy to improve query performance and reduce cost.

POSSIBLE ANSWERS:

1. Partition by dropoff_datetime
1. Partition by dispatching_base_num
1. Partition by dropoff_datetime and cluster by dispatching_base_num
1. Partition by dispatching_base_num and cluster by dropoff_dateti

ANSWER:

The answer is number 3.

## Question 4:

What is the count, estimated and actual data processed for query which counts trip between 2019/01/01 and 2019/03/31 for dispatching_base_num B00987, B02060, B02279
Create a table with optimized clustering and partitioning, and run a count(*). Estimated data processed can be found in top right corner and actual data processed can be found after the query is executed.

POSSIBLE ANSWERS:

1. Count: 0, Estimated data processed: 0MB, Actual data processed: 600MB
1. Count: 26558, Estimated data processed: 400 MB, Actual data processed: 155 MB
1. Count: 26558, Estimated data processed: 155 MB, Actual data processed: 400 MB
1. Count: 26558, Estimated data processed: 600 MB, Actual data processed: 155 MB

ANSWER:

```SQL
CREATE OR REPLACE TABLE silent-oasis-338916.trips_data_all.fhv_partitoned_clustered
PARTITION BY DATE(pickup_datetime)
CLUSTER BY dispatching_base_num AS
SELECT * FROM silent-oasis-338916.trips_data_all.fhv_non_partitoned;
```
* Create our partitioned and clustered table

```SQL
SELECT COUNT(*)
FROM `silent-oasis-338916.trips_data_all.fhv_partitoned_clustered`
WHERE (CAST(pickup_datetime AS DATE) BETWEEN '2019-01-01' AND '2019-03-31') AND 
       dispatching_base_num IN ('B00987', 'B02060', 'B02279');
```
* Run our query

The answer isn't exactly as appears in the solution, but it looks to be number 2.

## Question 5:

What will be the best partitioning or clustering strategy when filtering on dispatching_base_num and SR_Flag
Review partitioning and clustering video. Clustering cannot be created on all data types.

POSSIBLE ANSWERS:

* Partition by dispatching_base_num and cluster by SR_Flag
* Partition by SR_Flag and cluster by dispatching_base_num
* Cluster by dispatching_base_num and SR_Flag
* Partition by dispatching_base_num and SR_Flag

ANSWER:

The answer is 2. From the documentation, we can see the kinds of columns we can partition by:

```
Time-unit column: Tables are partitioned based on a TIMESTAMP, DATE, or DATETIME column in the table.

Ingestion time: Tables are partitioned based on the timestamp when BigQuery ingests the data.

Integer range: Tables are partitioned based on an integer column.
```

The `dispatching_base_num` doesn't appear to fit into any of these, so we can only really cluster by this. The answer I think would be 2. 

## Question 6
What improvements can be seen by partitioning and clustering for data size less than 1 GB
Partitioning and clustering also creates extra metadata.
Before query execution this metadata needs to be processed.

ANSWER:

Can be worse due to metadata.

## Question 7 (Not required):

In which format does BigQuery save data
Review big query internals video.

ANSWER:

Columnar. 