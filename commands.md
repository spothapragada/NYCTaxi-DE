# Commands used during the workshop

## Module 1 
### : Docker, postgres

 - Docker command to spin up a postgres container
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "$(pwd)"/ny_taxi_postgres_data:/var/lib/postgresql/data \
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
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root"  \
  -p 8080:80 \
dpage/pgadmin4
```

Now locally we can navigate to [http://localhost:8080](http://localhost:8080) and login with the credentials we provided. We can now add a new server and connect to the postgres container. You will notice that entering the connection details of the postgres instance we just created will not be accepted into pgAdmin. This is because `pgAdmin` and `postgres` are running in different containers and they are not able to communicate with each other. We need to create a network and attach both the containers to the network. 

We can do this by running the command below. This will create a network called `my_network` and attach both the containers to it. 

First stop both containers. the lets create the network, naming it `pg-network`.

```bash
docker network create pg_network
```

Now we must restart the containers and attach them to the network. We can begin with the postgres container, with some additional parameters. This will be the name of the network we just created (`pg_network`) and a name for the postgres container so it may be easily identified by the pgAdmin container (lets call it `pg-database`).

```bash
docker run -it \ 
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "$(pwd)"/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg_network \
  --name pg-database \
-d postgres:13
```

Now lets create the pgAdmin container and specify the network and the name of the postgres container. 

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root"  \
  -p 8080:80 \
  --network=pg_network \
  --name pg-admin \
dpage/pgadmin4
```

When in pgAdmin, create a new server (call it 'Postgres DB Docker Localhost' or something to indicate it points to the postgres Docker container) and enter the following  on the _"Connection"_ tab:

```
Host: pg-database
Port: 5432
Username: root
Password: root
```

The schemas and the tables will then populate the GUI and you will be able to query the database among other functionality.

