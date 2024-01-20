# Commands used during the workshop

## Module 1 
### : Docker, postgres

 - Docker command to spin up a postgres container
```bash
docker run -it \
  --name ny_taxi_postgres_container \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres:13
```


 - Changing permissions of the mounted volume
```bash
sudo chmod a+rwx ny_taxi_postgres_data
```

 - Install `pgcli` to connect to the postgres container
```bash
pip install pgcli
```

 - Connect to the postgres container
```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
 - Get the raw data from the course link and put it in the `data` folder
```bash
mkdir data
cd data
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
```

 - Check the first few rows of the data. Run `gzip -dc` to decompress the file first. 
```bash
gzip -dc yellow_tripdata_2021-01.csv.gz | head -n 10 
```

 - Create a table in postgres
```sql

### Connecting to the Postgres database using pgAdmin

Lets looks at some of the data elements in the table

```sql
SELECT * FROM yellow_tripdata_2021_01 LIMIT 10;
```

Lets see the earliest and latest pickup times for the uploaded data

```sql
SELECT 
  min(tpep_pickup_datetime) as earliest_pickup_time, 
  max(tpep_pickup_datetime) as latest_pickup_time
FROM yellow_taxi_data;
```

```
| earliest_pickup_time | latest_pickup_time  |
|----------------------|---------------------|
| 2008-12-31 23:05:14  | 2021-02-22 16:52:16 |
```

Looks like we have data from last day of 2008 to 2021. Whats the maximum fare amount given? (Ans: 7661.28)

```sql
SELECT max(total_amount) as max_fare_amount FROM yellow_taxi_data;
```
Since, it might become inconvenient to query the database using `pgcli` every time. Lets obtain a GUI based tool called pgAdmin to connect to the database. Let's find a docker image that comes with this pre-installed. This will also show us how to have docker images with difference applcations interact with each other. We can get this from Docker Hub(the download website for pgAdmin will point here)

Link to the docker image: https://hub.docker.com/r/dpage/pgadmin4

Lets construct the `docker run` command to spin up the pgAdmin container. What we did with the port forwarding parameter is that we are mapping the port 8080 of the container to the port 8080 of the host machine.
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="root@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root"  \
  -p 8080:8080 \
dpage/pgadmin4
```
