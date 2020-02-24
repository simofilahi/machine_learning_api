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


def DBconnect(uuid, modelname, features, target):
    # path of database
    DBpath = "/datasets/{uuid}.db".format(uuid=uuid)
    # Connect to Database
    Conn = Connect(DBpath)
    # Query
    Query = "select {features} from data;".format(features=features)
    # Load Data from Database
    train_X = LoadData(Conn, Query)
    Query = "select {target} from data;".format(target=target)
    train_Y = LoadData(Conn, Query)
    # # close Database Connection
    # print("train_X ==> ", train_X)
    # print("train_Y ==> ", train_Y)
    return Conn, train_X
