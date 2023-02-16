import streamlit
import pandas as pd
import requests as rq
import snowflake.connector

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatemal')
streamlit.text('🥗 Kale,Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg') 
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#streamlit.dataframe(my_fruit_list)

#pick list with name of fruits 'Fruit'
my_fruit_list = my_fruit_list.set_index('Fruit')
#pick list to let the user pich the fruit they want
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#show only the fruit selected
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)


#new section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
#fruityvice_response =rq.get("https://fruityvice.com/api/fruit/"+ "kiwi")
#streamlit.text(fruityvice_response.json())


#let the user choose the fruit to get advice
fruit_choice = streamlit.text_input('what fruit would you like information about?', 'kiwi')
streamlit.write('the user entered',fruit_choice) 
fruityvice_response =rq.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
                                    
                                    
# normalize the json version  
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# ouput the result like a table
streamlit.dataframe(fruityvice_normalized)






#connect to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)


#get some data
my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_row = my_cur.fetchall()
streamlit.header("the fruit load list contains:")
streamlit.dataframe(my_data_row)


#allow the user to a fruit to the list
fruit_add=streamlit.text_input('what fruit would you like to add?', 'jackfruit')
streamlit.write('Thank you for adding', fruit_add)
