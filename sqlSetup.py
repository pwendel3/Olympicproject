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
from pandas.io import sql

DB_NAME = 'Olympics_DB'
user = 'root'
password = 'raunak'


TABLES = OrderedDict()
def defineTables():
    TABLES['Country_Medals'] = (
    "CREATE TABLE `Country_Medals` ("
    "  `Id` char(20) NOT NULL,"
    "  `Year` char(20),"
    "  `Country` varchar(255) NOT NULL,"
    "  `Country_Code` varchar(255) NOT NULL,"
    "  `Gold_Medals` int,"
    "  `Silver_Medals` int,"
    "  `Bronze_Medals` int,"
    "  `Total` int,"
    "  `Total_Participants` int,"
    "  `Men` int,"
    "  `Women` int,"
    "  PRIMARY KEY (`Id`)"
    ") ENGINE=InnoDB")

    TABLES['Economic_Indicators'] = (
    "CREATE TABLE `Economic_Indicators` ("
    " `Id` char(255) NOT NULL,"
    " `GDP_Val` int,"
    " `Country_Name` varchar(255) NOT NULL,"
    " `Country_Code` varchar(255),"
    " `Year` int,"
    " `Total_Population` int,"
    " PRIMARY KEY (`Id`),"
    " CONSTRAINT FOREIGN KEY (`Id`) REFERENCES `Country_Medals`(`Id`) ON DELETE CASCADE"
    ") ENGINE = InnoDB")

    TABLES['Athlete'] = (
        "CREATE TABLE `Athlete` ("
        " `Key_ID` int NOT NULL AUTO_INCREMENT,"
        " `Rank` char(10),"
        " `Name` varchar(255) NOT NULL,"
        " `Gender` char(6) NOT NULL,"
        " `Age` int,"
        " `Sport` char(255),"
        " `Gold_Medals` int,"
        " `Silver_Medals` int,"
        " `Bronze_Medals` int,"
        " `Total` int,"
        " `Id` char(255) NOT NULL,"
        " `Year` int,"
        " PRIMARY KEY (`Key_ID`),"
        " CONSTRAINT FOREIGN KEY (`Id`) REFERENCES `Country_Medals`(`Id`) ON DELETE CASCADE"
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
    cnx = mysql.connector.connect(user=user,password = password)
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

def update_CountryMedals(Olympic_Medals):
    cnx = mysql.connector.connect(user=user,password = password)
    cursor = cnx.cursor()
    cnx.database = DB_NAME
    Olympic_Medals_sql = ("""INSERT INTO Country_Medals 
        (Id,Year,Country, Country_Code, Gold_Medals, Silver_Medals, Bronze_Medals,
        Total,Total_Participants,Men,Women) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
    try:
        cursor.executemany(Olympic_Medals_sql,Olympic_Medals)
    except Error as e:
        print ('Error:', e)  
    cnx.commit()
    cursor.close()
    cnx.close()

def update_EconomicIndicators(Economic_Indicators):
    cnx = mysql.connector.connect(user=user,password = password)
    cursor = cnx.cursor()
    cnx.database = DB_NAME
    # Write Pandas DF to SQL database
    Economic_Indicators.to_sql('Economic_Indicators',con = cnx,flavor='mysql',
        if_exists = 'replace')
    cnx.commit()
    cursor.close()
    cnx.close()

def update_Athlete(Athlete):
    cnx = mysql.connector.connect(user=user,password = password)
    cursor = cnx.cursor()
    cnx.database = DB_NAME
    Athlete_sql = ("""INSERT INTO Athlete 
        (Rank,Name,Gender, Age, Sport, Gold_Medals, Silver_Medals,Bronze_Medals,
        Total,Id,Year) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
    try:
        cursor.executemany(Athlete_sql,Athlete)
    except Error as e:
        print ('Error:', e)  
    cnx.commit()
    cursor.close()
    cnx.close()

def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row
            
def query_with_fetchmany(sel):
    query_list = list()
    try:
        cnx = mysql.connector.connect(user='root',password = "raunak")
        cursor = cnx.cursor()
        cnx.database = DB_NAME
 
        cursor.execute(sel)
 
        for row in iter_row(cursor):
            query_list.append(row)
        num_fields = len(cursor.description)
        field_names = [i[0] for i in cursor.description]
        field_names
 
    except Error as e:
        print(e)
    
    finally:
        cursor.close()
        cnx.close()
    
    return query_list,field_names

# Convert SQL query into a pandas data frame
def make_frame(list_of_tuples, legend):
    framelist = []
    for i, cname in enumerate(legend):
        framelist.append((cname,[e[i] for e in list_of_tuples]))
    return pd.DataFrame.from_items(framelist)