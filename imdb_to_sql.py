import mysql.connector
from mysql.connector import Error
import numpy as np
import pandas as pd

imdb_top250_TVshow = pd.read_csv('D:/imdb_top250_TVshow.csv')
imdb_top250_TVshow.fillna('N/A', inplace=True)


# create connection
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

# PASSWORD
pw = '?????'
connection = create_server_connection("localhost", "root", pw)

# create database
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

create_database_query = 'CREATE DATABASE imdb_TVshow'
create_database(connection, create_database_query)


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

        
# connect to imdb_TVshow database
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


create_imdb_table = """
CREATE TABLE imdb_TVshow (
  movie_id INT PRIMARY KEY,
  title VARCHAR(128) NOT NULL,
  link VARCHAR(128) NOT NULL,
  genre VARCHAR(128) NOT NULL,
  creator VARCHAR(128) NOT NULL,
  star VARCHAR(128) NOT NULL,
  rating float(2,1) NOT NULL
  );
 """

db = 'imdb_TVshow'

connection = create_db_connection("localhost", "root", pw, db) # Connect to the Database
execute_query(connection, create_imdb_table) # Execute our defined query


# insert data into imdb_tvshow

for idx, line in imdb_top250_TVshow.iterrows():

    insert_imdb_table=f"""
    INSERT INTO imdb_tvshow VALUES
    (
    "{line['movie_id']}",
    "{line['Title']}",
    "{line['link']}",
    "{line['Genre']}",
    "{line['Creators']}",
    "{line['Stars']}",
    {line['Rating']}
    );
    """
    execute_query(connection, insert_imdb_table) # Execute our defined query
