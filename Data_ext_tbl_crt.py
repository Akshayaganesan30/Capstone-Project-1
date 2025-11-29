##Import Required modules
import requests
import pandas as pd
from datetime import datetime,date
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import *

API_KEY = "Zw4ofbFSdqbPj5w6tAgItFZdfowsVuml1XXzbJmJ"

#Define the column names
columns_names=['id','neo_reference_id','name',
               'absolute_magnitude_h','estimated_dia_min_km','estimated_dia_max_km',
              'is_potentially_hazardous_asteroid','close_approach_date','relative_velocity_kmph',
              'astronomical','miss_distance_km','miss_distance_lunar','orbiting_body']
default_values = []

#Create a Data frame for storing the records
#Create a temporary dictionary to extract the required data from response and assign it to a dataframe
data_dict = {'id': [],
 'neo_reference_id': [],
 'name': [],
 'absolute_magnitude_h': [],
 'estimated_dia_min_km': [],
 'estimated_dia_max_km': [],
 'is_potentially_hazardous_asteroid': [],
 'close_approach_date': [],
 'relative_velocity_kmph': [],
 'astronomical': [],
 'miss_distance_km': [],
 'miss_distance_lunar': [],
 'orbiting_body': []}
data_neo_df = pd.DataFrame(columns=columns_names)

#Send request and receive the data as response from the API page
url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key={API_KEY}"
response = requests.get(url)

#Convert the response to json format
data = response.json()

# Extract the required data and assign to a dictionary and pass this dictionary as a row to the dataframe
# Repeat the procedure upto 10000 records
i = 0
while i < 10000:
    for date in data['near_earth_objects']:
        for asteroid in data['near_earth_objects'][date]:
            data_dict['id'].append(int(asteroid['id']))
            data_dict['neo_reference_id'].append(int(asteroid['neo_reference_id']))
            data_dict['name'].append(asteroid['name'])
            data_dict['absolute_magnitude_h'].append(asteroid['absolute_magnitude_h'])
            data_dict['estimated_dia_min_km'].append(asteroid['estimated_diameter']['kilometers']['estimated_diameter_min'])
            data_dict['estimated_dia_max_km'].append(asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'])
            data_dict['is_potentially_hazardous_asteroid'].append(asteroid['is_potentially_hazardous_asteroid'])
            data_dict['close_approach_date'].append(pd.to_datetime(asteroid['close_approach_data'][0]['close_approach_date']))
            data_dict['relative_velocity_kmph'].append(float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']))
            data_dict['astronomical'].append(float(asteroid['close_approach_data'][0]['miss_distance']['astronomical']))
            data_dict['miss_distance_km'].append(float(asteroid['close_approach_data'][0]['miss_distance']['kilometers']))
            data_dict['miss_distance_lunar'].append(float(asteroid['close_approach_data'][0]['miss_distance']['lunar']))
            data_dict['orbiting_body'].append(asteroid['close_approach_data'][0]['orbiting_body'])
            i=i+1
            if i == 10000:
                break
        if i == 10000:
            break
    url = data['links']['next'] #Assign the url to get data for the next 7 days
    response = requests.get(url) #Send request
    data = response.json() #Convert the response to json format

#Assign the data as a data frame and check for NULL values and data types
df = pd.DataFrame(data_dict)
df.info()

# Replace with your actual credentials
username = "root"
password = "Pgnkka#" ##Do not use @symbol in password. If used error 2003 : node name nor servname provided error will occur
host = "localhost"
port = 3306
database = "Nasa_neo"

# ## To create a new database for storing the NASA NEO DATA
# ## Create SQLAlchemy engine
# engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}")
# create_db_query = """
#                     CREATE DATABASE Nasa_neo;
#                     """
# with engine.connect() as conn:
#     conn.execute(text(create_db_query))
#     conn.commit()

#Create SQLALchemy engine
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

## To create Table Asteroid and Close Approach
create_tb_ast = """
                   CREATE TABLE asteroid(
                   pk INT NOT NULL AUTO_INCREMENT,
                   id INT,
                   name NVARCHAR(255),
                   absolute_magnitude_h FLOAT,
                   estimated_diameter_min_km FLOAT,
                   estimated_diameter_max_km FLOAT,
                   is_potentially_hazardous_asteroid BOOLEAN,
                   PRIMARY KEY (pk)
                   );
                   """
create_tb_cls_app = """
                       CREATE TABLE close_approach(
                       pk INT NOT NULL AUTO_INCREMENT,
                       neo_reference_id INT,
                       close_approach_date DATETIME,
                       relative_velocity_kmph FLOAT,
                       astronomical_AU FLOAT,
                       miss_distance_km FLOAT,
                       miss_distance_lunar FLOAT,
                       orbiting_body NVARCHAR(255),
                       PRIMARY KEY (pk)
                       );
                       """
with engine.connect() as conn:
    conn.execute(text(create_tb_ast))
    conn.execute(text(create_tb_cls_app))
    conn.commit()

###INSERT THE COLLECTED DATA TO ASTEROID TABLE
j=0
col_ast = ['id','name','absolute_magnitude_h','estimated_dia_min_km','estimated_dia_max_km','is_potentially_hazardous_asteroid']
while j < 10000:
    tempd_1 = {key: value[j] for key, value in data_dict.items()}
    tempd_2={}
    for z in col_ast:
        tempd_2.update({z:tempd_1[z]})
    q1 = """
        INSERT INTO asteroid(id,name,absolute_magnitude_h,estimated_diameter_min_km,estimated_diameter_max_km,is_potentially_hazardous_asteroid)
        VALUES(:id,:name,:absolute_magnitude_h,:estimated_dia_min_km,:estimated_dia_max_km,:is_potentially_hazardous_asteroid);"""
    with engine.connect() as conn:
        conn.execute(text(q1),tempd_2)
        conn.commit()
    j=j+1

###INSERT THE COLLECTED DATA TO CLOSE APPROACH TABLE
j=0
col_cls = ['neo_reference_id','close_approach_date','relative_velocity_kmph','astronomical','miss_distance_km','miss_distance_lunar','orbiting_body']
while j < 10000:
    tempd_1 = {key: value[j] for key, value in data_dict.items()}
    tempd_2={}
    for z in col_cls:
        tempd_2.update({z:tempd_1[z]})
    q1 = """
        INSERT INTO close_approach(neo_reference_id,close_approach_date,relative_velocity_kmph,astronomical_AU,
                                    miss_distance_km,miss_distance_lunar,orbiting_body)
        VALUES(:neo_reference_id,:close_approach_date,:relative_velocity_kmph,:astronomical,:miss_distance_km,:miss_distance_lunar,:orbiting_body);"""
    with engine.connect() as conn:
        conn.execute(text(q1),tempd_2)
        conn.commit()
    j=j+1

#Create a new table with merged data
join_qry="""CREATE TABLE filter_table AS
            SELECT a.id,a.name,a.absolute_magnitude_h,
                    a.estimated_diameter_min_km,a.estimated_diameter_max_km,a.is_potentially_hazardous_asteroid ,
                    cl.close_approach_date,cl.relative_velocity_kmph,cl.astronomical_AU,
                    cl.miss_distance_km,cl.miss_distance_lunar,
                    cl.orbiting_body
            FROM asteroid as a
            INNER JOIN close_approach as cl
            ON a.pk = cl.pk
            """
with engine.connect() as conn:
    conn.execute(text(join_qry))
    conn.commit()

