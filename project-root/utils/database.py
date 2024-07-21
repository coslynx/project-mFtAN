import os
import mysql.connector
import psycopg2
import pymongo
from utils.config import Config

class Database:
    """
    Handles database connections and interactions.
    """

    def __init__(self):
        self.config = Config()
        self.connection = None
        self.cursor = None
        self.database_type = self.config.get_value("DATABASE_TYPE")

        # Get database credentials from the .env file
        self.host = self.config.get_value("DATABASE_HOST")
        self.user = self.config.get_value("DATABASE_USER")
        self.password = self.config.get_value("DATABASE_PASSWORD")
        self.database = self.config.get_value("DATABASE_NAME")

    def connect(self):
        """
        Establishes a connection to the database.
        """
        try:
            if self.database_type == "mysql":
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            elif self.database_type == "postgresql":
                self.connection = psycopg2.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            elif self.database_type == "mongodb":
                self.connection = pymongo.MongoClient(
                    f"mongodb://{self.user}:{self.password}@{self.host}/{self.database}"
                )
            else:
                raise ValueError(f"Unsupported database type: {self.database_type}")

            self.cursor = self.connection.cursor()
            print(f"Connected to {self.database_type} database: {self.database}")

        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.disconnect()

    def disconnect(self):
        """
        Closes the database connection.
        """
        try:
            if self.connection:
                self.cursor.close()
                self.connection.close()
                print(f"Disconnected from {self.database_type} database: {self.database}")
        except Exception as e:
            print(f"Error disconnecting from database: {e}")

    def create_table(self, table_name, columns):
        """
        Creates a new table in the database.

        Args:
            table_name: The name of the table to create.
            columns: A list of tuples, where each tuple represents a column:
                (column_name, data_type, other_constraints)
        """
        try:
            if self.database_type in ("mysql", "postgresql"):
                create_table_query = f"CREATE TABLE {table_name} ("
                for column_name, data_type, constraints in columns:
                    create_table_query += f"{column_name} {data_type} {constraints}, "
                create_table_query = create_table_query[:-2] + ")"  # Remove trailing comma and space
                self.cursor.execute(create_table_query)
                self.connection.commit()
                print(f"Table '{table_name}' created successfully.")

            elif self.database_type == "mongodb":
                # MongoDB doesn't have explicit table creation like SQL databases
                # You can create collections dynamically by inserting data
                print(f"Collection '{table_name}' will be created when data is inserted.")

            else:
                raise ValueError(f"Unsupported database type: {self.database_type}")

        except Exception as e:
            print(f"Error creating table '{table_name}': {e}")

    def insert_data(self, table_name, data):
        """
        Inserts data into a table.

        Args:
            table_name: The name of the table to insert data into.
            data: A list of tuples, where each tuple represents a row:
                (value1, value2, ...)
        """
        try:
            if self.database_type in ("mysql", "postgresql"):
                insert_query = f"INSERT INTO {table_name} VALUES ({','.join(['%s' for _ in data[0]])})"
                self.cursor.executemany(insert_query, data)
                self.connection.commit()
                print(f"Data inserted into table '{table_name}' successfully.")

            elif self.database_type == "mongodb":
                self.connection[self.database][table_name].insert_many(data)
                print(f"Data inserted into collection '{table_name}' successfully.")

            else:
                raise ValueError(f"Unsupported database type: {self.database_type}")

        except Exception as e:
            print(f"Error inserting data into table '{table_name}': {e}")

    def update_data(self, table_name, data, where_clause):
        """
        Updates data in a table.

        Args:
            table_name: The name of the table to update data in.
            data: A dictionary of key-value pairs representing the data to update.
            where_clause: The WHERE clause of the SQL UPDATE statement.
        """
        try:
            if self.database_type in ("mysql", "postgresql"):
                update_query = f"UPDATE {table_name} SET "
                for key, value in data.items():
                    update_query += f"{key} = %s, "
                update_query = update_query[:-2] + f" WHERE {where_clause}"
                self.cursor.execute(update_query, tuple(data.values()))
                self.connection.commit()
                print(f"Data updated in table '{table_name}' successfully.")

            elif self.database_type == "mongodb":
                # MongoDB update requires a filter and an update document
                self.connection[self.database][table_name].update_many(
                    {"filter": eval(where_clause)},
                    {"$set": data}
                )
                print(f"Data updated in collection '{table_name}' successfully.")

            else:
                raise ValueError(f"Unsupported database type: {self.database_type}")

        except Exception as e:
            print(f"Error updating data in table '{table_name}': {e}")

    def delete_data(self, table_name, where_clause):
        """
        Deletes data from a table.

        Args:
            table_name: The name of the table to delete data from.
            where_clause: The WHERE clause of the SQL DELETE statement.
        """
        try:
            if self.database_type in ("mysql", "postgresql"):
                delete_query = f"DELETE FROM {table_name} WHERE {where_clause}"
                self.cursor.execute(delete_query)
                self.connection.commit()
                print(f"Data deleted from table '{table_name}' successfully.")

            elif self.database_type == "mongodb":
                self.connection[self.database][table_name].delete_many(eval(where_clause))
                print(f"Data deleted from collection '{table_name}' successfully.")

            else:
                raise ValueError(f"Unsupported database type: {self.database_type}")

        except Exception as e:
            print(f"Error deleting data from table '{table_name}': {e}")

    def select_data(self, table_name, columns, where_clause=None):
        """
        Retrieves data from a table.

        Args:
            table_name: The name of the table to retrieve data from.
            columns: A list of column names to retrieve.
            where_clause: The WHERE clause of the SQL SELECT statement.
        """
        try:
            if self.database_type in ("mysql", "postgresql"):
                select_query = f"SELECT {','.join(columns)} FROM {table_name}"
                if where_clause:
                    select_query += f" WHERE {where_clause}"
                self.cursor.execute(select_query)
                data = self.cursor.fetchall()
                return data

            elif self.database_type == "mongodb":
                if where_clause:
                    data = self.connection[self.database][table_name].find(eval(where_clause), {"_id": 0})
                else:
                    data = self.connection[self.database][table_name].find({}, {"_id": 0})
                return list(data)

            else:
                raise ValueError(f"Unsupported database type: {self.database_type}")

        except Exception as e:
            print(f"Error selecting data from table '{table_name}': {e}")
            return None