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
## Learning Spark

Apache Spark is a unified engine designed for large scale distributed processing, in data centers or in the cloud.

It provides in-memory storage for intermediate computations, making it faster than Hadoop MapReduce, which using disk storage.

1. Spark is Fast

    Spark takes advantage of unix-based operating systems, which themselves taking advantage of efficient multithreading and parallel processing. Spark also takes advantage of the fact that commodity servers come cheap.

    Spark also builds its query computations as a DAG. Its DAG scheduler construct an efficient computational graph that can usually be decomposed into task that are executed in parallel across workers on the cluster.

    Intermediate results are also retained in memory.

2. Ease of Use

    Spark offers a simple programming model that you can use to build big data applications in familiar languages.

3. Modular

    With Spark, you get a unified processing engine for workloads. No need for distinct engines for differing workloads.

4. Extensibility

    With Spark, you can use it to read data stored in various sources, processing it all in memory.

### Distributed Execution

As mentioned, Spark is a distributed data processing engine, with all its components working collectively on a cluster of machines.

A spark application consists of a:

- Spark Driver
    
    Responsible for instantiating a `SparkSession`. It communicates with the cluster manage, requests resources (cpu, memory etc) from the cluster manager, and transforms all Spark operations into DAG computations, schedules them, and distributes their execution as tasks across the Spark executors. It then communicates directly with the executors.

 - SparkSession

    Conduit to all Spark operations and data.

- Cluster Manager

    Responsible for managing and allocating resources for the cluster of nodes on which your Spark application runs. 

- Spark Executor

    Runs on each worker node in the cluster. It communicates with the driver program and is responsible for executing tasks on the workers.

- Deployment Modes

    Sparks supports multiple deployment modes, which allows for Spark to run in different configurations and environments. These can include `local` (e.g. runs on a single laptop), `Kubernetes` (runs in a Kubernetes pod), Standalone (can be run on any node in the cluster), etc.

- Distributed Data and Partitions

    Data is distributed across storage as partitions residing in either HDFS or cloud storage. While the data is distributed as partitions across the physical cluster, Spark treats each partition as a DataFrame in memory.

    This partitioning allows for efficient parallelism. It allows executors to process the data that is close to them, minimizing network bandwidth.
