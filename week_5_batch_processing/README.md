# Week 5 ~ Batch Processing 

## Processing Data

Different ways to process data - Batch & Streaming.

Batch processing generally refers to processing data in batches within a specific time span, or processing large volumes of data all at once. It generally takes longer to process data, and is used when data size is known and finite. 

Stream processing generally refers to the processing of continuous streams of data immediately as it's produced. Processing of data is quick here, and is used when data size is unknown and infinite.

## Batch Jobs

Batch jobs can run weekly, daily, hourly, 3 times per hour, every 5 minutes, etc. Daily and hourly are the most common.

Technologies we can use for batch jobs are Python Scripts, SQL, Spark, and Flink. We might use something like Airflow to orchestrate these jobs.

Advantages:

* easy to mange
* we can retry them if something fails
* easy to scale 

Disadvantages:

* Delay (if we need to see data from previous hour, we need to wait an hour). However, often it's fine to wait, in that things aren't super time sensitive.

## Introduction to Spark

Apache Spark is a data processing engine, used for executing batch jobs, although it can also be used for streaming.

It is distributed. In a cluster we may have multiple machines, each one doing something with the data, and saving it somewhere.

It is also multi-language (Java, scala, Python, R). The Python wrapper is called PySpark.

## When to use Spark

Typically it would be used when your data is in a data lake (e.g. S3). Spark would pull the data from the DL, do something with it, then save it somewhere (e.g. back to the DL).

If you can express your job with SQL, you can use HIVE, Presto/Athena. This is recommended. If not, then you can use Spark.

## Installation (Mac M1)

Took a little while to get this setup, especially since I already had some features setup in different ways.

I first followed some instructions (here)[https://stackoverflow.com/questions/66464412/install-scala-to-apple-silicon] regarding Scala.

I then followed some instructions (here)[https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_batch_processing/setup/macos.md] regarding Apache Spark.

I tested it worked by typing `spark-shell` in the command window.

For PySpark, I ran `pip install pyspark` then tested by just typing `pyspark` into the command window. If all that fails, take a look (here)[https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_batch_processing/setup/pyspark.md].

I had also previously installed Java (version 17.0.2) although can't recall the exact way I had installed it.

