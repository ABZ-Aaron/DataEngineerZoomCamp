# Week 2

The goal of this week is to orchestrate a job to ingest web data to a Data Lake in it's raw form.

## Data Lakes

### What is a Data Lake?

A Data Lake is a repository which holds Big Data from many sources, which include structured, semi-structured, and unstructured data.

* Ingest Unstructured and Structured data
* Stores, secures, and protects data at unlimited scales
* Connects data with analytics and machine learning tools
* Allows us to store and access data quickly, without thinking about schemas

They contain huge amounts of data, sometimes ingesting data everyday. In Data Warehousing, data is usually structured, and data size is generally small.

### ELT vs ETL

**Extract, Load and Transform** vs. **Extract, Transform and Load**.

ELT provides data lake support (schema on read). It is used for large amounts of data.

### Problems

Data lakes can turn into "data swamps". This happens due to no versioning, incompatible schemas for same data without versioning, no metadata associated, and joins are not possible. Basically, it can become a bit of a mess!

### Providers

Cloud providers provide data lakes solutions. 

* Azure - AZURE BLOB
* AWS - S3
* GCP - Cloud Storage

## Workflow Orchestration

A data pipelines can be generally defined as sript(s) that take in data, do something to the data, and output it somewhere. This is what our pipeline looked like last week:

<img src="https://github.com/ABZ-Aaron/DataEngineerZoomCamp/blob/master/images/pipeline.png" width=100% height=40%>

[source](https://youtu.be/0yK7LXwYeD0)

This week we will work on a slightly more complex pipeline. This will involve extracting data from the web with `wget` or something else to produce a CSV which we store locally. We will convert this CSV to a more effective format - parquet. We'll take this file and upload to Google Cloud Storage (data lake). We will then copy this to Google Biq Query (data warehouse).

We need to make sure we run these in the right order. 

<img src="https://github.com/ABZ-Aaron/DataEngineerZoomCamp/blob/master/images/workflow.png" width=100% height=40%>

[source](https://youtu.be/0yK7LXwYeD0)

This is called a data workflow, or sometimes known as a DAG (directed acyclic graph). The edges are the dependencies. So for example, parquet depends on the the `wget` stage. An example of the above with a cycle could be if we re-run the `wget` stage after uploading to GCS.

A parameter of the entire workflow could be month (e.g. 2021-01). 

But how to we manage this workflow / DAG? 

There are many tools:

* Luigi (not as popular nowadays)
* PREFECT
* Apache Airflow (this is what we will use, and is probably the most popular)

## Airflow

Apache Airflow is a platform to programmatically schedule and mointor workflows as DAGs. With Airflow, we have command line utilities as well as a user interface to visualise pipelines, monitor progress and troubleshoot issues.

Here's the general architecture:

<img src="https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_2_data_ingestion/airflow/arch-diag-basic.png" width=100% height=40%>

[source](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_2_data_ingestion/airflow/2_concepts.md)

* `Web Server` - GUI to inspect, trigger and debug behaviour of DAGS. Available at http://localhost:8080.
* `Scheduler` - Responsible for scheduling jobs.
* `Worker` - Executes the tasks given by scheduler.
* `MetaData Database` - Backend to Airflow. Used by scheduler and executeor and webserver to store data.
* `redis` - Forwards messages from scheduler to worker
* `flower`- Flower app for monitoring the environment. Available at http://localhost:5555.
* `airflow-inti` - Initialises service

If we're running Airflow in Docker, we use something called `CeleryExecutor`

### What is an Executor and what is CeleryExecutor?

Once we define a DAG, the following needs to happen in order for a single set of tasks within that DAG to execute and complete from start to finish:

1. The `Metadata Database` keeps a record of all tasks within the DAG, along with their status (e.g. failed, running, scheduled).

2. The `Scheduler` reads from the `Metadata Database` to check the status of each tasks and decide what needs done.

3. The `Executor` works with the `Scheduler` to determine what resources will complete those tasks as they're queued. 

One such `Executor` is `CeleryExecutor` which is built for horizontal scaling, or distributed computing. This works with pools of independent `workders` across which it can delegate tasks.

### Running Airflow with Docker

There's a few steps required to get Airflow working with Docker:

1. Install [Docker Community Edition](https://docs.docker.com/engine/installation/) on your local machine.
2. Configure Docker instance to use 4GB of memory.
3. Install [Dockder Compose](https://docs.docker.com/compose/install/).

We then fetch `docker-compose.yaml` which uses the latest airflow image. To do so, run:

`curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.3/docker-compose.yaml'`

Within this file, there are several definitions:

* `airflow-scheduler` - This monitors all tasks & DAGs.
* `airflow-webserver` - Available at http://localhost:8080
* `airflow-worker` - This executes the tasks given by scheduler
* `airflow-init` - Initialises services
* `flower` - Monitors oru environment
* `postgres` - The database
* `redis` - broker and forwards messages from scheduler to worker

With these services, we are able to run Airflow with `CeleryExecutor`.

Some of these services are mounted, meaning their contents are synced between our local machine and the container:

* `/dags` - DAG files go here
* `/logs` - Logs from task execution & scheduler
* `/plugins` - Custom plugins go here

Some workflow components:

* DAG - Specifies the dependencies between a set of tasks with explicit execution order
* Tasks - A definied unit of work. These define what to do (e.g. running analysis)
* DAG Run - Individual execution of a DAG
* Task Instance - Individual run of a single Task. Each task has a state (failed, success, etc). Ideally, they run from:

`none` > `scheduled` > `queued` > `running` > `success`

### Prerequisites for Week 2

Here is some initial setup required for week 2 of this zoomcamp:

1. Rename our Google Cloud Platform Service Account Credentials JSON file to `google_credentials.json`. Store it in our home directory.

```bash
cd ~ && mkdir -p ~/.google/credentials/
mv <path to JSON file> ~/.google/credentials/google_credentials.json
```

2. Upgrade `docker-compose` to version 2.x+ if required. 

3. Set memory of Docker Engine to 4-8GB. This can be done in Docker Desktop.

4. Make sure you have Python version 3.7+ installed. Find python version with `python --version`

4. Create subdirectory called `airflow` in `project` directory.

5. Import official image and setup for latest Airflow version. I mentioned this earlier:

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.3/docker-compose.yaml'
```

6. This might only be required on linux. The Quick Start needs to know our host user id and needs to have group id set to 0. This ensure files creates in `dags`, `logs` and `plugins` will be created with root user:

```bash
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

7. If you want to run Airflow locally, we might want to use an extended image with additional dependencies such as python packages. 

8. Create a `Dockerfile` pointing to Airflow version we've just downloaded (e.g. apache/airflow:2.2.3). In the `Dockerfile` add custom packages to be installed - `glcoud`. This will allow us to connect with the GCS bucket/data lake. Also integrate `requirements.txt` which will be used to install libraries via `pip install`.

9. In Docker Compose YAML file, under `x-airflow-common`, remove the image tag to replace with our build from the Dockerfile. Mount `google_credentials` in `volumes` section as read-only. Set environment variables `GOOGLE_APPLICATION_CREDENTIALS` AND `AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT`. Change `AIRFLOW__CORE__LOAD_EXAMPLES` to false

For the last steps, you can copy the `Dockerfile` and `docker-compose.yml` from the [zoomcamp repo](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_2_data_ingestion/airflow).

## Moving files from AWS to GPC with Transfer Service

`Google Transfer Service` allows us to pull data from a variety of different sources to our Google Cloud Storage, and move data between these. 

To initialise a job, we can use the UI, or we can use Terraform. 

### UI Method

1. Choose source packets (e.g. Amazon S3)
    * provide access keys (access key id and secret access key - at least if working with AWS)
2. Choose destination or bucket to store our data
3. Choose settings
    * Do we want to overwrite data, or delete data?
    * Name transfer job
4. Scheduling options
    * When do we want this to run? Every day?

And that's it!

If we go inside the job, we can view some details about it, pause the run, cancel it, check its progress, have fast its transferring, and so on.

BUT....

Google Transfer does cost money. You pay on a GB basis. This can be a cheaper option that spending a lot of time developing an Airflow DAG. But, if you're running it regularly, you might be better building a transfer service on your own using something like Airflow.

### Terraform Method

I'm not going to spend a lot of time understanding Terraform right now, but click [here](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_transfer_job) for an example usage (nightly transfer job from an AWS S3 bucket to a GCS bucket). It's not too difficult to understand what the code is doing at each step.

If we wanted to configue something like this, we would need to setup a transfer_service.tf file within our terraform directory and run the usual commands `terraform plan`, `terraform apply` etc. You can see more details of this by checking out the terraform branch from the Zoomcamp main GitHub repository.

