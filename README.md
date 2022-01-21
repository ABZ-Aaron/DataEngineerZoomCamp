# DataEngineerZoomCamp

I'm partaking in a Data Engineering [Bootcamp / Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp). 

I'll store my progress here.

## The Task 

The goal is to develop a data pipeline following the architecture below. We will be looking at New York City Taxi data!

![Alt text](/images/arch_1.jpg?raw=true "Optional Title")

We'll use a range of tools:

* Google Cloud Platform (GCP): Cloud-based auto-scaling platform by Google
* Google Cloud Storage (GCS): Data Lake
* BigQuery: Data Warehouse
* Terraform: Infrastructure-as-Code (IaC)
* Docker: Containerization
* SQL: Data Analysis & Exploration
* Airflow: Pipeline Orchestration
* DBT: Data Transformation
* Spark: Distributed Processing
* Kafka: Streaming

Each week we'll work through a series of [videos](https://youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb). We'll follow this up with homework exercises.

## Week 1

This week we'll be cover basics with the following:

* PostgreSQL
* Terraform
* Docker
* Google Cloud Platform

---

1. Our first task was creating a `Dockerfile` which is used to build our Docker image.

A Dockerfile is a text document. It contains all the commands one could call on the command line to create a Docker image. In other words, Docker can build images automatically by reading instructions from a Dockerfile.

But wait... what's a Docker image?

Think of this like a blueprint... a blueprint for creating Docker container. A container is a lightweight, standalone, executable package of software which includes everything needed to run an application)

As of right now, our Dockerfile will specify a `parent image` (in this case, Python) which all subsequent commands will be based on. The Dockerfile specifies certain Python packages that'll be installed. It also copies a Python pipeline file (see next step) to the filesystem of the container. Additionally, it will run this file upon creation of the container.

2. Next up, we created a `pipeline.py` file which will be run when we run our image to generate a container, at least for now.

3. I then setup a python virtual environment and pip installed `pgcli` in my main directory. This is a command line interface for Postgres.

4. Next up, we ran a `postgres` image using the below, in order to create a container where we can work with PostgreSQL. 

Notice we use `docker run -it`. The optional option ensures we can cancel the creation of our container if we wish. The first part `docker run` creates a container from a given image and starts the container. If the image is not present on the local system, it is pulled from the registry.

You can see below we're passing a number of options and inputs `-e`, `-v` etc. The name of image we've passed to it is `postgres:13` which will be pulled from the registry. 

```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5431:5432 \
  postgres:13
  ```

* -e POSTGRES_USER : The name of our PostgreSQL user
* -e POSTGRES_PASSWORD : The password for our user
* -e POSTGRES_DB : The name we want for our database
* -v : This specifies an external volume. Basically, postgres would by default create a database on a folder inside the container, which will disappear when we kill it. This is good, because it allows us to generate as many containers as needed (all of them identical). However, in our case, we mounted a volume. In other words, the internal folder in the container is replicated to the external, local folder we specified. This allows the container to access that info when recreated again. This is how we handle persistent data with stateless containers.
* -p 5431:5432 : This maps a postgres port on our host machine to one in our container. It seemed that 5432 was already in use on my machine, so I used 5431. 

---

I actually had some issues with this. What I ended up doing was deleting the `ny_taxi_postgres_data` folder from my current working directory, after it had been created. I then recreated this and adjusted permissions using:

`sudo chmod a+rwx ny_taxi_postgres_data`

I believe this adds read, write and execute permissions to the folder.

I then made sure to specify port `-p 5431:5432` and ran the image.

---

5. Next up, I connected to my new database using the postgres command line tool we installed earlier. I specified the postgres port, database name, user, and localhost as the host - just to check things are working okay, and that we can interact with our currently empty database.

`pgcli -h localhost -p 5431 -u root -d ny_taxi`

6. Next up I create a Jupyter Notebook file, which I'll write via VS Code. We'll use this to load CSV data into our database.

7. We need to download the data we're going to be working with (in CSV format). For this, it is the 2021 Yellow Taxi Trip Records located [here](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page). We can copy the link to this and run the following to download it to our current working directory. The `wget` command is a network donwloader.

`wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv`

8. In this step, we wrote our `upload-data` jupyter notebook script. This essentially connected to our database, read from the CSV file (chunk by chunk) into a pandas dataframe, created a table within our database, and added our CSV data to the database in chunks.

9. Next I setup `pgadmin`. This is a way for us to interact with our database in a more user friendly, web based graphical interface. I actually have pgadmin installed. But we can also run a docker container of this. We just need to make sure our postgres and pgadmin containers are in the same `network` - and give both of them a name in that network. This ensures that we can connect to our postgres engine, and thus database, from pgadmin.

Here's how we can amend our `docker run` command for postgres to add it to a network and give it a name. Giving a name to pgadmin isn't too important, but it's important we give postgres a name so we can connect to it from pgadmin.

```
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5431:5432 \
--network=pg-network \
--name pg-database-2 \
postgres:13
```

Here is how we set up pgadmin. Notice how we've given them both the same network name:

```
docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
--network=pg-network \
--name pgadmin-2 \
dpage/pgadmin4
```

* -e PGADMIN_DEFAUL_EMAIL = email we'll use to sign into pgadmin
* -e PGADMIN_DEFAULT_PASSWORD = password we'll need to sign into pgadmin
* -p 8080:80 = like with postgres, we set up ports to map pgadmin to our host machine.

10. Once we run both of these in seperate terminals, we have created two containers. To access pgadmin, we can got to `localhost:8080` in our browser, and use the pgadmin details to login. We should also make sure to specify `pg-database-2` as the host name we want to connect to.

11.  Next up, I completed the data ingestion pipeline script, now named `ingest-data` and converted it to a script (instead of a jupyter notebook). 

It's not perfect, but will fix it later. It's written in such a way that, when we run our image to create a container, we can pass it arguments to specify our table name, postgres details, and so.





