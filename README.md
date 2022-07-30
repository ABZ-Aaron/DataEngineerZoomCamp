# Data Engineering ZoomCamp

I am partaking in a Data Engineering [Bootcamp / Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) and will be tracking my progress here.

Each week I'll work through a series of [videos](https://youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb) and follow this up with homework exercises.

See my final project [here](https://github.com/ABZ-Aaron/Reddit-API-Pipeline).

## The Task 

The goal is to develop a data pipeline following the architecture below. We will be looking at New York City Taxi data.

<img src="https://github.com/ABZ-Aaron/DataEngineerZoomCamp/blob/master/images/arch_1.jpg" width=60% height=60%>

## Tools

We'll use a range of tools:

* [Google Cloud Platform (GCP)](https://cloud.google.com): Cloud-based auto-scaling platform by Google
* [Google Cloud Storage (GCS)](https://cloud.google.com/learn/what-is-a-data-lake): Data Lake
* [BigQuery](https://cloud.google.com/bigquery): Data Warehouse
* [Terraform](https://www.terraform.io): Infrastructure-as-Code (IaC)
* [Docker](https://www.docker.com): Containerization
* [SQL](https://www.postgresqltutorial.com): Data Analysis & Exploration
* [Airflow](https://airflow.apache.org): Pipeline Orchestration
* [DBT](https://www.getdbt.com): Data Transformation
* [Spark](https://spark.apache.org): Distributed Processing
* [Kafka](https://kafka.apache.org): Streaming

## Progress

* [Week1](https://github.com/ABZ-Aaron/DataEngineerZoomCamp/tree/master/week_1_basics_n_setup)

  **PostgreSQL | Terraform | Docker | Google Cloud Platform**

  This week we were introduced to Docker; a framework for managing containers. We created containers for PostgreSQL and PgAdmin, before finally creating our own image, which when run, created and populated tables within a PostgreSQL database.
  
  Next up we learned about Google Cloud Platform (GCP) which is a suite of Google Cloud Computing resources. Here we setup a service account (more or less a user account for services running in GCP) as well a a Virtual Machine, connecting to it using SSH via the command line.
  
  We was also introduced to Terraform - an infrastructure-as-code tool. We used this to generate Big Query and Google Cloud Storage on GCP.
  
  I enjoyed this week, although it was heavy going. A lot of late nights trying to understand new concepts and fix unexpected bugs related to Docker. I now feel significantly more confident in understanding and utilsing this tool.
  
* [Week 2](https://github.com/ABZ-Aaron/DataEngineerZoomCamp/tree/master/week_2_data_ingestion)

  **Airflow | Docker**

  This week we learned about Airflow; an orchestration tool.
  
  Here we setup a Docker container with Airflow. We then setup a few basic DAGs. Each of these extracted CSV data from a website, converted them to parquet format, before loading them into our GCP data lake.
  
  This week was easier than last week, but still challenging. It feels good to understand Airflow at a basic level, and implement some of my own DAGs. The configuation with Docker was a little tricky, but I plan on spending a bit more time going through the code to understand it all.
  
* [Week 3](https://github.com/ABZ-Aaron/DataEngineerZoomCamp/tree/master/week_3_data_warehouse)

  **BigQuery**

  This week was focused on Data Warehousing, specifically BigQuery.

  This was a more relaxed week. Not as much to take in, giving me a chance to catch up. It mostly consisted of BigQuery basics, ingesting more data into it, and playing around with partitioning and clustering. 

  I don't feel like I learned as much this week, and have made a note to spend more time on Data Warehousing and Dimensional Modeling in my own time.
 
* [Week 4](https://github.com/ABZ-Aaron/DataEngineerZoomCamp/tree/master/week_4_analytics_engineering)

  **DBT | Google Data Studio**

  This week we looked into DBT and Analytics Engineering.

  We learned that DBT sits on top of data warehouses and can be used to develop pipelines using SELECT statements, as well as test and document our models.

  Most of the week was spent writing some DBT models, before eventually pushing this to production. 

  We also gained some exposure to Google Data Studio, which we used to generate a simple dashboard.

  This was an interesting week, and was good to see what a more modern data stack might look like.

* [Week 5](https://github.com/ABZ-Aaron/DataEngineerZoomCamp/blob/master/week_5_batch_processing)

  **Spark | Batch Processing**

  pending...

* [Week 6](https://github.com/ABZ-Aaron/DataEngineerZoomCamp/blob/master/week_6_stream_processing)

  **Kafka | Stream Processing**

  pending...

