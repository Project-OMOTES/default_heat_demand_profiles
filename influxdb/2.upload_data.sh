#!/bin/bash

influx -username "${INFLUXDB_ADMIN_USER}" -password "${INFLUXDB_ADMIN_PASSWORD}" -import -path=/energy_profiles.warmingup_default_profiles.influx_line
