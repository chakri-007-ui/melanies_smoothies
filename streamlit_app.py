import streamlit as st
from snowflake.snowpark.functions import col
st.title('My Parents New Healthy Diner')
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")
import streamlit as st

title = st.text_input("Movie title", "Life of Brian")
st.write("The current movie title is", title)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
 
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe
    ,max_selections=5
)
 
 
if ingredients_list:
    ingredients_string = ''
 
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '


submitted = st.button('Submit')
 
if submitted:
    st.success("Someone clicked the button.", icon="👉")

import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)
