import streamlit
import pandas as pd
import requests as rq

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
