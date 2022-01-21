#!/usr/bin/env python
# coding: utf-8
import argparse

import os 

from re import U 

import pandas as pd

from sqlalchemy import create_engine

def main(params):
    
    user = params.user 
    password = params.password 
    host = params.host 
    port = params.port
    db = params.db
    table_name = params.table_name 
    url = params.url
    
    csv_name = 'output.csv'
    
    os.system(f"wget {url} -O {csv_name}")
    
    # Create connection to postgres. Here we specify type of database, then the user, the password, at local host, the port, and the database name
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # This will be an iterator object
    taxi_iter = pd.read_csv(csv_name, iterator = True, chunksize = 100000)

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
        print(f"Completed Iteration {count}")
        count += 1
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 'Ingest CSV data to Postgres')
    parser.add_argument('--user', help='Username for Postgres')
    parser.add_argument('--password', help='Password for Postgres')
    parser.add_argument('--host', help='Host for Postgres')
    parser.add_argument('--port', help='Port for Postgres')
    parser.add_argument('--db', help='Database for Postgres')
    parser.add_argument('--table_name', help='Table name for Postgres')
    parser.add_argument('--url', help='URL of CSV')
    args = parser.parse_args()
    
    main(args)