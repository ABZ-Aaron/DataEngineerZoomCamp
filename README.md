# DataEngineerZoomCamp

I'm partaking in a Data Engineering Bootcamp / Zoomcamp. I'll store files and progress here.

1. We start by creating a Dockerfile which is used to build our Docker image.

2. Next up, we created a `pipeline.py` file which will be run when we start our image.

3. We then configue postgres, setting various parameters and environment variables. See the `postgres_config.yaml` file for what was copied into the command line (on a Mac).

4. I then setup a python virtual environment and pip installed `pgcli` in my main directory. This is a command line interface for Postgres.

5. Next up, we ran a `postgres` image with the below. The `-v` parameter is to specify an external volume. Basically, postgres would by default create a database on a folder inside the container, which will disappear when we kill it. This is good, because it allows us to generate as many containers as needed (all of them identical). However, in our case, we mounted a volume. In other words, the internal folder in the container is replicated to the external, local folder we specified. This allows the container to access that info when recreated again. This is how we handle persistent data with stateless containers. We also need to map a posgres port on our host machine to one in our container using the `-p` parameter.

```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5431:5432 \
  postgres:13
  ```

  I had some issues with this. What I ended up doing was deleting the `ny_taxi_postgres_data` folder from my current working directory. I then recreated this and adjusted permissions using:

  `sudo chmod a+rwx ny_taxi_postgres_data`
  
  I believe this adds read, write and execute permissions to the folder.

  I then made sure to specify port `-p 5431:5432` and ran the image.

  6. Next up, I connected to my database using:

  `pgcli -h localhost -p 5431 -u root -d ny_taxi`

  7. All seems to be working find. Time to write a script which will populate our currently empty database. Next up I create a Jupyter Notebook file, which I'll write via VS Code.

  8. We also need to download the data we're going to be working with (in CSV format). For this, it is the 2021 Yellow Taxi Trip Records located [here](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page). We can copy the link to this and run the following to download it to our current working directory. The `wget` command is a network donwloader.

  `wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv`

  9. In this step, we wrote our `upload-data` jupyter notebook script. This essentially connected to our database, read from the CSV file (chunk by chunk) into a pandas dataframe, created a table within our database, and added our CSV data to the database in chunks.

  10. Here I'm going to utilse `pgadmin`. This is a way for us to interact with our database in a more user friendly, web based graphical interface. I actually have pgadmin installed. But we can also run a docker image of this. To do this, we need postgres and pgadmin in the same network - and give both of them a name in that network.

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

Here is how we set up pgadmin. Notice how they both have the same network name:

```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
  ```

 11. Once we run both of these in seperate terminals, we have created two containers. To access pgadmin, we can got to `localhost:8080` in our browser, and use the pgadmin details to login. We should also make sure to specify `pg-database-2` as the host name we want to connect to.

 12.  



