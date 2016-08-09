# -*- coding: utf-8 -*-
"""
Created on Tue May 24 16:14:19 2016

@author: Raunak Mundada
"""
from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
from mysql.connector import Error
from collections import OrderedDict
import pandas as pd


DB_NAME = 'Olympics'

TABLES = OrderedDict()
def defineTables():
    TABLES['Olympic_Medals'] = (
    "CREATE TABLE `Olympic_Medals` ("
    "  `Id` char(20) NOT NULL,"
    "  `Country` varchar(255) NOT NULL,"
    "  `Country_Code` varchar(255) NOT NULL,"
    "  `Gold_Medals` int,"
    "  `Silver_Medals` int,"
    "  `Bronze_Medals` int,"
    "  `Total` int,"
    "  PRIMARY KEY (`Id`)"
    ") ENGINE=InnoDB")

    TABLES['Economic_Indicators'] = (
    "CREATE TABLE `Economic_Indicators` ("
    " `Id` char(255) NOT NULL,"
    "  `Country` varchar(255) NOT NULL,"
    "  `Gold_Medals` int,"
    "  `Silver_Medals` int,"
    "  `Bronze_Medals` int,"
    "  `Total` int,"
    " PRIMARY KEY (`Id`),"
    " CONSTRAINT FOREIGN KEY (`Id`) REFERENCES `Olympic_Medals`(`Id`) ON DELETE CASCADE"
    ") ENGINE = InnoDB")

    return TABLES


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
        

def mysqlConn():
    cnx = mysql.connector.connect(user='root',password = "raunak")
    cursor = cnx.cursor()
    try:
        cnx.database = DB_NAME 
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)
    
    tables = defineTables()
    for name, ddl in tables.iteritems():
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    
    cursor.close()
    cnx.close()

def update_OlympicMedals(Olympic_Medals):
    cnx = mysql.connector.connect(user='root',password = "raunak")
    cursor = cnx.cursor()
    cnx.database = DB_NAME
    Olympic_Medals_sql = ("""INSERT INTO Olympic_Medals 
        (Id,Country, Country_Code, Gold_Medals, Silver_Medals, Bronze_Medals,
        Total) 
        VALUES (%s,%s,%s,%s,%s,%s,%s)""")
    try:
        cursor.executemany(Olympic_Medals_sql,Olympic_Medals)
    except Error as e:
        print ('Error:', e)  
    cnx.commit()
    cursor.close()
    cnx.close()