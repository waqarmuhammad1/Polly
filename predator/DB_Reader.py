import pandas as pd
import mysql.connector as sql
from logger import Logger

class DBReader():

    logger = Logger()
    username = None
    password = None
    host = None
    port = None
    db_name = None
    table_name = None
    db_connection = None
    def __init__(self):
        pass

    def read_databases(self):
        self.db_connection = sql.connect(host=self.host, port=self.port, user=self.username, passwd=self.password)
        database_df = pd.read_sql('show databases', self.db_connection)
        databases = list(database_df['Database'])
        return databases

    def select_database(self):
        sql_select_Query = "use "+self.db_name
        cursor = self.db_connection.cursor()
        cursor.execute(sql_select_Query)

    def read_tables(self):
        tables_df = pd.read_sql('show tables', self.db_connection)
        tables = list(tables_df['Tables_in_' + self.db_name])
        return tables

    def read_table(self):
        data_df = pd.read_sql('SELECT * FROM ' + self.table_name, self.db_connection)
        return data_df
