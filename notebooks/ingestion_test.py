#!/usr/bin/env python
# coding: utf-8

# Importing the libraries
import os
import subprocess
import pandas as pd
import time
import argparse

from tqdm import tqdm
from sqlalchemy import create_engine



def main(params):

  user = params.user
  password = params.password
  host = params.host
  port = params.port
  database = params.database
  table_name = params.table_name
  data_url = params.data_url
  data_fname  = "output.csv"

  # Lets obtain the data file from the path provided and name it output.csv
  os.system(f'wget {data_url} -O {data_fname}')

  # Get the number of lines in the data file
  command = ["wc", "-l", data_fname]
  result = subprocess.run(command, capture_output=True, text=True)

  # The stdout attribute contains the output
  output = result.stdout

  # The output will be a string like '100 filename', so we split it and take the first part
  num_lines = int(output.split()[0])


  engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

  # lets just add the header when creating the table
  #df.head(0).to_sql('yellow_taxi_data', engine, if_exists='replace')

  # Lets load the data into the database using the `to_sql` function using chunksize of 1000 rows.
  # Create a progress bar using tqdm

  df_iter = pd.read_csv(data_url, iterator=True, chunksize=100000)

  with tqdm(total=num_lines) as pbar:
    for chunk in df_iter:
        
        # Converting some of the columns to datetime
        chunk['tpep_dropoff_datetime'] = pd.to_datetime(chunk['tpep_dropoff_datetime'])
        chunk['tpep_pickup_datetime'] = pd.to_datetime(chunk['tpep_pickup_datetime'])

        # Loading the data into the database
        chunk.to_sql(name=f'{table_name}', con=engine, if_exists='append')

        # Sleep for 1 seconds, its just good practice to not overload the database
        # time.sleep(1)

        pbar.update(df_iter.chunksize)

if __name__ == '__main__':
  # Define parser object
  parser = argparse.ArgumentParser(description='Ingestion script for the yellow taxi data to load into Postgres')

  # Add the arguments
  # user
  # password, 
  # host,
  # port,
  # database name 
  # table_name 
  # data_path

  parser.add_argument('--user', type=str, help='Postgres username')
  parser.add_argument('--password', type=str, help='Postgres password')
  parser.add_argument('--host', type=str, help='Postgres host')
  parser.add_argument('--port', type=str, help='Postgres port')
  parser.add_argument('--database', type=str, help='Postgres database name')
  parser.add_argument('--table_name', type=str, help='Postgres table name')
  parser.add_argument('--data_url', type=str, help='URL to the data file')

  args = parser.parse_args()
  main(args)

  








