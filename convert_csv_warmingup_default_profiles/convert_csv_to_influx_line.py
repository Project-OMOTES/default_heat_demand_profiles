import csv

measurement_name = 'WarmingUp\\ default\\ profiles'
time_column_name = 'time'
field_keys = ['demand1_MW', 'demand2_MW', 'demand3_MW', 'demand4_MW', 'demand5_MW']

with open('energy_profiles.warmingup_default_profiles.csv') as csv_file:
    with open('../influxdb/energy_profiles.warmingup_default_profiles.influx_line', 'w+') as influx_line_file:
        influx_line_file.write('''# DDL
CREATE DATABASE energy_profiles

# DML
# CONTEXT-DATABASE: energy_profiles
''')

        csv_reader = csv.DictReader(csv_file)

        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Header is {", ".join(row)}')
                line_count += 1
            fields = []
            for field in field_keys:
                fields.append(f'{field}={row[field]}')

            influx_line_file.write(f'{measurement_name} {",".join(fields)} {row[time_column_name]}\n')
            line_count += 1
