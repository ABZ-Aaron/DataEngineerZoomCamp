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

### Docker & Postgres

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

  Here's how we can amend our `docker run` command for postgres to add it to a network and give it a name. Giving a name to pgadmin isn't too important, but it's important we give postgres a name so we can connect to it from pgadmin. We first creare the network:

  `docker network create pg-network`

  Then run postgres container:

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

10. Once we run both of these in seperate terminals, we have created two containers. 

 To access pgadmin, we can got to `localhost:8080` in our browser, and use the pgadmin details to login. We should also make sure to specify `pg-database-2` as the host name we want to connect to.

11. Next up, I completed the data ingestion pipeline script, now named `ingest-data` and converted it to a python script (instead of a jupyter notebook). 

It's not perfect, but will fix it later. It's written in such a way that, when we run our image to create a container, we can pass it arguments to specify our table name, postgres details, and so. Regarding passwords and usernames, these would typically be set as environmental variables, and loaded in. But we won't worry about that now.

Our Dockerfile is now set to run this ingestion script, as well as install relevant dependencies. 

12. So just a quick review. 

We can stop all of our containers using the below command:

`docker rm $(docker ps --filter status=exited -q)`

This prints the IDs all of containers that have exited, and removes them. 

We can list all ouf our containers using:

`docker ps -a`

We can list the currently running containers using:

`docker ps`

If we want to stop a running container, we use:

`docker stop <containerID>`

We can remove it then using:

`docker rm <containerID>`

Now let's run through some steps.

We run the below to run a postgres 13 container.

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

We can then run the following to run a pgadmin container.

```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```

13. We can now create an image using:

`docker build -t taxi_ingest:v001 .`

This build an image from our Dockerfile. We put a `.` at the end to specify the current working directory (where our Dockerfile is located). The `-t` specified we want to add a tag to the name of our image, in this caes, `001`. 

Once we build this, we then have a blueprint for our containers.

14. We can now run the following:

```
docker run -it  \
    --network=pg-network \
    taxi_ingest:v001 \
      --user=root \
      --password=root \
      --host=pg-database-2 \
      --port=5432 \
      --db=ny_taxi \
      --table_name=yellow_taxi_data \
      --url="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"
```

Here we are running our image to create a container.

We specify `pg-network` to ensure this container will be part of this network. Remember we, specified this earlier when we created our postgres and pgadmin containers. 

We are also passing a number of parameters, such as `user`,  `password`, and the `url` from where data will be downloaded. The python `argparse` programme will read these into the `ingest-data` script.

Now, whenever we run this container, we will end up with a database populated with the CSV data - which we can then access via pgadmin.

15. But... that's all a bit inconvient isn't it. Let's look into simplifying the process. We'll use `docker-compose`. This comes as part of docker desktop, which we already have installed.

16. We'll first create a `YAML` file (YAML is a language typically used for configuration files). 

Here we specify most of same details we specified when we ran the `docker build` commands for pgadmin and postgres database, only in a slightly different format. We don't actually need to specify the network (this will be done automatically). We also use the service name to connect to postgres from pgadmin now, rather than using the name we specified in the `docker build` command.

This is a convient way to create multiple containers from multiple images.

To actually run this file, we use:

`docker-compose up`

To shut down containers, we use the following the working directory we started the previous command:

`docker-compose down`

We can also start the containers in detached mode (this frees up our console, but keeps the container running):

`docker-compose up -d`

### Google Cloud Platform (GCP) & Terraform

Terraform is a infastructure as code tool. It allows us to provision infrasture resources as code, and bypass the GUI of cloud vendors like AWS or GCP.

GCP is a suite of cloud computing services offered by Google. Cloud computing is the on-demand availability of computer system resources without direct active management by the user.

1. The first thing we want to do is setup a free [Google Cloud Platform](https://cloud.google.com) account. You should get around $300 for free when signing up. This is enough for our purposes.

2. Next create a new project. I've called mine `dtc-de`. Switch to the project.

3. Creat a service account. I've called mine `dtc-de-user`

A service account is an identity that a compute instance or application can user to run API requests on our behalf. In other words, it is a user account you create for a service. It allows services to interact with each other.

4. Create key stored in JSON for service account. This will be saved down to our computer. Take a note of where it's stored.

5. Next we want to install Google SDK. This is a CLI tool which we can use to interact with our cloud service. Instructions [here](https://cloud.google.com/sdk/docs/quickstart).

6. I had some issues with the above step. Essentially I ended up setting my global python to system (2.7) using pyenv `pyenv global system` after removing the files that had been placed in my home folder in the previous step. I then followed through the install steps again. In order to continuusly access SDK, I need to make sure I have python 2.7 set. It's not convient, and no doubt there's a better way of doing this. But it'll do for now.

7. Finally, we setup an environmental variable to point to our authentications keys (the json file).

On my mac, I just ran the below:

`echo "GOOGLE_APPLICATION_CREDENTIALS="/Users/aaronwright/google-auth-key/dtc-de-338914-4da1c4a7cb0c.j" >> .zprofile`

I verified the authentication with this:

`gcloud auth application-default login`

Now our local environment is authenticated to work with the cloud environment.

8. Next up, I installed terraform. I have `homebrew` on my mac, so I used the following to install it.

```
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```
9. The next step involves assigning roles to our service account.

I had issues here. It seemed that under the IAM tab in GCP, there was a deleted user, but no service account like in the video.

Wasn't able to determine exactly what caused it, and didn't have time to fully understand it, so have made a note to look into this later.

However for the time being, I deleted my entire project, and decided to create a new one with a better name. My new project is `My-DE-Project` with service account `My-DE-Project-User`. Things seems to be working now.

I assigned some roles to my service account from the IAM tab - `Storage Admin` and `Storage Object Admin`. These are for managing buckets and objects within buckets. It's important to note that in a real production environment, we would typically assign customr roles, rather than choosing GCP's default ones.

We also added `Big Query Admin` as a role, as this is something we're going to want to interact with.

10. Let's now enable APIs. 

So when we are interacting with the cloud from our local environment, we don't interact with the resources. Instead, the APIs are the enablers of commmunication. 

We enabled these 2 APIs:

https://console.cloud.google.com/apis/library/iam.googleapis.com

* Manages identity and access control for Google Cloud Platform resources, including the creation of service accounts, which you can use to authenticate to Google and make API calls.

https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com

* Service Account Credentials API allows developers to create short-lived, limited-privilege credentials for their service accounts on GCP.
