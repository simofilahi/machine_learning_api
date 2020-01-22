import sqlite3 
import pandas as pd

def Connect(DBName):
    try:
        Conn = sqlite3.connect(DBName)
    except sqlite3.Error as error:
        return error
    return Conn

def LoadData(Conn, Query):
    try:
        Df = pd.read_sql_query(Query, Conn)
    except sqlite3.Error as error:
        return error
    return Df

def closeConnection(Conn):
    Conn.close()

def DBconnect():
    #name of database
    DBName = "db\latest.db"
    # Connect to Database
    Conn = Connect(DBName)
    # Query 
    Query = "select * from housing;"
    # Load Data from Database
    Df = LoadData(Conn, Query)
    # close Database Connection
    return Conn, Df