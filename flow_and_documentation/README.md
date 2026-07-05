# Global Weather History Builder (API)


## Overview
A Dockerized Python ETL project that collects weather data from the free Open-Meteo API, transforms it into a cleaner format, and loads it into a local PostgreSQL climate database.

The project is designed for an instructor or reviewer to run with simple Docker commands. The ETL pipeline can run automatically every hour with cron, and it can also be executed manually for testing.


**Author:** George Kleftogiannis

## Project Goal
The goal of this project is to create a local climate database for a fixed list of cities.

The intended final pipeline should:

- collect current weather and air-quality data for 5 selected cities using latitude and longitude coordinates
- transform the raw API response into a clean tabular format
- map numeric WMO weather codes into readable descriptions, such as `71` to `Snow`
- store the results in a PostgreSQL table named `weather_readings`
- run automatically every 1 hour using cron

## Data Source

The data source is the free Open-Meteo API.

The current code uses the Open-Meteo forecast endpoint:

```text
https://api.open-meteo.com/v1/forecast
```

### Data Description
Current weather variables in the uploaded code include:

- temperature at 2 meters
- relative humidity at 2 meters
- rain
- showers
- snowfall
- precipitation
- WMO weather code
- mean sea level pressure

## Project Structure

```text
2nd-BBDA-project
├──/src
|  ├── extract.py
|  ├── transform.py
|  ├── load.py
|  ├── etl_pipeline.py
├──/docker
|  ├──Dockerfile
|  ├── docker-compose.yml
|  ├── crontab
├──/sql_scripts
|  |── analysis.sql
|  ├── init.sql
├── flow_and_documentation
|  ├── requirements.txt
|  ├── .gitignore
|  ├── README.md

```
