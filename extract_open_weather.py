import os
import pandas as pd 
from dotenv import load_dotenv
import requests 
import psycopg2
from psycopg2 import sql 
from psycopg2 import extras

load_dotenv()

url = "http://api.openweathermap.org/data/2.5/weather"

api_key = os.getenv("OPEN_WEATHER_API_KEY")

params = {
    "q" : "Nairobi",
    "appid" : api_key
}

raw_data = requests.get(url,params=params)

raw_data.status_code

staging_data = raw_data.json() 

#staging_data

temp_kelvin = staging_data["main"]["temp"]
temp_min_kelvin = staging_data["main"]["temp_min"]
temp_max_kelvin = staging_data["main"]["temp_max"] 
humidity = staging_data["main"]["humidity"]
wind_speed = staging_data["wind"]["speed"]
description = staging_data["weather"][0]["description"]
country = staging_data["sys"]["country"] 
city = staging_data["name"]

#description

def kelvin_to_celcius(temp):
    return (temp - 273.15)

temp_celcuis = kelvin_to_celcius(temp_kelvin)

temp_min_celcius = kelvin_to_celcius(temp_min_kelvin)

temp_max_celcius = kelvin_to_celcius(temp_max_kelvin)



src_data = pd.DataFrame([{
    "country" : country,
    "city": city,
    "description": description,
    "temp_in_celcius": temp_celcuis,
    "temp_min_in_celcius": temp_min_celcius,
    "temp_max_in_celcius": temp_max_celcius,
    "humidity_perc": humidity,
    "wind_speed_in_m_per_s": wind_speed}])

#src_data

host_name = os.getenv("HOST_NAME")
db_name = os.getenv("DB_NAME")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
port = os.getenv("PORT")
target_table = os.getenv("TARGET_TABLE")

conn = psycopg2.connect(
    host = host_name,
    dbname = db_name,
    user = username,
    password = password,
    port = port
)

try:
    print(f"Successfully connected to database: {db_name} with user: {username}")

except psycopg2.Error as e:
    print(f"Check connection details. Error {e}")

cur = conn.cursor()

create_table = sql.SQL(""" 
    CREATE TABLE IF NOT EXISTS {table} (
    country VARCHAR(20),
    city VARCHAR(50),
    description VARCHAR(50),
    temp_in_celcius NUMERIC(5,2),
    temp_min_in_celcius NUMERIC(5,2),
    temp_max_in_celcius NUMERIC(5,2),
    humidity_perc INT,
    wind_speed_in_m_per_s NUMERIC(5,2),
    load_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
""").format(table = sql.Identifier(target_table))

try:
    cur.execute(create_table)
    conn.commit()
    print(f"Successfully created table: {target_table} or already exists ")

except psycopg2.Error as e:
    conn.rollback()
    print(f"Check syntax error {e}")


#src_data.columns.to_list()

src_data_columns = ['country','city','description','temp_in_celcius','temp_min_in_celcius','temp_max_in_celcius','humidity_perc','wind_speed_in_m_per_s']

values_to_load = [tuple(row) for row in src_data.values]

insert_data = sql.SQL("""
    INSERT INTO {table} ({columns})
    VALUES %s
""").format(table = sql.Identifier(target_table),
columns = sql.SQL(' ,').join(map(sql.Identifier, src_data_columns))
)

try:
    extras.execute_values(cur, insert_data,values_to_load)
    conn.commit()
    print(f"Successfully inserted {len(values_to_load)} rows into {target_table}")

except psycopg2.Error as e:
    conn.rollback()
    print(f"Check syntax error {e}")

