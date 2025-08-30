import mysql.connector
from mysql.connector import Error
from typing import Optional

class DatabaseManager:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._connection:
            try:
                self._connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Root@123",
                    database="serenity_hospital_db"
                )
                print("Database connection successful")
            except Error as e:
                print(f"Error connecting to database: {e}")

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = DatabaseManager()
        return cls._instance

    def get_connection(self):
        if not self._connection or not self._connection.is_connected():
            self.__init__()
        return self._connection

    def execute_query(self, query: str, params: tuple = None) -> Optional[list]:
        if not self._connection or not self._connection.is_connected():
            self.__init__()
            if not self._connection:
                raise Error("Could not establish database connection")
                
        cursor = None
        try:
            cursor = self._connection.cursor(dictionary=True)
            
            # Execute the query
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Handle SELECT queries
            if query.lower().strip().startswith('select'):
                result = cursor.fetchall()
                cursor.close()
                return result
            
            # Handle INSERT/UPDATE/DELETE queries
            self._connection.commit()
            affected = cursor.rowcount
            cursor.close()
            return [{"affected_rows": affected}]
            
        except Error as e:
            if cursor:
                cursor.close()
            raise e
        except Exception as e:
            if cursor:
                cursor.close()
            raise Error(f"Query execution failed: {str(e)}")
                
        except Error as e:
            print(f"Error executing query: {e}")
            if cursor:
                cursor.close()
            return None

    def close_connection(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Database connection closed")
