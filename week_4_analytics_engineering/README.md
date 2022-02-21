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

    We then create our DBT account and project, and link it to BigQuery and our Github Repo. I'm actually going to use a separate GitHub Repo for this.

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

Useful to note that DBT provides us with a starter project, which provides basic folders and files we will need.

Here I'll document the step I take to starting a project in DBT Cloud.

1. Upon entering the project in the DBT, because we've linked it up with Github, I can see my Data Engineering ZoomCamp file and folders within the cloud IDE. Note that I actually created a separate repo for [this](https://github.com/ABZ-Aaron/ny_taxi_rides_zoomcamp).

2. Click "Initialize your project" (big green button)

3. Follow the instructions [here](https://www.youtube.com/watch?v=UVI30Vxzd6c&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=38).

### Materialization

Read an overview of this [here](https://docs.getdbt.com/docs/building-a-dbt-project/building-models/materializations).

Materialization strategies are:

1. Table

    Drop table if exists in Data Warehouse, and create table in schema we are working with

1. View

    Create or alter view with our schema

1. Incremental

    Run our model incrementally

1. Ephemeral

    Derived model

### The FROM clause of a DBT Model

We want to use sources that we loaded from green and yellow trip data. For this we will use a macro called `sources`.

Here we can define however many sources as we want. The macro will resolve the name for us with the right schema, and build dependencies automatically. 

We can also load data from CSV files (this is called `seeds`). It's basically just a copy command. These CSV files will be stored in our repo under seed folder.

This is recommended for data that doesn't change frequently. Runs with `dbt seed -s file_name`. 

The `Ref` macro references the underlying tables and views that were building the data warehouse. Here dependencies are built automatically. 

## Errors when working with DBT

One issues I came across was that when trying to run DBT, I would get an error telling me that dataset could not be found in the US region. 

I think this was due my BigQuery being based in Europe. I went to Profile > Credentials > [big query project] and changed `dataset` value from `dbt_aaron` to `trips_data_all`. 

Need to investigate this further so I understand better. The `dbt_aaron` was set to US. I think perhaps this and the dataset we're taking data from both need to be in the same location. So by just setting my output location to trips_data_all it worked, although ideally I would just set that location to US as well (although the process for this is longer).

## Macros

These are like functions we write in Jinja. 

These macros return code. So rather than concatenating A and B (if that's what we want our function to do) it will actually return the code used to concat A & B, rather than do the concat itself.

This is helpful if we want to maintain same kind of transformation for different models.

To define it, we create files under the macros folder, using a combo of SQL and Jinja. 

* {# #} - comment block

* {% %} - Execute something

Note, we can see compiled code under the `target` folder.

So we can create our own macros. Or, we can import macros from other projects if we like using `packages`. By adding these packages, we can use their models and macros.

We just need to create a `packages.yml` and ad the relevant packages we want there. We then run `dbt deps` to install the packages specified here.

## Variables

Same concept as any other programming language. Means we can use variables across project, and translate during compilation time.

Global variables can be defined under the `project.yml` or they can be defined in the terminal

## DBT Seeds

For this part, we're just going to create a file `taxi_zone_lookup.csv` and copy from original file. This is the simplest for our purposes.

Under the `dbt_project.yml` we can actually add what column types we want for this csv. Columns we don't define here will just use the default type.

## DBT Run

When we run `dim run`, we'll run everything, except the seed. If we want to run the seeds too, we can run `dim build`.

If we run something like `dbt run --select fact_trips` this would only run the fact_trips model.

If we run something like `dbt run --select +fact_trips` this will run everything that fact_trips needs.

## Testing & Documenting DBT Models

This is not required. However, it is recommended. 

A test is an assumption that we make about our data (a behavior it should have).

Tests are essentially `select` statement. 

Tests are defined in a `yml` file. We can define tests here such as `Unique`, `Not NUll`, `Accepted Values`, or `A foreign key to another table`. These are run for the columns we specified. 

We can also create our own custom tests.

With DBT we have documentation, which is rendered as a website. Documentation includes model code, model dependencies, sources, etc. It will also add info about data warehouse.

For tests, we can define these is our `schema.yml` under our staging area.

## Deployment

This is the process of running the models we created in our development environment in a production environment.

We should be able to test our models without affecting production environment. 

A deployment environment will normally have a different schema in our DW and a different user.

The workflow is like:

- Develop in a user branch
- Open a PR to merge into main branch
- Merge branch to main branch
- Run the new models in the production environment using the main branch
- Schedule the models

## Running a DBT project in production

DBT cloud includes a scheduler where to create jobs to run in production. A single job can run multiple commands. These jobs can be run manually or on schedule. 

Each job will keep a log of runs over time. Each run will have logs for each command. A job can also generate documentation that could be viewed under the run information. 

If DBT source freshness was run, the results can also be viewed at the end of the job.

## What is continuous integration (CI)?

CI is the practice of regularly merging development branches into a central repo where automated builds and tests are run. 

The goal is to reduce adding bugs to the production code and maintain a more stable project.

DBT enables us to allow CI on pull requests, which is enabled via webhooks from GitHub where we are hosting our repo.

When a PR is ready to be merged, a webhook is received in DBT cloud from Github that will enqueue a new run of the specified job.

The run of the CI job will be against a temporary schema. 

No PR will be able to be merged unless the run has been completely successfully. 

## Example

Once we commit. Our changes will be seen in our Github repo.

Afterwards, we will need to create a new branch to work from in DBT. The main branch will be protected. By working on a separate branch, we ensure we are not working on a live production environment.

When we set this up, we specify a new dataset where we store the tables etc in BigQuery. I called this production.
