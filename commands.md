# Commands used during the workshop

## Module 1 : Docker, postgres

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