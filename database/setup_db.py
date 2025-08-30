import mysql.connector
from mysql.connector import Error
import os

def setup_database():
    connection = None
    cursor = None
    
    try:
        # Read the schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as file:
            sql_commands = file.read().split(';')
        
        # Connect to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root@123"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            print("Connected to MySQL")
            
            # Execute each command
            for command in sql_commands:
                command = command.strip()
                if command:  # Skip empty commands
                    try:
                        cursor.execute(command)
                        print(f"Executed: {command[:50]}...")
                    except Error as e:
                        print(f"Error executing command: {e}")
            
            connection.commit()
            print("Database setup completed successfully")
            
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Connection closed")

if __name__ == "__main__":
    setup_database()
