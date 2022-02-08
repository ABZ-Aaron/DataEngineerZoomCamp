#!/usr/bin/env python
import pandas as pd
import os
from time import time
from sqlalchemy import create_engine

def ingest_callable(user, password, host, port, db, table_name, csv_file):
    print(user, password, host, port, db, table_name, csv_file)
    
    # Create connection to postgres. Here we specify type of database, then the user, the password, at local host, the port, and the database name
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    # This will be an iterator object
    taxi_iter = pd.read_csv(csv_file, iterator = True, chunksize = 100000)

    taxi = next(taxi_iter)

    # Convert our date columns to a date-time data type
    taxi.tpep_pickup_datetime = pd.to_datetime(taxi.tpep_pickup_datetime)
    taxi.tpep_dropoff_datetime = pd.to_datetime(taxi.tpep_dropoff_datetime)

    taxi.head(0).to_sql(name = table_name, con = engine, if_exists = 'replace')
    taxi.to_sql(name=table_name, con=engine, if_exists='append')
        
    count = 1
    for i in taxi_iter:
        i.tpep_pickup_datetime= pd.to_datetime(i.tpep_pickup_datetime)
        i.tpep_dropoff_datetime= pd.to_datetime(i.tpep_dropoff_datetime)
        i.to_sql(name = table_name, con = engine, if_exists = 'append')
        print(f"Completed Iteration {count} for {table_name}")
        count += 1
    print("Completed Ingestion")
        