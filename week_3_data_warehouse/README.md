## Dare Warehouses & BigQuery

* OLTP

   `Online Transaction Processing` is used to control and run essential business operations in real time. The updates are short and fast, and initiated by users. These are typically normalized databases for efficiency, and are generally small if historical data is analyzed. 

   They typically require regular backups to ensure business continuity, and meet legal and governance requirements. They increase productivity of end users and the data lists day-to-day business transactions.

* OLAP

    `Online Analytical Processing` is used to plan, solve problems, support decisions and discover hidden insights. Data is periodically refreshed with scheduled, long-running batch jobs. They are typically demoralized for analysis. They are generally large due to aggregating large data.

    Lost data can typically be reloaded from OLTP databases as needed. They typically increase productivity for managers, data analysts, data scientists etc. They show a multidimensional view of enterprise data. 

### So what is a Data Warehouse?

These are **OLAP** solutions. They are used for reporting and data analysis. Generally they have many data sources. All of these report to a staging area, before being pushed to the Data Warehouse. Data here is typically then output to Data Marts (e.g. purchasing, sales, inventory) for different teams to pull from. Although Data Scientists and Analysts may pull directly from the warehouse itself. 

### Introduction to BigQuery (summary of external course)

Data Warehouses can be used for transactional processing, but are typically used for analysis.

#### Why use BigQuery?

* Building your own is expensive and time consuming, and also difficult to scale
* Just load data and only pay for what you use
* Can process billions of rows in seconds

#### Running a Query

BigQuery has public datasets available (e.g. usa_names) - each with their own tables. You can access these from GCP.

BigQuery has an query editor, where you can enter SQL queries. When entering a query, BigQuery will let you know if it's a valid query. It will also estimate how long it will take to process your query.

After entering a query, and clicking run, we can then see the output.

### So what is BigQuery? (summary from bootcamp)

This is a Data Warehouse solution by Google. 

* It is serverless, in that there are no servers to manage or database software to install. 
* Scalability and high-availability prioritized
* Features included like Machine Learning, Business Intelligence, and Geospatial Analysis. 
* BigQuery maximises flexibility by separating the compute engine that analyses your data from your storage. 

BigQuery stores data in a columnar storage format that is optimized for analytical queries, and storage is replicated across multiple locations for high availability. 

BigQuery has an on demand pricing model (1 TB of data processing for $5) or a flat based rate (100 slots equals $2000 per month, which is about 400 TB data processed).

We can query BigQuery using SQL queries.

There's a publicly available dataset available in BigQuery that we can query.:

```sql
SELECT station_id, name FROM
    bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;
```

### Create External Table 

When importing data into BigQuery, we do not always need to define the schema. 

When we create an `external table`, data is not actually inside BigQuery. In our case, it's stored in Google Cloud Storage. So basically we can query directly in BigQuery, even though the data isn't stored there.

The table metadata including the table schema is stored in BigQuery, but the data resides in the external source. 

By running the below in BigQuery query page, we are creating an external table called `external_yellow_tripdata` which contains the metadata for are parquet files (2019 and 2022).

It will show table size and other attributes as 0 B. This is because data itself is not inside BigQuery. 

```sql
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `silent-oasis-338916.trips_data_all.external_yellow_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://dtc_data_lake_silent-oasis-338916/raw/yellow_tripdata_2019-*.parquet', 'gs://dtc_data_lake_silent-oasis-338916/raw/yellow_tripdata_2020-*.parquet ']
);
```

Let's query our data to check it worked:

```sql
-- Check yellow trip data
SELECT * FROM silent-oasis-338916.trips_data_all.external_yellow_tripdata limit 10;
```

We can partition our data by date. This is useful because when we query our data, looking for records for a particular date, it will not read or process any data from a different date. This reduces costs.

Let's first create a non-partitioned table. I should have removed the word `external` from the table, so just ignore that.

```sql
-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE silent-oasis-338916.trips_data_all.external_yellow_tripdata_non_partitoned AS
SELECT * FROM silent-oasis-338916.trips_data_all.external_yellow_tripdata;
```

Now let's create a partitions table, partitioning by `tpep_pickup_datetime`

```sql
-- Create a partitioned table from external table
CREATE OR REPLACE TABLE silent-oasis-338916.trips_data_all.external_yellow_tripdata_partitoned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM silent-oasis-338916.trips_data_all.external_yellow_tripdata;
```

Now select all distinct Vendor IDs from our non-partitioned table where date is between two dates:

```sql
-- Impact of partition
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM silent-oasis-338916.trips_data_all.external_yellow_tripdata_non_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
```

Now do the same for the the partitioned table:

```sql
-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM silent-oasis-338916.trips_data_all.external_yellow_tripdata_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
```

When you hover over each query in the query editor, you should see up in the right hand side somewhere how much data will be processed. You'll notice the partitioned dataset processes a lot less data!

Now let's look into some details of our partition:

```sql
-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `trips_data_all.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'external_yellow_tripdata_partitoned'
ORDER BY total_rows DESC;
```

We can also cluster our data. This is where table data is automatically organised based on contents of one or more columns in the table's schema.

Where we cluster and partition depends on the kind of queries that are likely to be run on our table.

```sql
-- Creating a partition and cluster table
CREATE OR REPLACE TABLE silent-oasis-338916.trips_data_all.yellow_tripdata_partitoned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM silent-oasis-338916.trips_data_all.external_yellow_tripdata_partitoned;
```

Now run a similar exercise as before, to compare how much data will be processed:

For our partitioned table:

```sql
-- Query scans 1.1 GB
SELECT count(*) as trips
FROM silent-oasis-338916.trips_data_all.external_yellow_tripdata_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
```

For our clustered table:

```sql
-- Query scans 864.5 MB
SELECT count(*) as trips
FROM silent-oasis-338916.trips_data_all.yellow_tripdata_partitoned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
```

You'll see that the clustered-partitioned table performs better than the partitioned table.

### Partitioning and Clustering

Read up more on partitioning [here](https://cloud.google.com/bigquery/docs/partitioned-tables)

Read up more on clustering [here](https://cloud.google.com/bigquery/docs/clustered-tables)

### BigQuery Best Practices

Cost Reduction

* Avoid SELECT * (this will read all columns and data)
* Price your queries before running them
* Use clustered or partitioned tables
* Use streaming inserts with caution (can increase cost drastically)
* Materialize query result in stages

Query Performance

* Always filter on partitioned column
* Demoralize data
* Use nested or repeated columns
* use external data sources appropriately 
* Reduce data before using a JOIN
* Do not treat WITH clauses as prepared statement
* Avoid over-sharding tables
* Avoid Javascript user-defined functions
* Use approximate aggregate functions
* Order last
* Optimize join patterns
* Place table with largest number of rows first, followed by table with the fewest rows, and place remaining tables by decreasing size.

### BigQuery Internals

BigQuery stores our data in a storage area called Colossus (columnar format). The storage price here is very cheap.

Jupiter network is inside BigQuery data centers. This provides 1TB per second network speed. This allows Computer and Storage on separate hardware. 

Dremel is the query execution engine. This divides query into a tree structure which communicates with Colossus.

BigQuery using column orientated storage allows for better aggregation on columns. Typically in data warehouses, we don't query all columns at the same time.

## Integrating BigQuery with Airflow

Last week we setup Airflow with Docker using a multi-node setup (although single-node would have been fine), and setup some DAGs to ingest data into GCP. This week we will extend this. 

Further up, we set up a partitioned table using queries in the UI. We can streamline this, by adding what we've done here to our DAG from week 2. Here's the steps I took:

1. Copy over our Airflow folder from week 2. Remove our current DAGs from the DAG directory, and add a new one `gcs_2_bq_dag.py`

2. Start Airflow up by running `docker compose up`

3. Wrote the code for `gcs_2_bq_dag.py`. Check this file in the current working directory to see the updates. Essentially, the new DAG is taking yellow taxi data parquet files from the `raw` folder in our data lake, and copying them to another folder in our data lake called `yellow`. It then creates an external table in BigQuery, and from that external table, creates a new partitioned table. 

4. For the homework, we actually need the FHV data for 2019 stored in BigQuery. You may already have a table set up from the previous week. I did not, therefore I slightly adapted some of the queries (from earlier on in this readme) to first create an external table in BigQuery using the FHV data in my data lake, before creating a native table from that external table. I'm sure there's a way to skip the external table step, but for now I've just left it.



