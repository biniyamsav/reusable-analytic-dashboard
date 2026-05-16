import psycopg2
import pandas as pd 
import streamlit as st
import database as db
import plotly.express as px
conn=psycopg2.connect(
    host="localhost",
    database="sales_analytics",
    user="postgres",
    password=112123,  # <-- replaced private password
    port=5432
)
cursor=conn.cursor()
name="sales_transaction34"
cursor.execute(""" 
                  SELECT table_name 
                  FROM information_schema.tables 
                  WHERE table_schema = 'public';
                  """)
data = cursor.fetchall()
data = pd.DataFrame(data)
print(data[0][1])