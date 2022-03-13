# Apache Spark

Single machines typically don't have enough power or resources to perform huge computations. However, a cluster (group of machines) pools the resources of many machines together allows us to use the cumulative resources as if they were one.

To coordinate work between these groups of machines, we need a framework. This is where Spark comes in.

## Spark Applications

We submit `Spark Applications` to cluster managers (e.g. YARN) which grants resources to our applications so that we can complete our work.

These applications consist of a `driver` process and a set of `executor processes`. 

The driver process runs our main function, sits on a node within the cluster, and is responsible for maintaining information about the Spark Application, responding to user's input, and distributing work across executors. 

The executors are responsible for executing the work the driver assigns to them, and reporting the state of the computation back to the driver node.

The cluster manager controls the physical machines and allocates resources to Spark Application.

Note that Spark also has a `local mode`. In this mode, the driver and executors simple run as threads on an individual computer, rather than on a cluster of machines.

## Language APIs

Spark's APIs allow us to run Spark code in other languages. These include `Scala` (the default language of Spark), `Java`, `Python`, `R`, and `SQL`. 

## Starting Spark

But how do we send our user commands and data to a Spark Application?

For this, we use something known as a `SparkSession`.

Basically, the driver process which controls our Spark Application manifests itself to the user as an object called the SparkSession. This is the way Spark executes user-defined manipulation across a cluster. There is a one-to-one correspondence between a SparkSession and Spark Application.

## DataFrames

These are the most common structured APIs of Spark and represent a table of data with rows and columns. The difference between this and a spreadsheet, is that a spreadsheet sits on one computer in one specific location. A Spark DataFrame can span thousands of computers. They are similar to something like a Pandas DataFrame, except they are on multiple computers or threads. 

## Partitions

For all executors to work in parallel, Spark breaks data up into chunks called partitions. These are collections of rows that sit on a physical machine in the cluster. 

A DataFrame's partition represents how data is distributed across your cluster of machines during execution. 

## Transformations

In Spark, core data structures are immutable. Spark will transform these data structures, rather than change what's in them. 

Spark will not act on transformations until we call an action. 

In Spark we have `wide transformations` (shuffles) and `narrow transformations`

### Lazy Evaluation

When we express some operation, we build up a `plan of transformation`. Spark will wait until the last minute to execute the code. Spark will optimize the entire data flow from end to end.

## Actions

Transformations allow us to build up our logical transformation plan. To trigger the actual computation, we run an action. The simplest action is count:

```python
something.count()
```

Some action allow us to view data in a console, some allow us to collect data to native objects, and som allow us to write to output. 

In specifying an action, we start the Spark job. 

## Spark UI

During Spark's execution, users can monitor progress of their job via the Spark UI. This is available on port 4040 of the driver node

http://localhost:4040

This maintains info on the state of our Spark job, environment, and cluster state.

To sum up, a Spark job represents a set of transformations triggered by an individual action, and we can monitor this from the Spark UI.

## DataFrames and SQL

Spark SQL allows us to register any DataFrame as a Table or View (temporary table) and query it using SQL. There's no performance difference between SQL queries or writing DataFrame code. They both compile to the same underlying plan that we specify in DataFrame code.

Here's us creating a DataFrame:

```python
flightData2015 = spark\
   .read\
   .option("inferSchema", "true")\
   .option("header", "true")\
   .csv("/mnt/defg/flight-data/csv/2015-summary.csv")
```

Here's us creating a view from this DataFrame which we can then query with SQL:

```python
flightData2015.createOrReplaceTempView("flight_data_2015")
```

Now we can run our query and return a new DataFrame. We also do it with the DataFrame way:

```python
sqlWay = spark.sql("""
SELECT DEST_COUNTRY_NAME, count(1)
FROM flight_data_2015
GROUP BY DEST_COUNTRY_NAME
""")

dataFrameWay = flightData2015\
.groupBy("DEST_COUNTRY_NAME")\
.count()

sqlWay.explain()
dataFrameWay.explain()
```

Both plans compile the exact same underlying plan.

## Production Applications

Spark makes it easy to turn interactive exploration into production applications with a tool called `spark-submit`.

This allows you to submit your applications to currently managed clusters to run. Once you submit, application will run until application exits or errors. 

