## COMMON ISSUES

This is just a repo for common issues encountered. Will try update it where I can.

## #1

```
Could not translate host name "pgdatabase" to address: Name or service not known.
```

At some point you'll run `docker-compose up` - which creates two containers, one for Postgres and the other for PGAdmin. 

After this you'll create a new container called `ingest_taxi` or something similar using `docker run`. Most likely, you haven't updated the network name. 

When you run `docker-compose up`, if you don't specify a network name in the `YAML` file, Docker will create a default one. 

You'll be able to find this by running `docker network ls`. Replace `pg-network` in your docker run command with this new network. 

It's also probable that at this point you haven't updated the host name in your docker run command. This should be the name of the service you specified in the `YAML` file. This is likely `pgdatabase` rather than `pg-database`.

## #2





