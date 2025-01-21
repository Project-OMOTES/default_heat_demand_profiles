from collections import OrderedDict
import csv
import datetime

influx_measurement_name = 'Space\\ Heat\\ default\\ profiles'
time_column_name = 'time'
files_with_measurement_name = {'SpaceHeat&HotWater_PowerProfile_1700_1950.csv': 'SpaceHeat_and_HotWater',
         'SpaceHeat&HotWater_PowerProfile_1900_2000.csv': 'SpaceHeat_and_HotWater',
         'SpaceHeat&HotWater_PowerProfile_2000_2010.csv': 'SpaceHeat_and_HotWater',
         'SpaceHeat_PowerProfile_1700_1950.csv': 'SpaceHeat',
         'SpaceHeat_PowerProfile_1900_2000.csv': 'SpaceHeat',
         'SpaceHeat_PowerProfile_2000_2010.csv': 'SpaceHeat'}

dataframe = OrderedDict()

for file_name, measurement_name in files_with_measurement_name.items():
    field_key = file_name.rstrip('.csv')

    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            time = datetime.datetime.fromisoformat(row[time_column_name])
            dataframe.setdefault(time, OrderedDict())[field_key] = row[measurement_name]


with open('../influxdb/energy_profiles.space_heat_default_profiles.influx_line', 'w+') as influx_line_file:
    influx_line_file.write('''# DDL
CREATE DATABASE energy_profiles

# DML
# CONTEXT-DATABASE: energy_profiles
''')

    for time, fields_with_values in dataframe.items():
        fields = []
        for field_name, measurement in fields_with_values.items():
            fields.append(f'{field_name}={measurement}')

        influx_line_file.write(f'{influx_measurement_name} {",".join(fields)} {int(time.timestamp()) * 1_000_000_000}\n')
