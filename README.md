# Public influx database for Nieuwe Warmte Nu - Design Toolkit
This repository holds the codified infrastructure to deploy a public influx v1.7 database
which holds the default heat demand profiles.

The database has been configured with authentication
and a single user 'public' is configured with READ privileges. A reverse proxy is added for https
support as well as adding the credentials of 'public' to any requests to /query so any query
received is performed as if the credentials for 'public' were also configured. In other words,
requests from users do not have to contain credentials.

All other influxdb endpoints such as /ping, /debug and /write are blocked by the reverse proxy.
All authentication methods such as providing basic authorization headers or providing a username
and password through query parameters are blocked.

The goal of this database is to be a read-only database.

## Setup and running
Setup may be performed by creating a `.env` and filling the necessary parameters:

```bash
cp .env-template .env
# Change the values in .env
```

The database is configured upon initialization and all data is loaded as well. To run this system
all that is needed:

```bash
docker compose up -d
```

The system may be stopped:

```bash
docker compose stop
```

Or completely cleaned up:

```bash
docker compose down -v
```

## Tested against queries
This should suggest as it reads only data:
```bash
./influx -host profiles.here.com -port 80 -database energy_profiles -execute 'SELECT * FROM "WarmingUp default profiles"'
```

These should not work as they create changes in the database:
```bash
./influx -host profiles.here.com -port 80 -database energy_profiles -execute 'CREATE DATABASE hello'
./influx -host profiles.here.com -port 80 -database energy_profiles -execute 'INSERT WarmingUp\ default\ profiles field1=hello 10'
./influx -host profiles.here.com -port 80 -database energy_profiles -execute "CREATE USER \"fred\" WITH PASSWORD '123'"
./influx -host profiles.here.com -port 80  -import -path "./influxdb/energy_profiles.warmingup_default_profiles.influx_line"

curl -v -XPOST 'http://profiles.here.com:80/query?u=admin&p=1234' --data-urlencode 'q=CREATE DATABASE "mydb"' # Create database through curl and query parameter authentication
curl -v -XPOST 'http://profiles.here.com:80/query?u=admin' --data-urlencode 'q=CREATE DATABASE "mydb"'        # Even if just the username or password is added.
```