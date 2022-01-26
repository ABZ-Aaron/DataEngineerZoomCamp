# Data Engineering ZoomCamp

I'm partaking in a Data Engineering [Bootcamp / Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) and will be tracking my progress here. I can't promise these notes will be neat and tidy, but I hope they can help anyone who is working through this bootcamp. 

I'll aim to document any problems or errors I come across during my journey, and describe concepts that I found tricky.

Each week I'll work through a series of [videos](https://youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb) and follow this up with homework exercises.

## The Task 

The goal is to develop a data pipeline following the architecture below. We will be looking at New York City Taxi data!

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

* [Week1](https://github.com/ABZ-Aaron/DataEngineerZoomCamp/tree/master/week_1_basics_n_setup) - PostgreSQL | Terraform | Docker | Google Cloud Platform

  This week was a lot of setup, and a lot of work! Here I was introduced to Docker - a framework for managing containers. I created some containers for PostgreSQL and PgAdmin, before finally creating my own image, which when run, created and populated tables within my PostgreSQL database.
  
  Next up I learned a bit about Google Cloud Platform (GCP), which is suite of Google Cloud Computing resources. Here I setup a service account (more or less a user account for service running in GCP and even setup a Virtual Machine, and connected to it using SSH right from my terminal.
  
  I was also introduced to Terraform - an infrastructure-as-code tool. I used this to generate some stuff on GCP - Big Query and Google Cloud Storage - from a simple script.
  
  I enjoyed this week, although it was heavy going. A lot of late nights trying to understand new concepts and fix unexpected bugs. Although I'm by no means an expert in any of these tools, I do feel more confident in understanding and utilsing them. 
  
* [Week 2](https://github.com/ABZ-Aaron/DataEngineerZoomCamp/tree/master/week_2_data_ingestion)

This week I'm learning about Airflow!

* Week 3: Pending...
* Week 4: Pending...
* Week 5: Pending...
* Week 6: Pending...

