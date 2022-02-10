# Week 4 ~ Analytics Engineering

For this week, we'll be looking at DBT. Specifically, we'll be transforming the data in BigQuery to Analytical Views, developing a DBT project.

# Introduction to DBT

The following is based on a [YouTube](https://www.youtube.com/watch?v=M8oi7nSaWps) video I watched.

It used to be the case that many analytics teams were focused on infrastructure, compute and storage for large data. Nowadays, with the shift toward ELT and warehouse tech has addressed some issues (cheap storage, SQL for data transformation).

However, data modelling hasn't changed much. We typically use stuff like `custom code and airflow` or `GUI modeling`. These both come with issues (expensive, steep learning curves, lots of in-house infrastructure, sometimes slow).

These old methods result in datasets being slow to build, as well as untrustworthy data.

DBT addresses these issues:

1. Anyone who knowns SQL can author their own data pipelines
1. Their tools enable them to work like software engineers (version control, documentation, etc)

## Why should I transform my data?

* Cleaning Data
* De-duplicating Data
* Restructuring Data
* Filtering Data
* Aggregating Data
* Join Data

## What is DBT?

An open source transform tool that allows anyone with SQL knowledge to author their own data pipelines.

DBT is an orchestration layer that sits on top of a data warehouse. It pushes code down to warehouse versus ETL tools that do it in memory. Pushing down code is more secure, easier to maintain (one server to maintain), and faster.

* DBT Core - Open Source Data Transformation. You would interface with this via CLI. This is open source and free to use.
* DBT Cloud - Fully managed DBT experience. This sits on top of DBT Core. It includes a web based IDE, logging, alerting, integrated documentation, and free for individuals.

## Core Concepts

### Express Transforms in DBT with SQL SELECT

No reason to write boilerplate code. We express business logic in SQL. Anyone who can read SQL can understand transform code.

DBT generated the DDL at run time.

### Automatically build the DAG with ref(s)

The ref statement automatically handles dependencies in DBT models. The ref statement is Jinja code behind the scenes.

### Tests ensure model accuracy

DBT has a testing framework. Test assumptions are written in a YAML file. DBT can test if a column is unique, doesn't contain NULLs, etc.

If any test fails, you can prevent downstream models from running. This can essentially stop bad data from entering your data warehouse. Alerts can also be setup. 

You don't have to actually write SQL here. DBT will convert what you've written into the YAML to queries.

### Documentation is accessible and easily updated

Auto-generating documentation. DBT uses everything it knows about your project:

* Manually added descriptions (from YML file)
* Model dependencies
* Model SQL
* Sources
* Tests
* Column name and types of data warehouse
* Table Statistics

So as you are building out your models, as long as you write descriptions, everything is auto-generated for you.

### Use macros to write reusable SQL

Using Jinja turns your dbt project into a programming environment for SQL

* use control structures, such as loops, in SQL 
* use environment variables in your dbt project
* operate on the results in one query to generate another query
* abstract snippets of SQL into reusable macros (these are like functions in other programming languages). Jinja will generate SQL at runtime for us.

## Conclusion

DBT workflow offers higher quality analytics faster, cheaper, and of higher quality. This allows Data Engineers to move onto bigger and better things!

# Prerequisites

There are a few perquisites for this week, most of which I've done:

* BigQuery or Postgres
* Yellow Taxi Data (2019-2020
* Green Taxi Data (2019-2020)
* FHV Data (2019)

However, it turns out I haven't ingested Green Taxi data for years 2019 - 2020 into BigQuery, or even my Data Lake storage. So I'll start by copying over my `airflow` directory from Week 3. I'll remove some obsolete files, and update the `data_ingestion_gcs_dag_v02.py` and `gcs_2_bq_dag.py` file to download and ingest Green Taxi data for years 2019 - 2020. 

Although I could update the 'upload to GCS bucket' DGA to run twice for both Yellow and Green data, it's easier just to create a separate DAG for Green data, since we've already done everything we need to with the Yellow data. It's the same with our 'upload to GCS BigQuery from bucket' DAG. We'll just create one specific DAG for Green data rather than refactoring it for both Yellow and Green (since we already have our Yellow data in BigQuery).

We could also have chosen to combine DAGs to create one large DAG. I'll perhaps try doing this once I have time. Steps like creating a green and yellow folder could also be more easily be implemented when we first upload to our data lake bucket.

```python
download_dataset >> convert_csv_to_parquet >> upload_to_google_bucket >> move_data_to_folders >> create_external_table_in_bigquery >> create_native_table_in_bigquery
```
I've actually added 2021 and 2022 data to the storage bucket, so I'll delete these before running the `gcs_2_bq_dag.py`.

NOTE: There was a issue with the `ehail_fee` column for the green taxi data when ingesting into BigQuery. Didn't want to spend too long on this, so decided just to exclude the column when creating the native table in BigQuery.

# DBT Prerequisites

Next, we'll need to set DBT up using BigQuery.

1. Create [DBT Account](https://www.getdbt.com/signup/) and connect to BigQuery using the instruction [here](https://docs.getdbt.com/docs/dbt-cloud/cloud-configuring-dbt-cloud/cloud-setting-up-bigquery-oauth) and [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md).

    First we create some credentials for accessing BigQuery via DBT. These credentials are stored in a JSON, and act a bit like a password/email combo for BigQuery.

    We then create our DBT account and project, and link it to BigQuery and our Github Repo.

# Introduction to Analytics Engineering

In a typically data team, we have the data engineers, analytics engineer and data analysts. 

* Data Engineer - Prepare and maintain data infrastructure
* Data Analyst - Use data to answer questions
* Analytics Engineer - Introduces software engineering practices to the efforts of data analysts & scientists

## Tooling

* Data Loading
* Data Storing (data warehouses like Snowflake, Bigquery, and Redshift)
* Data Modelling (DBT or Data Form)
* Data Presentation (Tableu, Google Data Studio)

## ETL v ELT

* ETL - transform before data warehouse

    This is more stable and compliant for data analysis, but has higher storage and compute costs.

* ELT - transform in the data warehouse
    
    This is faster and more flexible for data analysis, as well as less maintenance and cost.

## Kimball's Dimensional Modeling

**Objective:**

Deliver data understandable to business users, and delivery must be fast.

**Approach:**

Prioritizes user understandability and query performance over non redundant data.

## Elements of Dimensional Modeling

STAR SCHEMA of a Data Warehouse

**Facts Table**

- Measurements, metrics or facts (e.g. Sales facts, or Orders)
- Corresponds to a business process
- 'verbs'

**Dimensional Table**

- Corresponds to a business entity (e.g. Customer or Product)
- Provides context to a business process
- 'nouns'

## Architecture of Dimensional Modeling

**Stage Area**

- Contains raw data and not meant to be exposed to everyone.

**Processing Area**

- From raw data to data models. Focuses in efficiency. Ensuring standards.

**Presentation Area**

- Final presentation of the data. Exposure to business stakeholders.

# Starting a DBT project

## How are we going to use DBT?

We'll use the cloud version, so no local installation - at least if using BigQuery. 

Our project will have trip data (which we've loaded into BigQuery). We'll add a CSV file with the taxi lookup data. We'll use DBT to transform our data in BigQuery, and then express our data within a dashboard.

## Create DBT project

