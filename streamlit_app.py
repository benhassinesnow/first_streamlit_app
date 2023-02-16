import streamlit
import pandas as pd
import requests as rq
import snowflake.connector
from urllib.error import URLError

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

def get_fruitvice_data(fruit_choice):
      fruityvice_response =rq.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
      # normalize the json version  
      fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
      return(fruityvice_normalized)
   
try:
#let the user choose the fruit to get advice
   fruit_choice = streamlit.text_input('what fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
      fruityvice_normalized=get_fruitvice_data(fruit_choice)
      streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()

#streamlit.stop()


streamlit.header("the fruit load list contains:")
#connect to snowflake
def get_fruit_load_list():
      with  my_cnx.cursor() as y_cur:
            my_cur.execute("SELECT * from fruit_load_list")
            return(my_cur.fetchall())

#add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows= get_fruit_load_list()
      streamlit.text(my_data_row)
      
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)


#get some data
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
#my_data_row = my_cur.fetchall()



#streamlit.dataframe(my_data_row)


#allow the user to a fruit to the list
fruit_add=streamlit.text_input('what fruit would you like to add?', 'jackfruit')
streamlit.write('Thank you for adding', fruit_add)


#add that fruit to the databsae
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
