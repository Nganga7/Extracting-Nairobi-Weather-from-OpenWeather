# Extracting Nairobi Weather from OpenWeather

This batch ETL is designed to extract real-time weather metrics from OpenWeather and load the data to a database. Database chosen here is a local Postgres instance

## Description

The ETL fetches data from the OpenWeather API and specifically Nairobi weather data at that particular time. It does this via the URL and using the api key provided. The raw data is saved as json before transformation.

Data fetched is rendered as a nested dictionary, hence we need to slice the data to get the required columns. Columns needed for our pipeline are: country, city, description, temperature, humidity & wind speed. Once sliced, we then need to convert the temperature readings from Kelvin to Celcius.

Following the transformations above, we then create a database called api_data on the database. Once created, we test the connection details. We then create a table on the public schema named, "src_open_weather".

The table src_open_weather should have columns that match the data transformed. Additionally, a column for load_date is added so as to know which day / time the data for Nairobi weather was collected.


## Getting Started

### Dependencies

* Libraries required:
    - pandas 
    - requests 
    - psycopg2
    - sql 
    - extras
    - os
    - dotenv

### Installing

* The ETL pipeline can be downloaded from the GitHub repository: https://github.com/Nganga7/LuxDev_Assignments/openweather/extract_openweather.ipynb
* Users can then setup their own virtual environment using uv and use ```uv sync``` to install the required dependencies
* Users can modify the database connection details to their own database connection

### Executing program

* Since the program is saved as a ipynb file, you can run it with any IDE of your choice
