

# Tested against queries

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
```