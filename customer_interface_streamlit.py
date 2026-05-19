# Import python packages
import streamlit as st
import os
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark import Session

connection_parameters = {
    "account": "JUUDHJU-NAB87893",
    "user": "JENILTHAKKAR208",
    "password": "Dataengineering@208",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC",
    "role": "SYSADMIN"
}

session = Session.builder.configs(connection_parameters).create()

# Write directly to the app
st.title(" \U0001F964 Customize Your Smoothie! \U0001F964 ")
st.write(
"Choose the fruits you want in your custom Smoothie!"
)

# option= st.selectbox("What is your favourite fruit?",("Banana","Strawberries","Peaches"))

# st.write("Your favourite fruit is: ",option)

name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your smoothie will be:', name_on_order)

# session = get_active_session()
# cnx=st.raw_connection("snowflake")
cnx = st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list= st.multiselect ('Choose up to 5 ingredients:', my_dataframe,max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string= ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    # st.write(ingredients_string)    
    
    # my_insert_stmt = """ insert into smoothies.public.orders
    #                 values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    # time_to_insert = st.button('Submit Order')
    
    my_insert_stmt = """ insert into smoothies.public.orders
                    (NAME_ON_ORDER,INGREDIENTS)
                    values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    time_to_insert = st.button('Submit Order')
    
    # st.write(my_insert_stmt)
    # st.stop(my_insert_stmt)
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered,  {name_on_order}!", icon="✅")

    
