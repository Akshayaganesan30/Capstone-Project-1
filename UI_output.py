#Import required modules
import streamlit as st
from streamlit_option_menu import option_menu
import query_sql

#Set the page layour as wide
st.set_page_config(layout="wide")

#To Set the background image of the UI
page_bg_img = '''
    <style>
    .stApp {
    background-image: url("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdG4ybzF4aTRoZnM2aXJ1cnRjYWgwMmswb21oamIzYW96dHlsZWJhbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/W5g5W5hMkzrJQDpN3P/giphy.gif");
    background-size: cover;
    }
    </style>
    '''
st.markdown(page_bg_img, unsafe_allow_html=True)

#To display the title of the project
st.title(":blue[NASA NEAR EARTH OBJECT(NEO) TRACKING]")

#To create a sidebar menu with options Filter Criteria and Queries
with st.sidebar:
    selected = option_menu("Asteroid Approaches", ["Filter Criteria", 'Queries'], 
        icons=['filter', 'question'], menu_icon="cast", default_index=1)
    
#If Filter is selected display the output based on the input paramters selected
if selected == "Filter Criteria":
    with st.container(border=True,height = 750):
        c1, c2, c3 = st.columns(3,gap = 'large')
        with c1:
            mag = st.slider("Min Magnitude", 0, 100, (0,100))
            dia_min = st.slider("Estimated Diamter - Minimum (km)", 0, 10,(0,10))
            dia_max = st.slider("Estimated Diamter - Maximum (km)", 0, 20, (0,20))
        with c2:
            rel_velo = st.slider("Relative Velocity", 0, 200000, (0,200000))
            au = st.slider("Astronomical Unit", 0.0, 1.0, (0.0,1.0))
            options = st.selectbox("Is Potentially Hazardous?",
                                       ["True", "False"],
                                   index=None,
                                  placeholder="Select option")
        with c3:
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
        if st.button("Apply"):
            st.table(query_sql.filter(mag,dia_min,dia_max,rel_velo,au,options,start_date,end_date))
            

#If queries is selected display the queries and its answers based on the selected queries
qry = ["1.How many times each asteroid has approached Earth", 
       "2.Average velocity of each asteroid over multiple approaches",
       "3.List top 10 fastest asteroids",
       "4.Find potentially hazardous asteroids that have approached Earth more than 3 times",
       "5.Find the month with the most asteroid approaches",
       "6.Get the asteroid with the fastest ever approach speed",
       "7.Sort asteroids by maximum estimated diameter (descending)",
       "8.An asteroid whose closest approach is getting nearer over time",
       "9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
       "10.List names of asteroids that approached Earth with velocity > 50,000 km/h",
       "11.Count how many approaches happened per month",
       "12.Find asteroid with the highest brightness (lowest magnitude value)",
       "13.Get number of hazardous vs non-hazardous asteroids",
       "14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance",
       "15.Find asteroids that came within 0.05 AU(astronomical distance)",
       "16.Find the hazardous asteroid which has the maximum diameter",
      "17.On which month there are more hazardous asteroids approach",
      "18.Find the non - hazardous asteroid which has the maximum diameter",
      "19.Find the average velocity of hazardous asteroids",
      "20.Get number of hazardous vs non-hazardous asteroids for each month"]

if selected == "Queries":
    #with col2:
    with st.container(border=True,height = 450):
        option = st.selectbox("Queries about asteroids",
                            (qry
                            ),
                            index=None,
                            placeholder="Select your Query"
                        )
        if option == qry[0]:
                st.table(query_sql.qn1())
        if option == qry[1]:
                st.table(query_sql.qn2())
        if option == qry[2]:
                st.table(query_sql.qn3())
        if option == qry[3]:
                st.table(query_sql.qn4())
        if option == qry[4]:
                st.table(query_sql.qn5())
        if option == qry[5]:
                st.table(query_sql.qn6())
        if option == qry[6]:
                st.table(query_sql.qn7())
        if option == qry[7]:
                st.table(query_sql.qn8())
        if option == qry[8]:
                st.table(query_sql.qn9())
        if option == qry[9]:
                st.table(query_sql.qn10())
        if option == qry[10]:
                st.table(query_sql.qn11())
        if option == qry[11]:
                st.table(query_sql.qn12())
        if option == qry[12]:
                st.table(query_sql.qn13())
        if option == qry[13]:
                st.table(query_sql.qn14())
        if option == qry[14]:
                st.table(query_sql.qn15())
        if option == qry[15]:
                st.table(query_sql.qn16())
        if option == qry[16]:
                st.table(query_sql.qn17())
        if option == qry[17]:
                st.table(query_sql.qn18())
        if option == qry[18]:
                st.table(query_sql.qn19())
        if option == qry[19]:
                st.table(query_sql.qn20())
               
            
                