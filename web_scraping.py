import requests
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Database connection parameters
host = 'localhost'
user = 'ganesh'
password = 'test@123'
database = 'data_storage'

# Define the API URL
url = 'https://pokeapi.co/api/v2/pokemon?limit=20'

# Function to fetch data from API
def fetch_data_from_api(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

# Function to store data into MySQL database
def store_data_into_mysql(data, table_name):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # Create table if it does not exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            url VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        
        # Insert data into table
        insert_query = f"INSERT INTO {table_name} (name, url) VALUES (%s, %s)"
        for item in data['results']:
            cursor.execute(insert_query, (item['name'], item['url']))
        
        # Commit the transaction
        connection.commit()
        print(f"Data has been successfully stored into the '{table_name}' table.")
    except Error as e:
        print(f"An error occurred: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to display data from MySQL database
def display_data_from_mysql(table_name):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # Create a SQL query
        query = f"SELECT * FROM {table_name}"
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all results
        results = cursor.fetchall()
        
        # Create a DataFrame from the results
        df = pd.DataFrame(results, columns=['id', 'name', 'url'])
        
        # Display the data
        print(f"Contents of the '{table_name}' table:")
        print(df)
    except Error as e:
        print(f"An error occurred: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Main script execution
if __name__ == "__main__":
    # Fetch data from API
    api_data = fetch_data_from_api(url)
    
    # Store data into MySQL database
    store_data_into_mysql(api_data, 'api_data')
    
    # Display data from MySQL database
    display_data_from_mysql('api_data')
