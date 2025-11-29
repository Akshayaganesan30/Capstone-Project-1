from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import *
import pandas as pd
from datetime import datetime

# Replace with your actual credentials
username = "root"
password = "Pgnkka#" ##Do not use @symbol in password. If used error 2003 : node name nor servname provided error will occur
host = "localhost"
port = 3306
database = "Nasa_neo"

#Create SQLALchemy engine
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")


def filter(a,b,c,d,e,f,g,h):
    ans=[]
    fq = f"""SELECT * FROM filter_table
            WHERE absolute_magnitude_h BETWEEN {a[0]} AND {a[1]}
            AND estimated_diameter_min_km BETWEEN {b[0]} AND {b[1]}
            AND estimated_diameter_max_km BETWEEN {c[0]} AND {c[1]}
            AND relative_velocity_kmph BETWEEN {d[0]} AND {d[1]}
            AND astronomical_AU BETWEEN {e[0]} AND {e[1]}
            AND is_potentially_hazardous_asteroid = {f}
            AND close_approach_date BETWEEN :start_date AND :end_date
            """
    with engine.connect() as conn:
        for row in conn.execute(text(fq),{"start_date":g,"end_date":h}):
            ans.append(row._mapping)
    return ans

# ## Question 1 : Count how many times each asteroid has approached Earth

def qn1():
    ans = []
    qt1 = """SELECT 
            COUNT(id),  id
            FROM filter_table 
            GROUP BY id
            ORDER BY COUNT(id)
            """
    with engine.connect() as conn:
        for row in conn.execute(text(qt1)):
            ans.append(row._mapping)
    return ans
            


# ## QUESTION 2 Average Velocity of each asteroid over multiple approaches

def qn2():
    ans=[]
    qt2 = """ SELECT id,AVG(relative_velocity_kmph) FROM filter_table
                GROUP BY id"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt2)):
            ans.append(row._mapping)
    return ans


# ## QUESTION 3 List top 10 fastest asteroids

# In[97]:


def qn3():
    ans=[]
    qt3 = """ SELECT id,AVG(relative_velocity_kmph) FROM filter_table
        GROUP BY id
        ORDER BY AVG(relative_velocity_kmph) LIMIT 10"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt3)):
            ans.append(row._mapping)
    return ans
    

# ## QUESTION 4 Find potentially hazardous asteroids that have approached Earth more than 3 times

def qn4():
    ans=[]
    qt4 = """ SELECT id,COUNT(id) FROM filter_table
            WHERE is_potentially_hazardous_asteroid = True
            GROUP BY id
            HAVING COUNT(id) > 3
            """
    with engine.connect() as conn:
        for row in conn.execute(text(qt4)):
            ans.append(row._mapping)
    return ans


# ## QUESTION 5 Find the month with the most asteroid approaches

def qn5():
    ans=[]
    qt5 = """SELECT  MONTH(close_approach_date) as month,
          COUNT(id)
          FROM filter_table
          GROUP BY MONTH(close_approach_date)
          ORDER BY COUNT(id) DESC LIMIT 1
        """
    with engine.connect() as conn:
        for row in conn.execute(text(qt5)):
            ans.append(row._mapping)
    return ans


# ## QUESTION 6 asteroid with the fastest ever approach speed

def qn6():
    ans=[]
    qt6 ="""SELECT id FROM filter_table
        ORDER BY relative_velocity_kmph DESC LIMIT 1"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt6)):
            ans.append(row._mapping)
    return ans


# ## QUESTION 7 Sort asteroids by maximum estimated diameter (descending)

def qn7():
    ans=[]
    qt7 ="""SELECT id FROM filter_table
        ORDER BY estimated_diameter_max_km DESC"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt7)):
            ans.append(row._mapping)
    return ans


# ## QUESTION 8 An asteroid whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance).

def qn8():
    ans=[]
    qt8 ="""SELECT id,close_approach_date,miss_distance_km FROM filter_table
            ORDER BY close_approach_date DESC,miss_distance_km LIMIT 1"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt8)):
            ans.append(row._mapping)
    return ans

# ## QUESTION 9 Display the name of each asteroid along with the date and miss distance of its closest approach to Earth.

# In[374]:
def qn9():
    ans=[]
    qt9 = """SELECT id,close_approach_date,miss_distance_km FROM filter_table"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt9)):
            ans.append(row._mapping)
    return ans


# ## QUESTION 10 List names of asteroids that approached Earth with velocity > 50,000 km/h

def qn10():
    ans=[]
    qt10 ="""SELECT id FROM filter_table
        WHERE relative_velocity_kmph > 50000"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt10)):
            ans.append(row._mapping)
    return ans


# ## QUESTION 11 Count how many approaches happened per month

def qn11():
    ans=[]
    qt11 = """SELECT  MONTH(close_approach_date) as month,
          COUNT(id)
          FROM filter_table
          GROUP BY MONTH(close_approach_date)
        """
    with engine.connect() as conn:
        for row in conn.execute(text(qt11)):
            ans.append(row._mapping)
    return ans


# ## QUESTION 12 Find asteroid with the highest brightness (lowest magnitude value)

# In[386]:

def qn12():
    ans=[]
    qt12 = """SELECT id FROM filter_table
        ORDER BY absolute_magnitude_h ASC LIMIT 1"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt12)):
            ans.append(row._mapping)
    return ans


# ## QUESTION 13 Get number of hazardous vs non-hazardous asteroids

def qn13():
    ans=[]
    qt13 ="""SELECT is_potentially_hazardous_asteroid,count(is_potentially_hazardous_asteroid)
         FROM filter_table
         GROUP BY is_potentially_hazardous_asteroid"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt13)):
            ans.append(row._mapping)
    return ans


# ## QUESTION 14 Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance

# In[428]:

def qn14():
    ans=[]
    qt14 ="""SELECT id,close_approach_date,miss_distance_lunar
         FROM filter_table
         WHERE miss_distance_lunar < 1"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt14)):
            ans.append(row._mapping)
    return ans


# ## QUESTION 15 Find asteroids that came within 0.05 AU(astronomical distance)

# In[426]:

def qn15():
    ans=[]
    qt15 ="""SELECT id
         FROM filter_table
         WHERE astronomical_AU < 0.05"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt15)):
            ans.append(row._mapping)
    return ans

## QUESTION 16 Find the hazardous asteroid which has the maximum diameter

def qn16():
    ans=[]
    qt16 ="""SELECT estimated_diameter_max_km,id,is_potentially_hazardous_asteroid
            FROM filter_table
            WHERE is_potentially_hazardous_asteroid = True
            ORDER BY estimated_diameter_max_km DESC LIMIT 1
            """
    with engine.connect() as conn:
        for row in conn.execute(text(qt16)):
            ans.append(row._mapping)
    return ans

## QUESTION 17 On which month there are more hazardous asteroids approach

def qn17():
    ans=[]
    qt17="""SELECT MONTH(close_approach_date) as month,
            COUNT(id)
            FROM filter_table
            WHERE is_potentially_hazardous_asteroid = True
            GROUP BY MONTH(close_approach_date)
            ORDER BY COUNT(id) DESC LIMIT 1
          """
    with engine.connect() as conn:
        for row in conn.execute(text(qt17)):
            ans.append(row._mapping)
    return ans

## QUESTION 18 Find the non - hazardous asteroid which has the maximum diameter

def qn18():
    ans=[]
    qt18 ="""SELECT estimated_diameter_max_km,id,is_potentially_hazardous_asteroid
            FROM filter_table
            WHERE is_potentially_hazardous_asteroid = False
            ORDER BY estimated_diameter_max_km DESC LIMIT 1
            """
    with engine.connect() as conn:
        for row in conn.execute(text(qt18)):
            ans.append(row._mapping)
    return ans

##QUESTION 19 Find the average velocity of hazardous asteroids

def qn19():
    ans=[]
    qt19="""SELECT AVG(relative_velocity_kmph)
            FROM filter_table
            WHERE is_potentially_hazardous_asteroid = True
            """
    with engine.connect() as conn:
        for row in conn.execute(text(qt19)):
            ans.append(row._mapping)
    return ans

##QUESTION 20 Get number of hazardous vs non-hazardous asteroids for each month

def qn20():
    ans=[]
    qt20="""SELECT  MONTH(close_approach_date) as month,
          COUNT(id),is_potentially_hazardous_asteroid
          FROM filter_table
          GROUP BY is_potentially_hazardous_asteroid,MONTH(close_approach_date)"""
    with engine.connect() as conn:
        for row in conn.execute(text(qt20)):
            ans.append(row._mapping)
    return ans