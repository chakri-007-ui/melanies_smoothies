# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
 
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
  """Choose the fruits you want to in your Smoothie! 
  """
)
# option = st.selectbox(
# 'What is your favorite fruit?',
# ('Banana','Strawberries','peaches') )
 
# st.write('You favorite fruit is:', option)
 
 
name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name on your smoothie will be:',name_on_order)
 
cnx = st.Connection("Snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect( 'Choose up to 5 ingredients:',my_dataframe,
                                 max_selections = 5)
if ingredients_list:
   ingredients_string = ''
 
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_chosen + ''
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
        sf_df= st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
 
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
 
    if  time_to_insert :
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered',icon= "✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
